# High-Level Requirements — abogados-cowork

**Last updated:** 2026-04-18  
**Status:** Approved

## 1. Purpose

Define the high-level requirements for the full system (not phase-based), aligned to the charter and objectives, and suitable for decomposition into feature definitions, user stories, architecture, and sprint plans.

## 2. Scope Boundary

### In scope (MVP baseline)
- Spanish immigration procedure workflow automation with EX forms.
- First end-to-end implementation target: EX11.
- AI-assisted document extraction and data normalization.
- Requirements and evidence validation support.
- Automated PDF form filling.
- Lawyer approval gate before external filing.
- Mercurio portal submission workflow support.
- Multi-tenant law-firm model.
- SaaS and on-premise deployment modes.
- English development language plus Spanish and Catalan for MVP release.
- GDPR-oriented data handling controls.

### Out of scope (MVP)
- PMS integrations (MyCase, Kleos, others).
- Billing and invoicing capabilities.
- Non-Spanish jurisdictions.
- Native mobile applications.
- Non-immigration legal domains.

## 3. Stakeholders and Actors

- Lawyer
- Assistant or Secretary
- Client
- Firm Admin
- Platform Admin (SaaS only)

## 4. Functional Requirements

### 4.1 Case and Workflow Management
- FR-001: The system must allow firm users to create and manage immigration cases.
- FR-002: The system must represent case progress with explicit workflow states.
- FR-003: The system must assign tasks and actions to specific actors by role.
- FR-004: The system must preserve a complete, time-ordered case activity trail.

### 4.2 Client Intake and Data Capture
- FR-010: The system must provide guided client intake for required case information.
- FR-011: The system must support secure client document upload.
- FR-012: The system must normalize captured information into a canonical case data model.
- FR-013: The system must allow assistant review and correction of extracted values.
- FR-014: The system must automatically identify and classify uploaded documents (for example passport, NIE, bank statement, certificate) and suggest filing tags to simplify document organization.
- FR-015: The system must allow assistants to confirm or correct system-suggested document type and tags before downstream automation.

### 4.3 AI Extraction and Validation
- FR-020: The system must extract relevant fields from uploaded documents.
- FR-021: The system must surface extraction confidence to users for review decisions.
- FR-021a: The system must retain and expose extraction provenance for each field, including source document, source location/snippet, extraction reasoning, and confidence score.
- FR-021b: The system must provide a UI view of extracted information so users can inspect, validate, and correct extracted values before they are used by validation and form filling.
- FR-022: The system must detect missing required data and required supporting documents.
- FR-023: The system must flag inconsistent values across sources.
- FR-024: The system must maintain a reviewable mapping between source evidence and extracted fields.
- FR-025: The system must validate extracted and captured data against business and legal rules, not just field format.
- FR-026: The system must use a legal knowledge graph (GraphRAG) as the authoritative source for procedure-specific eligibility rules, documentation requirements, and filing conditions.
- FR-027: Every legal validation result or eligibility determination must include a traceable citation to the source rule in the knowledge graph.
- FR-028: The system must detect conditions where extracted client data conflicts with legal eligibility criteria and surface this to the assistant and lawyer.
- FR-029: The legal knowledge graph is a product-managed asset, maintained by legal experts and operated by the platform. Firms consume it as a service — they do not own or edit it.
- FR-030a: For MVP, the knowledge graph will be bootstrapped from the curated graph artifact files (`graph_nodes.jsonl`, `graph_relationships.jsonl`) produced by the `simple-graphrag` project. The system must support loading these files as the initial graph state into Neo4j.
- FR-030b: The `simple-graphrag` project also defines the canonical graph schema (`legal_schema.py`) covering node types: Procedure, EligibilityRule, Requirement, RequiredDocument, Form, Fee, Deadline, SubmissionChannel, LegalReference, Outcome, Authority, ApplicantProfile, ResolutionRule, Appeal. This schema is adopted as-is for MVP.
- FR-030c: Post-MVP, a knowledge graph authoring and maintenance interface will be required for legal experts to update rules without engineering involvement. This is out of scope for MVP.

### 4.4 Procedure and Form Automation
- FR-030: The system must support procedure-specific requirements and validation rules.
- FR-031: The system must support all EX forms as part of the product scope.
- FR-032: The system must generate and prefill form artifacts using canonical case data.
- FR-033: The system must prevent filing progression when required validations fail.
- FR-034: The first complete end-to-end filing path must be EX11.

### 4.5 Human Review and Approval Controls
- FR-040: The system must enforce a lawyer approval gate before external filing actions.
- FR-041: The system must record approval decisions, actor identity, timestamps, and rationale notes.
- FR-042: The system must allow return-to-assistant with explicit correction feedback.

### 4.6 Mercurio Submission Support
- FR-050: The system must support a filing workflow compatible with Mercurio process steps.
- FR-051: The system must support operation with firm-local FNMT certificate context.
- FR-052: The system must record submission attempts, outcomes, and references.
- FR-053: The system must support supervised retry paths for failed filing attempts.

### 4.7 Tenant and Administration
- FR-060: The system must model each tenant as a law firm with isolated data.
- FR-061: The system must support role-based user administration by Firm Admin.
- FR-062: The system must support platform-level tenant administration for SaaS operations.

### 4.8 Internationalization
- FR-070: The system must implement internationalization infrastructure from the start.
- FR-071: The system must support English, Spanish, and Catalan interface content for MVP release.
- FR-072: The system must allow language selection per user context.

### 4.9 Plugin Extensibility and Governance
- FR-080: The system must implement a plugin runtime and capability registry so core platform behavior can be extended without core code changes.
- FR-081: The system must support domain logic plugins for procedure-specific orchestration logic and readiness behavior.
- FR-082: The system must support form pack plugins for form definitions, mappings, and mapping-version metadata.
- FR-083: The system must support validation rule pack plugins for legal/business rule evaluation with citation-aware outputs.
- FR-084: The system must support submission channel plugins, including ONLINE_MERCURIO and OFFLINE_PDF, with a stable adapter contract for future channels.
- FR-085: Plugins must declare a manifest with capability declarations, contract version, compatibility range, and configuration schema.
- FR-086: Plugin activation must enforce signature verification, tenant-safe permission scope, and auditable lifecycle events.
- FR-087: Plugin execution must emit plugin-scoped telemetry (health, errors, latency) and support safe disablement.

## 5. Non-Functional Requirements

### 5.1 Security and Privacy
- NFR-001: Data in transit must be protected by TLS.
- NFR-002: Sensitive data at rest must be encrypted.
- NFR-003: Access control must be role-based and tenant-aware.
- NFR-004: The system must support GDPR obligations for data export and deletion workflows.
- NFR-005: The system must maintain consent and data-processing auditability.

### 5.2 Reliability and Durability
- NFR-010: Long-running workflows must survive restarts and transient failures.
- NFR-011: External side-effect operations must be idempotent where feasible.
- NFR-012: Failures must be observable with actionable error context.

### 5.3 Observability and Auditability
- NFR-020: The system must emit structured logs for critical workflow actions.
- NFR-021: The system must expose operational metrics for workflow success and failure.
- NFR-022: The system must preserve auditable records for approvals and filing actions.

### 5.4 Usability and Accessibility
- NFR-030: Core workflows must be navigable for assistant-first daily usage.
- NFR-031: Validation errors must be understandable and actionable.
- NFR-032: UI language and legal terminology must be clear for intended actor roles.

### 5.5 Deployability and Operability
- NFR-040: The same product codebase must support SaaS and on-premise deployments.
- NFR-041: On-premise deployment must support customer-managed infrastructure and app operations.
- NFR-042: SaaS deployment must support provider-managed infrastructure with customer app administration.

## 6. Integration Requirements

- IR-001: MVP must operate without PMS dependencies.
- IR-002: Architecture must preserve clean integration extension points for future PMS adapters.
- IR-003: Filing workflow design must preserve compatibility with Mercurio process requirements.

## 7. Data and Governance Requirements

- DGR-001: A canonical case data model must be maintained as the source for automation.
- DGR-002: Field-level provenance must be retained for extracted or manually corrected data.
- DGR-003: Audit logs must be immutable for critical legal and submission events.
- DGR-004: Tenant data segregation must be enforced in all read and write paths.

## 8. Prioritization

### Priority P0 (must-have for MVP)
- FR-001 to FR-004
- FR-010 to FR-015
- FR-020 to FR-029, FR-021a, FR-021b
- FR-030, FR-031, FR-032, FR-033, FR-034
- FR-040 to FR-042
- FR-050 to FR-053
- FR-060, FR-061
- FR-070 to FR-072
- FR-080 to FR-087
- NFR-001 to NFR-005
- NFR-010, NFR-012
- NFR-020, NFR-022
- NFR-040 to NFR-042
- DGR-001 to DGR-004

### Priority P1 (next after MVP)
- FR-062 (platform admin depth depending on SaaS launch sequence)
- NFR-011, NFR-021, NFR-030 to NFR-032
- IR-002 (PMS integration adapters implementation)

## 9. Acceptance Gate for Step 2 Completion

Step 2 is complete when all requirements are:
- Unambiguous.
- Testable at high level.
- Traceable to charter and objectives.
- Tagged with priority.
- Free of unresolved contradictions.

## 10. Consistency and Contradiction Review

### Checked against charter and objectives
- Standalone-first with future integration: consistent.
- EX11 as first full filing path: consistent.
- All EX forms in MVP scope: consistent; EX11 remains the first end-to-end implementation path.
- Plugin-first extensibility for domain logic, form packs, rule packs, and submission channels: consistent.
- SaaS and on-premise from first release: consistent.
- English start plus Spanish/Catalan for MVP release: consistent.
- GDPR day-one: consistent.

### Clarifications resolved
- CL-01 resolved: Minimum extraction quality baseline for MVP is 90% required-field accuracy on pilot validation sets with mandatory human review prior to filing.
- CL-02 resolved: Mercurio operates in supervised automation mode for MVP (mandatory lawyer approval and supervised retry).
- CL-03 resolved: Minimum viable on-premise deployment includes both standard and compact profiles.
