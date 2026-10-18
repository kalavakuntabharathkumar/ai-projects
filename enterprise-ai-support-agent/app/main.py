from fastapi import FastAPI, HTTPException, Query
from .schemas import Ticket, TriageResult
from .agent import claude_triage, heuristic_triage
from .prompts import PROMPTS, CURRENT_PROMPT_VERSION
from .tools import notify_ticketing_system

app = FastAPI(title="Enterprise AI Support Agent", version="1.0.0", description="Demo ticket triage API with versioned prompts and safe routing.")

@app.get("/health")
def health():
    return {"status": "ok", "prompt_version": CURRENT_PROMPT_VERSION}

@app.get("/prompts")
def list_prompts():
    return {"current": CURRENT_PROMPT_VERSION, "versions": list(PROMPTS.keys())}

@app.post("/triage", response_model=TriageResult)
async def triage(ticket: Ticket, version: str = Query(default=CURRENT_PROMPT_VERSION)):
    if version not in PROMPTS:
        raise HTTPException(status_code=400, detail="Unknown prompt version")
    try:
        return await claude_triage(ticket, version)
    except Exception as exc:
        # Keep API available but make fallback explicit and request human review.
        result = heuristic_triage(ticket, version)
        result.needs_human_review = True
        return result

@app.post("/triage/batch", response_model=list[TriageResult])
async def triage_batch(tickets: list[Ticket], version: str = Query(default=CURRENT_PROMPT_VERSION)):
    if len(tickets) > 100:
        raise HTTPException(status_code=400, detail="Maximum 100 tickets per batch")
    if version not in PROMPTS:
        raise HTTPException(status_code=400, detail="Unknown prompt version")
    results = []
    for ticket in tickets:
        try: results.append(await claude_triage(ticket, version))
        except Exception:
            result = heuristic_triage(ticket, version); result.needs_human_review = True; results.append(result)
    return results

@app.post("/route/{ticket_id}")
async def route(ticket_id: str, result: TriageResult):
    if ticket_id != result.ticket_id:
        raise HTTPException(status_code=400, detail="ticket_id mismatch")
    payload = result.model_dump()
    try:
        return {"ticket_id": ticket_id, "team": result.team, "webhook": await notify_ticketing_system(payload)}
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Ticketing webhook failed") from exc
