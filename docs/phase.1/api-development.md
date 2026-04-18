# API Development Blueprint

This document defines a production-oriented API strategy for Simple Mercurio Forms, including functionality, design, architecture, contracts, security, operations, and implementation phases.

---

## 1. Objectives

### Primary objective
Expose the existing form-processing engine (models + mappers + fill pipeline) through stable HTTP APIs that are usable by web apps, internal tools, and partner systems.

### Secondary objectives
- Preserve current domain-model quality and mapper determinism.
- Make form support discoverable and self-describing.
- Provide synchronous and asynchronous processing modes.
- Introduce operational controls (auth, observability, quotas, jobs).

### Non-goals (phase 1)
- Multi-tenant enterprise IAM complexity.
- Full workflow orchestration (review/approval/signature) inside this service.
- Browser-hosted editing UI in this repository.

---

## 2. Existing System Capabilities (Mapped to API)

Current code capabilities:
- PDF source acquisition: `downloader.py`
- Field definition extraction: `extract_fields.py`
- Definition persistence: `import_to_db.py` to `forms.db`
- Domain model to field-values mapping: `models/` + `mappers/`
- Fill execution: `fill_form.py`
- Dynamic mapper routing: `forms_registry.py`

API design should wrap these primitives, not replace them.

---

## 3. High-Level Architecture

### Logical components
1. API Gateway Layer
- Auth, rate limits, request IDs, error normalization.

2. Application Service Layer
- Form catalog service
- Validation service
- Fill orchestration service
- Job orchestration service
- Admin ingestion service

3. Domain Layer
- Existing Pydantic form schemas and mapper modules.

4. Infrastructure Layer
- SQLite metadata store (`forms.db`) for form definitions and lookup queries.
- File storage for generated PDFs (`forms/filled/` local in dev, object storage in prod).
- Queue backend for async jobs (Redis/RQ or Celery).

### Recommended runtime stack
- Framework: FastAPI
- Validation: Pydantic
- ASGI server: Uvicorn/Gunicorn
- Queue: Redis + RQ (simple) or Celery (advanced)
- Metrics: Prometheus/OpenTelemetry
- Logging: structured JSON logs

---

## 4. API Surface

Base path: `/api/v1`

### 4.1 Forms Catalog APIs

#### GET `/api/v1/forms`
Returns all supported forms.

Response shape:
- `form_code`
- `title`
- `field_count`
- `page_count`
- `has_domain_example`
- `supported_fill_modes` (`field_values`, `domain_model`, `semantic_values`)

#### GET `/api/v1/forms/{formCode}`
Returns one form metadata record and availability flags.

#### GET `/api/v1/forms/{formCode}/fields`
Returns extracted field definitions for UI rendering and rule engines.

Optional query parameters:
- `type` (Text, CheckBox, RadioButton, ...)
- `page`
- `section_code`

#### GET `/api/v1/forms/{formCode}/sections`
Returns section grouping metadata inferred from extractor output.

### 4.2 Validation APIs

#### POST `/api/v1/forms/{formCode}/validate`
Validates payload shape and semantic compatibility before filling.

Request modes:
- `field_values`
- `domain_model`
- `semantic_values`

Response:
- `valid: bool`
- `errors[]` (field path, code, message)
- `warnings[]`

#### POST `/api/v1/forms/{formCode}/validate-mapping`
Runs mapping integrity checks:
- missing definition keys
- extra mapping keys
- blank text fields (optional strict mode)

### 4.3 Fill APIs

#### POST `/api/v1/forms/{formCode}/fill`
Fills PDF from direct payload.

Request:
- `field_values`
- optional `semantic_values`
- optional output options (`flatten`, `include_debug_report`)

Response:
- `file_id`
- `download_url` or inline stream
- `assignment_summary`

#### POST `/api/v1/forms/{formCode}/fill-from-model`
Fills PDF from domain model JSON (mapped via `forms_registry.py` + mapper).

Request:
- `model_payload` (validated with form-specific Pydantic schema)

Response:
- same as `/fill`

#### POST `/api/v1/forms/{formCode}/preview-fill`
Dry-run only, no output file.

Returns:
- resolved widget assignments
- warnings for non-matching semantic selectors

### 4.4 Async Job APIs

#### POST `/api/v1/jobs/fill`
Creates async fill job.

Request:
- formCode
- mode (`fill` or `fill-from-model`)
- payload

Response:
- `job_id`
- `status_url`

#### GET `/api/v1/jobs/{jobId}`
Returns status (`queued`, `running`, `failed`, `completed`) and progress.

#### GET `/api/v1/jobs/{jobId}/result`
Returns download metadata for completed jobs.

### 4.5 Admin/Ingestion APIs

#### POST `/api/v1/admin/download-forms`
Runs downloader pipeline.

#### POST `/api/v1/admin/extract-fields`
Runs extractor for editable forms.

#### POST `/api/v1/admin/import-definitions`
Loads definitions into SQLite.

#### GET `/api/v1/admin/pipeline-status`
Returns last execution summaries for the ingestion pipeline.

---

## 5. Request/Response Standards

### Standard success envelope
```json
{
  "request_id": "uuid",
  "data": {},
  "meta": {}
}
```

### Standard error envelope
```json
{
  "request_id": "uuid",
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human-readable summary",
    "details": [
      {"path": "field_values.Texto2", "message": "Expected string"}
    ]
  }
}
```

### HTTP status policy
- `200` success
- `202` accepted for async jobs
- `400` malformed request
- `401/403` auth failures
- `404` unknown form/job
- `409` incompatible versions or locked resources
- `422` semantic validation errors
- `429` rate-limited
- `500` internal failures

---

## 6. Security and Access Model

### Authentication
Phase 1:
- API key in `Authorization: Bearer <token>` or `X-API-Key`.

Phase 2:
- OAuth2/JWT with scoped permissions.

### Authorization scopes
- `forms:read`
- `forms:fill`
- `forms:validate`
- `jobs:read`
- `admin:pipeline`

### Additional controls
- Rate limiting per key.
- Request payload size limits.
- MIME/content checks for upload endpoints (if introduced).
- Audit log for admin endpoints.

---

## 7. Data and Storage Design

### Metadata source
- `forms.db` remains source for field metadata APIs.

### Output files
Development:
- local disk (`forms/filled/`)

Production:
- object storage bucket (S3-compatible)
- store only references in API response

### Optional API tables (recommended)
- `api_jobs`
  - `id`, `type`, `status`, `payload_hash`, `created_at`, `started_at`, `ended_at`, `error`
- `api_artifacts`
  - `id`, `job_id`, `form_code`, `storage_uri`, `sha256`, `created_at`

---

## 8. Observability and Operations

### Logging
- Structured JSON logs
- Include `request_id`, `form_code`, `endpoint`, `duration_ms`, `status`

### Metrics
- request count and latency per endpoint
- fill success/failure rate by form
- validation failure distribution by code
- async queue depth and job latency

### Tracing
- OpenTelemetry trace spans across API -> mapper -> fill -> storage steps

### Health endpoints
- `GET /health/live`
- `GET /health/ready`
- `GET /health/deps` (optional detailed dependency checks)

---

## 9. Versioning Strategy

### API versioning
- URI-based major versions: `/api/v1`

### Form definition versioning
Expose per-form:
- `definition_version` (hash or timestamp)
- `mapper_version` (git commit/tag)

### Backward compatibility
- Additive response evolution preferred.
- Avoid breaking response key removals inside same API major.

---

## 10. Testing Strategy for APIs

### Unit tests
- Endpoint validation and schema coercion
- mapper invocation and error handling

### Integration tests
- full fill-from-model path per sample forms
- validate output artifact existence and assignment counts

### Regression tests
- reuse canonical-v3 smoke checks
- detect drift in missing/extra mapping keys

### Performance tests
- synchronous fill throughput
- queue saturation behavior

---

## 11. Incremental Delivery Plan

### Phase 1 (MVP)
- Catalog APIs
- Validation API
- Sync fill APIs
- basic auth + logging

### Phase 2
- Async job APIs
- artifact retrieval
- stronger observability + metrics

### Phase 3
- Admin ingestion APIs
- version introspection APIs
- finer-grained authorization scopes

### Phase 4
- external SDK generation from OpenAPI
- advanced multi-tenant controls (if needed)

---

## 12. Proposed Project Layout for API Code

```text
api/
  main.py
  dependencies.py
  routers/
    forms.py
    validate.py
    fill.py
    jobs.py
    admin.py
  schemas/
    common.py
    forms.py
    validate.py
    fill.py
    jobs.py
  services/
    form_catalog_service.py
    validation_service.py
    fill_service.py
    job_service.py
    pipeline_service.py
  repositories/
    form_definition_repo.py
    job_repo.py
    artifact_repo.py
  security/
    auth.py
    permissions.py
  observability/
    logging.py
    metrics.py
```

This keeps API concerns separate from existing script-oriented modules while reusing domain and mapper logic.

---

## 13. Key Design Principles

- Reuse current business logic; do not duplicate mapping logic in API layer.
- Keep endpoint contracts explicit and strongly typed with Pydantic.
- Make fill behavior deterministic and auditable.
- Design for operational safety first (auth, limits, logs, traceability).
- Phase delivery to get value quickly without destabilizing the existing workflow.
