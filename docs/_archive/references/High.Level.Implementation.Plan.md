## Plan: Spanish Large Duration E2E Flows — Offline + Online

**TL;DR**: Extend the existing Phase 1–8 PoC with five new components that wire together into two complete HITL flows (offline paper forms, online portal submission) for all Spanish immigration procedures (Hojas 1–9+). The existing state machine, APIs, document pipeline, and browser automation are all reused; we add procedure scoping, extraction review, form filling, certificate handling, and a form review/submit-decision gate.

---

### Scope decisions

- **Procedures**: All hojas (1–9+) from sop_inventory.json
- **Form output**: HTML (browser-renderable) + PDF export — both
- **Digital certificate**: `.p12` / `.pfx` file upload; stored encrypted, purged after use
- **Procedure selection**: Infer via existing reasoning step by default; `procedure_id` override at case creation

---

### Current state vs. what's new

**Reused as-is**: Case CRUD, 19-state machine, 20 signal types, reasoning adapter, document upload + coverage, submission plan approval gate, browser automation (Playwright/sandbox), monitoring, appeals, channel webhooks.

**Gaps to fill** (5 new components):

| Gap | New Component |
|---|---|
| No procedure-scoped requirements query | `GET /cases/{id}/procedure/requirements` |
| No extraction field review/correction | `ExtractionReview` model + HITL endpoints |
| No form template or form filler | `form_filler.py` + Hoja HTML templates |
| No .p12 certificate upload | `certificate_handler.py` + encrypted cert store |
| No form review + submit decision | Form HITL endpoints + FORM_REVIEW_PENDING state |

---

### New workflow states & signals

**States to add** (extending 19 → 25):

```
EXTRACTION_REVIEW_PENDING       ← after all docs uploaded + coverage computed
FORM_FILLING_IN_PROGRESS        ← system generating filled form
AWAITING_DIGITAL_CERTIFICATE    ← online: Playwright detected cert requirement
FORM_REVIEW_PENDING             ← HITL: user reviews form (offline & online)
FORM_APPROVED                   ← final pre-submission/post-review gate
SUBMISSION_DECLINED             ← online: user chose not to submit
```

**Signals to add** (extending 22 → 30):

```
EXTRACTION_REVIEW_READY, EXTRACTION_APPROVED, EXTRACTION_CORRECTION_SAVED
FORM_GENERATED, FORM_APPROVED, FORM_CORRECTION_SAVED
CERTIFICATE_REQUESTED, CERTIFICATE_PROVIDED
SUBMIT_APPROVED, SUBMIT_DECLINED
```

---

### Phase A — Procedure Scoping *(no new HITL, unblocks everything)*

1. Add `procedure_id` (nullable) column to `cases` table — new Alembic migration `20260402_000006_add_procedure_scoping.py`
2. Extend `POST /cases` request body to accept optional `procedure_id`
3. Extend `reasoning_adapter.py`: when `procedure_id` is set, skip candidate discovery; run a direct Cypher query for that procedure's graph subgraph
4. New endpoint `GET /cases/{id}/procedure/requirements` — returns structured JSON:
   - `required_documents`: list from `RequiredDocument` nodes (name, description, mandatory flag)
   - `prerequisites`: list from `Requirement` nodes (text, type: eligibility/general)
   - `fees`: from `Fee` nodes
   - `deadlines`: from `Deadline` nodes
   - `submission_channels`: from `SUBMITTED_VIA` relationships
5. New Cypher templates in cypher_templates.py: `procedure_requirements_by_id`

*Parallel with nothing — all subsequent phases depend on this.*

---

### Phase B — Document Extraction Review + HITL (Step 5)

*Depends on: Phase A (procedure_id determines which fields to extract)*

1. **Enhance `analyze_document()`** in document_pipeline.py: add LLM-based deep field extraction (full name, DOB, nationality, document number, issue/expiry dates, issuing authority). Store in `analysis_json.extracted_fields`.
2. **New DB model** `ExtractionReview` — `extraction_reviews` table: `case_id`, `artifact_id` (FK → document_artifacts), `extracted_fields_json`, `corrected_fields_json` (operator corrections), `correction_history_json` (audit trail of all edits), `approved_by`, `approved_at`, `status` (pending | partially_corrected | approved)
3. **New migration** `20260402_000007_add_extraction_review_table.py`
4. **New workflow state** `EXTRACTION_REVIEW_PENDING` — triggered by signal `EXTRACTION_REVIEW_READY` after coverage recompute
5. **New files**: `src/graphrag/workflows/extraction_review.py`, `src/graphrag/workflows/extraction_schemas.py`
6. **New endpoints**:
   - `GET /cases/{id}/extractions` — list all extraction reviews with fields + corrections
   - `PATCH /cases/{id}/extractions/{artifact_id}` — apply operator corrections to extracted fields
   - `POST /cases/{id}/extractions/approve` — HITL approve all extractions → fires `EXTRACTION_APPROVED` → state moves to `FORM_FILLING_IN_PROGRESS`

---

### Phase C — Form Filling *(Steps 5→6 transition)*

*Depends on: Phase B (approved extraction data drives form fill)*

1. **HTML templates** for each Hoja: `data/form_templates/hoja_<N>.html` — one per procedure, listing all required fields as labeled inputs. Generated once from SOP graph data (script can be a helper, not shipped).
2. **New DB model** `FormArtifact` — `form_artifacts` table: `case_id`, `procedure_id`, `submission_mode` (offline | online), `form_template_id`, `filled_fields_json`, `correction_history_json`, `html_content` (stored text or path), `pdf_path`, `status` (generating | ready | approved | submitted), `approved_by`, `approved_at`
3. **New migration** `20260402_000008_add_form_artifacts_table.py`
4. **New file** `src/graphrag/workflows/form_filler.py`:
   - `generate_form_offline()`: merges approved `ExtractionReview.corrected_fields_json` → Hoja template → outputs HTML (inline) + PDF (via `weasyprint` or similar)
   - `fill_form_online()`: Playwright fills portal form fields from corrected extraction data; does NOT click submit; captures a screenshot artifact; handles missing fields gracefully
5. **New files**: `src/graphrag/workflows/form_schemas.py`
6. **New states**: `FORM_FILLING_IN_PROGRESS` (system works) → `FORM_REVIEW_PENDING` (HITL)
7. **New signal**: `FORM_GENERATED`
8. **New endpoints**:
   - `POST /cases/{id}/forms/generate` — triggers form filler, creates `FormArtifact`, fires `FORM_GENERATED`
   - `GET /cases/{id}/forms` — list form artifacts
   - `GET /cases/{id}/forms/{form_id}` — return filled HTML or PDF (content-type negotiated)

---

### Phase D — Digital Certificate (Online only) *(parallel with Phase C)*

*Depends on: Phase A only*

1. **New DB model** `DigitalCertificate` — `digital_certificates` table: `case_id`, `certificate_ref` (path to encrypted file on disk), `algorithm` (e.g., AES-256), `provided_at`, `used_at`, `purged_at`. Never log cert content, never persist in response payloads.
2. **New migration** `20260402_000009_add_digital_certificates_table.py`
3. **New file** `src/graphrag/workflows/certificate_handler.py`:
   - `store_certificate(case_id, raw_bytes)` — encrypts with AES-256 using a per-case key derived from app secret, stores to `data/certs/{case_id}.enc`, stores ref in DB
   - `load_certificate(case_id)` — decrypts for Playwright use, returns raw bytes
   - `purge_certificate(case_id)` — wipes file and marks DB record purged
4. **New endpoint** `POST /cases/{id}/certificate` — multipart file upload, calls `store_certificate()`, fires `CERTIFICATE_PROVIDED` signal
5. **New state** `AWAITING_DIGITAL_CERTIFICATE` — browser automation pauses when it detects cert required, fires `CERTIFICATE_REQUESTED`; on `CERTIFICATE_PROVIDED` resumes fill
6. **Playwright integration** in browser_automation.py: detect cert dialog → emit `CERTIFICATE_REQUESTED` → poll / wait for `CERTIFICATE_PROVIDED` before continuing

---

### Phase E — Form Review + Submit Decision (HITL Steps 6-7)

*Depends on: Phase C (form artifacts exist), Phase D (cert available for online)*

1. **New endpoints**:
   - `PATCH /cases/{id}/forms/{form_id}` — operator corrects specific form fields; appended to `correction_history_json`; regenerates filled form artifact
   - `POST /cases/{id}/forms/{form_id}/approve` — HITL approve; fires `FORM_APPROVED`; for offline this ends the flow (`CLOSED_OFFLINE_READY`); for online opens submit decision
   - `POST /cases/{id}/forms/{form_id}/submit-decision` — online only; body `{"decision": "submit" | "decline"}`; fires `SUBMIT_APPROVED` → triggers actual Playwright submit click → `SUBMITTED_WAITING_RECEIPT`; or `SUBMIT_DECLINED` → `SUBMISSION_DECLINED`
2. **New states**: `FORM_APPROVED`, `SUBMISSION_DECLINED`, `CLOSED_OFFLINE_READY`
3. **New signals**: `FORM_APPROVED`, `FORM_CORRECTION_SAVED`, `SUBMIT_APPROVED`, `SUBMIT_DECLINED`
4. **Certificate purge**: on `FORM_APPROVED` for online flow, `purge_certificate()` is called

---

### Phase F — Documentation (save to uc-large-duration)

*Parallel with implementation phases — can be written incrementally*

1. `docs/uc-large-duration/README.md` — use case overview, two flow diagrams (ASCII/table), quick-start guide
2. `docs/uc-large-duration/DESIGN.md` — extended state machine diagram, new data models, API reference for all new endpoints, security notes on certificate handling
3. `docs/uc-large-duration/IMPLEMENTATION_PLAN.md` — this plan reformatted as a living tracker with phase checkboxes

---

### Files to modify / create

**Modify:**
- models.py — add `procedure_id` to `Case`; add `ExtractionReview`, `FormArtifact`, `DigitalCertificate` models
- repository.py — CRUD methods for new models
- schemas.py — extend `CaseCreateRequest`; add response schemas
- state_machine.py — add 6 new states + 10 new signals + TRANSITIONS entries
- document_pipeline.py — enhance `analyze_document()` with LLM field extraction
- browser_automation.py — add cert detection + form fill (no submit) logic
- cypher_templates.py — add `procedure_requirements_by_id` template
- reasoning_adapter.py — short-circuit candidate discovery for scoped `procedure_id`
- api.py — register all new endpoints

**Create:**
- `src/graphrag/workflows/extraction_review.py`
- `src/graphrag/workflows/extraction_schemas.py`
- `src/graphrag/workflows/form_filler.py`
- `src/graphrag/workflows/form_schemas.py`
- `src/graphrag/workflows/certificate_handler.py`
- `alembic/versions/20260402_000006_add_procedure_scoping.py`
- `alembic/versions/20260402_000007_add_extraction_review_table.py`
- `alembic/versions/20260402_000008_add_form_artifacts_table.py`
- `alembic/versions/20260402_000009_add_digital_certificates_table.py`
- `data/form_templates/hoja_<1..9>.html` (one per procedure)
- `docs/uc-large-duration/README.md`
- `docs/uc-large-duration/DESIGN.md`
- `docs/uc-large-duration/IMPLEMENTATION_PLAN.md`

---

### Verification

1. **Phase A smoke test**: Create case with `procedure_id="hoja_1"`, call `GET /cases/{id}/procedure/requirements`, verify documents list + prerequisites returned from graph correctly
2. **Phase B smoke test**: Upload a passport PDF, call `GET /cases/{id}/extractions`, verify `extracted_fields` has `full_name`, `dob`, `nationality`, `doc_number`; PATCH to correct one field; POST approve; verify state → `FORM_FILLING_IN_PROGRESS`
3. **Phase C offline test**: POST `forms/generate` with `submission_mode=offline`, verify HTML artifact generated and PDF path recorded; GET form → HTML response includes filled values from approed extraction
4. **Phase C online test**: POST `forms/generate` with `submission_mode=online`, verify Playwright fills fields without submitting, screenshot artifact captured
5. **Phase D test**: POST `.p12` file to `POST /cases/{id}/certificate`; verify encrypted file on disk; verify DB row; verify purge after form approval
6. **Phase E offline test**: PATCH form to correct one field; POST approve; verify state = `CLOSED_OFFLINE_READY`; verify cert purge not called (offline)
7. **Phase E online test**: POST `submit-decision` with `{"decision": "submit"}`; verify Playwright submits; state → `SUBMITTED_WAITING_RECEIPT`; verify cert purged; POST `{"decision": "decline"}` alternate → `SUBMISSION_DECLINED`
8. **Full offline E2E**: Walk all 7 steps in the offline flow via API calls, verify state machine progression at each HITL gate
9. **Full online E2E**: Walk all 7 steps in the online flow; inject cert; verify form review; submit decision

---

### Decisions & exclusions

- **Procedure templates**: HTML templates will be generated from SOP graph data programmatically (a one-time helper script), not hand-coded
- **PDF generation**: Use `weasyprint` (pure Python, no external binary dep) for HTML→PDF conversion
- **Certificate security**: AES-256, per-case key derivation from `SECRET_KEY` env var + case_id as salt; no cert bytes in logs or API responses; auto-purged on `FORM_APPROVED`
- **Not in scope**: actual portal submission for online (the user decides after reviewing); multi-applicant batch; certificate renewal; appeal flow extension (reuses Phase 8 as-is)
- **Existing phases untouched**: Phases 0–8 smoke tests must still pass unchanged after new code lands

---