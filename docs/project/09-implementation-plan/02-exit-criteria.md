# Exit Criteria (Step 6.2) — Sprint and Feature Completion

Last updated: 2026-04-18  
Status: Approved

## 1. Purpose

Define objective, testable exit criteria for:
1. Each sprint in Step 6.1
2. Each feature definition (especially P0)

This ensures progress is measurable and prevents ambiguous completion claims.

## 2. Global Exit Rules (Apply Everywhere)

A sprint or feature is complete only when all are true:
1. Functional acceptance criteria are met.
2. Required automated tests pass.
3. Security and audit requirements are satisfied.
4. Observability hooks (logs/metrics/traces) are in place.
5. Documentation and traceability mappings are updated.
6. No open Sev-1 or Sev-2 defects for delivered scope.

## 3. Sprint Exit Criteria

## Sprint 0 — Foundations and Scaffolding
Complete when:
1. Template scaffold command generates web/api/worker/plugin skeletons successfully.
2. CI runs lint/type/test baseline on generated outputs.
3. Environment profiles (`dev`, `test`, `staging`, `prod`, `onprem`) are validated.
4. SQLite local profile and PostgreSQL CI profile both execute basic smoke tests.

Evidence:
- Successful scaffold logs
- CI run links/artifacts
- Environment validation checklist

## Sprint 1 — Core Platform and Security
Complete when:
1. Case create/read/update/assign APIs are operational and tenant-aware.
2. RBAC blocks unauthorized actions with standard error envelope.
3. Audit events are generated for case and assignment actions.
4. Cross-tenant access tests pass.

Evidence:
- API contract test report
- Authorization test report
- Audit event sample outputs

## Sprint 2 — Plugin Runtime v1
Complete when:
1. Plugin install/enable/disable/list/health APIs are operational.
2. Manifest validation, signature verification, and compatibility checks are enforced.
3. Capability resolver supports required MVP capabilities.
4. Plugin lifecycle actions are auditable.

Evidence:
- Plugin contract test report
- Negative tests for invalid plugin activation
- Audit log records for lifecycle actions

## Sprint 3 — Intake, Documents, Extraction
Complete when:
1. Intake flow captures mandatory fields and persists case-linked data.
2. Document upload + smart classification + tag override path is functional.
3. Extraction outputs include confidence + provenance + reasoning metadata.
4. Extraction review/correction UI is usable for assistant/lawyer roles.

Evidence:
- E2E test for intake->extraction review
- Provenance field coverage report
- Role-based UI validation evidence

## Sprint 4 — Graph Validation and Rule-Pack Plugins
Complete when:
1. Neo4j bootstrap from curated artifacts is successful.
2. Validation execution runs through `validation.rule_pack` plugin contract.
3. Validation outputs include citations and blocking status.
4. Procedure checklist API returns requirement states.

Evidence:
- Graph bootstrap log + schema check
- Validation contract tests
- Citation payload sample report

## Sprint 5 — Form Packs and EX11 End-to-End
Complete when:
1. EX11 form generation runs through `form.pack` plugin.
2. Mapping/version metadata stored on generated artifacts.
3. Lawyer approval gate blocks/unblocks transitions correctly.
4. EX11 path reaches APPROVED_FOR_SUBMISSION with full traceability.

Evidence:
- EX11 E2E run report
- Artifact metadata record samples
- Approval gate test report

## Sprint 6 — Submission Channels (Online + Offline)
Complete when:
1. `submission.channel` plugins for ONLINE_MERCURIO and OFFLINE_PDF are active.
2. Online dispatch via local Tauri agent executes and returns standardized outcomes.
3. Offline packet generation and filing confirmation flow works end-to-end.
4. Retryable/blocked failure states transition correctly.

Evidence:
- Online dispatch integration report
- Offline flow E2E report
- State transition test matrix

## Sprint 7 — All-EX Coverage
Complete when:
1. Every EX form in scope has mapping coverage and validation readiness.
2. No unsupported EX form remains in release checklist.
3. At least one non-EX11 E2E path passes with full validation and artifact generation.

Evidence:
- EX coverage dashboard/report
- Gap list = zero
- Non-EX11 E2E artifact

## Sprint 8 — Hardening and Compliance
Complete when:
1. P0 security checklist passes (secrets, encryption, auth, audit controls).
2. P0 observability/alerts are configured and validated.
3. Recovery runbooks are validated through at least one drill per critical failure class.
4. On-prem standard and compact deployment validation passes.

Evidence:
- Security validation checklist
- Alert simulation outputs
- Runbook drill reports
- Deployment validation reports

## Sprint 9 — Stabilization and Release Readiness
Complete when:
1. Full regression suite passes (API, plugin contracts, integration, E2E).
2. MVP acceptance checklist is fully green.
3. Release notes, migration notes, and operational handoff docs are complete.
4. Go/no-go review records explicit approval.

Evidence:
- Regression test summary
- MVP checklist
- Release package
- Go/no-go decision log

## 4. Feature Completion Criteria (P0)

## F01 Case Management
Complete when:
1. Case CRUD + assignment are functional under tenant/RBAC controls.
2. Workflow stage projection is visible and consistent.
3. Case actions generate audit events.

## F02 Client Intake and Data Capture
Complete when:
1. Guided intake captures mandatory data.
2. Validation feedback is user-actionable.
3. Intake data maps into canonical model.

## F03 Document Management
Complete when:
1. Upload, classification, tagging, and override flows are functional.
2. Document lifecycle states are tracked and auditable.
3. Case-document linking is reliable.

## F04 AI Extraction and Canonical Normalization
Complete when:
1. Extracted fields include confidence and provenance.
2. Review/correction loop is functional and auditable.
3. Canonical data updates are version-safe.

## F05 Legal Knowledge Graph and Validation
Complete when:
1. Rule evaluation runs via `validation.rule_pack` plugin.
2. Outputs include citations and conflict detection.
3. Blocking issues integrate with workflow guardrails.

## F06 Procedure Scoping and Requirements Checklist
Complete when:
1. Procedure recommendation and readiness status are produced.
2. Checklist tracks requirement states with legal traceability.
3. Missing items are actionable in UI.

## F07 Form Generation and PDF Autofill
Complete when:
1. Form generation resolves mappings through `form.pack` plugin.
2. Artifacts include template/mapping/validation version metadata.
3. EX11 is fully certified; all EX forms meet readiness gate.

## F08 Lawyer Review and Approval Gate
Complete when:
1. Approval gate is enforced in workflow logic.
2. Approve/reject/return decisions are recorded immutably.
3. Return-for-correction loop is functional.

## F09a Mercurio Portal Automation
Complete when:
1. Online submission uses `submission.channel` plugin contract.
2. Outcomes are standardized and persisted.
3. Retryable/blocked behaviors match defined state model.

## F09b Local Agent and FNMT Bridge
Complete when:
1. Tauri agent can execute certificate-bound actions.
2. Signed job/result protocol is enforced.
3. Agent health and heartbeat are observable.

## F10 Workflow and State Orchestration
Complete when:
1. Case lifecycle states and guardrails are implemented.
2. Long-running durability and restart recovery are validated.
3. UI projection reflects authoritative workflow state.

## F11 Multi-Tenancy and Firm Administration
Complete when:
1. Tenant boundaries are enforced in data access.
2. Firm admin controls are functional.
3. On-prem/SaaS operational roles are supported.

## F12 User Management and RBAC
Complete when:
1. User lifecycle and role assignment are functional.
2. Permission policy enforcement is verified by tests.
3. Privileged actions are auditable.

## F13 Internationalization
Complete when:
1. `en`, `es`, `ca` locales are complete for P0 journeys.
2. Missing translation keys fail CI for P0 routes.
3. Locale switching works per user context.

## F14 Audit Log and Traceability
Complete when:
1. Legal-critical events are immutable.
2. Audit query endpoints support case/user/event filtering.
3. Approval and submission actions are fully reconstructable.

## F19 Plugin Runtime and Capability Registry
Complete when:
1. Plugin lifecycle APIs and policy checks are operational.
2. Required MVP capability contracts are active and test-validated:
   - domain.logic
   - form.pack
   - validation.rule_pack
   - submission.channel
   - llm.provider
3. Signature, compatibility, and permission scope checks are enforced.
4. Plugin telemetry and lifecycle audit trails are operational.

## 5. MVP Program Exit Criteria

MVP is complete when all are true:
1. All P0 features meet feature completion criteria.
2. All P0 user stories are in done state with Step 5.2 alignment maintained.
3. EX11 full path is production-ready and validated.
4. All EX forms meet mapping + validation readiness gates.
5. Both submission modes validated:
   - ONLINE_MERCURIO
   - OFFLINE_PDF
6. Plugin-first capability model is operational for required MVP capabilities.
7. SaaS and on-prem deployment profiles pass acceptance checks.
8. Security, auditability, and observability baselines are met.

## 6. Evidence and Sign-off Process

For each sprint and feature closeout:
1. Attach test artifacts and coverage summaries.
2. Attach operational evidence (alerts, dashboards, runbook drills where relevant).
3. Record unresolved issues with severity and explicit disposition.
4. Capture sign-off by role:
   - Product/Platform owner
   - Engineering implementation owner
   - Compliance review (for legal-critical flows)

## 7. Step 6.2 Exit Criteria

Step 6.2 is complete when:
1. Each sprint has objective completion gates and evidence requirements.
2. Each P0 feature has explicit completion criteria.
3. MVP-level release criteria are defined and testable.
4. Sign-off process is documented.
