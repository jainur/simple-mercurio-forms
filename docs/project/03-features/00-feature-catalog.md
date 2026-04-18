# Feature Definitions Catalog — abogados-cowork

Last updated: 2026-04-18  
Status: Approved

## 1. Purpose

Define product features as the bridge between high-level requirements and detailed design, user stories, and sprint planning.

## 2. Feature Inventory

| ID | Feature | Priority | Notes |
|---|---|---|---|
| F01 | Case Management | P0 | Core case lifecycle and assignment |
| F02 | Client Intake and Data Capture | P0 | Structured intake across actors |
| F03 | Document Management | P0 | Upload, classify, lifecycle management |
| F04 | AI Extraction and Canonical Data Normalization | P0 | Extract and normalize reusable case data |
| F05 | Legal Knowledge Graph and Legal Validation (GraphRAG) | P0 | Business and legal validation engine |
| F06 | Procedure Scoping and Requirements Checklist | P0 | Procedure fit, required evidence, readiness |
| F07 | Form Generation and PDF Autofill | P0 | EX form population and output artifacts |
| F08 | Lawyer Review and Approval Gate | P0 | Mandatory human legal checkpoint |
| F09a | Mercurio Portal Automation | P0 | Filing workflow execution against portal |
| F09b | Local Agent and FNMT Certificate Bridge | P0 | Local execution context for certificate-bound actions |
| F10 | Workflow and State Orchestration | P0 | Visible user workflow + durable platform orchestration |
| F11 | Multi-Tenancy and Firm Administration | P0 | Law-firm tenant model and controls |
| F12 | User Management and RBAC | P0 | Role-driven access and permissions |
| F13 | Internationalisation (i18n) | P0 | English, Spanish, Catalan |
| F14 | Audit Log and Traceability | P0 | Legal-grade action traceability |
| F19 | Plugin Runtime and Capability Registry | P0 | Plugin-first extensibility for domain logic, forms, rules, and submission channels |
| F15 | Notifications and Alerts | P1 | Email + in-app real-time notifications |
| F16 | PMS Integration Framework | P1 | Post-MVP integration foundation |
| F17 | Knowledge Graph Authoring for Legal Experts | P1 | Product feature for legal experts to maintain graph |
| F18 | Observability and Platform Operations | P1 | Telemetry, diagnostics, operational readiness |

## 3. Feature Definitions

## F01 — Case Management (P0)

### Objective
Provide the assistant and lawyer with a reliable case workspace from initiation to completion.

### Primary actors
Assistant, Lawyer, Firm Admin.

### In scope
- Case creation and metadata.
- Case ownership and assignment.
- Case status progression visibility.
- Case-level search and filtering.

### Acceptance indicators
- Users can create, assign, and update cases with role constraints.
- Case status is visible and consistent across users.
- Case timeline integrates with audit logging.

### Maps to requirements
FR-001, FR-002, FR-003, FR-004, DGR-004.

## F02 — Client Intake and Data Capture (P0)

### Objective
Collect complete client information in a structured and guided way.

### Primary actors
Client, Assistant.

### In scope
- Guided intake forms.
- Data entry validation for required fields.
- Assistant-assisted correction path.

### Acceptance indicators
- Intake can be completed without external forms.
- Missing mandatory data is clearly identified.
- Captured data is available for extraction normalization.

### Maps to requirements
FR-010, FR-011, FR-012, FR-013.

## F03 — Document Management (P0)

### Objective
Manage required case documents securely through upload, organization, and retrieval.

### Primary actors
Client, Assistant, Lawyer.

### In scope
- Secure document upload.
- Smart document identification and categorization.
- Suggested document tags and filing metadata to simplify downstream workflow.
- Document status markers (uploaded, reviewed, rejected, superseded).
- Version-aware document references.

### Acceptance indicators
- Required documents can be uploaded and linked to case context.
- Document type and tag suggestions are generated automatically and can be corrected by assistants.
- Document state changes are auditable.
- Document set supports extraction and legal validation workflows.

### Maps to requirements
FR-011, FR-014, FR-015, FR-022, DGR-002, DGR-003.

## F04 — AI Extraction and Canonical Data Normalization (P0)

### Objective
Extract key data from uploaded evidence and normalize it into a canonical model reusable across procedures and forms.

### Primary actors
Assistant, Lawyer.

### In scope
- OCR and field extraction from evidence.
- Confidence scoring and review workflows.
- Field-level provenance capture (source document, source snippet/location, reasoning, confidence).
- Extracted information review UI for assistant and lawyer validation/correction.
- Assistant correction and confirmation loop.
- Canonical data model updates with provenance.

### Acceptance indicators
- Required fields are extracted with confidence metadata.
- Every extracted field includes source and reasoning provenance.
- Users can view extracted information in UI before form generation.
- Users can review and correct extracted values.
- Canonical data is reusable across downstream features.

### Maps to requirements
FR-020, FR-021, FR-021a, FR-021b, FR-024, DGR-001, DGR-002.

## F05 — Legal Knowledge Graph and Legal Validation (GraphRAG) (P0)

### Objective
Validate client data and procedure readiness using business and legal rules grounded in the legal knowledge graph.

### Primary actors
Assistant, Lawyer, Platform legal operations.

### In scope
- Graph-based eligibility and requirement validation.
- Citation-backed validation outcomes.
- Conflict detection between case data and legal criteria.
- MVP graph bootstrap from simple-graphrag data artifacts.
- Validation rule-pack plugin execution through stable capability contracts.

### Acceptance indicators
- Validation outcomes include legal rationale and source citation.
- Missing legal conditions are explicit and actionable.
- Contradictory data is flagged before filing steps.
- Initial graph load from existing JSONL artifacts is successful.

### Maps to requirements
FR-025, FR-026, FR-027, FR-028, FR-029, FR-030a, FR-030b, FR-030c, FR-083.

## F06 — Procedure Scoping and Requirements Checklist (P0)

### Objective
Determine appropriate procedure path and evidence checklist for a case.

### Primary actors
Assistant, Lawyer.

### In scope
- Procedure candidate identification.
- Procedure-specific requirement checklists.
- Readiness status (ready, missing data, missing evidence, blocked).

### Acceptance indicators
- Users receive a procedure recommendation with rationale.
- Requirement checklist is complete and traceable to legal references.
- Readiness status prevents premature filing.

### Maps to requirements
FR-022, FR-030, FR-033.

## F07 — Form Generation and PDF Autofill (P0)

### Objective
Auto-populate official forms from canonical case data and generate filing-ready artifacts.

### Primary actors
Assistant, Lawyer.

### In scope
- Form selection based on scoped procedure.
- Data mapping to form fields.
- Generated artifacts for review and filing.
- Coverage of all EX procedures and forms in MVP, with EX11 as the first end-to-end execution path.
- Form-pack plugin loading for mappings and template metadata.

### Acceptance indicators
- EX11 is generated end-to-end from case data.
- All EX forms in MVP scope have defined mapping coverage and validation readiness.
- Validation failures block generation of filing-ready status.

### Maps to requirements
FR-031, FR-032, FR-034, FR-082.

## F08 — Lawyer Review and Approval Gate (P0)

### Objective
Ensure legal accountability and controlled progression to external filing.

### Primary actors
Lawyer, Assistant.

### In scope
- Mandatory lawyer approval checkpoint.
- Approve, reject, return-with-comments actions.
- Structured legal notes and decision rationale.

### Acceptance indicators
- Filing cannot proceed without lawyer approval.
- Approval and return actions are fully auditable.
- Assistant receives actionable correction guidance when returned.

### Maps to requirements
FR-040, FR-041, FR-042, NFR-022.

## F09a — Mercurio Portal Automation (P0)

### Objective
Execute filing steps against Mercurio with robust handling of submission states.

### Primary actors
Assistant, Lawyer.

### In scope
- Guided or automated filing sequence execution.
- Submission attempt tracking.
- Outcome capture (success, partial, failure).
- Supervised retry path.
- Submission channel plugin abstraction (ONLINE_MERCURIO, OFFLINE_PDF, future channels).

### Acceptance indicators
- Filing attempts are reproducible and traceable.
- Submission outcomes are recorded with references.
- Failed attempts support controlled retry workflows.

### Maps to requirements
FR-050, FR-052, FR-053, FR-084, NFR-010.

## F19 — Plugin Runtime and Capability Registry (P0)

### Objective
Enable controlled, auditable extensibility using plugins for domain logic, form packs, validation rule packs, and submission channels.

### Primary actors
Platform operations, Firm Admin (configuration scope), Assistant/Lawyer (indirect behavior consumers).

### In scope
- Plugin manifest parsing and compatibility checks.
- Capability registry for domain.logic, form.pack, validation.rule_pack, submission.channel, and provider adapters.
- Signed plugin verification and permission-scoped activation.
- Plugin lifecycle events: install, enable, disable, upgrade.
- Plugin health and telemetry exposure.

### Acceptance indicators
- Core platform can execute domain logic via plugin contract without code changes.
- Form mappings are loaded from a form-pack plugin.
- Validation executes through rule-pack plugin contracts with citation outputs.
- Submission mode dispatch resolves via submission channel plugin contract.
- Plugin lifecycle actions are auditable and safe rollback/disable is supported.

### Maps to requirements
FR-080, FR-081, FR-082, FR-083, FR-084, FR-085, FR-086, FR-087.

## F09b — Local Agent and FNMT Certificate Bridge (P0)

### Objective
Provide secure local execution capability for certificate-bound operations required by Mercurio.

### Primary actors
Firm Admin, Assistant, Platform operations.

### In scope
- Local agent deployment for on-prem and SaaS-assisted firm context.
- Secure access path to local FNMT certificate context.
- Controlled handoff between cloud workflow and local execution.

### Acceptance indicators
- Certificate-bound Mercurio steps can be executed through local context.
- Local execution events are visible in central case workflow.
- Deployment documentation supports firm setup.

### Maps to requirements
FR-051, NFR-040, NFR-041, NFR-042.

## F10 — Workflow and State Orchestration (P0)

### Objective
Provide both a user-visible workflow model and a durable backend state engine for long-running legal processes.

### Primary actors
Assistant, Lawyer, Platform operations.

### In scope (user-visible)
- Case stage progression and blockers.
- Pending approvals and action queues.
- SLA-sensitive steps and overdue indicators.

### In scope (platform-embedded)
- Durable state progression with retries and recovery.
- Long-running wait states.
- Idempotent side-effect guardrails.

### Acceptance indicators
- Users can always see current case state and next required action.
- Workflow state survives service restarts and transient failures.
- Reprocessing does not create duplicate external effects.

### Maps to requirements
FR-002, FR-004, NFR-010, NFR-011, NFR-012, NFR-020.

## F11 — Multi-Tenancy and Firm Administration (P0)

### Objective
Support law-firm tenant boundaries and firm-level configuration control.

### Primary actors
Firm Admin, Platform Admin.

### In scope
- Tenant creation and isolation.
- Firm-level admin configuration.
- SaaS platform admin controls.
- On-premise customer-operated administration model.

### Acceptance indicators
- Tenant data isolation is consistently enforced.
- Firm admins can manage tenant-level app settings.
- SaaS and on-prem responsibilities are clearly separated.

### Maps to requirements
FR-060, FR-061, FR-062, DGR-004.

## F12 — User Management and RBAC (P0)

### Objective
Enforce role-based authorization for all product operations.

### Primary actors
Firm Admin, Platform Admin.

### In scope
- User invitation and lifecycle management.
- Role assignment and revocation.
- Permission checks across all core actions.

### Acceptance indicators
- Users only access role-appropriate data and actions.
- Privileged operations require the correct role.
- Authorization decisions are auditable.

### Maps to requirements
NFR-003, NFR-005, DGR-003.

## F13 — Internationalisation (i18n) (P0)

### Objective
Deliver a multilingual user experience suitable for target firms and users.

### Primary actors
All user roles.

### In scope
- i18n architecture from day one.
- English, Spanish, Catalan for MVP release.
- Language preference and runtime switching.

### Acceptance indicators
- Core user flows are available in English, Spanish, and Catalan.
- Missing translations are detectable through QA and build checks.
- Legal terminology remains consistent per locale.

### Maps to requirements
FR-070, FR-071, FR-072.

## F14 — Audit Log and Traceability (P0)

### Objective
Provide legal-grade traceability for key user and system actions.

### Primary actors
Lawyer, Firm Admin, Platform Admin.

### In scope
- Immutable event logs for critical actions.
- Actor, timestamp, and rationale metadata.
- Searchable audit trail by case and user.

### Acceptance indicators
- Critical actions are fully reconstructable.
- Approval and submission events are immutable.
- Audit records satisfy governance and legal review needs.

### Maps to requirements
FR-041, NFR-022, DGR-003.

## F15 — Notifications and Alerts (P1)

### Objective
Improve responsiveness across case collaboration with timely updates.

### Primary actors
Assistant, Lawyer, Firm Admin.

### In scope
- Email notifications.
- In-app real-time notifications.
- Notification preferences by role.

### Acceptance indicators
- Approval requests and blockers notify relevant users in near real time.
- Users can see an in-app history of actionable alerts.
- Duplicate or noisy notifications are controlled.

### Maps to requirements
NFR-030, NFR-031.

## F16 — PMS Integration Framework (P1)

### Objective
Enable future integrations with external PMS systems while preserving standalone operation.

### Primary actors
Platform operations, Firm Admin.

### In scope
- Integration extension points and adapters.
- Data mapping boundaries.
- Sync status observability.

### Acceptance indicators
- Core product remains fully usable without PMS.
- Integration module boundaries are explicit and testable.

### Maps to requirements
IR-001, IR-002.

## F17 — Knowledge Graph Authoring for Legal Experts (P1)

### Objective
Provide legal experts with controlled workflows to maintain legal graph content without engineering releases.

### Primary actors
Legal experts, Platform operations.

### In scope
- Rule update workflows.
- Citation editing and validation.
- Change history and approval controls.

### Acceptance indicators
- Legal experts can maintain rules without direct code changes.
- Changes are versioned and auditable.
- Validation checks prevent inconsistent legal graph updates.

### Maps to requirements
FR-030c.

## F18 — Observability and Platform Operations (P1)

### Objective
Provide operational insight for reliability, performance, and support.

### Primary actors
Platform operations, Firm Admin (limited tenant-facing diagnostics).

### In scope
- Metrics, logs, traces for key workflows.
- Tenant-aware operational dashboards.
- Alerting for high-severity failures.

### Acceptance indicators
- Failure causes are diagnosable without deep manual forensics.
- Workflow reliability metrics are visible over time.
- Operations can detect and respond to filing pipeline degradation.

### Maps to requirements
NFR-020, NFR-021, NFR-012.

## 4. Cross-Feature Dependencies

- F04 depends on F03 for source documents.
- F05 depends on F04 canonical data and graph availability.
- F06 depends on F05 validation outcomes.
- F07 depends on F04 and F06 outputs.
- F08 depends on F07 packet readiness and F14 traceability.
- F09a depends on F08 approval and F09b local certificate bridge.
- F10 underpins F01 to F09a orchestration behavior.
- F19 provides extensibility contracts used by F05, F07, and F09a.
- F13 applies across all user-facing features.
- F14 applies across all critical action features.

## 5. Contradictions and Risk Flags

- RF-01: Full all-EX-form support as P0 plus EX11-first end-to-end path creates a breadth-versus-depth delivery risk for a solo build.
- RF-02: MVP includes both SaaS and on-premise, increasing operational complexity early.
- RF-03: MVP includes Mercurio automation and local certificate bridge, which are high-risk integration surfaces.
- RF-04: Existing graph artifact currently includes fewer Form nodes than full EX form scope, requiring graph enrichment before full FR-031 completeness.
- RF-05: Plugin-first scope in MVP adds runtime and governance complexity; capability boundaries must remain strict to prevent core-state fragmentation.

## 6. Step 3 Exit Criteria

Step 3 is complete when:
- Each feature has objective, scope, acceptance indicators, and requirement mapping.
- P0/P1 assignments are explicit.
- Dependency and risk flags are captured for planning.
