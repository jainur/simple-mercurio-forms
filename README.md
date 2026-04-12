# Simple Mercurio Forms

Monorepo for downloading, modeling, and filling Spanish immigration form PDFs — with a FastAPI backend and a Next.js browser client.

## Documentation Index

- Framework overview: [docs/framework/project-architecture.md](docs/framework/project-architecture.md)
- Form filling details: [docs/framework/form-filling.md](docs/framework/form-filling.md)
- API development blueprint: [docs/framework/api-development.md](docs/framework/api-development.md)
- Web client architecture: [docs/framework/web-client-architecture.md](docs/framework/web-client-architecture.md)

## Repository Structure

```
apps/
  web/           Next.js browser client (TypeScript, Tailwind, App Router)
services/
  es-immigration-forms/  FastAPI Python backend
docs/
  framework/     Technical framework documentation
```

## Quick Start

**Python API** (from `services/es-immigration-forms/`):

```bash
cd services/es-immigration-forms
pip install -r requirements.txt
uvicorn api.main:app --reload
```

**Web client** (from `apps/web/`):

```bash
cd apps/web
npm install
npm run dev
```

See each service's README for full details:

- [services/es-immigration-forms/README.md](services/es-immigration-forms/README.md)
- [apps/web/README.md](apps/web/README.md)

