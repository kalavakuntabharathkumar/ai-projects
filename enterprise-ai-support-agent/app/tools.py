"""Small, auditable tools used by the agent. External side effects are opt-in."""
from urllib.parse import urlparse
import os
import httpx

TEAM_BY_CATEGORY = {"billing": "Billing Support", "technical": "Technical Support", "account": "Account Support", "shipping": "Fulfillment", "other": "General Support"}

def route_ticket(category: str) -> str:
    """Resolve a category to a known support queue; no network side effect."""
    return TEAM_BY_CATEGORY.get(category, TEAM_BY_CATEGORY["other"])

async def notify_ticketing_system(payload: dict) -> dict:
    """Post to a configured webhook only. Unconfigured by default for safe local demos."""
    url = os.getenv("TICKETING_WEBHOOK_URL", "").strip()
    if not url:
        return {"sent": False, "reason": "TICKETING_WEBHOOK_URL is not configured"}
    parsed = urlparse(url)
    if parsed.scheme != "https":
        raise ValueError("Ticketing webhook must use HTTPS")
    async with httpx.AsyncClient(timeout=8.0) as client:
        response = await client.post(url, json=payload)
        response.raise_for_status()
    return {"sent": True, "status_code": response.status_code}
