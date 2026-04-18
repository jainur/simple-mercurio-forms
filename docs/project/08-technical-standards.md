# Technical Standards (Step 5.3) — abogados-cowork

Last updated: 2026-04-18  
Status: Approved

## 1. Purpose

Define enforceable technical standards for implementation consistency across backend, frontend, workflows, data, APIs, operations, and documentation.

## 2. Applicability

These standards apply to:
- API and worker services
- Web client
- Local agent (Tauri)
- Workflow definitions (Temporal)
- Data models and persistence
- CI/CD, telemetry, and operations

## 3. Stack Baseline (Confirmed)

- Frontend: Next.js + TypeScript.
- Backend: FastAPI + Python.
- Workflow orchestration: Temporal.
- SQL persistence: PostgreSQL (production), SQLite (local development profile).
- ORM/migrations: SQLAlchemy + Alembic.
- Graph store: Neo4j.
- Cache: Redis.
- Storage: S3-compatible (SaaS), S3-compatible or local filesystem (on-prem).
- Local agent runtime: Tauri.
- LLM integration: provider abstraction, Gemini default implementation.

## 4. Repository and Project Structure Standards

## 4.1 Top-level structure
- `apps/`: user-facing applications (`web`, local agent app if colocated).
- `services/`: backend domain services and workers.
- `plugins/`: plugin packages grouped by capability (`domain_logic`, `form_packs`, `rule_packs`, `submission_channels`, `providers`).
- `docs/project/`: authoritative project documentation.
- `infra/`: deployment manifests, IaC, environment templates.
- `scripts/`: repeatable automation scripts.

## 4.2 Service structure standard
Each backend service should follow:
- `api/`: route handlers and request/response schemas.
- `domain/`: core business logic (no framework coupling).
- `repositories/`: persistence adapters and query isolation.
- `workflows/`: Temporal workflow/activity definitions.
- `integrations/`: external systems (Neo4j, email, LLM providers, storage).
- `tests/`: unit, integration, contract tests.

## 4.3 Dependency direction
Allowed direction:
- `api -> domain -> repositories/integrations`
- `workflows -> domain/integrations`
Disallowed:
- `repositories -> api`
- `integrations -> domain` (integration code must not hold business rules)

## 4.4 Template families and scaffolding standards

### 4.4.1 Template families
The platform maintains predefined template families for common project types:
- Web app template (Next.js, i18n, auth guards, telemetry hooks).
- API service template (FastAPI, SQLAlchemy, Alembic, error envelope, health endpoints).
- Worker template (Temporal activity/service worker scaffold, retry/idempotency baseline).
- Local agent template (Tauri runtime, signed job handling, heartbeat, diagnostics).
- Plugin template (manifest, capability contracts, contract tests, compatibility checks).
- Integration adapter template (external client wrapper, mapping layer, retry/backoff policies).
- Infrastructure template (environment overlays, secrets/config skeletons, observability defaults).
- Documentation template (README, ADR, runbook, release/migration notes).

### 4.4.2 Template source of truth
- Templates must live in a dedicated internal templates location.
- Preferred structure:
  - In-repo: `templates/` for tightly coupled teams.
  - Separate internal repository: `abogados-cowork-templates` for multi-project reuse.
- Every template must include metadata:
  - `template_id`
  - `template_version`
  - `supported_core_versions`
  - `owner`

### 4.4.3 Generator command standard
- A generator command must scaffold projects by template type.
- Command pattern (example):
  - `./scripts/scaffold --type <template_family> --name <project_name> --profile <dev|prod|onprem>`
- The generator must:
  - apply standard directory layout,
  - include baseline lint/test config,
  - stamp template metadata in generated output.

### 4.4.4 CI enforcement
- CI must verify generated project structure consistency against template standards.
- Required checks:
  - directory and file presence checks,
  - lint/type/test baseline checks,
  - template metadata validity checks.
- Drift from template standards must fail CI unless explicitly approved with rationale.

### 4.4.5 Template versioning and upgrades
- Templates use semantic versioning.
- Breaking template changes require migration guidance.
- Every template release must include migration notes:
  - affected project types,
  - required manual steps,
  - compatibility constraints,
  - rollback guidance.

### 4.4.6 Initial template catalog (v1)

| Template ID | Family | Initial Version | Owner | Primary Use |
|---|---|---|---|---|
| `tmpl.web.nextjs.app` | Web app | 1.0.0 | Frontend | Next.js app scaffold with i18n, auth guard hooks, telemetry baseline |
| `tmpl.api.fastapi.service` | API service | 1.0.0 | Backend | FastAPI service with SQLAlchemy, Alembic, health endpoints, error envelope |
| `tmpl.worker.temporal.activity` | Worker | 1.0.0 | Backend | Temporal worker/activity scaffold with retry and idempotency helpers |
| `tmpl.agent.tauri.local` | Local agent | 1.0.0 | Platform | Tauri agent with signed job handling, heartbeat, diagnostics |
| `tmpl.plugin.domain.logic` | Plugin | 1.0.0 | Platform | Plugin scaffold for `domain.logic` capability |
| `tmpl.plugin.form.pack` | Plugin | 1.0.0 | Platform | Plugin scaffold for `form.pack` capability |
| `tmpl.plugin.validation.rule-pack` | Plugin | 1.0.0 | Platform | Plugin scaffold for `validation.rule_pack` capability |
| `tmpl.plugin.submission.channel` | Plugin | 1.0.0 | Platform | Plugin scaffold for `submission.channel` capability |
| `tmpl.plugin.llm.provider` | Plugin | 1.0.0 | AI Platform | Plugin scaffold for `llm.provider` capability (Gemini default implementation) |
| `tmpl.integration.adapter` | Integration adapter | 1.0.0 | Platform | Adapter scaffold for external APIs/webhooks with mapping/retry structure |
| `tmpl.infra.service.bundle` | Infrastructure | 1.0.0 | DevOps | Environment-aware infra skeleton with observability defaults |
| `tmpl.docs.project.change` | Documentation | 1.0.0 | Platform | ADR, runbook, and release/migration note templates |

Catalog governance:
- Template IDs are immutable once published.
- Version increments follow semantic versioning.
- Owners are responsible for compatibility and migration notes.

## 5. Naming Standards

## 5.1 General
- Use English for code identifiers.
- Use descriptive names; avoid abbreviations unless domain-standard (`NIE`, `FNMT`, `EX11`).
- Prefer singular nouns for model/entity names (`Case`, `Document`).

## 5.2 Python
- Modules/files: `snake_case.py`
- Classes: `PascalCase`
- Functions/variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`

## 5.3 TypeScript/Next.js
- Components: `PascalCase.tsx`
- Non-component modules: `kebab-case.ts` or `snake_case.ts` (choose one repo-wide; default `kebab-case.ts`)
- Variables/functions: `camelCase`
- Types/interfaces/enums: `PascalCase`

## 5.4 API naming
- Resource nouns are plural: `/api/v1/cases`, `/api/v1/documents`.
- Action endpoints only when non-CRUD semantics are needed: `/submission-dispatch`, `/retry`.
- Use path versioning: `/api/v1/...`

## 5.4a Plugin naming
- Plugin IDs: `<domain_or_vendor>.<capability>.<name>` (for example `immigration.form_pack.ex_forms`).
- Capability keys are dot-separated lowercase (`domain.logic`, `form.pack`, `validation.rule_pack`, `submission.channel`, `llm.provider`).

## 5.5 Database naming
- Tables: `snake_case`, prefixed by bounded context where useful (`case_`, `doc_`, `extract_`).
- Columns: `snake_case`.
- Primary key columns: `id` (UUID preferred).
- Foreign keys: `<entity>_id`.
- Timestamp columns minimum: `created_at`, `updated_at`; optional `deleted_at` for soft-delete models.

## 5.6 Workflow and event naming
- Workflow names: `<Domain><Purpose>Workflow` (for example `CaseLifecycleWorkflow`).
- Activity names: verb-first, explicit side effect (`run_extraction_activity`).
- Event types: `UPPER_SNAKE_CASE` (for example `CASE_CREATED`, `LEGAL_VALIDATION_COMPLETED`).

## 6. API Standards

## 6.1 Request/response envelope
Success response envelope:
```json
{
  "data": {},
  "meta": {
    "request_id": "uuid",
    "timestamp": "ISO-8601"
  }
}
```

Error response envelope:
```json
{
  "error": {
    "code": "DOMAIN_ERROR_CODE",
    "message": "Human-readable summary",
    "details": {},
    "retryable": false
  },
  "meta": {
    "request_id": "uuid",
    "timestamp": "ISO-8601"
  }
}
```

## 6.2 Error code standard
- Use stable machine-readable codes (`VALIDATION_BLOCKING_ISSUE`, `SUBMISSION_RETRYABLE_FAILURE`).
- Do not expose stack traces in API responses.
- Include `retryable=true|false` for operational clarity.

## 6.3 Pagination/filtering
- List endpoints must support cursor or page-based pagination.
- Filter keys must be explicit and documented.
- Sorting defaults must be deterministic.

## 6.4 Idempotency
- Required for side-effecting endpoints likely to be retried (`submission-dispatch`, `retry`).
- Accept `Idempotency-Key` header and persist key-result mapping for defined TTL.

## 6.5 Auth and tenancy
- JWT access token required for protected endpoints.
- Tenant context resolved from claims and validated against request path/resource.
- Cross-tenant access returns authorization error, never not-found masking for internal tools.

## 7. ORM and Database Standards

## 7.1 ORM baseline
- SQLAlchemy ORM models are canonical persistence contracts.
- Domain logic must not leak raw SQL into handlers.
- Repository layer abstracts ORM queries and transaction boundaries.

## 7.2 Migrations
- Alembic migrations are mandatory for schema changes.
- Every migration must include downgrade path unless explicitly waived with rationale.
- Production schema baseline targets PostgreSQL.

## 7.3 SQLite local profile rules
- SQLite is development-only (not production profile).
- Use SQLite-compatible model definitions for core entities.
- PostgreSQL-specific SQL must be isolated and guarded by repository adapters.
- Integration tests that validate release readiness must run on PostgreSQL.

## 7.4 Data integrity
- Use DB constraints for invariants (FK, unique, check) where feasible.
- Audit and legal-critical tables should be append-only by policy and permissions.

## 8. Workflow Standards (Temporal)

## 8.1 State authority
- Workflow state is source of truth for case progression.
- UI state projections are read models derived from workflow events.

## 8.2 Activity design
- Activities must be deterministic in interface and idempotent in side effects where possible.
- External calls must include timeouts and retry policy configuration.

## 8.3 Human gate enforcement
- Lawyer approval gate is mandatory in workflow logic, not bypassable via API convenience endpoints.

## 8.4 Retry and failure classes
- Use defined error classes: `USER_CORRECTABLE`, `SYSTEM_TRANSIENT`, `SYSTEM_FATAL`, `EXTERNAL_DEPENDENCY`.
- Retry policies differ by class and activity type.

## 8.5 Plugin execution boundaries
- Plugins may not directly mutate core workflow state tables.
- Workflow decisions may consume plugin outputs, but transitions are applied only by core workflow handlers.
- Plugin failures must be translated into standard failure classes and routed through workflow guardrails.

## 9. LLM and GraphRAG Standards

## 9.1 Provider abstraction
Define an internal interface with at least:
- `extract_fields(document, schema_hint, locale)`
- `summarize_reasoning(extraction_context)`
- `health_check()`

Gemini is default implementation; additional providers must be plug-compatible.

LLM providers are implemented as `llm.provider` plugins under capability contracts.

## 9.5 Plugin contract standards

### 9.5.1 Required MVP plugin capabilities
- `domain.logic`
- `form.pack`
- `validation.rule_pack`
- `submission.channel`
- `llm.provider`

### 9.5.2 Required manifest fields
- `plugin_id`
- `plugin_version`
- `capabilities`
- `api_contract_version`
- `core_compatibility`
- `config_schema`
- `permissions_required`
- `signature_metadata`

### 9.5.3 Lifecycle standards
- Lifecycle operations: install, enable, disable, upgrade.
- Every lifecycle operation must be auditable.
- Incompatible plugins must fail activation with explicit error code.

### 9.5.4 Security and trust standards
- Signed plugins only in MVP.
- Capability-based permission scoping is mandatory.
- Tenant scope must be explicit in activation and execution context.

### 9.5.5 Runtime policy standards
- One active plugin per capability per tenant scope in MVP.
- Contract version mismatch blocks activation.
- Safe disablement must preserve in-flight workflow integrity.

## 9.2 Prompt and output controls
- All extraction outputs must conform to typed schema validation.
- Reasoning summaries are stored for provenance but must be concise and redact sensitive data.

## 9.3 Citation and explainability
- Validation outputs must include legal citation payload (`reference_id`, source text, graph snapshot version).
- Any eligibility decision without citation is treated as invalid output.

## 9.4 Model risk controls
- Confidence scores are required per extracted field.
- Low-confidence thresholds must route to human review.

## 10. Frontend and UI Standards

## 10.1 Component standards
- Shared UI components for common controls (status badges, validation alerts, provenance viewer).
- Keep business logic out of presentation components.

## 10.2 Internationalization standards
- All user-visible strings use translation keys.
- Required locales for MVP: `en`, `es`, `ca`.
- Build must fail on missing required locale keys for P0 screens.

## 10.3 Accessibility baseline
- Keyboard navigability for core workflows.
- Color contrast and focus indicators for validation and status UI.

## 11. Security Standards

## 11.1 Secrets and credentials
- No secrets in source code.
- Use environment-specific secret management.
- Rotate credentials and signing keys on defined schedule.

## 11.2 Data protection
- TLS for all service-to-service and client-to-server traffic.
- Encrypt sensitive at-rest data.
- Redact PII in logs and error payloads.

## 11.3 Local agent trust
- Signed job payloads and signed result payloads are mandatory.
- Nonce + expiry required to prevent replay.

## 11.4 Auditability
- Approval and submission events are immutable and tagged `LEGAL_CRITICAL`.
- Include actor, tenant, request ID, timestamp, and state transition context.

## 12. Telemetry and Instrumentation Standards

## 12.1 Logging standard
- JSON logs only.
- Mandatory fields: `timestamp`, `level`, `service`, `request_id`, `trace_id`, `tenant_id`, `case_id` (when applicable), `event_type`.
- Do not log raw document contents.

## 12.2 Metrics standard
Minimum metrics by domain:
- Extraction: run success/failure, confidence distribution.
- Validation: issue counts by type and severity.
- Forms: generation success/failure, mapping coverage gaps.
- Submission: outcome counts, retry counts, latency.
- Workflow: stage duration, stuck-case count.

## 12.3 Tracing standard
- OpenTelemetry-compatible trace propagation across API, workers, workflow engine, and local agent callbacks.
- Trace IDs must be returned in response metadata for supportability.

## 12.4 Alerting standard
P0 alerts:
- Submission failure spikes.
- Workflow stuck beyond threshold.
- Local agent heartbeat missing for active filing windows.
- Graph validation service unavailable.

## 13. Configuration Standards

## 13.1 Environment model
- Profiles: `dev`, `test`, `staging`, `prod`.
- Separate `onprem` profile overlays for storage and deployment differences.

## 13.2 Config source of truth
- Environment variables for deploy-time config.
- Typed config objects validated at startup.
- Fail-fast on missing mandatory config.

## 13.3 Feature flags
- Use feature flags for rollout of risky capabilities (for example online submission auto-dispatch).
- Flags must be tenant-aware where needed.

## 14. Versioning and Release Standards

## 14.1 API versioning
- Backward-compatible changes remain in same major API version.
- Breaking API changes require new major path (`/api/v2`).

## 14.2 Schema versioning
- Every DB schema change tracked by Alembic revision.
- Graph snapshots versioned and referenced by validation runs.

## 14.3 Form/mapping versioning
- Form template version and mapping version are required metadata on every generated artifact.

## 14.4 Release notes
- Every release must include migration notes and operational impact summary.

## 15. Testing and Quality Gates

## 15.1 Minimum quality gates for merge
- Unit tests for changed logic pass.
- Contract tests for changed API interfaces pass.
- Linting and type checks pass.
- Security checks pass for known high-risk categories.

## 15.2 Environment-specific test gates
- Local dev: SQLite-compatible tests and fast unit suites.
- CI/staging: PostgreSQL integration tests and workflow integration tests mandatory.

### 15.2a Plugin quality gates
- Contract conformance tests must pass for each plugin capability.
- Signature and manifest validation tests must pass.
- Compatibility tests must verify plugin activation against target core version.

## 15.3 E2E gates
- EX11 golden path required.
- At least one non-EX11 E2E path required before MVP release.
- Online and offline submission modes must each have at least one validated E2E scenario.

## 16. Documentation and Decision Standards

## 16.1 Documentation updates
Any change to architecture/design/contracts must update:
- Step 5.1 or Step 5.2 docs if affected.
- Relevant feature and requirement mappings if behavior changes.

## 16.2 Decision records
- Significant technical decisions require a short ADR-style entry in project docs.
- Each decision must include context, choice, alternatives, and impact.

## 16.3 Template governance records
- Template family changes must include a short template change record.
- Record must include:
  - old template version,
  - new template version,
  - migration impact,
  - required rollout actions.

## 17. Compliance Checklist for Step 5.3 Completion

Step 5.3 is complete when:
- Naming, API, ORM/DB, workflow, LLM, security, telemetry, and configuration standards are defined.
- Standards align with confirmed architecture decisions.
- Local SQLite development and PostgreSQL production compatibility rules are explicit.
- Online and offline filing mode standards are covered in testing and operations.
- Plugin runtime, governance, and capability contract standards are explicitly defined.
