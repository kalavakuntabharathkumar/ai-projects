import json
import os
import re
from typing import Any
import httpx
from .prompts import render_prompt, CURRENT_PROMPT_VERSION
from .schemas import Ticket, TriageResult
from .tools import route_ticket

KEYWORDS = {
 "billing": ("invoice", "charged", "refund", "payment", "subscription", "bill"),
 "technical": ("error", "crash", "bug", "not working", "failed", "exception", "login loop"),
 "account": ("password", "account", "locked", "email change", "verification"),
 "shipping": ("delivery", "shipment", "tracking", "package", "arrived", "shipping"),
}

def heuristic_triage(ticket: Ticket, version: str = CURRENT_PROMPT_VERSION) -> TriageResult:
    text = f"{ticket.subject} {ticket.body}".lower()
    scores = {cat: sum(1 for word in words if word in text) for cat, words in KEYWORDS.items()}
    category = max(scores, key=scores.get) if max(scores.values(), default=0) else "other"
    priority = "urgent" if any(x in text for x in ("fraud", "account takeover", "data breach", "safety issue")) else "high" if any(x in text for x in ("outage", "cannot access", "charged twice", "deadline today")) else "normal"
    confidence = min(.86, .52 + .11 * scores.get(category, 0)) if category != "other" else .45
    summary = re.sub(r"\s+", " ", ticket.body).strip()[:220]
    reply = "Thanks for contacting support. We’ve logged your issue and routed it to the appropriate team. A support specialist will review the details and follow up."
    return TriageResult(ticket_id=ticket.id, category=category, priority=priority, team=route_ticket(category), summary=summary, suggested_reply=reply, confidence=confidence, prompt_version=version, needs_human_review=confidence < .65 or priority == "urgent")

async def claude_triage(ticket: Ticket, version: str = CURRENT_PROMPT_VERSION) -> TriageResult:
    """Use Anthropic Messages API when configured; fallback is explicit and local."""
    api_key = os.getenv("ANTHROPIC_API_KEY", "").strip()
    if not api_key or api_key == "replace-me":
        return heuristic_triage(ticket, version)
    prompt = render_prompt(ticket.subject, ticket.body, version)
    model = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-latest")
    headers = {"x-api-key": api_key, "anthropic-version": "2023-06-01", "content-type": "application/json"}
    body = {"model": model, "max_tokens": 700, "messages": [{"role": "user", "content": prompt}]}
    async with httpx.AsyncClient(timeout=25.0) as client:
        response = await client.post("https://api.anthropic.com/v1/messages", headers=headers, json=body)
        response.raise_for_status()
    raw = "".join(block.get("text", "") for block in response.json().get("content", []) if block.get("type") == "text")
    # Robustly extract JSON; never execute model-provided code or tool instructions.
    match = re.search(r"\{.*\}", raw, re.S)
    if not match:
        result = heuristic_triage(ticket, version); result.needs_human_review = True; return result
    try:
        data: dict[str, Any] = json.loads(match.group())
        category = data.get("category") if data.get("category") in ("billing", "technical", "account", "shipping", "other") else "other"
        priority = data.get("priority") if data.get("priority") in ("low", "normal", "high", "urgent") else "normal"
        confidence = max(0.0, min(1.0, float(data.get("confidence", .4))))
        return TriageResult(ticket_id=ticket.id, category=category, priority=priority, team=route_ticket(category), summary=str(data.get("summary", ""))[:300], suggested_reply=str(data.get("suggested_reply", ""))[:1200], confidence=confidence, prompt_version=version, needs_human_review=confidence < .7 or priority == "urgent")
    except (ValueError, TypeError, json.JSONDecodeError):
        result = heuristic_triage(ticket, version); result.needs_human_review = True; return result
