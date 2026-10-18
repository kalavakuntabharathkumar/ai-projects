# AI Workflow Automation Dashboard — FlowPilot

A responsive Next.js/React/TypeScript internal dashboard prototype for listing, searching, filtering, creating, and editing AI workflow configurations. Includes four node types, a REST route, sample workflows, and unit tests. It uses a small in-memory store to keep the project easy to run without external services.

## Requirements

- Node.js 20+ and npm
- Internet access on first install to download npm dependencies

## Run

```bash
npm install
npm run dev
```

Visit `http://localhost:3000`. Browse Overview, All workflows, or create a workflow. Run tests with `npm test`; run a production build with `npm run build`.

## Features

- Responsive overview with counts derived from sample workflow data
- Search by workflow name, description, or owner; filter by Draft / Active / Paused
- Create/edit workflow metadata and add/remove/rename trigger, LLM, condition, and action nodes
- `GET /api/workflows` lists workflows; `POST /api/workflows` validates and saves a workflow
- Empty-state, validation, and loading/error feedback
- Vitest coverage for the store's initial data, lookup, updates, validation, deletion, and defensive copies

## Important limitations

This is a portfolio-ready UI prototype, not a production automation engine. The workflow store is in-memory and resets when the server restarts; it is not shared across serverless instances. There is no authentication, database persistence, actual execution engine, or provider integration. Cursor and GitHub Copilot are developer tools and are not runtime dependencies. Do not claim 9,000 LOC, 85% coverage, production deployment, or measured delivery gains unless you actually achieve and measure those outcomes in your own environment.
