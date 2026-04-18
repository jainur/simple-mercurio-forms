# Phase 2 Frontend API Contract Specification

## Standards
1. Base path: /v1
2. Auth: Bearer JWT
3. Content type: application/json
4. Idempotency header required for mutating requests: Idempotency-Key
5. Correlation header: X-Request-ID (optional client-supplied, echoed in response)
6. Tenant context header for service/admin tooling: X-Tenant-ID (required only for privileged contexts)
7. Standard envelope:
{
  "request_id": "string",
  "api_version": "v1",
  "data": {},
  "error": null
}

## Status Code Conventions
1. 200 OK: successful read and successful idempotent update replay
2. 201 Created: successful resource creation
3. 202 Accepted: asynchronous workflow-triggering command accepted
4. 400 Bad Request: schema or validation failure
5. 401 Unauthorized: missing or invalid token
6. 403 Forbidden: role or state guard denial
7. 404 Not Found: unknown or inaccessible resource in current tenant scope
8. 409 Conflict: unresolved state or sync conflict
9. 422 Unprocessable Entity: domain-level validation failure
10. 429 Too Many Requests: rate-limit threshold exceeded

## Pagination, Filtering, and Sorting
1. Pagination query params: page (1-based), page_size (default 25, max 100)
2. List response shape:
{
  "items": [],
  "total": 0,
  "page": 1,
  "page_size": 25,
  "has_next": false
}
3. Sorting query params: sort_by and sort_dir (asc or desc)
4. Date range filtering: from and to ISO-8601 timestamps

## API Groups

## A01 Cases and Overview
GET /v1/cases
- Query: q, state, assignee, procedure_id, page, page_size
- Response data: items[], total, page, page_size

POST /v1/cases
Request:
{
  "external_matter_id": "string",
  "procedure_id": "string|null",
  "priority": "normal|high|urgent"
}
Response data: case summary object

GET /v1/cases/{case_id}/overview
Response data: next_action, blockers[], stage, risk_flags[], deadlines[]

### Example: POST /v1/cases
Request
{
  "external_matter_id": "MC-2026-000981",
  "procedure_id": "ex-01",
  "priority": "high"
}

Response
{
  "request_id": "req_8f1f4ab1",
  "api_version": "v1",
  "data": {
    "case_id": "case_01J2X4F7X7X",
    "external_matter_id": "MC-2026-000981",
    "procedure_id": "ex-01",
    "state": "CASE_CREATED",
    "priority": "high",
    "opened_at": "2026-04-12T08:21:02Z"
  },
  "error": null
}

## A02 Intake and Documents
POST /v1/cases/{case_id}/intake/submissions
Request: intake answers and declarations payload
Response: intake status and completeness score

POST /v1/cases/{case_id}/documents
Request: metadata + upload token or multipart reference
Response: artifact_id, processing_status

GET /v1/cases/{case_id}/documents
Response: checklist[], artifacts[], unresolved_requirements[]

POST /v1/cases/{case_id}/document-requests
Request: missing_items[], due_date, message_template_id
Response: request_id, status

### Example: POST /v1/cases/{case_id}/intake/submissions
Request
{
  "intake_version": "v2",
  "answers": [
    {"question_id": "q_full_name", "value": "Ana Lopez"},
    {"question_id": "q_passport_number", "value": "P1234567"},
    {"question_id": "q_country_of_birth", "value": "AR"}
  ],
  "declarations": {
    "data_accuracy_confirmed": true,
    "consent_to_processing": true
  }
}

Response
{
  "request_id": "req_0268ad",
  "api_version": "v1",
  "data": {
    "case_id": "case_01J2X4F7X7X",
    "intake_status": "submitted",
    "completeness_score": 0.82,
    "missing_sections": ["employment_history"],
    "next_action": "assistant_review"
  },
  "error": null
}

## A03 Data Review and Extractions
GET /v1/cases/{case_id}/extractions
Response: extraction reviews with source and confidence

PATCH /v1/cases/{case_id}/extractions/{artifact_id}
Request:
{
  "field_updates": [
    {"field_key": "passport_number", "new_value": "X12345"}
  ],
  "comment": "corrected from source image"
}
Response: updated extraction review

POST /v1/cases/{case_id}/extractions/approve
Request: {"approval_note": "string"}
Response: gate status and next_state

### Example: GET /v1/cases/{case_id}/extractions
Response
{
  "request_id": "req_ef32a1",
  "api_version": "v1",
  "data": {
    "items": [
      {
        "artifact_id": "art_01J2YQ",
        "document_type": "passport",
        "status": "partially_corrected",
        "fields": [
          {
            "field_key": "passport_number",
            "value": "P1234567",
            "source": "ocr",
            "confidence": 0.93,
            "corrected": false
          },
          {
            "field_key": "expiry_date",
            "value": "2031-01-10",
            "source": "manual",
            "confidence": 1.0,
            "corrected": true
          }
        ]
      }
    ]
  },
  "error": null
}

## A04 Eligibility and Requirements
GET /v1/cases/{case_id}/procedure/requirements
Response: required_documents[], prerequisites[], fees[], deadlines[], channels[]

POST /v1/cases/{case_id}/eligibility/runs
Request: {"procedure_ids": ["ex-01", "ex-10"]}
Response: assessment_id, ranked_options[]

GET /v1/cases/{case_id}/eligibility/{assessment_id}
Response: matrix rows with citations and gaps

### Example: GET /v1/cases/{case_id}/procedure/requirements
Response
{
  "request_id": "req_9c23bb",
  "api_version": "v1",
  "data": {
    "procedure_id": "ex-01",
    "required_documents": [
      {"code": "doc_passport", "name": "Passport", "mandatory": true}
    ],
    "prerequisites": [
      {"code": "pre_income", "description": "Proof of sufficient funds"}
    ],
    "fees": [{"code": "fee_790", "amount": 16.08, "currency": "EUR"}],
    "deadlines": [{"code": "dl_submission", "days_from_start": 30}],
    "channels": ["online", "office"]
  },
  "error": null
}

## A05 Forms and Review
POST /v1/cases/{case_id}/forms/generate
Request: {"submission_mode": "offline|online"}
Response: form_id, status

GET /v1/cases/{case_id}/forms
GET /v1/cases/{case_id}/forms/{form_id}

PATCH /v1/cases/{case_id}/forms/{form_id}
Request: field updates and rationale
Response: updated artifact and unresolved count

POST /v1/cases/{case_id}/forms/{form_id}/approve
POST /v1/cases/{case_id}/forms/{form_id}/submit-decision
Request: {"decision": "submit|decline", "rationale": "string"}
Response: next_state and submission intent summary

### Example: POST /v1/cases/{case_id}/forms/generate
Request
{
  "submission_mode": "online"
}

Response
{
  "request_id": "req_e9bb44",
  "api_version": "v1",
  "data": {
    "form_id": "form_01J2Z7",
    "status": "generating",
    "unresolved_fields": 0,
    "next_state": "FORM_FILLING_IN_PROGRESS"
  },
  "error": null
}

### Example: POST /v1/cases/{case_id}/forms/{form_id}/submit-decision
Request
{
  "decision": "submit",
  "rationale": "All discrepancies resolved and client declarations complete"
}

Response
{
  "request_id": "req_701cbd",
  "api_version": "v1",
  "data": {
    "case_id": "case_01J2X4F7X7X",
    "form_id": "form_01J2Z7",
    "decision": "submit",
    "next_state": "SUBMITTED_WAITING_RECEIPT"
  },
  "error": null
}

## A06 Filing and Monitoring
POST /v1/cases/{case_id}/certificate
Request: multipart certificate payload metadata
Response: certificate_status

GET /v1/cases/{case_id}/filing/status
Response: readiness, submission_state, receipt_refs[]

GET /v1/cases/{case_id}/timeline
Response: unified event stream entries

### Example: GET /v1/cases/{case_id}/filing/status
Response
{
  "request_id": "req_3048aa",
  "api_version": "v1",
  "data": {
    "readiness": "ready",
    "submission_state": "SUBMITTED_WAITING_RECEIPT",
    "certificate_status": "purged",
    "receipt_refs": [
      {"receipt_id": "rcp_01", "captured_at": "2026-04-12T10:17:45Z"}
    ]
  },
  "error": null
}

## A07 Sync and Integrations
GET /v1/cases/{case_id}/external-record
Response: source fields, last sync, conflict count

GET /v1/cases/{case_id}/sync-log
POST /v1/cases/{case_id}/sync/retry
POST /v1/cases/{case_id}/sync/conflicts/{conflict_id}/resolve
Request: {"strategy": "use_local|use_external|merge", "merged_value": "optional"}

### Example: POST /v1/cases/{case_id}/sync/conflicts/{conflict_id}/resolve
Request
{
  "strategy": "merge",
  "merged_value": "Calle Gran Via 10, Madrid"
}

Response
{
  "request_id": "req_b4ab22",
  "api_version": "v1",
  "data": {
    "conflict_id": "cnf_1002",
    "status": "resolved",
    "resolution": "merge",
    "publish_back_queued": true
  },
  "error": null
}

## A08 Admin and Governance
GET /v1/admin/connectors
PATCH /v1/admin/connectors/{connector_id}
GET /v1/admin/templates
POST /v1/admin/templates
GET /v1/admin/security/roles
PATCH /v1/admin/security/users/{user_id}/roles

## Error Model
Example error envelope:
{
  "request_id": "req_123",
  "api_version": "v1",
  "data": null,
  "error": {
    "code": "CONFLICT_UNRESOLVED",
    "message": "Field conflict must be resolved before publish-back",
    "details": {"field_key": "client_address"}
  }
}

## Common Error Codes
1. VALIDATION_ERROR
2. UNAUTHORIZED
3. FORBIDDEN_ROLE
4. FORBIDDEN_STATE
5. NOT_FOUND
6. CONFLICT_UNRESOLVED
7. IDEMPOTENCY_KEY_REPLAY
8. RATE_LIMITED
9. EXTERNAL_CONNECTOR_FAILURE
10. WORKFLOW_BLOCKED_MANUAL_INTERVENTION
