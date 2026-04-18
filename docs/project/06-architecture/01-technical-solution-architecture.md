# Technical Solution Architecture (Step 5.1) — abogados-cowork

Last updated: 2026-04-18  
Status: Approved

## 1. Purpose

Define the target technical architecture for abogados-cowork, covering platform topology, technology stack, data architecture, multi-tenancy, versioning, caching, security, integrations, and operational concerns for MVP and immediate scale.

## 2. Architecture Goals

1. Support end-to-end EX procedure automation with EX11 as first complete path.
2. Keep a single codebase deployable as SaaS and on-prem.
3. Guarantee durable workflow execution for long-running legal processes.
4. Enforce legal-grade traceability for extraction, validation, approvals, and filing.
5. Keep architecture extensible for post-MVP integrations and domain expansion.

## 3. High-Level Architecture Style

Hybrid cloud-local workflow architecture with five execution planes:

1. Presentation plane
- Web application for assistant, lawyer, client, and firm admin workflows.

2. Control plane (cloud or on-prem app backend)
- API, auth, workflow orchestration, business rules, audit, notifications.

3. Intelligence plane
- Document extraction pipeline plus GraphRAG legal validation services.

4. Execution plane (local bridge)
- Local agent on firm infrastructure for FNMT certificate-bound Mercurio actions.

5. Extensibility plane
- Plugin runtime and capability registry for domain logic, form packs, rule packs, submission channels, and provider adapters.

This split keeps legal filing actions close to certificate context while centralizing workflow state and business logic.

## 4. Proposed Technology Stack

## 4.1 Frontend and user-facing
- Framework: Next.js (TypeScript, App Router).
- UI components: reusable design-system components with i18n-ready labels.
- i18n: message-catalog approach with English, Spanish, Catalan locales.
- Real-time updates: WebSocket or Server-Sent Events for in-app notifications and workflow status.

## 4.2 Backend and API
- API framework: FastAPI (Python).
- API style: REST-first for MVP with versioned endpoints.
- ORM and migrations: SQLAlchemy ORM + Alembic migrations.
- Background jobs and durable workflows: Temporal.
- Event integration: Outbox pattern for reliable event publication.

## 4.3 Data and storage
- SQL operational database: PostgreSQL.
- Local development SQL mode: SQLite supported via ORM for developer environments and lightweight local testing.
- Graph legal knowledge store: Neo4j.
- Object/document storage: S3-compatible storage (SaaS) or MinIO/S3-compatible equivalent (on-prem).
- Cache and short-lived state: Redis.

## 4.4 AI and extraction
- OCR and extraction pipeline: Python extraction services with provider abstraction.
- LLM access: provider-agnostic adapter interface with Gemini as default provider implementation; swappable without domain logic changes.
- GraphRAG retrieval: Cypher template retrieval + citation packaging.

## 4.5 Portal automation and local bridge
- Browser automation: Playwright (Python).
- Local bridge runtime: Tauri-based local agent.
- Secure command channel between API workflow and local agent.

## 5. Logical Component Model

## 5.1 Core services
1. Identity and Access Service
- Authentication, RBAC, tenant context enforcement.

2. Case Service
- Case lifecycle, assignment, metadata, status transitions.

3. Document Service
- Upload APIs, smart document identification, tagging, document lifecycle.

4. Extraction Service
- OCR, field extraction, confidence scoring, provenance generation.

5. Validation Service
- GraphRAG-driven business and legal validation.

6. Procedure Service
- Procedure scoping, requirement checklists, readiness status.

7. Form Service
- EX form mappings, prefill pipeline, output artifact generation.

8. Approval Service
- Lawyer gate, return-for-correction loops, rationale capture.

9. Submission Service
- Mercurio submission orchestration, retries, outcome capture.

10. Audit and Compliance Service
- Immutable event records, consent and processing metadata.

11. Notification Service
- Email and in-app real-time alerts.

12. Tenant Admin Service
- Firm-level user and role administration.

13. Plugin Runtime and Capability Registry Service
- Plugin discovery, signature verification, capability registration, lifecycle management, and plugin telemetry.

## 5.2 Workflow orchestration model
- User-visible workflow: stage model shown in UI.
- Durable workflow: Temporal workflow state machine for long-running execution.
- Activity boundaries:
  - Document ingest and extraction.
  - Graph validation.
  - Form generation.
  - Approval wait state.
  - Local submission dispatch.
  - Submission status reconciliation.

## 6. Data Architecture

## 6.1 Canonical data domains (PostgreSQL)
- Tenant and user domain.
- Case and workflow domain.
- Canonical applicant profile domain.
- Extraction result and provenance metadata domain.
- Form artifact and mapping execution domain.
- Approval decision domain.
- Submission attempt and outcome domain.
- Audit event domain.

Portability note:
- Schema and query design must stay compatible with both PostgreSQL (production default) and SQLite (local development profile).
- PostgreSQL-specific features should be isolated behind repository abstractions when unavoidable.

## 6.2 Legal knowledge graph (Neo4j)
Source and schema:
- Bootstrap source: simple-graphrag artifacts (`graph_nodes.jsonl`, `graph_relationships.jsonl`).
- Canonical schema source: `legal_schema.py` in simple-graphrag.

Core usage patterns:
- Eligibility checks.
- Requirement and document checklist derivation.
- Legal conflict detection.
- Citation lookup for explainability.

## 6.3 Document and artifact storage
- Store uploaded documents and generated forms in object storage.
- Store only metadata and references in PostgreSQL.
- Use content hash and immutable versioned object keys for traceability.

## 6.4 Reference data
Reference data domains include:
- Form definitions and field maps.
- Procedure configuration metadata.
- Document type taxonomy and tag catalog.
- Supported locale catalogs.

Reference data must be versioned and environment-portable.

## 7. Multi-Tenancy Strategy

## 7.1 Tenant model
- Tenant equals one law firm.
- SaaS: logical tenant isolation in shared control plane.
- On-prem: isolated customer deployment (single-tenant by deployment).

## 7.2 Tenant isolation controls
- Tenant ID mandatory in all business records.
- Tenant-aware query filters enforced at service and persistence layers.
- RBAC checks include tenant scope.
- Object storage paths namespaced per tenant.

## 7.3 Graph tenancy model
- MVP graph is product-managed shared legal graph.
- Tenant data is not written into legal graph nodes.
- Case-specific validation inputs are transient query context, not persistent graph mutations.

## 8. Caching Strategy

1. Redis cache tiers
- Short-lived retrieval caches for graph validation query results.
- API response caches for static reference data.
- Session and websocket presence support.

2. Cache invalidation rules
- Reference data version bump invalidates dependent caches.
- Graph snapshot version bump invalidates legal validation caches.
- Tenant-level cache keys to avoid cross-tenant leakage.

3. Do-not-cache data
- Approval decisions and submission outcomes.
- PII-heavy extraction payloads unless encrypted and short-lived.

## 9. Versioning Strategy

## 9.1 API versioning
- URL-based semantic versioning (`/api/v1/...`) for external and frontend contract stability.

## 9.2 Workflow versioning
- Temporal workflow definitions versioned by workflow type and compatible migration strategy.
- New workflow versions support in-flight case continuity.

## 9.3 Graph and rule versioning
- Every graph snapshot carries:
  - `schema_version`
  - `source_capture_date`
  - `valid_from`
  - `valid_to`
- Validation results record graph snapshot version used.

## 9.4 Form and mapping versioning
- Each EX form mapping has explicit mapping version.
- Generated form artifacts record form template version and mapping version.

## 10. Integration Architecture

## 10.1 MVP integrations
- simple-graphrag data bootstrap pipeline to Neo4j.
- Mercurio portal automation via local agent.
- Email provider integration.

## 10.2 Post-MVP integration extension points
- PMS connector interface boundary.
- Webhook/event adapter framework.
- External identity provider support (optional future).

## 10.4 Plugin integration contracts
- Capability contracts are versioned and resolved at runtime by capability key.
- Required MVP plugin capabilities:
  - domain.logic
  - form.pack
  - validation.rule_pack
  - submission.channel
  - llm.provider
- Core workflow state remains platform-owned; plugins may not directly mutate workflow persistence tables.
- Plugin lifecycle events (install, enable, disable, upgrade) must be auditable.

## 10.3 Local agent integration contract
- Control-plane dispatches signed job payload.
- Local agent validates signature, executes certificate-bound activity, returns signed result.
- Workflow engine reconciles result and persists immutable submission event.

## 11. Security and Privacy Architecture

## 11.1 Identity and authorization
- Role-based access controls by actor type.
- Tenant-scoped authorization checks on every protected action.
- Least-privilege defaults.

## 11.2 Data protection
- TLS in transit.
- Encryption at rest for database and object storage.
- Secret management via deployment-specific secret stores.
- Document access URLs short-lived and scoped.

## 11.3 GDPR controls
- Data minimization in extraction storage.
- Data subject export and deletion workflows.
- Processing activity and consent audit records.

## 11.4 Audit integrity
- Immutable append-only audit event model for approvals, validation outcomes, and submission events.
- Tamper-evident hashes for high-sensitivity event classes (recommended for MVP if feasible, mandatory post-MVP).

## 12. Reliability and Resilience

- Durable workflows with retry policies and backoff.
- Idempotency keys for external side effects (filing attempts, notification sends).
- Dead-letter handling for failed background activities.
- Graceful degradation for temporary AI/provider failures.
- Manual recovery tools for failed cases.

## 13. Observability and Operations

- Structured logs with tenant-safe redaction.
- Metrics:
  - extraction success rate
  - validation pass/fail rates
  - form generation success rate
  - submission success and retry rates
- Trace spans across API, workflow, extraction, graph validation, and local agent dispatch.
- Operational dashboards per environment and tenant scope.

## 14. Deployment Architecture

## 14.1 SaaS deployment
- Managed cloud deployment operated by platform owner.
- Multi-tenant control plane services.
- Shared legal graph and shared service tier.
- Per-tenant logical data isolation.

## 14.2 On-prem deployment
- Customer-operated deployment.
- Single-tenant topology by default.
- Same application components and APIs as SaaS.
- Optional reduced operational profile for smaller firms.

## 14.3 Recommended MVP topology options
1. Standard topology
- Next.js app
- FastAPI app
- Temporal server + worker
- PostgreSQL
- Neo4j
- Redis
- Object storage (S3-compatible in SaaS; object storage or local filesystem in on-prem)

2. Compact topology (resource constrained firms)
- Same components with reduced scale settings and documented operational limits.
- Storage profile: local filesystem storage is allowed for on-prem compact deployments.

## 15. Architecture Decisions and Status

| Decision | Status | Rationale |
|---|---|---|
| Backend with FastAPI + Python | Confirmed | Alignment with extraction, GraphRAG, Playwright ecosystem |
| Durable orchestration with Temporal | Confirmed | Required for long-running approvals and retries |
| PostgreSQL as system-of-record SQL store | Confirmed | Strong consistency, relational integrity, audit workflows |
| SQLAlchemy ORM + Alembic migrations | Confirmed | Supports clean domain persistence and controlled schema evolution |
| SQLite local development profile | Confirmed | Faster local setup while preserving production compatibility via ORM |
| Neo4j for legal graph validation | Confirmed | Required by FR-026 and existing simple-graphrag assets |
| Redis for caching and ephemeral coordination | Confirmed | Performance and real-time support |
| Storage for docs/artifacts | Confirmed | SaaS uses S3-compatible object storage; on-prem supports object storage or local filesystem |
| Shared product-managed legal graph for MVP | Confirmed | Matches FR-029 and legal-expert maintenance model |
| Local agent required for FNMT certificate steps | Confirmed | Required by FR-051 and operational reality |
| On-prem topology options | Confirmed | MVP supports both standard and compact topology profiles |
| Local agent runtime | Confirmed | Tauri selected for Step 5.2 design |
| Legal graph update cadence | Confirmed | Ad-hoc, trigger-based updates |
| Plugin-first extensibility model | Confirmed | Domain logic, form packs, rule packs, and submission channels implemented via capability contracts |
| Plugin governance model | Confirmed | Signed manifests, compatibility checks, tenant-safe permissions, and auditable lifecycle actions |

## 16. Contradictions, Risks, and Feedback Required

## 16.1 No direct contradictions with prior steps
Architecture is consistent with Steps 0 to 4.

## 16.2 Risk and tension points
1. Scope-risk tension
- All EX forms are P0 while EX11 is the first full path. Breadth may threaten timeline for solo build.

2. Dual deployment complexity
- SaaS plus on-prem from day one increases operational and support overhead.

3. Local certificate automation complexity
- FNMT local integration introduces significant setup and support variance by firm environment.

4. Graph coverage gap risk
- Existing graph has fewer Form nodes than full EX coverage target; enrichment pipeline is required.

5. Plugin complexity risk
- Plugin-first scope can increase runtime complexity. Mitigation: strict capability contracts and core-owned workflow state boundaries.

## 16.3 Decision confirmations
1. Baseline stack confirmed: FastAPI + Temporal + PostgreSQL + Neo4j + Redis + storage profile per deployment mode.
2. On-prem MVP topology confirmed: both standard and compact profiles.
3. Local agent runtime confirmed: Tauri.
4. Legal graph update cadence confirmed: ad-hoc trigger-based.

## 17. Step 5.1 Exit Criteria

Step 5.1 is complete when:
- Architecture covers stack, data stores, caching, versioning, security, integrations, and deployment models.
- Core decisions are recorded with status.
- Risks and unresolved feedback points are explicit.
- Traceability to requirements is intact.
