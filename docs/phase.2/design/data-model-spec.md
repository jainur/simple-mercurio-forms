# Phase 2 Data Model Specification

## Scope
Defines transactional, reference, and audit data needed for Phase 2 delivery.

## Entity Groups

## Transactional Data (D01-D20)
D01 Tenant
- tenant_id, name, status, plan, created_at

D02 Workspace
- workspace_id, tenant_id, name, locale, timezone

D03 User
- user_id, tenant_id, email, display_name, status

D04 RoleAssignment
- user_id, role_id, workspace_id, effective_from, effective_to

D05 Case
- case_id, tenant_id, external_matter_id, procedure_id, state, priority, opened_at

D06 ApplicantProfile
- case_id, canonical_json, completeness_score, last_reviewed_at

D07 DocumentArtifact
- artifact_id, case_id, type, source_channel, storage_uri, uploaded_at

D08 ExtractionReview
- review_id, case_id, artifact_id, extracted_fields_json, corrected_fields_json, status, approved_by

D09 EligibilityAssessment
- assessment_id, case_id, procedure_id, matrix_json, confidence_score, generated_at

D10 RequirementCoverage
- coverage_id, assessment_id, requirement_id, status, supporting_artifact_ids

D11 FormArtifact
- form_id, case_id, procedure_id, submission_mode, html_uri, pdf_uri, status

D12 FormCorrection
- correction_id, form_id, field_key, old_value, new_value, actor_id, created_at

D13 SubmissionAttempt
- attempt_id, case_id, channel, status, submission_ref, submitted_at

D14 ReceiptArtifact
- receipt_id, attempt_id, type, storage_uri, captured_at

D15 MonitoringEvent
- event_id, case_id, source, event_type, payload_json, occurred_at

D16 SyncEvent
- sync_event_id, case_id, direction, system_name, operation, status, correlation_id

D17 ConflictRecord
- conflict_id, case_id, field_key, local_value, external_value, resolution, resolved_by

D18 DigitalCertificate
- cert_id, case_id, encrypted_ref, provided_at, used_at, purged_at

D19 HitlTask
- task_id, case_id, task_type, assigned_role, status, deadline_at

D20 NotificationDelivery
- delivery_id, case_id, channel, template_id, status, sent_at

## Reference Data (R01-R12)
R01 Procedure
R02 Requirement
R03 DocumentType
R04 FormTemplate
R05 SubmissionChannel
R06 Role
R07 Permission
R08 StatusCode
R09 Country
R10 Language
R11 ConnectorType
R12 EscalationPolicy

## Audit and Event Data (E01-E08)
E01 AuditLog
- audit_id, actor_id, tenant_id, action, entity_type, entity_id, diff_json, created_at

E02 ApprovalRecord
- approval_id, case_id, gate_type, decision, rationale, actor_id, decided_at

E03 AccessLog
- access_id, actor_id, resource, operation, outcome, ip_hash, at

E04 ApiRequestLog
- request_id, route, method, actor_id, tenant_id, status_code, latency_ms

E05 IntegrationDeliveryLog
- delivery_id, connector, direction, payload_hash, retry_count, final_status

E06 SecurityEvent
- sec_event_id, category, severity, actor_or_client, evidence_json, at

E07 RetentionPurgeLog
- purge_id, subject_type, subject_id, policy_id, purged_by, purged_at

E08 WorkflowStateLog
- state_log_id, case_id, from_state, to_state, trigger, actor_id, at

## Data Governance Rules
1. All mutable business entities carry tenant_id and created/updated metadata.
2. Critical write operations must create matching AuditLog entries.
3. PII fields are encrypted or tokenized where feasible.
4. Soft-delete preferred for case-linked transactional entities unless legal purge requested.
