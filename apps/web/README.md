This is the browser client for Simple Mercurio Forms.

It is colocated with the FastAPI backend in the same repository, but it remains a separate application with its own runtime and deployment.

## Development

Install dependencies:

```bash
npm install
```

Create a local env file:

```bash
cp .env.example .env.local
```

Run the development server:

```bash
npm run dev
```

Open http://localhost:3000.

By default the app expects the API at `http://localhost:8000`.

## Environment

Supported variables:

- `MERCURIO_API_BASE_URL`: Base URL for the FastAPI service. Used server-side.

## Intended architecture

- Next.js is the browser-facing application.
- FastAPI remains the system-of-record API and PDF-processing service.
- Browser calls should go through Next.js server routes or use real end-user auth on the API.
- Do not expose a shared API key directly in browser code.

## Suggested first features

- Forms catalog
- Form detail and field inspection
- Validation and preview flows
- Fill-from-model submission
- Artifact download and job history

## Commands

```bash
npm run dev
npm run lint
npm run build
```
