# Architecture

`POST /triage` -> input schema validation -> versioned prompt -> Claude Messages API (when configured) -> constrained JSON parsing -> allowed category/priority validation -> fixed team mapping -> response with confidence and human-review flag.

If no key is configured, the local deterministic heuristic keeps the demo runnable. If the API fails, the endpoint returns a heuristic result flagged for human review. `POST /route/{ticket_id}` optionally sends the validated result to a configured HTTPS webhook. It does not perform arbitrary tool execution.

## Evaluation protocol

`data/eval_cases.jsonl` contains 300 synthetic labeled cases. `scripts_eval.py` measures category accuracy for the local baseline. For a meaningful model comparison, use a held-out, representative and privacy-reviewed dataset; record prompt version, model identifier, accuracy, macro-F1, review rate, latency, and cost. Review samples for unsupported claims and hallucinations; do not treat the synthetic set as evidence of production quality.
