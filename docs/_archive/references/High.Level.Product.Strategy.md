The unified documentation suite fuses the **integration-first product strategy** (UX/UI, PMS sync, role-based workflows) with your **agentic backend architecture** (Temporal, LangGraph, Neo4j, Playwright).

***

# 1. Unified Functional Requirements Document (FRD)

This document defines what the system must *do* to successfully orchestrate Spanish immigration cases from intake to portal submission.

### 1.1 Integration & Master Data Management
*   **PMS Bidirectional Sync:** The system must connect to external Practice Management Systems (e.g., MyCase, Kleos) via API to ingest new matter events and sync back statuses, notes, and final documents.
*   **Canonical Data Model:** The system must extract and maintain a single source of truth for an applicant (Name, NIE, Passport info, Address) to populate all subsequent forms without duplicate data entry.

### 1.2 Intake & Document Collection
*   **Dynamic Client Portal:** The system must provide a secure, mobile-friendly web interface for clients to answer localized intake questions and upload documents securely.
*   **Intake Normalization:** The system must classify uploaded documents, run OCR, and map extracted entities (e.g., expiration dates, ID numbers) to the Canonical Data Model.

### 1.3 AI Reasoning & Legal Grounding (GraphRAG)
*   **Eligibility Assessment:** The system must evaluate the applicant's data against a Neo4j legal graph to determine eligibility for specific Spanish pathways (e.g., Non-Lucrative, Golden Visa, Arraigo).
*   **Evidence Gap Detection:** The system must cross-reference required evidence for a procedure against uploaded documents and automatically generate a "Missing Evidence" checklist.
*   **Citation Grounding:** Every legal recommendation or eligibility flag must include a citation reference back to the original Spanish legal text stored in the graph.

### 1.4 Form Preparation & Packet Assembly
*   **EX Form Generation:** The system must automatically map the Canonical Data Model to official Spanish immigration forms (EX-01, EX-15, M-IT, etc.) and generate submission-ready PDFs.
*   **Assistant Exception Queue:** The system must flag low-confidence data extractions or conflicting information for human review by the legal assistant.

### 1.5 Durable Workflow & Approvals
*   **Stateful Orchestration:** The system must track cases over months, managing wait states, follow-ups, and reminders without timing out.
*   **Lawyer Review Gate:** The system must enforce a hard stop requiring explicit Lawyer approval of the submission packet, risk flags, and legal arguments before external filing.

### 1.6 Execution Automation & Filing
*   **Local-First Certificate Filing:** The system must support a local or hybrid execution environment to utilize the lawyer’s physically installed FNMT Digital Certificate for Spanish government portals (Mercurio).
*   **Automated Status Checking:** The system must periodically execute headless browser tasks (Playwright) to check portal statuses and download official notifications/resolutions.

***

# 2. Unified Solution Architecture

This architecture bridges the "Clear Path" UI UX with the durable, agentic backend. 

### 2.1 Presentation & UX Layer
*   **Web Portal (React/Next.js):** Hosts the Client Intake Wizard, the Assistant Operations Dashboard, and the Lawyer Review Console. Follows the "Clear Path" design system (navy, white, structured typography).
*   **Local Desktop Agent (Tauri/Electron) [Hybrid Component]:** A lightweight local application installed on the law firm's machine. It securely bridges the cloud workflow engine with the lawyer's local FNMT Digital Certificate for automated Playwright submissions to the Spanish *Mercurio* portal.

### 2.2 API & Integration Layer
*   **API Gateway (FastAPI):** Exposes REST/GraphQL endpoints for the frontends.
*   **PMS Sync Adapters:** Webhook listeners and polling workers that keep the external system of record (MyCase/Kleos) in sync with the current workflow state.

### 2.3 Durable Workflow Layer
*   **Temporal.io:** The heartbeat of the system. Manages the `CaseLifecycleWorkflow`. It handles scheduling (e.g., "wait 30 days for document", "retry portal check every 24 hours"), state transitions, and pauses the process when it hits a `RequireLawyerApproval` activity.

### 2.4 AI Reasoning Layer (LangGraph)
*   **Supervisor Agent:** Routes sub-tasks.
*   **Worker Agents:**
    *   *Intake Worker:* Normalizes OCR data.
    *   *Eligibility Matrix Worker:* Queries the Neo4j graph to score readiness.
    *   *Document Strategy Worker:* Flags missing or expired documents.

### 2.5 Legal Knowledge Layer
*   **Neo4j Graph Database:** Stores nodes for Spanish immigration laws, requirements, procedures, and historical precedents. Enables hybrid retrieval (vector + semantic relationships) for high-accuracy legal grounding.

### 2.6 Persistence Layer
*   **Postgres:** Stores transactional case operations data (Applicant info, Approval Records, Audit Logs, Workflow States).
*   **S3/Object Storage:** Securely stores uploaded passports, financial records, and generated EX-form PDFs.

***

# 3. Unified Tech Stack

| Component | Technology | Role in Architecture |
| :--- | :--- | :--- |
| **Frontend Framework** | **Next.js (React) + TailwindCSS** | Delivers the "Clear Path" UI. Tailwind enforces the strict design tokens (navy/white, accessible contrast). |
| **Local Desktop Agent** | **Tauri (Rust/React)** | Allows the platform to securely access local file systems and OS-level certificate stores (FNMT) for Spanish portal submissions without uploading private keys to the cloud. |
| **Backend API** | **Python (FastAPI)** | High-performance API layer. Python is chosen specifically to maintain native compatibility with the LangGraph and AI data science ecosystem. |
| **Workflow Engine** | **Temporal.io** | Replaces brittle cron jobs and ad-hoc state machines. Guarantees that a case workflow running for 6 months will not drop data or lose its place if a server restarts. |
| **AI Orchestration** | **LangGraph** | Structures the LLM calls into a deterministic, multi-agent graph (Supervisor → Intake → Eligibility → Form Prep). |
| **LLM Provider** | **Gemini Pro / GPT-4o** | The core reasoning engine. Called strictly by LangGraph workers. |
| **Knowledge Graph** | **Neo4j** | Stores the parsed Spanish immigration laws and case chunks for GraphRAG. Ensures the LLM cannot hallucinate legal requirements. |
| **Transactional DB** | **PostgreSQL** | The operational database. Stores normalized case facts, audit logs, and sync states matching the PMS. |
| **Execution Engine** | **Playwright (Python)** | Automates the filling of web forms on government portals and scrapes status updates/receipts. |
| **File Storage** | **AWS S3** | Immutable, encrypted-at-rest storage for all client artifacts and generated PDFs. |

***

# 4. Refined Product Requirements Document (PRD)

## 4.1 Product Vision & Positioning
**Product Name:** Clear Path Operations (Placeholder)
**Vision:** To be the definitive workflow and AI reasoning layer for Spanish immigration practices. We do not replace a firm's Practice Management System; we sit on top of it, transforming messy intake and manual form-filling into a deterministic, legally-grounded, automated pipeline.

## 4.2 Target Market (SAM & SOM)
*   **SAM (Serviceable Addressable Market):** Spanish law firms and *gestorías* that handle immigration matters and use existing digital case management tools (approx. 1,000 - 3,000 firms).
*   **SOM (Serviceable Obtainable Market):** Small-to-midsize immigration boutiques (3-30 staff) in major expat/migration hubs (Madrid, Barcelona, Malaga, Valencia) suffering from high administrative overhead.

## 4.3 Key Personas & UX Goals
1.  **The Legal Assistant (Primary User):** Needs to process cases 5x faster. They live in the "Data Review" and "Documents" screens, resolving exceptions flagged by the AI, rather than doing manual data entry.
2.  **The Lawyer (Approver):** Needs absolute trust. They live in the "Lawyer Review Console," evaluating GraphRAG-cited legal risks and clicking "Approve for Filing."
3.  **The Client (End User):** Needs reduced anxiety. They see a calm, premium "Clear Path" wizard to upload documents and view progress.

## 4.4 Core Value Propositions
*   **Zero Double-Entry:** Bidirectional sync with MyCase/Kleos means the firm's system of record remains pristine.
*   **Defensible AI (GraphRAG):** We don't use generic LLM wrappers. Every eligibility claim is mapped to a specific node in Spanish immigration law.
*   **Hybrid Execution for Spain:** Uniquely solves the "AutoFirma/FNMT Certificate" problem by allowing cloud-orchestrated workflows to execute the final portal submission securely via a local desktop client.
*   **Unbreakable Workflows:** Temporal ensures that a case waiting 90 days for a government response is perfectly tracked, monitored, and escalated without manual calendar reminders.

## 4.5 Phased Rollout Scope
### Phase 1 (MVP)
*   **Focus:** Intake, Extraction, GraphRAG Eligibility, and Document Packet Generation.
*   **Scope:** 3 high-volume pathways (e.g., EX-15 NIE, EX-01 Non-Lucrative, EX-10 Arraigo).
*   **Execution:** Manual filing. The system generates the perfect PDF packet and checklist; the assistant physically submits it to the portal.
*   **Integration:** One primary PMS sync (e.g., MyCase open API).

### Phase 2 (The Moat)
*   **Focus:** Autonomous Execution and Status Monitoring.
*   **Scope:** Rollout the Local Tauri App for hybrid execution.
*   **Execution:** Playwright automation connects to the local FNMT certificate to autonomously file the approved packet on *Mercurio* and pull the submission receipt. Daily headless scraping for status changes (Approved, Requires More Info, Denied).

## 4.6 Success Metrics
*   **Time-to-File:** Reduce assistant preparation time per case by 70%.
*   **First-Pass Yield:** Achieve 95%+ acceptance rate on government portals without "Requests for Further Evidence" (Requerimientos) due to the GraphRAG requirement coverage worker.
*   **PMS Sync Integrity:** 99.9% uptime on data syncs to ensure the firm's main ledger is never corrupted.