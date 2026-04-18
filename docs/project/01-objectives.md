# Objectives and Goals — abogados-cowork

**Last updated:** 2026-04-18  
**Status:** Approved

## 1. Purpose of This Document

Define concrete, measurable objectives for the product so requirements, architecture, and sprint planning can be evaluated against explicit outcomes.

## 2. Objective Hierarchy

### O1. Deliver End-to-End Immigration Procedure Automation
Enable law firms to complete Spanish immigration procedures from intake to filing with minimal manual handling.

**Success outcomes**
- Assistant can run client intake, upload documents, and trigger automated extraction.
- System validates required evidence and flags gaps.
- System auto-fills EX forms and prepares filing artifacts.
- Lawyer review gate is enforced before any external filing action.
- Filing can be completed through Mercurio workflow support.

### O2. Improve Operational Throughput and Quality
Reduce repetitive manual work while increasing consistency and traceability.

**Success outcomes**
- Reduced manual data re-entry across workflow steps.
- Reduced form completion errors (missing or inconsistent fields).
- Standardised process states visible to assistant and lawyer.
- Auditable timeline of who changed/approved what and when.

### O3. Support Real-World Firm Operating Modes
Serve both digitally mature firms and low-tooling firms without blocking adoption.

**Success outcomes**
- Product is usable standalone with no PMS required.
- Product can be extended later for PMS integrations without redesign.
- Tenant model supports firm-level access control and administration.

### O4. Ship as a Commercially Viable Product
Reach market proof with paying usage and measurable customer value.

**Success outcomes**
- First paying customer onboarded.
- At least one real case completed end-to-end.
- First successful EX11 filing workflow completed via Mercurio.

### O5. Establish a Scalable Foundation Beyond Immigration
Use immigration as the proving vertical for a broader process-automation platform.

**Success outcomes**
- Core architecture separates domain-specific rules from reusable workflow capabilities.
- Internationalisation built from the start (English development, Spanish/Catalan for MVP release).
- Deployment model supports both SaaS and on-premise customers.

## 3. MVP Goal Statement

For MVP, abogados-cowork must allow a law firm assistant to take a new client from zero to a lawyer-approved and filed EX11 procedure with AI-assisted extraction, validation, and form automation, while meeting GDPR expectations and supporting Spanish/Catalan interfaces.

## 4. KPI Candidates (to baseline and finalize in planning)

### Adoption and business
- Number of active tenant firms.
- Number of active users by role (assistant, lawyer, admin).
- First paying customer achieved (yes/no, date).

### Workflow performance
- Median time from case creation to lawyer-ready packet.
- Median time from lawyer approval to filing attempt completion.
- Percentage of cases completed end-to-end without manual PDF edits.

### Automation quality
- Extraction field accuracy rate on required fields.
- Form prefill completeness rate.
- Validation pass rate before lawyer review.

### Reliability and operations
- Filing workflow success rate (including retried attempts).
- Error rate by workflow stage.
- Mean time to recover from failed automation runs.

### Compliance and governance
- Percentage of auditable actions with actor and timestamp metadata.
- Time to fulfill data subject deletion/export requests.
- Percentage of users with role-consistent access behavior (authorization conformance).

## 5. Objective Constraints

- Scope is intentionally limited to immigration procedure automation for MVP.
- PMS integrations are postponed to post-MVP.
- Team capacity is constrained by solo implementation with AI-assisted development.
- Dual deployment (SaaS + on-premise) is required from the first release.

## 6. Decision Baselines (Resolved)

- KPI baselines for MVP release:
	- At least 1 paying tenant.
	- At least 1 real end-to-end EX11 case completed.
	- At least 1 successful Mercurio filing in production.
	- At least 80% of pilot cases completed without manual PDF edits.
- Minimum extraction quality baseline:
	- At least 90% accuracy on required fields across pilot validation set.
	- Mandatory human review for low-confidence fields before filing.
- On-prem deployment baseline:
	- MVP supports both standard and compact on-prem profiles.
- Mercurio automation boundary:
	- Supervised automation in MVP with mandatory lawyer approval gate and supervised retry path.
