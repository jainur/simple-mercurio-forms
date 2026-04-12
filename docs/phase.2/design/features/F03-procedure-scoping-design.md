# F03 Procedure Scoping - Detailed Design

## Design Goals
- Implement Allow procedure override and retrieve scoped requirements from graph with deterministic contracts and auditable behavior.
- Minimize coupling with adjacent features.
- Keep interfaces stable for iterative delivery.

## Components
1. API/interface boundary for /cases /procedure/requirements
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
- Primary state context: PROCEDURE_CANDIDATES_READY
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
- Primary interfaces: /cases /procedure/requirements
- State anchor: PROCEDURE_CANDIDATES_READY
- Ensure contracts are traceable to requirements ID F03.

## Concrete Design
- Components: procedure resolver, requirements query service, fallback candidate inferencer.
- Data entities: case.procedure_id, procedure_version_snapshot.
- API contracts: case create optional procedure_id, requirements retrieval endpoint.
- State impact: procedure scope influences downstream eligibility and form template selection.
