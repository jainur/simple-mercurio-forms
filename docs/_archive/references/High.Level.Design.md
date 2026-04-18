***

## 1. Solution Overview

The system is an **immigration case operations layer** that sits on top of existing Practice Management Systems (PMS) like MyCase/Kleos. It orchestrates:

- Client intake and document collection  
- AI-assisted extraction and eligibility assessment  
- Form and packet preparation  
- Lawyer approval  
- (Phase 2) Semi‑automated filing and status monitoring  

All long-running workflows are orchestrated centrally, while PMS remains the system of record for matters and billing. [geeksforgeeks](https://www.geeksforgeeks.org/system-design/what-is-high-level-design-learn-system-design/)

***

## 2. Major Components

### 2.1 External Systems

- **PMS (MyCase, Kleos, etc.)**  
  - Own matter records, contacts, billing, general documents.  
  - Send events like “matter created/updated”.  
  - Receive updates like status, notes, and final PDFs.

- **Spanish Government Portals (e.g., Mercurio)**  
  - Receive finalized packets and forms.  
  - Provide submission receipts and status updates (approved, pending, RFE, denied).

### 2.2 Frontend / UX Layer

- **Web App (Next.js + React)**  
  - Client Portal: guided intake, document upload, progress tracker.  
  - Assistant Workspace: case overview, documents, data review, forms, tasks.  
  - Lawyer Console: legal summary, risk flags, side‑by‑side doc vs extracted data, approve/return.

- **Local Desktop Agent (Tauri/Electron)** – Phase 2  
  - Runs on the law firm’s machine.  
  - Holds local FNMT digital certificate.  
  - Executes Playwright scripts against government portals for filing and status checks.  

***

## 3. Backend Logical Architecture

### 3.1 API & Integration Layer

- **API Gateway (FastAPI)**  
  - Serves UI (REST/GraphQL) and exposes hooks for PMS and Desktop Agent.  
  - Authenticates users (lawyers, assistants, clients) and enforces tenant boundaries.

- **PMS Integration Adapters**  
  - Webhook receivers or polling jobs.  
  - Map external matter/contact schemas to internal case model.  
  - Push back status, notes, and final artifacts.

### 3.2 Workflow & Orchestration (Temporal)

- **CaseLifecycleWorkflow**  
  - Orchestrates: intake → docs → AI extraction → eligibility → packet → review → (optional) portal submission → follow‑up.  
  - Manages timers (reminders, deadlines), retries, compensations, and approval wait states.  

- **Activities** (examples)  
  - `RunIntakeExtraction`  
  - `ComputeEligibilityMatrix`  
  - `GenerateFormsAndPacket`  
  - `WaitForLawyerApproval`  
  - `TriggerDesktopAgentFiling`  
  - `CheckPortalStatus`  

Temporal guarantees durability and visibility for each case workflow. [blog.langchain](https://blog.langchain.com/building-langgraph/)

### 3.3 AI Reasoning Layer (LangGraph)

- **Supervisor Graph**  
  - Receives a structured “reasoning request” from Temporal activities.  
  - Routes to worker sub‑graphs.

- **Workers**  
  - Intake Normalization Worker – cleans OCR data, deduplicates, maps to canonical fields.  
  - Eligibility Matrix Worker – queries Neo4j + vectors to generate requirement coverage per procedure.  
  - Document Strategy Worker – produces missing‑evidence checklists and risk flags.  
  - Submission‑Readiness Worker – computes readiness score and blockers.

All outputs are **structured** (JSON) with confidence scores and citation IDs pointing back into the graph. [youtube](https://www.youtube.com/watch?v=rMXz_Upv1Dw)

### 3.4 Legal Knowledge Layer (Neo4j + Vector Store)

- **Neo4j Graph**  
  - Nodes: procedures, requirements, legal sources (articles, regulations), evidence types.  
  - Relationships: “requires”, “satisfied_by”, “applies_to”, “exception_to”.  

- **Hybrid Retrieval**  
  - Vector search for semantic similarity over text chunks.  
  - Graph expansion from relevant nodes.  
  - Ensures every legal recommendation is backed by explicit legal references. [youtube](https://www.youtube.com/watch?v=nIM_NimxxRc)

### 3.5 Case Operations Data Layer (Postgres + Object Storage)

- **Postgres**  
  - Case, Applicant, CaseFact, RequirementCoverage, DeadlineInstance, SubmissionAttempt, ApprovalRecord, ChannelEvent, AuditLog, AutomationRun.  
  - Acts as operational truth for workflow state and reporting.

- **Object Storage (S3 or equivalent)**  
  - Raw uploads (scans, PDFs, photos).  
  - Generated forms and packets.  
  - Portal artifacts (receipts, HTML snapshots).

***

## 4. Execution Automation Layer

### 4.1 Cloud‑side Automation

- **Playwright Workers (Cloud)**  
  - For read‑only tasks that do not require local certificates (e.g., open unauthenticated status pages, simulate simple flows).  
  - Mostly used for prototyping and low‑risk automation.

### 4.2 Hybrid / Local Automation (Phase 2)

- **Desktop Agent + Playwright**  
  - Desktop Agent receives a signed “Submission Plan” and “Automation Run ID” from the API.  
  - Executes Playwright against Spanish portals using local FNMT certificate.  
  - Returns results (status, receipts, screenshots) to backend via secure API.  

This design keeps private keys local, satisfying strong security and compliance constraints.

***

## 5. Data & Control Flows (High Level)

### 5.1 New Case Flow

1. Matter created in PMS → webhook to Integration Adapter.  
2. Adapter creates/links `Case` in Postgres and starts `CaseLifecycleWorkflow` in Temporal.  
3. Temporal notifies Web App: assistant can now open the Immigration Workspace for this matter.

### 5.2 Intake & Document Flow

1. Assistant sends client an intake link.  
2. Client answers questions and uploads docs → API → S3 + metadata in Postgres.  
3. Temporal triggers `RunIntakeExtraction` → LangGraph Intake Worker → Canonical Applicant profile + extracted fields.  
4. Assistant reviews and corrects in “Data Review” screen.

### 5.3 Eligibility & Packet Flow

1. Temporal calls `ComputeEligibilityMatrix` → LangGraph Eligibility Worker → uses Neo4j to produce requirement coverage, citations.  
2. Assistant sees eligibility summary, missing-evidence checklist, and risk flags.  
3. When ready, Temporal calls `GenerateFormsAndPacket` → form templates filled from canonical data → PDFs stored in S3 and linked to `SubmissionPlan`.  

### 5.4 Lawyer Review & Approval

1. Temporal enters `WaitForLawyerApproval` state.  
2. Lawyer opens Review Console, sees legal reasoning (with citations) and packet preview.  
3. Lawyer can: Approve, Request Changes, or Reject.  
4. Temporal resumes workflow depending on the decision.

### 5.5 Filing & Follow‑Up

1. If automated filing enabled: Temporal sends `SubmissionPlan` to Desktop Agent.  
2. Desktop Agent runs Playwright, files on *Mercurio*, and posts back `AutomationRunResult`.  
3. Temporal records `SubmissionAttempt`, uploads receipts, and schedules periodic status checks.  
4. Changes in status are pushed into PMS and surfaced in Timeline/Status UI.

***

## 6. Non‑Functional Considerations

- **Security:**  
  - JWT or OIDC auth; role‑based access; tenant isolation.  
  - PII encrypted at rest; TLS in transit.  
  - AuditLog for all substantive changes.

- **Reliability & Observability:**  
  - Temporal for durable workflows.  
  - Structured logging (e.g., OpenTelemetry), metrics, and alerting on workflow failures.

- **Extensibility:**  
  - New procedures or countries can be added by extending Neo4j graph + templates, not by rewriting core logic.  
  - Flexible adapter layer for new PMS integrations.

***