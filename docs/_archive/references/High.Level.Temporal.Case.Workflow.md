# Temporal Case Workflow

Date: 2026-04-01

## 1. Purpose

Define the durable workflow model for immigration case handling using Temporal-style workflow states, transitions, timers, retries, and human approvals.

## 2. Workflow Model

Use one parent workflow per case:

- CaseLifecycleWorkflow

Use child workflows where needed:

- IntakeAndDiscoveryWorkflow
- DocumentCollectionWorkflow
- SubmissionWorkflow
- MonitoringWorkflow

Use activities for external side effects:

- Graph retrieval
- LLM reasoning
- Email or messaging send
- Browser automation
- Status checks
- Document extraction

## 3. State Machine

## 3.1 States

1. CASE_CREATED
2. INTAKE_IN_PROGRESS
3. PROCEDURE_CANDIDATES_READY
4. ELIGIBILITY_ASSESSMENT_READY
5. WAITING_FOR_CLIENT_INFO
6. DOCUMENT_PLAN_READY
7. DOCUMENT_COLLECTION_IN_PROGRESS
8. READINESS_REVIEW_PENDING
9. READY_FOR_SUBMISSION
10. SUBMISSION_IN_PROGRESS
11. SUBMITTED_WAITING_RECEIPT
12. SUBMISSION_CONFIRMED
13. MONITORING_ACTIVE
14. RESOLUTION_RECEIVED
15. APPEAL_EVALUATION_PENDING
16. CLOSED_APPROVED
17. CLOSED_REJECTED
18. CLOSED_WITHDRAWN
19. BLOCKED_MANUAL_INTERVENTION

## 3.2 Transition Triggers

- Client message received
- Document uploaded
- Operator approval received
- Operator rejection received
- Automation completed
- Automation failed
- Deadline approaching
- Resolution notification received
- Appeal window started
- Timeout reached

## 4. Transition Table

| From State | Trigger | To State | Notes |
|---|---|---|---|
| CASE_CREATED | workflow_start | INTAKE_IN_PROGRESS | Initialize case context |
| INTAKE_IN_PROGRESS | intake_complete | PROCEDURE_CANDIDATES_READY | Run discovery worker |
| PROCEDURE_CANDIDATES_READY | eligibility_run_complete | ELIGIBILITY_ASSESSMENT_READY | Build eligibility matrix |
| ELIGIBILITY_ASSESSMENT_READY | missing_info_detected | WAITING_FOR_CLIENT_INFO | Send targeted request |
| WAITING_FOR_CLIENT_INFO | client_info_received | INTAKE_IN_PROGRESS | Re-run intake normalization |
| ELIGIBILITY_ASSESSMENT_READY | eligibility_sufficient | DOCUMENT_PLAN_READY | Build requirement to evidence plan |
| DOCUMENT_PLAN_READY | collection_started | DOCUMENT_COLLECTION_IN_PROGRESS | Open document tasks |
| DOCUMENT_COLLECTION_IN_PROGRESS | required_docs_covered | READINESS_REVIEW_PENDING | Compile readiness packet |
| READINESS_REVIEW_PENDING | operator_approved | READY_FOR_SUBMISSION | Lock approved package |
| READINESS_REVIEW_PENDING | operator_rejected | DOCUMENT_COLLECTION_IN_PROGRESS | Return with review comments |
| READY_FOR_SUBMISSION | submission_started | SUBMISSION_IN_PROGRESS | Start execution workflow |
| SUBMISSION_IN_PROGRESS | submit_action_complete | SUBMITTED_WAITING_RECEIPT | Await receipt artifacts |
| SUBMITTED_WAITING_RECEIPT | receipt_captured | SUBMISSION_CONFIRMED | Persist receipt and references |
| SUBMISSION_CONFIRMED | monitoring_start | MONITORING_ACTIVE | Schedule reminders and checks |
| MONITORING_ACTIVE | resolution_received | RESOLUTION_RECEIVED | Parse resolution outcome |
| RESOLUTION_RECEIVED | approved_outcome | CLOSED_APPROVED | Close with outcome |
| RESOLUTION_RECEIVED | rejected_outcome | APPEAL_EVALUATION_PENDING | Prepare appeal options |
| APPEAL_EVALUATION_PENDING | no_appeal | CLOSED_REJECTED | Close rejected |
| APPEAL_EVALUATION_PENDING | appeal_submitted | MONITORING_ACTIVE | Continue monitoring appeal |
| Any active state | manual_blocker_detected | BLOCKED_MANUAL_INTERVENTION | Escalation queue |
| BLOCKED_MANUAL_INTERVENTION | blocker_resolved | previous_state | Resume suspended execution |
| Any non-closed state | withdrawal_requested | CLOSED_WITHDRAWN | Archive case |

## 5. Workflow Signals and Queries

## 5.1 Signals

- SignalClientMessage
- SignalDocumentUploaded
- SignalOperatorApproval
- SignalOperatorRejection
- SignalPortalResult
- SignalManualBlocker
- SignalResolutionEvent
- SignalWithdrawal

## 5.2 Queries

- GetCurrentState
- GetOpenTasks
- GetPendingApprovals
- GetReadinessScore
- GetUpcomingDeadlines
- GetAuditTrailSummary

## 6. Timers and SLA Policies

1. Intake follow-up timer: 24h after missing info request.
2. Document reminder timer: configurable per requirement priority.
3. Submission receipt timeout: 15 to 60 minutes based on channel.
4. Monitoring status check interval: configurable by procedure type.
5. Appeal window timer: based on detected resolution date and rule.

Timer expiration behavior:

- Generate reminder event.
- Increment escalation counter.
- Route to operator queue after threshold.

## 7. Retry and Idempotency Rules

1. Activities must be idempotent by case_id plus command_id.
2. External side effects require dedupe keys.
3. Use exponential backoff retries for transient failures.
4. On non-retryable errors, transition to BLOCKED_MANUAL_INTERVENTION.
5. Persist run artifacts on every attempt for auditability.

## 8. Human Gate Policy

Required approvals:

1. Before submission start.
2. Before resubmission after rejection or deficiency response.
3. Before appeal filing.

Approval payload must include:

- approver_id
- approval_timestamp
- approved_submission_plan_version
- comments

## 9. Temporal Workflow Pseudocode

```text
CaseLifecycleWorkflow(case_id):
  state = CASE_CREATED
  while state not in CLOSED_*:
    switch state:
      CASE_CREATED:
        state = INTAKE_IN_PROGRESS

      INTAKE_IN_PROGRESS:
        run IntakeAndDiscoveryWorkflow
        state = PROCEDURE_CANDIDATES_READY

      PROCEDURE_CANDIDATES_READY:
        run EligibilityAssessmentActivity
        if missing_info:
          emit request_missing_info
          state = WAITING_FOR_CLIENT_INFO
        else:
          state = DOCUMENT_PLAN_READY

      WAITING_FOR_CLIENT_INFO:
        await SignalClientMessage or timeout
        if timeout threshold exceeded:
          escalate
        else:
          state = INTAKE_IN_PROGRESS

      DOCUMENT_PLAN_READY:
        run BuildDocumentPlanActivity
        state = DOCUMENT_COLLECTION_IN_PROGRESS

      DOCUMENT_COLLECTION_IN_PROGRESS:
        await SignalDocumentUploaded and run DocumentValidationActivity
        if all_mandatory_covered:
          state = READINESS_REVIEW_PENDING

      READINESS_REVIEW_PENDING:
        await SignalOperatorApproval or SignalOperatorRejection
        if approved:
          state = READY_FOR_SUBMISSION
        else:
          state = DOCUMENT_COLLECTION_IN_PROGRESS

      READY_FOR_SUBMISSION:
        run SubmissionWorkflow
        state = SUBMISSION_CONFIRMED

      SUBMISSION_CONFIRMED:
        run MonitoringWorkflow
        state = MONITORING_ACTIVE

      MONITORING_ACTIVE:
        await SignalResolutionEvent or timer
        if resolution_approved:
          state = CLOSED_APPROVED
        elif resolution_rejected:
          state = APPEAL_EVALUATION_PENDING

      APPEAL_EVALUATION_PENDING:
        await operator_decision
        if appeal_filed:
          state = MONITORING_ACTIVE
        else:
          state = CLOSED_REJECTED
```

## 10. Suggested Workflow IDs and Versioning

- Workflow ID: case-{case_id}
- Workflow type versioning: CaseLifecycleWorkflow.v1
- Child workflow versioning: IntakeAndDiscoveryWorkflow.v1, SubmissionWorkflow.v1

Versioning rules:

1. Additive changes can stay in same major version.
2. Breaking transition changes require a new workflow major version.
3. Existing in-flight workflows continue on old version until completion.

## 11. Testing Focus Areas

1. State transition correctness.
2. Signal handling correctness under out-of-order events.
3. Timer and escalation behavior.
4. Retry and idempotency behavior.
5. Human approval gate enforcement.
6. Recovery after worker restart.
