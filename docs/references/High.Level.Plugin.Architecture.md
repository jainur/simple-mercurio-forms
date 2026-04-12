# Platform Plugin Architecture — Feasibility and Recommended Approach

**Document Type**: Architecture Decision  
**Status**: Approved for implementation  
**Last Updated**: April 2, 2026  
**Companion document**: PRODUCT_ROADMAP_PHASE9_FEATURES.md

---

## 1. Feasibility Summary

**Verdict: High feasibility.**

The codebase is already correctly layered for a plugin architecture. The `SubmissionAutomationExecutor` Protocol in `src/graphrag/workflows/browser_automation.py` is the exact pattern to generalise across all Phase A–H features. The main engineering effort is formalising and industrialising that pattern — not inventing something new.

Key existing assets:
- `SubmissionAutomationExecutor` — Python `Protocol`-based adapter contract (canonical template)
- `CaseRepository` — clean data-access abstraction (mockable, scope-injectable)
- Per-domain adapter modules (`reasoning_adapter.py`, `document_pipeline.py`, `channel_adapter.py`, `submission_orchestration.py`) — already separated from the API and state machine layers
- Temporal stub (`temporal_stub.py`) — async task runtime already scaffolded
- Alembic migration chain — straightforward to extend with new tables

**Anti-pattern to avoid**: Do not let the monolithic `src/graphrag/interfaces/api.py` grow further. API decomposition (Phase A2) is a prerequisite for all downstream phases.

---

## 2. Recommended Approach: Protocol + Registry Plugin Architecture

### Core Idea

Every cross-cutting capability (OCR, filing, channel ingestion, reasoning policy, HITL task type, workflow template) is expressed as a typed Python `Protocol`. A central `PluginRegistry` maps `(kind, name)` → implementing class. Tenant configuration selects which plugin is active at runtime. No platform code needs to change when a new provider or customer adapter is added.

**Why `Protocol` over ABC (Abstract Base Class)?**
- Consistent with the existing `SubmissionAutomationExecutor` pattern (structural subtyping).
- Simpler for third-party contributors — no import of a platform base class required.
- Runtime conformance check via `isinstance(instance, ProtocolClass)` with `@runtime_checkable`.

### Plugin Infrastructure (prerequisite for all phases)

New directory: `src/graphrag/plugins/`

| File | Purpose |
|---|---|
| `base.py` | Six typed `Protocol` contracts (see below) |
| `registry.py` | `PluginRegistry`: `register(kind, name, cls)` / `resolve(kind, name)` — validates conformance at registration |
| `loader.py` | Auto-discovers bundled adapters from `src/graphrag/adapters/` and third-party plugins via `importlib.metadata.entry_points` |

### The Six Plugin Kinds

| Kind | Roadmap Phases | Replaces / Extends |
|---|---|---|
| `OcrBackendPlugin` | B1 | Hardcoded Tesseract/PyMuPDF logic in `document_pipeline.py` |
| `FilingAdapterPlugin` | E1–E3 | Extends existing `SubmissionAutomationExecutor` Protocol |
| `ChannelIngestPlugin` | A2, Phase 6 | `channel_adapter.py` ingest logic |
| `ReasoningPolicyPlugin` | D3 | Hardcoded system prompts in `reasoning_adapter.py` |
| `HitlTaskPlugin` | F1–F3 | Task type definitions and result schemas |
| `WorkflowTemplatePlugin` | C1–C3 | Hardcoded `CaseState` enum and transition rules |

### Registry Usage Pattern

```python
# Registration (at startup, in loader.py or plugin's own module)
registry.register("ocr", "tesseract", TesseractAdapter)
registry.register("ocr", "google_document_ai", GoogleDocAIAdapter)
registry.register("filing", "html_form", HTMLFormFillerAdapter)

# Resolution (at request time, using tenant config)
ocr_backend = registry.resolve("ocr", tenant_config.ocr_backend)
result = ocr_backend.extract(document_bytes, mime_type, template)
```

---

## 3. Phase-by-Phase Implementation Plan

### Phase 0 — Plugin Infrastructure *(unblocks everything)*

1. Create `src/graphrag/plugins/base.py` with all six Protocol definitions.
2. Create `src/graphrag/plugins/registry.py` with `PluginRegistry`.
3. Create `src/graphrag/plugins/loader.py` with bundled + entry_point discovery.
4. Unit tests: register mock implementation, resolve by name, assert non-conforming class raises `TypeError`.

---

### Phase A — Integration Foundation *(parallel: A1 + A2)*

**A1: Multi-Tenancy**
- Add `tenant_id UUID NOT NULL` to all existing tables via a single Alembic migration.
- Add `TenantContext` FastAPI middleware: extracts tenant from JWT claim or `X-Tenant-ID` header.
- Add `workspace_id` for sub-tenant project scoping.
- Scope all `CaseRepository` queries: `WHERE tenant_id = :tenant_id`.
- RBAC: add `roles` claim to JWT; permission check decorator per endpoint.

**A2: API Decomposition**
- Split api.py into `APIRouter` sub-modules:
  - `routers/cases.py`, `routers/workflow.py`, `routers/reasoning.py`
  - `routers/documents.py`, `routers/submission.py`, `routers/channels.py`
  - `routers/monitoring.py`, `routers/tasks.py`, `routers/telemetry.py`
- No behaviour changes — pure structural decomposition.
- Add API version prefix: `/v1/...`
- Add standard API envelope: `request_id`, `api_version`, `error` schema on all responses.
- Add idempotency key middleware (dedup write operations via `idempotency_key` header).
- Add webhook subscription table + delivery substrate (sign payload with HMAC-SHA256).

**A3: SDKs** — defer until v1 API contracts stabilise; generate from OpenAPI spec.

*A1 and A2 are parallel. Both block all downstream phases.*

---

### Phase B — Document Intelligence *(OcrBackendPlugin)*

**B1: OCR Pipeline**
- Define `OcrBackendPlugin` Protocol:
  ```
  extract(bytes, mime_type, extraction_template) → OcrResult(fields: list[ExtractedField], confidence: float, model_provenance: str)
  ```
- Bundled adapters: `TesseractAdapter`, `GoogleDocAIAdapter`, `AWSTextractAdapter`, `ClaudeVisionAdapter`.
- `ExtractionTemplate`: JSON schema per document type — defines required fields, types, validation constraints.
- Field-level confidence: each `ExtractedField` carries `ocr_confidence`, `llm_confidence`, `flag` (high/low/needs_review).
- Translation and notarisation detection: flag in `OcrResult.metadata`.
- Store template definitions in new `document_type_templates` DB table (tenant-scoped).

**B2: Document Linking**
- `DocumentLinker` module: regex + LLM cross-reference detection in extracted text.
- Writes `REFERENCES` edge in Neo4j: `(doc_A)-[:REFERENCES {section}]->(doc_B)`.
- Temporal validity checker: flags post-deadline, stale, and conflicting-date documents.
- `DocumentInterdependencyMapper`: evaluates customer-defined proof-satisfaction rules (e.g., `birth_certificate + marriage_certificate → PROOF_OF_RELATIONSHIP`).
- *Depends on B1.*

**B3: Compliance Rules**
- `ComplianceRuleEngine`: evaluates JSON-defined proof-satisfaction trees with expiry constraints and alternative satisfaction paths.
- Evidence expiry warnings: `days_until_expiry`, `already_expired`, `exceeds_freshness_threshold` flags.
- Full document lifecycle audit: upload → analysis → review → rejection/re-upload → archive.
- Compliance report endpoint: `GET /v1/cases/{case_id}/compliance-report` (JSON/CSV/PDF).
- *Depends on B1.*

---

### Phase C — Workflow Orchestration *(WorkflowTemplatePlugin)*

**C1: Workflow Templates**
- New DB table `workflow_templates` (`template_id`, `tenant_id`, `name`, `version`, `definition_json`, `is_active`).
- `WorkflowTemplatePlugin` Protocol: `load(template_id) → WorkflowDefinition`.
- `WorkflowDefinition`: JSON/YAML schema defining states, transitions, guards, timeouts, SLAs, responsible roles.
- `CaseWorkflowEngine` resolves template from `cases.workflow_template_id` at runtime.
- New cases pick up the latest active version; in-flight cases remain on their original version.
- Pre-built templates for immigration, lending, corporate legal, appeals — stored as seed data.
- Visual editor: deferred (separate frontend project).

**C2: Signal Routing with Guards**
- Extend `state_machine.py`: transitions read guard conditions from template definition before firing.
- Guard DSL: simple expression language (`reasoning_run.confidence > 0.85 AND documents_complete == true`).
- Role-based signal permissions: signal emission checked against JWT role claim.
- Time-based signals: schedule via Temporal workflow timers or APScheduler.

**C3: Async Task Queue**
- `GenericTaskQueue` Protocol: `enqueue(task_type, payload, timeout, retries)` → `task_id`.
- Preferred implementation: Temporal (already stubbed in `temporal_stub.py`).
- Task type registry maps `task_type` string → handler function.
- HITL tasks are a special task type: `assigned_to_role`, `result_schema`, webhook on completion.

---

### Phase D — Intelligent Reasoning *(ReasoningPolicyPlugin)*

**D1: Domain Graph Builder**
- Generalise `build_immigration_graph.py` script into a `DomainGraphBuilder` service.
- API endpoint: `POST /v1/tenants/{tenant_id}/domain-graphs` (accepts SOP PDF, policy doc, or regulatory guidance).
- LLM extracts entities (Procedure, Requirement, Document, Fee, Deadline) and relationships.
- Writes into tenant-namespaced Neo4j subgraph (label prefix by `tenant_id`).
- Customers optionally refine via web editor (deferred) or PATCH API.

**D2: Eligibility Matrix**
- Generalise `eligibility_assessments` table: remove immigration-hardcoded Cypher queries.
- `EligibilityMatrixBuilder`: accepts any `procedure_id` from any tenant's domain graph.
- Output matrix: per-requirement rows with `status` (SATISFIED / PARTIALLY_SATISFIED / MISSING / CONFLICTING / NEEDS_REVIEW), `supporting_document_ids`, `confidence`, `last_updated`.
- Gap identification: for each MISSING row, suggest documents that would satisfy it.
- Requirement versioning: store `procedure_graph_version` on each `reasoning_run`.
- Multi-procedure comparison: `POST /v1/cases/{case_id}/reasoning/compare` — rank alternative procedures by coverage.

**D3: Reasoning Calibration**
- `ReasoningPolicyPlugin` Protocol: `get_system_prompt(tenant_id, policy_name) → str`.
- Tenant config selects active policy by name (conservative, permissive, domain-specific).
- A/B shadow-run harness: run same case input through two policy versions; persist both outputs with `policy_version` tag; comparison endpoint shows deltas.
- Full retrieval audit log: which graph nodes/edges searched, which chunks retrieved, citation mapping per claim.

---

### Phase E — Filing Adapters *(FilingAdapterPlugin)*

**E1: Portal-Agnostic Adapter Framework**
- Extend `SubmissionAutomationExecutor` into `FilingAdapterPlugin` Protocol with additional methods:
  - `capabilities() → FilingCapabilities` (declares supported filing types, auth method)
  - `dry_run(case_data, plan) → DryRunArtifact` (pre-filled PDF/data, no network call)
  - `calculate_fee(case_data, plan) → FeeBreakdown`
- Bundled adapters: `HTMLFormFillerAdapter` (wraps current Playwright code), `EmailSubmissionAdapter`, `RestApiAdapter`, `UscisElisAdapter`.
- `FormPopulationDSL`: JSON field-mapping schema (field mapping, type conversions, conditional population, validation).
- Portal credentials stored in tenant-scoped secrets store (never in application DB).

**E2: Multi-Channel Orchestration**
- `ChannelOrchestrator`: selects submission channel by ranking (cost, deadline proximity, confidence, tenant policy).
- Batch filing: group related cases by filing requirement, coordinate all-or-nothing submission.
- Hybrid workflows: multi-phase filing model (online portal + courier + payment) coordinated as a Temporal workflow.
- *Depends on E1.*

**E3: Receipt Management**
- `ReceiptParserPlugin` Protocol: `parse(receipt_bytes, mime_type) → ReceiptData` (filing_id, filing_date, next_deadline, confirmation_number, fee_received).
- Courier polling adapter Protocol: `poll_tracking(tracking_number) → DeliveryStatus`.
- Reconciliation checker: compare filed beneficiary count from plan vs. receipt; flag discrepancies as tasks.
- Auto-create monitoring deadlines from extracted `next_action_date`.
- *Depends on E1 + B1 (for OCR of receipt).*

---

### Phase F — HITL Framework *(HitlTaskPlugin)*

**F1: Generic Task Model**
- New DB table `hitl_tasks`: `task_id`, `tenant_id`, `case_id`, `task_type`, `assigned_to_role`, `assigned_to_user`, `priority`, `sla_hours`, `deadline_at`, `payload_json`, `result_schema_json`, `status` (created/assigned/in_progress/completed/rejected), `result_json`, `completed_at`, `duration_seconds`.
- `HitlTaskPlugin` Protocol: defines `task_type`, `result_schema`, `default_sla_hours`.
- Webhook emitter fires on every task state transition (signed, with task payload).
- Result ingestion endpoint: `POST /v1/tasks/{task_id}/complete` — validates against `result_schema_json`.

**F2: Escalation Rule DSL**
- `EscalationRuleEngine`: evaluates YAML escalation rules from roadmap specification.
- Condition evaluator: references case state, reasoning run fields, document counts, time-until-deadline, custom case tags.
- SLA breach handler: re-assigns task to next role in escalation chain; emits `task.overdue` webhook.
- Load balancing: assign to least-busy team member in role (query `hitl_tasks` for open task count per user).
- *Depends on F1.*

**F3: Feedback Loop**
- Join `hitl_tasks` with `cases` on closure outcome to build correlation table.
- Calibration metrics endpoint: `GET /v1/tenants/{tenant_id}/calibration-report` — attorney override accuracy, task override rate, confidence gap.
- Labeled dataset export: `GET /v1/tenants/{tenant_id}/hitl-export` — JSON with `{case_data, ai_assessment, human_override, final_outcome}`.
- *Depends on F2.*

---

### Phase G — Observability

**G1: Tenant Dashboards**
- New `metrics_snapshots` table: tenant-scoped time-series of case throughput, reasoning confidence, OCR success rate, HITL SLA rate, API latency percentiles.
- Background job (Temporal schedule or APScheduler): recomputes snapshots hourly.
- Dashboard endpoints: `GET /v1/tenants/{tenant_id}/metrics?from=...&to=...&procedure_type=...`.
- Custom alert table: threshold rules → `POST /v1/tenants/{tenant_id}/alerts` → evaluation on each snapshot → delivery via email/Slack/webhook.

**G2: Health and Circuit Breaker**
- `CircuitBreaker` utility in `src/graphrag/plugins/base.py`: wraps external calls; opens after N consecutive failures; half-opens after cooldown.
- Each plugin adapter base wraps `execute()` with `CircuitBreaker`.
- `GET /v1/tenants/{tenant_id}/health`: aggregates subsystem status (DB, Neo4j, OCR backend, Temporal, filing portals).
- Fallback routing: failed OCR backend → try next registered backend; failed filing adapter → try fallback channel.

**G3: Data Governance**
- PII log filter middleware: redacts SSN, passport number, DOB from structured logs.
- Field-level encryption: `pgcrypto`-based encryption for sensitive columns (SSN, passport_number) — decrypt only in authorised service layer.
- GDPR purge endpoint: `POST /v1/tenants/{tenant_id}/data-subject/{subject_id}/purge` — cascading delete with purge audit record.
- Data retention policy table: per tenant, per data-type retention period; Temporal schedule runs purge jobs.
- *Depends on A1 (tenant scoping).*

---

### Phase H — Marketplace *(Low priority)*

**H1: Extension Framework**
- Signed plugin packages: sign with platform keypair; verify at load time.
- Capability allowlist: tenant config declares which plugin kinds are enabled.
- Extension isolation: load third-party plugins in restricted subprocess with limited I/O.
- Marketplace registry: certified plugin listing endpoint; tenant enables/disables per workspace.
- Revenue attribution hook: metered usage per plugin call.

H2 and H3 are primarily business/operational deliverables with minimal platform code change.

---

## 4. Build Sequencing

```
Phase 0:  Plugin infrastructure          (no deps — unblocks all)
    │
Phase 1:  A1 multi-tenancy schema        (parallel)
          A2 API decomposition           (parallel)
    │
Phase 2:  B1 OCR adapters               (parallel)
          E1 filing adapter framework    (parallel — extends existing Protocol)
          F1 HITL task model             (parallel)
    │
Phase 3:  B2 doc linking                (needs B1)
          C1 workflow templates          (needs A2)
          D1 domain graph builder        (needs A2 + Neo4j)
    │
Phase 4:  B3 compliance rules           (needs B1)
          C2 signal routing guards       (needs C1)
          D2 eligibility matrix          (needs D1)
          E2 channel orchestration       (needs E1)
    │
Phase 5:  D3 reasoning calibration      (needs D2)
          F2 HITL escalation DSL         (needs F1)
          E3 receipt management          (needs E1 + B1)
          G1 dashboards                  (can layer at any point)
    │
Phase 6:  G2 health/circuit breaker     (parallel with G3)
          G3 data governance             (needs A1)
          F3 feedback loop               (needs F2)
    │
Phase 7:  H1 marketplace                (if prioritised)
```

---

## 5. Verification

1. **Plugin registry unit tests**: register mock Protocol implementation, resolve by name, assert non-conforming class raises `TypeError`.
2. **Tenant isolation integration test**: create data under two tenants, assert no cross-tenant rows returned by any repository method.
3. **OCR adapter smoke tests**: each bundled adapter returns `OcrResult` with correct schema; confidence in [0.0, 1.0].
4. **Filing adapter dry-run test**: `dry_run()` returns correct pre-filled artifact; no network call made.
5. **HITL task lifecycle test**: create → assign → complete → assert webhook payload matches `result_schema`.
6. **Escalation DSL test**: inject case state meeting a condition, assert correct task created with correct role and SLA.
7. **Existing smoke scripts**: all `scripts/phase*_smoke.py` pass without regression after API decomposition.

---

## 6. Decision Log

| Decision | Rationale |
|---|---|
| `Protocol` over `ABC` | Consistent with existing codebase; simpler for third-party contributors |
| Logical multi-tenancy (`tenant_id` column) | Appropriate for current scale; physical DB isolation deferred to G3 data residency option |
| Temporal for async tasks | Already stubbed; avoids second dependency (vs. Celery) |
| API decomposition before domain features | Monolithic `api.py` is a scaling and ownership bottleneck; must be resolved first |
| Bundled adapters ship alongside Protocols | Provides working reference implementations; customers can override without forking |
| No visual workflow editor now | Frontend project; decouple from backend API delivery |
| A3 SDKs deferred | Generate from stabilised OpenAPI spec; premature SDK means constant regeneration |

---

**Prepared for**: Engineering team  
**Covers**: Phases A through H from PRODUCT_ROADMAP_PHASE9_FEATURES.md