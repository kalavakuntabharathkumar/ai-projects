"""Evaluate the deterministic local baseline against data/eval_cases.jsonl."""
import json
from pathlib import Path
from app.schemas import Ticket
from app.agent import heuristic_triage

path = Path(__file__).parent / "data" / "eval_cases.jsonl"
rows = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
correct = 0
for row in rows:
 result = heuristic_triage(Ticket(id=row["id"], subject=row["subject"], body=row["body"]))
 correct += result.category == row["expected_category"]
print(f"Cases: {len(rows)} | category accuracy: {correct/len(rows):.1%}")
print("Note: this synthetic benchmark measures the local keyword baseline, not Claude model quality.")
