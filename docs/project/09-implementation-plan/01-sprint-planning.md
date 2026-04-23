# Implementation Plan and Sprint Planning (Step 6.1) — abogados-cowork

Last updated: 2026-04-18  
Status: Approved

## 1. Purpose

Define a realistic sprint plan for a solo build, aligned with approved requirements, feature definitions, architecture, technical design, and technical standards.

## 2. Planning Assumptions

1. Delivery model: solo developer with AI-assisted implementation.
2. Sprint length: 2 weeks.
3. Planning horizon: 8 MVP sprints + 1 stabilization sprint.
4. Extensibility is implemented via dependency injection (DI) from MVP implementation start. No plugin runtime or registry is present in the MVP.
5. PostgreSQL is production DB; SQLite is local-dev profile.
6. Online and offline filing modes are both required for MVP acceptance.

## 3. MVP Scope Boundaries for This Plan

Included in this sprint plan:
- P0 requirements including FR-080 to FR-087 (DI-based extensibility model).
- All EX forms in MVP scope, with EX11 as first full end-to-end certified path.
- Mercurio online path and offline PDF path.

Not included in MVP sprint scope:
- PMS integrations (post-MVP).
- Knowledge graph authoring UI (post-MVP).
- Marketplace-style third-party plugin onboarding (post-MVP).

## 4. Delivery Strategy

1. Build thin vertical slices early:
- Establish one end-to-end flow quickly (EX11), then harden and expand.

2. Keep core state centralized:
- Workflow state remains core-owned, with extensible capabilities injected/configured via DI.

3. Implement DI-based extensibility before broad feature expansion:
- Avoid retrofitting extensibility after business logic is deeply embedded.

4. Treat all-EX support as progressive coverage with hard release gate:
- Mappings/checks can be incrementally delivered, but MVP release requires full EX coverage.

## 5. Sprint Plan Overview

## Sprint 0 — Foundations and Scaffolding
Objective:
- Establish implementation baseline and scaffolding model.

Scope:
- Repository/service skeleton aligned with standards.
- Template families bootstrap (`templates/` layout and initial generator command).
- CI baseline (lint, tests, type checks, structure checks).
- Core config profiles (`dev`, `test`, `staging`, `prod`, `onprem`).

Key deliverables:
- Project scaffold command available.
- Base FastAPI + Next.js + Temporal + SQLAlchemy + Alembic skeleton.
- SQLite local profile functional.

Exit checks:
- Template catalog IDs from standards represented in scaffolding repository/folder.
- CI passes on generated API/Web/Worker templates.

## Sprint 1 — Core Platform and Security
Objective:
- Build tenant-aware platform foundation.

Scope:
- Auth, tenant context, RBAC baseline.
- Case creation and assignment APIs (F01).
- Audit event baseline (F14).
- API error envelope and idempotency middleware baseline.

Key deliverables:
- Assistant/lawyer can create and assign cases.
- Tenant isolation enforced in API layer.
- Audit events recorded for core case actions.

Exit checks:
- US-001, US-002 partial readiness.
- Cross-tenant access tests pass.

## Sprint 2 — Plugin Runtime v1 (P0 critical)
Objective:
- Deliver plugin runtime and capability registry for core extension points.

Scope:
- Plugin manifest parser/validator.
- Signature verification path.
- Capability registry and resolver.
- Plugin lifecycle APIs (install/enable/disable/list/health).
- Plugin telemetry and lifecycle audit events.

Key deliverables:
- F19 baseline functional.
- One active plugin per capability enforced.

Exit checks:
- US-044 ready.
- Contract/safety tests for plugin activation and incompatibility pass.

## Sprint 3 — Intake, Documents, Extraction, Provenance
Objective:
- Make intake and extraction workflows usable with provenance visibility.

Scope:
- Intake APIs/UI path.
- Document upload, smart classification, tagging.
- Extraction pipeline with confidence and reasoning.
- Extracted-field review/correction UI.

Key deliverables:
- End-to-end intake to reviewed extracted fields.
- Provenance model persisted and visible in UI.

Exit checks:
- US-010 to US-014 ready.
- FR-014, FR-015, FR-021a, FR-021b acceptance evidence.

## Sprint 4 — Graph Validation and Rule-Pack Plugins
Objective:
- Enable legal validation through pluginized rule-pack contracts.

Scope:
- Neo4j bootstrap from simple-graphrag artifacts.
- Validation engine integration through `validation.rule_pack` plugin.
- Procedure scoping and requirements checklist APIs.
- Citation payload persistence and presentation.

Key deliverables:
- Legal validation results with citations.
- Blocking/ready outcomes integrated into workflow.

Exit checks:
- US-020 to US-024 ready.
- Rule-pack plugin activation and execution verified.

## Sprint 5 — Form-Pack Plugins and EX11 End-to-End Path
Objective:
- Deliver form generation using pluginized form packs and complete EX11 path.

Scope:
- `form.pack` plugin contract and EX11 mapping implementation.
- Form generation and artifact persistence.
- Lawyer approval gate and correction loop.
- EX11 online/offline pre-submission readiness.

Key deliverables:
- EX11 complete from case creation to approved-for-submission.
- Mapping/version metadata captured in artifacts.

Exit checks:
- US-030, US-031, US-033, US-032a ready.

## Sprint 6 — Submission Channels (Online Mercurio + Offline PDF)
Objective:
- Implement pluginized submission channels and both filing modes.

Scope:
- `submission.channel` contract.
- ONLINE_MERCURIO channel plugin with Tauri local-agent handshake.
- OFFLINE_PDF channel plugin and filing confirmation flow.
- Retry and blocked/failure workflow handling.

Key deliverables:
- Online dispatch and result reconciliation.
- Offline packet readiness and filing confirmation workflow.

Exit checks:
- US-034, US-035, US-036 ready.
- Online/offline E2E paths execute in controlled test environments.

## Sprint 7 — All-EX Coverage Expansion and Readiness Gates
Objective:
- Reach full EX scope coverage required for MVP.

Scope:
- Add/verify form-pack mappings for all EX forms.
- Add/verify procedure-specific validation and checklist coverage.
- Coverage dashboards for mapping readiness and validation readiness.

Key deliverables:
- All EX forms marked mapping-ready and validation-ready.
- Gap list reduced to zero for MVP acceptance.

Exit checks:
- US-032 fully satisfied.
- No unsupported EX forms in MVP release checklist.

## Sprint 8 — Hardening, Compliance, and Operations Readiness
Objective:
- Production hardening for security, observability, and operational support.

Scope:
- Security controls completion (secrets, encryption, key rotation runbook).
- Observability/alerts completion.
- Performance, reliability, and failure recovery drills.
- On-prem standard + compact deployment validation.

Key deliverables:
- Operational runbooks and dashboards.
- Release candidate quality gates green.

Exit checks:
- US-041, US-043 completion confirmation.
- P0 alerting and runbook checks validated.

## Sprint 9 — Stabilization and MVP Release Readiness
Objective:
- Final integration stabilization and release-go decision.

Scope:
- Full regression suite across plugin contracts and E2E paths.
- Documentation freeze and release notes.
- Pilot-tenant onboarding checklist.

Key deliverables:
- MVP release candidate approved.
- First-customer readiness package.

Exit checks:
- All P0 user stories in done state.
- Step 6.2 feature/sprint exit criteria fully met.

## 6. Story-to-Sprint Allocation (P0 highlights)

- E1 stories (US-001, US-002, US-003): Sprints 1 to 2
- E2 stories (US-010 to US-014): Sprint 3
- E3 stories (US-020 to US-024): Sprint 4
- E4 stories (US-030 to US-036): Sprints 5 to 7
- E5 stories (US-040 to US-044): Sprints 1, 2, 8

## 7. Dependency Plan

1. Plugin runtime (Sprint 2) is a dependency for:
- rule-pack validation (Sprint 4),
- form-pack mappings (Sprint 5 onward),
- submission channels (Sprint 6).

2. Extraction and canonical data (Sprint 3) is a dependency for:
- validation (Sprint 4),
- form generation (Sprint 5).

3. Approval gate (Sprint 5) is a dependency for:
- submission dispatch (Sprint 6).

4. All-EX coverage (Sprint 7) is required before MVP go-live.

## 8. Quality Gates per Sprint

Every sprint must pass:
1. Lint, type checks, unit tests.
2. API contract tests for changed endpoints.
3. Plugin contract tests for changed capabilities.
4. Security static checks and secrets scan.
5. Documentation update check for changed contracts/behavior.

## 9. Risk Register (Planning View)

1. Scope overload risk (solo build + broad MVP)
- Mitigation: strict sprint scope cut lines and no unplanned feature expansion.

2. Plugin runtime complexity risk
- Mitigation: enforce one-plugin-per-capability in MVP; postpone marketplace features.

3. Mercurio/FNMT environment variability
- Mitigation: early Tauri diagnostics and environment validation in Sprint 6.

4. All-EX breadth risk
- Mitigation: progressive mapping scoreboard from Sprint 5 onward; explicit Sprint 7 closure gate.

## 10. Definition of Ready for Sprint Work

A story enters sprint only if:
1. Acceptance criteria are testable.
2. API/contract impact is documented.
3. Plugin capability impact is clear (if applicable).
4. Observability and audit implications are identified.

## 11. Definition of Done for Sprint Work

A story is done only if:
1. Functional acceptance criteria pass.
2. Required tests pass in CI.
3. Audit/telemetry hooks are present.
4. Documentation and traceability mappings are updated.

## 12. Planning Outputs Required Before Sprint 1 Kickoff

1. Prioritized backlog with story points/effort sizing.
2. Sprint 0 task breakdown and owners (single owner + AI-assisted sub-tasks).
3. Plugin capability contract stubs and test harness skeleton.
4. Environment matrix for SaaS and on-prem validation.

## 13. Step 6.1 Exit Criteria

Step 6.1 is complete when:
- Sprint sequence and dependencies are documented.
- P0 scope is mapped to sprint waves.
- Risks and mitigations are explicit.
- Definition of ready/done is established for execution control.
