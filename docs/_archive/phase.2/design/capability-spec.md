# Phase 2 Capability Specification

## 1. Purpose
Define an implementation-grade capability map for Phase 2 with clear boundaries, component responsibilities, contracts, and operational controls.

## 2. Capability Catalog

| Capability | Name | Primary Objective |
|---|---|---|
| C01 | OCR and Document Understanding | Convert raw uploaded documents into structured, reviewable field data |
| C02 | LLM Reasoning and Legal Grounding | Produce eligibility and requirement evaluations with grounded citations |
| C03 | Workflow Orchestration | Execute durable, auditable, long-running case workflows |
| C04 | Form Preparation | Generate and maintain submission-ready forms and packet artifacts |
| C05 | Browser Automation (Playwright) | Execute filing and status-check automations in controlled channels |
| C06 | Integration and Sync | Keep internal workflow and external systems synchronized safely |
| C07 | Security and Compliance Controls | Enforce identity, access, data protection, and auditability controls |

## 3. Architecture Principles
1. Capability responsibilities are explicit and non-overlapping.
2. External side effects require idempotency, retry policy, and audit trail.
3. Human gate checkpoints are enforced before irreversible actions.
4. Capability outputs are structured and traceable to source evidence.

## 4. C01 OCR and Document Understanding

## 4.1 Scope and Responsibility
1. Document parsing and OCR are handled by docling.
2. Document understanding and field or attribute extraction are handled by LLM.
3. The capability includes confidence scoring, extraction review support, and evidence linking.

## 4.2 Pipeline
1. Ingestion and normalization
- Input: uploaded files from client portal, assistant uploads, and integrations.
- Output: normalized artifact metadata and raw text chunks.

2. Parsing and OCR by docling
- Input: raw file bytes plus file metadata.
- Output: layout-aware text, table segments, section boundaries, page references.

3. Semantic extraction by LLM
- Input: docling outputs plus extraction template and case context.
- Output: field candidates, normalized values, confidence scores, source spans.

4. Post-processing
- Validation against expected formats, value ranges, and entity consistency.
- Flagging for low confidence and conflict states.

## 4.3 Core Components
1. Artifact ingestion service
2. docling parser adapter
3. LLM extraction worker
4. Field normalizer and validator
5. Extraction review publisher

## 4.4 Inputs
1. DocumentArtifact and metadata
2. Procedure context and expected field schema
3. Language hints and locale hints

## 4.5 Outputs
1. Extracted fields with source spans
2. Field-level confidence and extraction status
3. Review queue items for unresolved fields

## 4.6 API Surfaces
1. A02 document upload and listing endpoints
2. A03 extraction read/update/approve endpoints

## 4.7 UI Surfaces
1. Documents screen
2. Data Review screen
3. Timeline event surfaces

## 4.8 Workflow Touchpoints
1. Entry: DOCUMENT_COLLECTION_IN_PROGRESS
2. Gate: EXTRACTION_REVIEW_PENDING
3. Exit: FORM_FILLING_IN_PROGRESS after extraction approval

## 4.9 Quality Signals
1. OCR parse completeness
2. LLM extraction confidence per field
3. Extraction correction rate and approval latency

## 4.10 Failure Modes and Fallbacks
1. docling parse failure
- Fallback: manual upload retention + retry parse task.
2. Low-confidence extraction
- Fallback: mandatory human correction in Data Review.
3. Schema mismatch for extracted values
- Fallback: normalization warning and unresolved field status.

## 4.11 Observability
1. Metrics: parse success rate, extraction accuracy proxy, correction ratio
2. Logs: parser stage timings, extraction stage diagnostics, field validation failures
3. Traces: document ingestion -> parse -> extract -> review publish

## 4.12 Security and Compliance
1. PII-safe logs and redaction
2. Artifact access scoped by tenant and case permissions
3. Immutable audit entries for field corrections and approvals

## 5. C02 LLM Reasoning and Legal Grounding

## 5.1 Scope and Responsibility
1. Use LLM for legal reasoning, confidence scoring, and requirement evaluation.
2. Use GraphRAG over Neo4j as the grounding layer.
3. Use existing Neo4j graph with ingested legal documents and topics.

## 5.2 GraphRAG Model
1. Retrieval source
- Neo4j graph containing procedures, requirements, legal sources, topics, and relationships.

2. Retrieval strategy
- Graph neighborhood expansion from case-relevant nodes.
- Optional vector-assisted retrieval over legal text chunks linked to graph nodes.

3. LLM reasoning stage
- Inputs: case facts, extracted fields, retrieved legal evidence, procedure context.
- Outputs: requirement status matrix, confidence per evaluation, rationale, citation list.

## 5.3 Core Components
1. Retrieval orchestrator for GraphRAG
2. Neo4j query service
3. LLM reasoning worker
4. Confidence calibration and policy layer
5. Eligibility matrix builder

## 5.4 Inputs
1. Canonical case profile and extracted data
2. Procedure candidates or selected procedure
3. Neo4j-grounded legal evidence and topics

## 5.5 Outputs
1. Procedure ranking and readiness scores
2. Requirement-level evaluation matrix
3. Missing-evidence recommendations
4. Citation-grounded rationale with confidence scores

## 5.6 API Surfaces
1. A04 procedure requirements
2. A04 eligibility run and eligibility detail

## 5.7 UI Surfaces
1. Data Review
2. Lawyer Review
3. Matter Overview risk and readiness summaries

## 5.8 Workflow Touchpoints
1. Entry: PROCEDURE_CANDIDATES_READY or explicit procedure scope
2. Mid-state: ELIGIBILITY_ASSESSMENT_READY
3. Exit: READINESS_REVIEW_PENDING or back to info/document collection when gaps detected

## 5.9 Quality Signals
1. Citation coverage ratio per recommendation
2. Requirement classification confidence
3. Override rate by lawyer and assistant

## 5.10 Failure Modes and Fallbacks
1. Graph retrieval miss
- Fallback: broader retrieval query and explicit insufficient-grounding status.
2. Ambiguous reasoning output
- Fallback: mark NEEDS_REVIEW and require human disposition.
3. Citation mismatch
- Fallback: reject result publication and re-run with stricter grounding policy.

## 5.11 Observability
1. Metrics: retrieval latency, grounded-response rate, confidence distribution
2. Logs: retrieval query ids, citation mappings, reasoning policy version
3. Traces: retrieve -> reason -> matrix publish

## 5.12 Security and Compliance
1. Prevent leakage of non-tenant legal graphs via scoped query policies
2. Persist reasoning outputs with immutable version and policy metadata
3. Audit all legal approval decisions with rationale

## 5.13 Confidence Scoring Model

### 5.13.1 Field-Level Confidence (C01 to C02 handoff)
For each extracted field `f`, compute:

`field_confidence(f) = w_ocr * ocr_conf + w_llm * llm_conf + w_schema * schema_conf + w_cross * cross_doc_conf`

Default weights:
1. `w_ocr = 0.25`
2. `w_llm = 0.35`
3. `w_schema = 0.20`
4. `w_cross = 0.20`

Notes:
1. `ocr_conf` comes from docling extraction quality and source span quality.
2. `llm_conf` comes from LLM structured extraction confidence.
3. `schema_conf` is 1.0 for valid format/domain values, reduced by validation errors.
4. `cross_doc_conf` is derived from consistency against other trusted artifacts.

### 5.13.2 Requirement-Level Confidence
For each requirement `r`, compute:

`req_conf(r) = a * evidence_conf + b * reasoning_conf + c * citation_conf`

Default weights:
1. `a = 0.45`
2. `b = 0.35`
3. `c = 0.20`

Where:
1. `evidence_conf` is aggregated from supporting field confidences.
2. `reasoning_conf` is LLM confidence for requirement evaluation.
3. `citation_conf` measures citation relevance and coverage.

### 5.13.3 Case-Level Confidence
For mandatory requirement set `R`, compute:

`case_conf = weighted_mean(req_conf(r), importance(r)) - penalties`

Penalty examples:
1. unresolved contradictions
2. missing mandatory requirement evidence
3. missing mandatory citations

### 5.13.4 Confidence Bands and Gating
1. `HIGH`: >= 0.85
2. `MEDIUM`: >= 0.65 and < 0.85
3. `LOW`: < 0.65

Gating policy:
1. `LOW` on mandatory requirement forces `NEEDS_REVIEW`.
2. `MEDIUM` plus contradiction forces human review.
3. only `HIGH` with no blockers can auto-progress to next non-irreversible stage.

## 5.14 Reasoning Algorithm

### 5.14.1 Inputs
1. canonical case profile
2. extracted fields with provenance and confidence
3. selected procedure or procedure candidates
4. Neo4j GraphRAG retrieval bundle (legal nodes, relations, text chunks)

### 5.14.2 Pipeline Steps
1. Retrieve legal context
- query Neo4j for procedure node and expand relevant requirement subgraph.
- fetch linked legal text chunks and citation metadata.

2. Build requirement prompts
- convert each requirement to a machine-checkable prompt frame:
	- requirement condition
	- accepted evidence types
	- exceptions
	- freshness/expiry constraints

3. Evaluate requirements with LLM
- for each requirement, LLM returns structured output:
	- status
	- rationale
	- confidence
	- supporting evidence IDs
	- missing evidence list
	- citations

4. Consistency pass
- detect conflicts between requirement outputs.
- re-run only conflicting requirement evaluations with focused prompt context.

5. Publish deterministic result
- emit eligibility matrix, readiness summary, blocker list, and confidence summary.

### 5.14.3 Guardrails
1. no `SATISFIED` status without supporting evidence references.
2. no legal rationale without at least one citation ID.
3. if citations are weak or irrelevant, downgrade to `NEEDS_REVIEW`.

## 5.15 Requirement Coverage Algorithm

### 5.15.1 Status Set
1. `SATISFIED`
2. `PARTIALLY_SATISFIED`
3. `MISSING`
4. `CONFLICTING`
5. `NEEDS_REVIEW`

### 5.15.2 Evaluation Steps (per requirement)
1. gather candidate evidence artifacts and fields by requirement mapping.
2. validate freshness and temporal constraints.
3. validate integrity and schema compliance.
4. validate cross-document consistency.
5. apply exception and substitution rules.
6. assign status using decision policy.

Decision policy baseline:
1. mandatory evidence present + valid + consistent -> `SATISFIED`
2. some evidence present but not complete -> `PARTIALLY_SATISFIED`
3. no acceptable evidence -> `MISSING`
4. contradictory accepted evidence -> `CONFLICTING`
5. ambiguity or low confidence -> `NEEDS_REVIEW`

### 5.15.3 Coverage Score
Compute weighted coverage:

`coverage = sum(weight(r) * status_score(r)) / sum(weight(r))`

Default status scores:
1. `SATISFIED = 1.00`
2. `PARTIALLY_SATISFIED = 0.60`
3. `NEEDS_REVIEW = 0.40`
4. `MISSING = 0.00`
5. `CONFLICTING = 0.00`

## 5.16 Structured Output Contracts

### 5.16.1 Requirement Evaluation Output
```json
{
	"requirement_id": "req_income_proof",
	"status": "PARTIALLY_SATISFIED",
	"confidence": 0.78,
	"supporting_evidence": ["artifact_123", "artifact_891"],
	"missing_evidence": ["bank_statement_last_3_months"],
	"conflicts": [],
	"citations": ["law_node_44", "article_12_3"],
	"recommended_action": "request_latest_statement"
}
```

### 5.16.2 Eligibility Matrix Output
```json
{
	"assessment_id": "assess_01",
	"procedure_id": "ex-01",
	"overall_confidence": 0.81,
	"coverage_score": 0.74,
	"requirements": [
		{
			"requirement_id": "req_income_proof",
			"status": "PARTIALLY_SATISFIED",
			"confidence": 0.78,
			"citations": ["article_12_3"]
		}
	],
	"blockers": ["missing_bank_statement"],
	"next_actions": ["request_missing_evidence", "send_for_review"]
}
```

### 5.16.3 Procedure Ranking Output
```json
{
	"case_id": "case_01",
	"ranked_procedures": [
		{
			"procedure_id": "ex-01",
			"readiness_score": 0.74,
			"confidence": 0.81,
			"top_blockers": ["missing_bank_statement"]
		},
		{
			"procedure_id": "ex-10",
			"readiness_score": 0.52,
			"confidence": 0.69,
			"top_blockers": ["employment_history_gap"]
		}
	]
}
```

## 6. C03 Workflow Orchestration

## 6.1 Scope and Responsibility
1. Orchestrate case lifecycle with durable state, retries, timers, and human gates.
2. Coordinate C01-C07 capability execution in deterministic sequences.

## 6.2 Core Components
1. Parent case workflow
2. Child workflows for intake, submission, and monitoring
3. Signal router and timer manager
4. Activity execution manager and retry policy engine

## 6.3 Inputs and Outputs
1. Inputs: user actions, integration events, capability outputs
2. Outputs: state transitions, task assignments, escalation events

## 6.4 API and UI Surfaces
1. API: A01, A03, A05, A06 workflow-affecting endpoints
2. UI: matter stage rail, blockers, next-action controls, timeline

## 6.5 Reliability Controls
1. Idempotency keys for side-effecting commands
2. Retry with exponential backoff for transient errors
3. BLOCKED_MANUAL_INTERVENTION path for non-retryable failures

## 6.6 Observability
1. Workflow duration by stage
2. Timeout and escalation counts
3. Signal delivery and processing latencies

## 7. C04 Form Preparation

## 7.1 Scope and Responsibility
1. Generate procedure-specific forms from canonical data.
2. Maintain corrected form state and unresolved field loop.
3. Produce HTML and PDF artifacts for review and submission.

## 7.2 Core Components
1. Template resolver
2. Field mapping engine
3. Form rendering engine
4. Artifact storage adapter
5. Form correction and re-generation service

## 7.3 Inputs and Outputs
1. Inputs: approved extraction data, procedure template, submission mode
2. Outputs: form artifacts, unresolved field lists, review-ready packets

## 7.4 API and UI Surfaces
1. API: A05 form generation and approval endpoints
2. UI: Forms, Lawyer Review, Filing readiness references

## 7.5 Workflow Touchpoints
1. Entry: FORM_FILLING_IN_PROGRESS
2. Gate: FORM_REVIEW_PENDING
3. Exit: FORM_APPROVED

## 7.6 Quality and Controls
1. Coverage of mapped required fields
2. Unresolved field count and trend
3. Role and state guard enforcement on approve and submit decisions

## 8. C05 Browser Automation (Playwright)

## 8.1 Scope and Responsibility
1. Execute controlled automation for online filing channels.
2. Capture receipts and monitor status updates.
3. Handle certificate-required steps through gated workflow controls.

## 8.2 Core Components
1. Automation runner
2. Portal adapter scripts
3. Receipt capture and parser
4. Monitoring scheduler

## 8.3 Inputs and Outputs
1. Inputs: approved submission plan, form data, certificate availability
2. Outputs: submission attempts, receipts, monitoring events

## 8.4 API and UI Surfaces
1. API: A06 filing status and certificate endpoints
2. UI: Filing, Timeline, Sync and audit views

## 8.5 Workflow Touchpoints
1. Entry: FORM_APPROVED and submit decision
2. States: AWAITING_DIGITAL_CERTIFICATE, SUBMITTED_WAITING_RECEIPT
3. Exit: SUBMISSION_CONFIRMED or escalation path

## 8.6 Safety Controls
1. Manual confirmation before irreversible submit action
2. Screenshot and artifact capture for auditability
3. Circuit-breaker behavior for repeated automation failures

## 9. C06 Integration and Sync

## 9.1 Scope and Responsibility
1. Synchronize data bi-directionally with PMS and channel systems.
2. Manage conflict detection, resolution, and replay controls.

## 9.2 Core Components
1. Connector adapters
2. Event ingestion and delivery queues
3. Conflict detection and resolution engine
4. Sync health monitor

## 9.3 Inputs and Outputs
1. Inputs: external webhook events, polling snapshots, internal publish events
2. Outputs: synced records, conflict records, retry jobs, sync logs

## 9.4 API and UI Surfaces
1. API: A07 sync endpoints and A08 connector management
2. UI: External Record, Sync Center, Linked Matters health indicators

## 9.5 Reliability and Control
1. Event dedupe keys and replay-safe outbound writes
2. Dead-letter queues and operator replay tooling
3. Conflict policy with human review on sensitive legal fields

## 10. C07 Security and Compliance Controls

## 10.1 Scope and Responsibility
1. Enforce authentication, authorization, tenant isolation, and auditability.
2. Protect PII and certificate material through policy and cryptography.

## 10.2 Core Components
1. Identity and token validation layer
2. Permission and state guard engine
3. Data protection and secret management controls
4. Audit and retention management services

## 10.3 Key Controls
1. Role and state-based authorization checks
2. Encryption at rest and in transit
3. PII redaction in logs
4. Immutable audit records for approvals and submissions
5. Retention and purge workflows

## 10.4 API and UI Surfaces
1. API: A08 admin security endpoints and all guarded mutating endpoints
2. UI: Admin, Filing decision dialogs, External Record conflict actions

## 11. Cross-Capability Dependency Map

| Capability | Depends On | Primary Consumers |
|---|---|---|
| C01 | C07 | C02, C04, UI Data Review |
| C02 | C01, Neo4j GraphRAG, C07 | C03, Lawyer Review, Matter Overview |
| C03 | C01-C07 outputs | All UI stages and integrations |
| C04 | C01, C02, C03 | Forms, Lawyer Review, Filing |
| C05 | C04, C03, C07 | Filing, Timeline, Monitoring |
| C06 | C03, C07 | Linked Matters, External Record, Sync Center |
| C07 | Foundation | All capabilities |

## 12. Capability Readiness Criteria
1. Each capability has API surface, UI surface, telemetry, and failure handling.
2. Each capability has explicit inputs, outputs, and schema expectations.
3. Each capability supports happy path and exception path validation.
4. Capabilities with external side effects enforce idempotency and audit logging.
5. Capabilities with legal impact preserve explainability and citation traceability.

## 13. Validation and Test Strategy
1. Unit tests
- Extraction parsers and normalizers
- Reasoning post-process validators
- Permission and state guards

2. Integration tests
- API contracts and capability handoff payloads
- Neo4j retrieval and citation integrity checks
- Connector sync and conflict flows

3. End-to-end tests
- Offline and online filing journeys
- Human gate approvals and return loops
- Failure injection for retries and escalations

4. Quality validation
- Extraction correction rate trends
- Legal recommendation override rates
- Submission success and rework rates

## 14. Implementation Artifacts
1. Pseudocode reference:
- ./capability-algorithms-pseudocode.md

2. JSON Schema references:
- ./capability-schemas/requirement-evaluation.schema.json
- ./capability-schemas/eligibility-matrix.schema.json
- ./capability-schemas/procedure-ranking.schema.json
