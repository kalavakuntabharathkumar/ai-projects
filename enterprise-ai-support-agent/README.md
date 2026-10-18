# Enterprise AI Support Agent Platform

A runnable support-ticket triage API with Claude Messages API integration, versioned prompts, safe category-to-team routing, an optional HTTPS webhook, synthetic evaluation cases, and tests.

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate | macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # optional; leave key unset for deterministic local fallback
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs`. `POST /triage` accepts `{"id":"T-101","subject":"Refund invoice","body":"I was charged twice."}`. Set `ANTHROPIC_API_KEY` in the environment to use Claude. Without it, a transparent local heuristic fallback is used. Configure `TICKETING_WEBHOOK_URL` only for a trusted HTTPS test endpoint.

## Test and evaluate

```bash
pytest -q
python scripts_eval.py
```

The 300-case JSONL set is synthetic and balanced across five categories. Do not claim any particular accuracy or hallucination reduction without running a labeled benchmark against the intended production data. The sample includes a prompt-version comparison framework, not a fabricated performance result.

## Safety / design

- Ticket text is untrusted; the prompt explicitly says not to follow embedded instructions.
- Model output is parsed as JSON and validated against allowed categories/priorities.
- Low confidence and urgent cases are flagged for human review.
- Routing maps to a fixed allowlist of teams; the model cannot provide arbitrary destinations.
- Webhook is disabled unless explicitly configured, requires HTTPS, and is never silently enabled.
- Add authentication, rate limiting, audit persistence, PII redaction, secrets management, and organization-specific policy before production deployment.
