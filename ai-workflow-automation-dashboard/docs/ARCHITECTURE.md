# Architecture

- `app/`: Next.js App Router pages and API endpoint.
- `components/Shell.tsx`: shared navigation layout.
- `components/WorkflowList.tsx`: client-side search and status filtering.
- `components/WorkflowEditor.tsx`: editable metadata and visual step list.
- `lib/types.ts`: shared TypeScript contracts.
- `lib/workflows.ts`: isolated in-memory store with defensive copies and validation.
- `app/api/workflows/route.ts`: JSON GET/POST endpoints.
- `tests/workflows.test.ts`: store unit tests.

## Production next steps

Replace the in-memory store with PostgreSQL, add authentication and role-based permissions, persist workflow revisions, define a validated node schema, implement a queue-backed execution engine, store secrets outside workflow JSON, add audit logs and retries, and instrument latency/error/cost metrics. AI nodes should call a server-side provider adapter and require evaluation plus human approval for sensitive actions.
