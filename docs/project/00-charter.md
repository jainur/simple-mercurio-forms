# Project Charter — abogados-cowork

**Domain:** abogadoscowork.com  
**Last updated:** 2026-04-18  
**Status:** Approved

---

## 1. Vision

abogados-cowork is a horizontal **business process automation platform** that uses AI and modern technology to streamline, integrate, and simplify legal workflows. It brings all actors in a case (lawyers, assistants, clients) to work closely together — eliminating silos, optimising information capture, and automating repetitive tasks.

**Spanish immigration law is the first vertical** used to prove and validate the model, not the final scope of the product.

---

## 2. Problem Statement

Immigration lawyers and their assistants spend significant time on manual, error-prone work: gathering client information, validating documents, filling multi-page government forms (EX forms), coordinating approvals, and filing via government portals (Mercurio). Much of this is done using disconnected tools (Office, email, PDFs). The process is fragmented, slow, and leaves little room for value-added legal work.

---

## 3. Product Goals

1. Automate the end-to-end immigration case workflow — from client intake to filed form.
2. Bring lawyers, assistants, and clients into a single collaborative workspace.
3. Use AI to extract, validate, and map client documents to form fields automatically.
4. Automate form PDF generation and government portal submission (Mercurio).
5. Provide a standalone product for firms with no existing PMS, while integrating with PMS tools (MyCase, Kleos etc.) as an optional extension.
6. Offer the product as multi-tenant SaaS and support on-premise deployment.

---

## 4. Actors

| Actor | Description |
|---|---|
| **Lawyer** | Reviews, approves, and takes legal responsibility for submissions. Has final sign-off authority. |
| **Assistant / Secretary** | Handles day-to-day case operations: data entry, document collection, form preparation, status tracking. Primary daily user. |
| **Client** | The applicant. Provides personal documents and information via a client-facing interface. |
| **Firm Admin** | Manages the firm's users, roles, settings, and subscription within the product. One per tenant. |
| **Platform Admin** | Manages tenants and infrastructure in the SaaS deployment (operated by the product owner). |

---

## 5. MVP Scope

### In scope
- **Procedures and forms:** All EX forms. First form to implement end-to-end: **EX11**.
- **Document intelligence:** AI extraction of client data from uploaded documents (passport, NIE, financial docs etc.).
- **Form autofill:** Mapping extracted data to EX form PDF fields automatically.
- **Requirements & validation:** System communicates applicable procedure requirements and validates completeness.
- **Lawyer approval gate:** Hard stop requiring lawyer review and sign-off before filing.
- **Portal automation:** Automated submission via the Mercurio government portal using the firm's FNMT digital certificate.
- **Multi-language UI:** English for initial development; Spanish and Catalan required before MVP release.
- **GDPR compliance:** Day-one requirement given EU/Spain context and sensitivity of client data.
- **Deployment modes:** Cloud (SaaS) and on-premise both supported from first release.

### Out of scope for MVP
- PMS integration (MyCase, Kleos etc.)
- Billing and subscription management
- Non-Spanish jurisdictions
- Mobile application
- Non-immigration legal domains

---

## 6. Success Criteria for MVP

1. At least one end-to-end procedure completed (client intake → document extraction → form filled → lawyer approved → filed via Mercurio).
2. First paying customer onboarded.
3. First EX form (EX11) successfully filed via the Mercurio portal in a real case.

---

## 7. Deployment & Tenancy Model

| Aspect | SaaS | On-Premise |
|---|---|---|
| Infrastructure management | Product owner (platform admin) | Customer |
| Application management | Customer (firm admin) | Customer (firm admin) |
| Tenant isolation | Logical (per-firm data segregation) | Physical (dedicated deployment) |

A **tenant** is a law firm. Each firm has one or more users with distinct roles.

---

## 8. Key Constraints

| Constraint | Detail |
|---|---|
| **Solo build** | Built by a single developer using AI-assisted development. Scope and sprint sizes must be realistic. |
| **i18n from day one** | UI must be built with internationalisation infrastructure from the start. Content will be in English first, Spanish + Catalan before MVP release. |
| **GDPR** | Personal and sensitive client data (passports, financial records) requires encryption at rest, data minimisation, consent tracking, and right-to-erasure support. |
| **FNMT certificate** | Mercurio portal automation requires access to the firm's locally-installed FNMT digital certificate. This drives the need for a local agent component. |
| **Dual deployment** | Architecture must support both cloud-hosted and on-premise deployments without forking the codebase. |

---

## 9. Non-Goals (explicit)

- This product does **not** replace existing PMS tools (MyCase, Kleos). In firms that use them, it integrates alongside.
- This product does **not** handle billing, invoicing, or time-tracking.
- This product does **not** provide legal advice — it assists with procedure execution under lawyer supervision.
- This product is **not** a mobile-first application.

---

## 10. Decision Log (Resolved)

| # | Question | Status |
|---|---|---|
| OQ-01 | What LLM provider(s) will be used for document extraction? Single provider or abstracted? | Resolved: Provider abstraction with Gemini as default implementation |
| OQ-02 | Will on-premise deployment use Docker/Kubernetes, or a simpler single-machine install? | Resolved: Standard and compact on-prem profiles supported in MVP |
| OQ-03 | What is the local agent technology for FNMT certificate access — Tauri, Electron, or CLI? | Resolved: Tauri |
