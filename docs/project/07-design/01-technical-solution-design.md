# Technical Solution Design (Step 5.2) — abogados-cowork

Last updated: 2026-04-18  
Status: Approved

## 1. Purpose

Define feature-level technical design aligned to the approved architecture, with enough detail to implement APIs, workflows, data contracts, and integration behaviors for MVP.

## 2. Design Principles

1. One canonical case model drives extraction, validation, forms, and filing.
2. Workflow state is authoritative in Temporal; UI shows projected state views.
3. External side effects are idempotent and auditable.
4. Human approval is a hard technical gate, not a UI convention.
5. Legal validation outputs must be citation-backed and explainable.
6. Same domain model and APIs for SaaS and on-prem.
7. Extensible capabilities are plugin-resolved while workflow state remains core-owned.

## 3. System Context and Boundaries

## 3.1 Internal components
- Web App (Next.js): assistant, lawyer, client, firm admin experiences.
- API (FastAPI): domain APIs and orchestration triggers.
- Worker services: extraction, validation, form generation, submission adapters.
- Workflow engine (Temporal): durable process execution.
- Data stores: PostgreSQL (production), SQLite (local dev via ORM), Neo4j, Redis, storage backend.
- Local agent (Tauri): FNMT-bound operations for Mercurio.
- Plugin runtime: capability registry and signed plugin lifecycle manager.

## 3.2 External dependencies
- Email delivery provider.
- Mercurio portal.
- LLM provider via abstraction layer (Gemini default implementation).
- Bootstrap graph artifacts from simple-graphrag.

## 4. Canonical Domain Model (Design View)

## 4.1 Core entities
- Tenant
- User
- Case
- CaseParty (client, lawyer, assistant relationships)
- Document
- DocumentClassification
- ExtractionRun
- ExtractedField
- ValidationRun
- ValidationIssue
- ProcedureSelection
- RequirementChecklistItem
- FormTemplate
- FormMappingVersion
- FormArtifact
- ApprovalDecision
- SubmissionAttempt
- SubmissionReceipt
- WorkflowInstance
- AuditEvent

## 4.2 Field-level provenance model
For every ExtractedField:
- field_key
- field_value
- confidence_score
- source_document_id
- source_locator (page/bbox or text span)
- source_snippet
- reasoning_summary
- extracted_at
- extracted_by_model
- correction_status
- corrected_value
- corrected_by
- corrected_at

## 4.3 Multi-form readiness model
Each Case maintains per-form readiness records:
- form_code
- mapping_coverage_percent
- unresolved_required_fields
- unresolved_validation_issues
- approval_status
- filing_eligibility_status

This supports all EX forms while still sequencing EX11 first.

## 5. Workflow Design (F10)

## 5.1 CaseLifecycleWorkflow states
1. CASE_CREATED
2. INTAKE_IN_PROGRESS
3. DOCUMENTS_UPLOADED
4. EXTRACTION_IN_PROGRESS
5. EXTRACTION_REVIEW_REQUIRED
6. LEGAL_VALIDATION_IN_PROGRESS
7. REQUIREMENTS_GAP_OPEN
8. FORM_GENERATION_IN_PROGRESS
9. LAWYER_REVIEW_PENDING
10. APPROVED_FOR_SUBMISSION
11. SUBMISSION_MODE_SELECTED
12. ONLINE_SUBMISSION_DISPATCHED
13. ONLINE_SUBMISSION_SUCCEEDED
14. ONLINE_SUBMISSION_FAILED_RETRYABLE
15. ONLINE_SUBMISSION_FAILED_BLOCKED
16. OFFLINE_PACKET_READY
17. OFFLINE_FILED_CONFIRMED
18. CLOSED

## 5.2 Transition guardrails
- No transition to APPROVED_FOR_SUBMISSION without ApprovalDecision.approved=true.
- No transition to FORM_GENERATION_IN_PROGRESS if blocking ValidationIssue exists.
- No transition to SUBMISSION_MODE_SELECTED unless required form artifacts exist for selected form.
- Online path: SUBMISSION_MODE_SELECTED -> ONLINE_SUBMISSION_DISPATCHED requires local-agent availability and valid signing context.
- Offline path: SUBMISSION_MODE_SELECTED -> OFFLINE_PACKET_READY requires complete, validated filing packet export.
- OFFLINE_FILED_CONFIRMED requires explicit user confirmation metadata (who filed, when, external reference if available).

## 5.3 Retry and compensation
- Extraction and validation activities: retry with bounded exponential backoff.
- Online submission activity: retry only through supervised retry command.
- Offline submission path: no automated retry; workflow waits for user confirmation or correction loop.
- Compensation events are audit-only (no destructive rollback of evidence).

## 6. Feature-Level Design

## 6.1 F01 Case Management
APIs:
- POST /api/v1/cases
- GET /api/v1/cases/{case_id}
- PATCH /api/v1/cases/{case_id}
- POST /api/v1/cases/{case_id}/assign

Design details:
- Case creation writes Case row and emits CASE_CREATED event.
- Assignment changes append audit events and notify assignee.
- Case status is read from workflow projection, not manually editable.

## 6.2 F02/F03 Intake and Document Management
APIs:
- POST /api/v1/cases/{case_id}/intake
- POST /api/v1/cases/{case_id}/documents
- GET /api/v1/cases/{case_id}/documents
- PATCH /api/v1/documents/{document_id}/classification

Design details:
- Upload stores file in configured storage backend and metadata in PostgreSQL.
- Document classification service runs async and suggests type/tags.
- Assistant can confirm/override classification before extraction lock-in.

## 6.3 F04 Extraction and Canonical Normalization
APIs:
- POST /api/v1/cases/{case_id}/extraction-runs
- GET /api/v1/cases/{case_id}/extracted-fields
- PATCH /api/v1/extracted-fields/{field_id}

Design details:
- Extraction run creates immutable ExtractionRun record.
- Each extracted field persists provenance and reasoning metadata.
- Assistant and lawyer UI consume extracted field view with confidence and source preview.
- Correction updates preserve original value and write correction metadata.

## 6.4 F05/F06 GraphRAG Validation and Procedure Scoping
APIs:
- POST /api/v1/cases/{case_id}/validation-runs
- GET /api/v1/cases/{case_id}/validation-issues
- POST /api/v1/cases/{case_id}/procedure-selection
- GET /api/v1/cases/{case_id}/requirements-checklist

Design details:
- Validation worker queries Neo4j using deterministic templates first.
- Validation execution resolves active `validation.rule_pack` plugin by capability and version.
- Every ValidationIssue stores citation payload:
  - reference_id
  - citation_text
  - graph_node_ids
  - graph_snapshot_version
- ProcedureSelection combines legal fit score + completeness score.
- Checklist item statuses: REQUIRED_MISSING, REQUIRED_UPLOADED, VERIFIED, WAIVED_WITH_REASON.

## 6.5 F07 Form Generation and PDF Autofill
APIs:
- POST /api/v1/cases/{case_id}/forms/{form_code}/generate
- GET /api/v1/cases/{case_id}/forms/{form_code}/artifacts
- GET /api/v1/forms/{form_code}/mapping-coverage

Design details:
- Form mapping service resolves active `form.pack` plugin and loads versioned field map per form_code.
- Generation fails fast when unresolved mandatory fields exist.
- Generated output stores:
  - artifact_uri
  - template_version
  - mapping_version
  - generated_from_validation_run_id
- EX11 path is first certified E2E, but all EX forms must have mapping + readiness checks.

## 6.6 F08 Lawyer Approval Gate
APIs:
- POST /api/v1/cases/{case_id}/approvals
- GET /api/v1/cases/{case_id}/approvals

Design details:
- Decision types: APPROVE, RETURN_FOR_CORRECTION, REJECT.
- Approval command checks actor role and current workflow state.
- Approval events are immutable and trigger workflow transitions.

## 6.7 F09a/F09b Mercurio Submission + Local Agent (Tauri)
APIs:
- POST /api/v1/cases/{case_id}/submission-dispatch
- POST /api/v1/cases/{case_id}/submission-mode
- GET /api/v1/cases/{case_id}/submission-attempts
- POST /api/v1/submission-attempts/{attempt_id}/retry
- POST /api/v1/cases/{case_id}/offline-filing-confirmation
- POST /api/v1/local-agent/heartbeat

Agent protocol design:
1. Control plane creates signed submission job with nonce and expiry.
2. Tauri agent polls or subscribes to firm-scoped queue.
3. Agent validates signature, executes Playwright flow with local certificate context.
4. Agent posts signed result with artifacts (receipt, logs, outcome code).
5. Backend validates response signature and records SubmissionAttempt.

Channel plugin design:
- Submission dispatch resolves active `submission.channel` plugin for selected mode.
- MVP channel plugins:
  - `ONLINE_MERCURIO`
  - `OFFLINE_PDF`
- Channel plugins are responsible for dispatch semantics; workflow transitions remain core-owned.

Submission outcome model:
- SUCCESS
- PARTIAL
- RETRYABLE_FAILURE
- BLOCKED_FAILURE

Submission mode model:
- ONLINE_MERCURIO
- OFFLINE_PDF

Offline flow design:
1. Lawyer-approved case enters SUBMISSION_MODE_SELECTED with OFFLINE_PDF.
2. System generates filing packet bundle (filled forms, checklist, supporting docs index).
3. Assistant/lawyer performs external offline filing process.
4. User confirms filing with reference metadata, transitioning to OFFLINE_FILED_CONFIRMED.

## 6.8 F11/F12 Tenant Admin and RBAC
APIs:
- POST /api/v1/tenants/{tenant_id}/users
- PATCH /api/v1/users/{user_id}/role
- POST /api/v1/users/{user_id}/deactivate

Design details:
- Every request resolves tenant context from auth token + path checks.
- Role matrix enforced in API policy layer.
- Security audit event emitted for every privilege change.

## 6.9 F13 Internationalization
Design details:
- Locale files versioned by release.
- Translation keys validated at CI time.
- Case/legal labels stored as stable key + localized display string.

## 6.10 F14 Audit and Traceability
APIs:
- GET /api/v1/cases/{case_id}/audit-events
- GET /api/v1/audit-events?actor_id=&event_type=&from=&to=

Design details:
- Append-only event store table with hash-chain optional extension.
- Event payload includes actor, tenant, workflow_state_before, workflow_state_after.
- Submission and approval events tagged as LEGAL_CRITICAL.

## 6.11 F19 Plugin Runtime and Capability Registry
APIs:
- POST /api/v1/plugins/install
- POST /api/v1/plugins/{plugin_id}/enable
- POST /api/v1/plugins/{plugin_id}/disable
- GET /api/v1/plugins
- GET /api/v1/plugins/{plugin_id}/health

Design details:
- Plugins are loaded from signed manifests and validated for compatibility.
- Capability resolver maps capability key + contract version to active plugin implementation.
- Required MVP capabilities:
  - domain.logic
  - form.pack
  - validation.rule_pack
  - submission.channel
  - llm.provider
- Plugin lifecycle actions emit immutable audit events.

Plugin manifest (minimum):
- plugin_id
- plugin_version
- capabilities
- api_contract_version
- core_compatibility
- config_schema
- permissions_required
- signature_metadata

## 7. Data Store Design

## 7.1 PostgreSQL schema groupings
- auth_* tables for identity and roles.
- case_* tables for case and workflow projections.
- doc_* tables for document metadata and classification.
- extract_* tables for extraction runs and fields.
- validate_* tables for legal checks and issues.
- form_* tables for templates, mappings, artifacts.
- submit_* tables for submission attempts and receipts.
- audit_* tables for immutable events.

ORM and local DB design note:
- SQLAlchemy models are canonical persistence contracts.
- Alembic migrations target PostgreSQL baseline schema.
- SQLite local mode uses same ORM models with compatibility guardrails (avoid PostgreSQL-only SQL in core repositories).

## 7.1a Repository and portability contracts
- Repository layer must isolate vendor-specific SQL.
- JSON and enum usage must provide SQLite-compatible fallback representations in local mode.
- Integration tests must run against PostgreSQL; local developer tests may run on SQLite.

## 7.2 Neo4j query contracts
Minimum deterministic query templates:
- get_eligibility_rules(procedure, applicant_profile)
- get_required_documents(procedure)
- get_deadlines_and_fees(procedure)
- get_legal_references(requirement_or_rule)
- detect_rule_conflicts(case_facts, procedure)

## 7.3 Storage abstraction design
StorageAdapter interface:
- put_object(path, bytes, metadata)
- get_object(path)
- create_signed_url(path, ttl)
- delete_object(path)

Implementations:
- S3Adapter (SaaS default)
- S3CompatibleAdapter (on-prem object storage)
- LocalFilesystemAdapter (on-prem compact mode)

## 7.4 Plugin contract registry design
Registry model:
- capability_key
- contract_version
- plugin_id
- plugin_version
- activation_status
- tenant_scope

Runtime guarantees:
- Exactly one active plugin per capability/tenant scope in MVP.
- Contract incompatibility blocks activation.
- Plugin disablement must not corrupt in-flight workflow state.

## 8. Caching and Performance Design

Cache keys:
- tenant:{tenant_id}:procedure:{procedure_id}:requirements:v{graph_snapshot}
- tenant:{tenant_id}:form:{form_code}:mapping:v{mapping_version}
- tenant:{tenant_id}:case:{case_id}:ui_projection:v{projection_version}

Policies:
- TTL for legal retrieval cache: short, invalidated by graph snapshot changes.
- No caching of mutable approval decisions.
- PII-heavy extracted payloads cached only when encrypted and short-lived.

## 9. Security Design Details

1. Authentication
- JWT with tenant and role claims.
- Short-lived access tokens and revocable refresh tokens.

2. Authorization
- Policy checks at endpoint and service layers.
- Cross-tenant access denied by default.

3. Sensitive data controls
- Encrypt extraction provenance and document metadata with field-level encryption where needed.
- Redact sensitive snippets in logs.

4. Local agent trust model
- Mutual trust via key pairs and signed job/result payloads.
- Replay protection with nonce and expiry windows.

## 10. Error Handling and Supportability

Error categories:
- USER_CORRECTABLE
- SYSTEM_TRANSIENT
- SYSTEM_FATAL
- EXTERNAL_DEPENDENCY

Support runbook anchors:
- Failed extraction rerun command.
- Validation rerun with graph snapshot pinning.
- Submission retry with manual approval requirement.

## 11. Observability Design

Metrics (minimum):
- extraction_run_success_total
- extraction_field_confidence_distribution
- validation_issue_count_by_type
- form_generation_fail_total
- approval_cycle_time_seconds
- submission_attempt_outcome_total

Traces:
- trace_id propagated across API, workflow, workers, and local-agent callbacks.

Logs:
- JSON structured logs with case_id, tenant_id, workflow_id, actor_id, event_type.
- Plugin logs include plugin_id, capability_key, plugin_version.

## 12. Test Design Strategy

1. Unit tests
- Mapping logic, validation rule adapters, permission policies.

2. Contract tests
- API contracts for case, extraction, validation, submission.
- Local agent job/result schema contracts.

3. Integration tests
- PostgreSQL + Neo4j + workflow integration path.
- Storage adapter compatibility (S3 and local filesystem).

3a. Local profile tests
- SQLite compatibility tests for repository layer and core CRUD paths.
- Workflow state projection tests in local profile.

3b. Plugin contract tests
- Capability contract conformance tests per plugin type.
- Manifest/signature/compatibility validation tests.
- Negative tests for unauthorized or incompatible plugin activation.

4. End-to-end tests
- EX11 golden path.
- At least one non-EX11 path for all-EX readiness regression.
- Lawyer return-for-correction loop.
- Submission retry path.

## 13. Design Linkage to Step 5.3 (Resolved)

1. Endpoint naming conventions and API error envelope are defined in Technical Standards section 6.
2. RBAC representation and enforcement standards are defined in Technical Standards sections 6.5 and 7.
3. Translation workflow and locale governance are defined in Technical Standards section 10.2.
4. Audit integrity baseline is defined in Technical Standards sections 11.4 and 14.

## 13.1 LLM abstraction contract (resolved direction)
Interface:
- `extract_fields(document, schema_hint, locale) -> ExtractedField[]`
- `summarize_reasoning(extraction_context) -> reasoning_summary`
- `health_check() -> provider_status`

Implementations:
- GeminiProvider (default)
- Future providers through same interface without domain-service rewrites

Pluginization note:
- LLM providers are implemented as `llm.provider` plugins and resolved by capability registry.

## 14. Risks and Mitigations (Design Level)

1. Risk: all-EX coverage breadth may dilute quality.
- Mitigation: enforce per-form mapping coverage gate and regression suite.

2. Risk: local-agent operational variability across law firm machines.
- Mitigation: Tauri diagnostics bundle, health checks, and setup validation wizard.

3. Risk: legal graph drift from regulatory changes.
- Mitigation: ad-hoc triggered graph snapshot updates with version pinning in validation runs.

4. Risk: extraction confidence ambiguity in legal contexts.
- Mitigation: mandatory provenance UI and lawyer override controls before filing.

## 15. Step 5.2 Exit Criteria

Step 5.2 is complete when:
- Each P0 feature has a technical design path.
- API, workflow, data, and integration contracts are defined at implementation level.
- Security, observability, and testing are covered for MVP.
- Open design decisions are listed for standards and sprint planning.

## 16. P0 User Story Alignment Matrix

This matrix confirms Step 4 P0 user stories are explicitly covered by Step 5.2 design sections.

| User Story | Design Coverage |
|---|---|
| US-001, US-002, US-003 | 6.1 F01 Case Management; 5.1 workflow states; 5.2 guardrails |
| US-010, US-011, US-012 | 6.2 F02/F03 Intake and Document Management |
| US-013, US-014 | 4.2 provenance model; 6.3 F04 Extraction and Canonical Normalization |
| US-020, US-021, US-022, US-023, US-024 | 6.4 F05/F06 GraphRAG Validation and Procedure Scoping; 6.11 F19 Plugin Runtime |
| US-030, US-031, US-032, US-032a | 4.3 multi-form readiness; 6.5 F07 Form Generation and PDF Autofill; 6.11 F19 Plugin Runtime |
| US-033 | 6.6 F08 Lawyer Approval Gate; 5.2 transition guardrails |
| US-034, US-035, US-036 | 5.1 workflow states; 6.7 F09a/F09b Submission and Local Agent; 6.11 F19 Plugin Runtime |
| US-040, US-041 | 6.8 F11/F12 Tenant Admin and RBAC |
| US-042 | 6.9 F13 Internationalization |
| US-043, US-044 | 6.10 F14 Audit and Traceability; 6.11 F19 Plugin Runtime |

Alignment rule:
- Any new P0 user story added in Step 4 must include a corresponding design section reference in this matrix before Step 5.2 can be considered complete.
