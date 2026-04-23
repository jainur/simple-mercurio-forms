# User Stories Catalog — abogados-cowork

Last updated: 2026-04-18  
Status: Approved

## 1. Purpose

Define user stories for MVP and near-term roadmap in a way that is testable, traceable, and ready for implementation planning.

## 2. Story Format

Each story includes:
- Story ID
- Priority (P0 or P1)
- Actor
- Story statement
- Business value
- Acceptance criteria (high-level)
- Traceability (feature and requirements)

## 3. P0 User Stories (MVP)

## Epic E1 — Case Setup and Collaboration

### US-001
- Priority: P0
- Actor: Assistant
- Story: As an assistant, I want to create a new immigration case with core client metadata so I can begin the workflow without external tools.
**MVP Note:** The MVP is delivered as a desktop application (Tauri) only. All extensibility and alternate implementations are handled via dependency injection (DI), not plugins. The web application and runtime plugin model are deferred until after MVP.
- Business value: Establishes the canonical workspace for all downstream automation.

### US-024
- Priority: P0
- Actor: Platform Operations
- Story: As platform operations, I want to configure and inject alternate validation rule-pack implementations at startup so legal rule updates can be delivered without core code changes.
- Business value: Enables extensible and controlled legal-rule evolution.
- Acceptance criteria:
  - DI configuration supports alternate rule-pack implementations.
  - Configuration changes are auditable.
  - Only compatible implementations can be injected.
- Traceability: Extensibility (DI-based), F05; FR-083, FR-085, FR-086, FR-087.
- Story: As an assistant, I want to assign and reassign case ownership so work can continue when staffing changes.

### US-032a
- Priority: P0
- Actor: Platform Operations
- Story: As platform operations, I want EX mappings delivered as injectable form-pack implementations so forms can evolve without core redeployments.
- Business value: Decouples form evolution from platform release cadence.
- Acceptance criteria:
  - DI configuration supports alternate form-pack implementations.
  - Mapping upgrades are auditable and reversible.
  - Only compatible implementations can be injected.
- Traceability: Extensibility (DI-based), F07; FR-082, FR-085, FR-086.
- Actor: Lawyer

### US-036
- Priority: P0
- Actor: Assistant
- Story: As an assistant, I want submission mode behavior (online Mercurio or offline PDF) to be injectable/configurable so future filing channels can be added without workflow redesign.
- Business value: Future-proofs filing execution while preserving current operations.
- Acceptance criteria:
  - Submission dispatch resolves the selected channel implementation via DI.
  - Online and offline channels produce standardized outcomes.
  - Channel failures map to workflow-safe retry/blocked states.
- Traceability: Extensibility (DI-based), F09a, F09b; FR-084, FR-087, NFR-010.


### US-044
- Priority: P0
- Actor: Platform Admin
- Story: As a platform admin, I want DI configuration governance (inject, swap, upgrade) with permission checks so extensibility remains secure and controlled.
- Business value: Prevents unsafe configuration changes from impacting case integrity.
- Acceptance criteria:
  - Only authorized actors can perform DI configuration changes.
  - Configuration changes require compatibility checks.
  - Every configuration change is captured in audit trail.
- Traceability: Extensibility (DI-based); FR-080, FR-085, FR-086, DGR-003.
  - Failure mode: System provides clear error feedback and allows user to recover from incomplete or invalid intake submissions.
- Traceability: F02; FR-010, FR-012.

### US-011
- Priority: P0
- Actor: Client
- Story: As a client, I want to upload documents securely so the firm can process my case quickly.
- Business value: Enables downstream automation and legal validation.
- Acceptance criteria:
  - Client can upload supported file types.
  - Upload success and failure are clearly communicated.
  - Uploaded files are linked to the correct case.
  - Failure mode: Upload errors (unsupported file, network, virus scan fail) are clearly reported and user can retry or contact support.
- Traceability: F03; FR-011.

### US-012
- Priority: P0
- Actor: Assistant
- Story: As an assistant, I want the system to auto-identify document type and suggest filing tags so I spend less time manual sorting.
- Business value: Speeds intake and reduces filing errors.
- Acceptance criteria:
  - System proposes document type on upload.
  - System proposes one or more filing tags.
  - Assistant can accept or override suggestions.
  - Failure mode: If document type/tag suggestion fails, assistant is notified and can proceed with manual entry.
- Traceability: F03; FR-014, FR-015.

### US-013
- Priority: P0
- Actor: Assistant
- Story: As an assistant, I want extracted document fields displayed in UI so I can validate and correct before form filling.
- Business value: Prevents propagation of extraction errors into legal and filing steps.
- Acceptance criteria:
  - Extracted fields are shown in structured view.
  - Each field shows confidence score.
  - Assistant edits are saved and tracked.
  - Failure mode: Extraction or field display errors are surfaced with actionable error messages and user can retry or escalate.
- Traceability: F04; FR-020, FR-021, FR-021b, FR-024.

### US-014
- Priority: P0
- Actor: Lawyer
- Story: As a lawyer, I want to see extraction provenance for critical fields so I can trust or challenge the extracted data.
- Business value: Increases legal confidence and accountability.
- Acceptance criteria:
  - Field view includes source document reference.
  - Field view includes source snippet or location.
  - Field view includes extraction reasoning and confidence.
  - Failure mode: If provenance cannot be displayed, system notifies user and logs the issue for review.
- Traceability: F04; FR-021a, DGR-002.

## Epic E3 — Legal Validation and Procedure Readiness

### US-020
- Priority: P0
- Actor: Assistant
- Story: As an assistant, I want the system to evaluate case data against legal and business rules so I know whether the case is filing-ready.
- Business value: Reduces invalid submissions and rework.
- Acceptance criteria:
  - System runs legal rule validation from GraphRAG.
  - Validation result indicates ready, missing data, or blocked.
  - Blocking issues include recommended corrective actions.
  - Failure mode: Validation errors or rule evaluation failures are reported with guidance for resolution or escalation.
- Traceability: F05, F06; FR-025, FR-026, FR-030, FR-033.

### US-021
- Priority: P0
- Actor: Assistant
- Story: As an assistant, I want a requirements checklist tied to legal references so I can close evidence gaps systematically.
- Business value: Improves completion predictability and auditability.
- Acceptance criteria:
  - Checklist lists required documents and conditions.
  - Each requirement links to legal source citation.
  - Checklist updates when new documents are uploaded.
  - Failure mode: Checklist or legal reference errors are reported and user can retry or request support.
- Traceability: F05, F06; FR-022, FR-027, FR-028.

### US-022
- Priority: P0
- Actor: Lawyer
- Story: As a lawyer, I want legal conflict alerts when client data contradicts eligibility rules so I can intervene early.
- Business value: Prevents legal-risk filings.
- Acceptance criteria:
  - System highlights contradictory data points.
  - Alert links to rule citation and source evidence.
  - Lawyer can mark as accepted risk or return for correction.
  - Failure mode: Conflict detection or alerting errors are surfaced and user can proceed with manual override or escalate.
- Traceability: F05, F08; FR-028, FR-040, FR-042.

### US-023
- Priority: P0
- Actor: Platform Operations
- Story: As platform operations, I want to initialize Neo4j from curated graph artifacts so MVP can run with legal knowledge from day one.
- Business value: Enables rapid MVP readiness without building authoring tooling first.
- Acceptance criteria:
  - Graph loads successfully from nodes and relationships artifacts.
  - Schema compatibility checks pass against expected model.
  - Load results are logged and auditable.
  - Failure mode: Graph load or schema compatibility errors are reported and system provides rollback or retry options.
- Traceability: F05; FR-030a, FR-030b.

### US-024
- Priority: P0
- Actor: Platform Operations
- Story: As platform operations, I want to install and activate signed validation rule-pack plugins so legal rule updates can be delivered without core code changes.
- Business value: Enables extensible and controlled legal-rule evolution.
- Acceptance criteria:
  - Plugin manifest compatibility is validated before activation.
  - Signature verification is mandatory.
  - Activation/deactivation events are auditable.
  - Failure mode: Plugin activation or signature verification errors are reported and system blocks unsafe activation.
- Traceability: F19, F05; FR-083, FR-085, FR-086, FR-087.

## Epic E4 — Form Preparation and Filing

### US-030
- Priority: P0
- Actor: Assistant
- Story: As an assistant, I want the system to auto-fill EX forms from canonical case data so I do not edit PDFs manually.
- Business value: Major productivity gain and consistency improvement.
- Acceptance criteria:
  - Form prefill uses latest validated canonical values.
  - Missing required fields are flagged before output.
  - Generated form artifact is available for lawyer review.
  - Failure mode: Form generation errors (missing data, mapping fail) are reported and user can correct or retry.
- Traceability: F07; FR-031, FR-032, FR-033.

### US-031
- Priority: P0
- Actor: Assistant
- Story: As an assistant, I want EX11 to run as the first full end-to-end path so we can validate the complete operating model.
- Business value: Creates an MVP proving path.
- Acceptance criteria:
  - EX11 can progress from intake to filing-ready state.
  - Required validations and approvals are enforced.
  - Workflow outcomes are traceable.
  - Failure mode: If EX11 cannot progress due to system or data errors, user is notified and can retry or escalate.
- Traceability: F07, F10; FR-034, FR-033.

### US-032
- Priority: P0
- Actor: Assistant
- Story: As an assistant, I want all EX procedures/forms available in MVP so I can operate across real firm demand, not a single procedure.
- Business value: Supports practical adoption and commercial viability.
- Acceptance criteria:
  - Each EX form has defined data mapping and validation profile.
  - Procedure-specific checklist and legal validation are available per form.
  - Unsupported EX form gaps are not allowed in MVP release criteria.
  - Failure mode: If a form or mapping is missing, system blocks progression and provides clear error message.
- Traceability: F07, F06, F05; FR-031.

### US-032a
- Priority: P0
- Actor: Platform Operations
- Story: As platform operations, I want EX mappings delivered as form-pack plugins so forms can evolve without core redeployments.
- Business value: Decouples form evolution from platform release cadence.
- Acceptance criteria:
  - Form pack plugin exposes mapping version metadata per form.
  - Core form generation resolves active form-pack capability at runtime.
  - Mapping plugin upgrades are auditable and reversible.
  - Failure mode: Plugin resolution or upgrade errors are reported and system prevents data loss or corruption.
- Traceability: F19, F07; FR-082, FR-085, FR-086.

### US-033
- Priority: P0
- Actor: Lawyer
- Story: As a lawyer, I want a formal approval gate before filing so legal accountability is enforced.
- Business value: Mandatory control point for regulated legal activity.
- Acceptance criteria:
  - Filing actions are blocked before lawyer approval.
  - Lawyer can approve, reject, or return with comments.
  - Decision rationale is stored in immutable audit log.
  - Failure mode: Approval or audit log errors are reported and system blocks filing until resolved.
- Traceability: F08, F14; FR-040, FR-041, FR-042, DGR-003.

### US-034
- Priority: P0
- Actor: Assistant
- Story: As an assistant, I want the system to execute Mercurio filing steps and capture outcomes so I can complete submissions reliably.
- Business value: Converts packet preparation into actual procedural completion.
- Acceptance criteria:
  - Filing attempt is initiated from approved case state.
  - Submission status is recorded as success, partial, or failure.
  - Failed attempts support supervised retries.
  - Failure mode: Submission errors (network, agent, channel) are reported and user can retry or escalate.
- Traceability: F09a; FR-050, FR-052, FR-053.

### US-035
- Priority: P0
- Actor: Firm Admin
- Story: As a firm admin, I want a local agent and FNMT certificate bridge setup so certificate-bound filing actions can run in my environment.
- Business value: Enables legal portal interaction that depends on local certificate context.
- Acceptance criteria:
  - Local agent can be configured by firm admin.
  - Certificate-bound steps execute through local context.
  - Execution events sync back to case timeline.
  - Failure mode: Local agent or certificate errors are reported and user is guided to resolve or contact support.
- Traceability: F09b, F10; FR-051, NFR-041.

### US-036
- Priority: P0
- Actor: Assistant
- Story: As an assistant, I want submission mode behavior (online Mercurio or offline PDF) to run through channel plugins so future filing channels can be added without workflow redesign.
- Business value: Future-proofs filing execution while preserving current operations.
- Acceptance criteria:
  - Submission dispatch resolves the selected channel capability.
  - Online and offline channels produce standardized outcomes.
  - Channel failures map to workflow-safe retry/blocked states.
  - Failure mode: Channel plugin or dispatch errors are reported and workflow transitions to a safe retry or blocked state.
- Traceability: F19, F09a, F09b; FR-084, FR-087, NFR-010.

## Epic E5 — Tenant, Security, and Governance

### US-040
- Priority: P0
- Actor: Firm Admin
- Story: As a firm admin, I want to manage users and roles so each staff member has appropriate access.
- Business value: Operational control and compliance.
- Acceptance criteria:
  - Firm admin can invite, deactivate, and role-assign users.
  - Role checks are enforced on protected actions.
  - Changes are logged in audit trail.
- Traceability: F11, F12, F14; FR-061, NFR-003, DGR-003.

### US-041
- Priority: P0
- Actor: Platform Admin
- Story: As a platform admin, I want tenant-level controls in SaaS so I can operate the platform safely.
- Business value: Supports commercial operation and incident response.
- Acceptance criteria:
  - Platform admin can view tenant health and status.
  - Tenant data isolation boundaries are enforced.
  - Critical tenant admin actions are auditable.
- Traceability: F11, F18; FR-062, DGR-004.

### US-042
- Priority: P0
- Actor: Any user
- Story: As a user, I want to use the product in English, Spanish, or Catalan so I can work in my preferred language.
- Business value: Market fit and usability.
- Acceptance criteria:
  - Core workflow UI is available in all three languages.
  - Language can be changed per user preference.
  - Missing translation keys are detectable before release.
- Traceability: F13; FR-070, FR-071, FR-072.

### US-043
- Priority: P0
- Actor: Compliance reviewer
- Story: As a compliance reviewer, I want immutable audit records for approvals and filings so legal actions can be reconstructed.
- Business value: Regulatory confidence and defensibility.
- Acceptance criteria:
  - Approval and filing records cannot be modified.
  - Records include actor, timestamp, and context.
  - Audit queries can filter by case and event type.
- Traceability: F14; FR-041, NFR-022, DGR-003.

### US-044
- Priority: P0
- Actor: Platform Admin
- Story: As a platform admin, I want plugin lifecycle governance (install, enable, disable, upgrade) with permission checks so extensibility remains secure and controlled.
- Business value: Prevents unsafe plugin changes from impacting case integrity.
- Acceptance criteria:
  - Only authorized actors can perform lifecycle operations.
  - Lifecycle operations require compatibility checks.
  - Every lifecycle action is captured in audit trail.
- Traceability: F19; FR-080, FR-085, FR-086, DGR-003.

## 4. P1 User Stories (Post-MVP)

### US-100
- Priority: P1
- Actor: Assistant
- Story: As an assistant, I want email and in-app real-time notifications so I never miss approvals or blocker events.
- Traceability: F15; NFR-030, NFR-031.

### US-101
- Priority: P1
- Actor: Platform integrations engineer
- Story: As an integrations engineer, I want adapter interfaces for PMS systems so data can sync without affecting standalone mode.
- Traceability: F16; IR-001, IR-002.

### US-102
- Priority: P1
- Actor: Legal expert
- Story: As a legal expert, I want to update legal graph rules in product so regulatory changes are reflected without code releases.
- Traceability: F17; FR-030c.

### US-103
- Priority: P1
- Actor: Platform operations
- Story: As platform operations, I want observability dashboards and alerts so filing and extraction failures can be diagnosed quickly.
- Traceability: F18; NFR-020, NFR-021, NFR-012.

### US-104
- Priority: P1
- Actor: Platform operations
- Story: As platform operations, I want plugin marketplace-style onboarding workflows so third-party plugins can be managed safely after MVP.
- Traceability: F19; FR-087.

## 5. Contradictions and Clarifications

- No direct contradictions found between Step 2 and Step 4.
- Clarification C4-01: US-032 requires full all-EX MVP coverage. Implementation planning must define a sequencing model that still ships complete coverage for MVP exit.
- Clarification C4-02: US-035 requires environment-specific certificate handling details to be finalized in architecture.
- Clarification C4-03: US-041 depends on deciding how much FR-062 depth is included in MVP vs immediate post-MVP.

## 6. Step 4 Exit Criteria

Step 4 is complete when:
- Each P0 feature has at least one implementable user story.
- Stories are actor-specific and testable.
- Stories are mapped to feature and requirement IDs.
- Contradictions and unresolved clarifications are explicitly listed.

## 7. Alignment with Step 5.2 Design

Alignment status: Confirmed for all P0 stories.

Reference:
- Implementation coverage is maintained in Step 5.2 section `16. P0 User Story Alignment Matrix`.

Governance rule:
- A P0 user story is not considered implementation-ready until it maps to a concrete design section in Step 5.2.
