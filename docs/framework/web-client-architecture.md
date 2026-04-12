# Web Client Architecture

This note defines the initial structure and operating model for adding a Next.js browser client to the Simple Mercurio Forms repository.

## Decision

The web client should live in the same repository as the existing FastAPI backend, but as a separate application under `apps/web`.

Rationale:

- The frontend and backend contracts will evolve together during the first product phases.
- One repository keeps API and UI changes in a single pull request when contracts change.
- Local development is simpler because the Python API and Next.js client are colocated.
- The deployment boundary still remains clean because `apps/web` is independently buildable and deployable.

## Proposed repository structure

```text
simple-mercurio-forms/
├── api/
├── apps/
│   └── web/
│       ├── public/
│       ├── src/
│       │   ├── app/
│       │   ├── components/
│       │   ├── lib/
│       │   └── types/
│       ├── .env.example
│       ├── package.json
│       └── README.md
├── docs/
│   └── framework/
├── forms/
├── mappers/
└── models/
```

Recommended responsibilities inside `apps/web/src`:

- `app/`: routes, layouts, route groups, and server components
- `components/`: reusable presentation and feature components
- `lib/`: API clients, server helpers, configuration, and shared utilities
- `types/`: application types that are not generated elsewhere

## Frontend architecture

Use Next.js App Router with TypeScript.

Guiding rules:

- Keep browser-facing UI in Next.js.
- Treat FastAPI as the system-of-record API and PDF-processing service.
- Prefer server-side data access in Next.js for protected or sensitive API traffic.
- Generate a typed API client from FastAPI OpenAPI once the contracts stabilize.
- Build the UI vertically: forms catalog, form detail, validation, preview, fill, then artifact download.

Recommended near-term additions:

- `src/features/forms/` for catalog and form-detail screens
- `src/features/fill/` for validation, preview, and submit flows
- `src/features/auth/` once user authentication is introduced
- `src/lib/generated/` for OpenAPI-generated types and clients

## Authentication decision

The current shared API-key model is acceptable for server-to-server access, but it should not be exposed directly to browser code.

Initial browser-safe approach:

- Keep credentials on the server side.
- Let Next.js server components, route handlers, or server actions call the FastAPI service.
- Return only the required user-facing data to the browser.

Target SaaS approach:

- Introduce real end-user authentication and authorization on the backend.
- Support user sessions or JWT-based access tokens.
- Add tenant-aware authorization before onboarding multiple customer organizations.
- Protect artifact download endpoints with the same user/tenant model.

In short: browser users authenticate as users, not as holders of a shared API key.

## Deployment model

Two deployment modes should use the same application code:

### Local/self-hosted

- Run Next.js and FastAPI together with Docker Compose.
- Store generated PDFs on local disk or a mounted volume.
- Use a simple database footprint appropriate to the installation size.

### SaaS

- Deploy Next.js and FastAPI as separate services.
- Move artifact storage to object storage.
- Add async job handling for fill operations that may take noticeable time.
- Add centralized logging, metrics, and request tracing.

## First implementation steps

1. Keep `apps/web` independent from the Python runtime.
2. Add environment-based API base URL configuration.
3. Build a health/readiness check into the frontend for local setup feedback.
4. Add forms catalog and form detail routes.
5. Add server-side API access helpers.
6. Introduce typed API generation from the FastAPI OpenAPI schema.
7. Add auth before exposing the system as a public SaaS application.