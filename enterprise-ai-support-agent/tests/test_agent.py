from app.schemas import Ticket
from app.agent import heuristic_triage
from app.prompts import render_prompt
from app.tools import route_ticket

def test_billing_ticket_routes_to_billing():
    result = heuristic_triage(Ticket(id="T-1", subject="Refund invoice", body="I was charged twice for my subscription."))
    assert result.category == "billing"
    assert result.team == "Billing Support"

def test_urgent_ticket_requires_review():
    result = heuristic_triage(Ticket(id="T-2", subject="Possible account takeover", body="I think fraud has accessed my account."))
    assert result.priority == "urgent"
    assert result.needs_human_review

def test_prompt_versions_are_distinct():
    assert "untrusted data" not in render_prompt("x", "y", "v1")
    assert "untrusted data" in render_prompt("x", "y", "v2")

def test_unknown_prompt_rejected():
    try: render_prompt("x", "y", "v9")
    except ValueError: pass
    else: assert False, "expected ValueError"

def test_unknown_category_routes_to_general():
    assert route_ticket("unexpected") == "General Support"
