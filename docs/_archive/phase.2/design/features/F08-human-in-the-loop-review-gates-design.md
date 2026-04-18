# F08 Human-in-the-Loop Review Gates - Detailed Design

## Design Goals
- Implement Support extraction review, form review, and submission decision approvals with deterministic contracts and auditable behavior.
- Minimize coupling with adjacent features.
- Keep interfaces stable for iterative delivery.

## Components
1. API/interface boundary for /extractions /forms/{id}/approve /submit-decision
2. Domain service for feature orchestration
3. Persistence updates for feature artifacts and status
4. Signal/event integration with workflow runtime

## Data Model Design
1. Feature records linked to case_id and tenant_id.
2. Status model aligned with workflow state transitions.
3. Audit fields required for approvals and external side effects.

## API and Contract Design
1. Request and response schemas must be versioned and explicit.
2. Validation must reject malformed payloads with actionable errors.
3. Idempotency keys required for mutating operations.

## Workflow and State Design
- Primary state context: FORM_REVIEW_PENDING
- Entry conditions and exit conditions must be explicit.
- Failure transitions route to safe retry or manual intervention paths.

## Failure and Recovery Design
1. Retry transient errors with backoff.
2. Mark non-retryable failures with blocker state and operator task.
3. Preserve partial outputs for diagnosis and resumption.

## Security Design
1. RBAC and tenant scoping checks at endpoint and repository layers.
2. Encrypt sensitive fields and secrets.
3. Exclude secret material from logs and API payloads.

## Test Design
1. Unit tests for business rules and validation.
2. Integration tests for API and persistence contracts.
3. Workflow tests for state progression and failure paths.

## Feature-Specific Design Notes
- Primary interfaces: /extractions /forms/{id}/approve /submit-decision
- State anchor: FORM_REVIEW_PENDING
- Ensure contracts are traceable to requirements ID F08.

## Concrete Design
- Components: extraction review controller, form review controller, submit decision controller.
- Data entities: review decision logs, correction history, approver metadata.
- API contracts: approve/correct endpoints for extraction and forms, submit decision endpoint.
- State impact: enforced transitions through review gates before irreversible actions.
