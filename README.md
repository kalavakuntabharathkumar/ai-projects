# AI Projects

A public monorepo containing two independent AI application projects.

## Projects

### AI Workflow Automation Dashboard
A responsive Next.js, React, and TypeScript prototype for browsing, searching, creating, and editing workflow configurations. The project uses an in-memory store and includes a REST route and Vitest tests. It is a prototype, not a production automation engine; it has no authentication, durable database, or actual workflow execution engine.

Path: [ai-workflow-automation-dashboard](./ai-workflow-automation-dashboard/)

Run locally from that directory with Node.js 20+:

```sh
npm install
npm run dev
```

### Enterprise AI Support Agent
A FastAPI ticket-triage demo with constrained category/team routing, human-review flags, a deterministic local fallback, optional Claude integration, and synthetic evaluation cases.

Path: [enterprise-ai-support-agent](./enterprise-ai-support-agent/)

Run locally from that directory:

```sh
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Safety and evaluation

The support-agent evaluation cases are synthetic. Do not commit real credentials or a local .env file; use environment variables for local secrets. Neither project claims production readiness or measured performance results.
