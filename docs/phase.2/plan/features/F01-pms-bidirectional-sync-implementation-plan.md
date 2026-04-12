# F01 PMS Bidirectional Sync - Implementation Plan

## Objective
Deliver PMS Bidirectional Sync for Phase 2 with testable milestones.

## Dependencies
- Platform dependencies: F11, F09 where applicable
- Feature dependencies: upstream producers and downstream consumers

## Milestones
1. Specification lock
- Finalize request/response contracts and state impacts.

2. Data and model updates
- Add or update persistence models and migrations.

3. Service and workflow integration
- Implement domain service logic and workflow signal handling.

4. API integration
- Expose endpoints/interfaces: /cases webhooks adapters

5. Test implementation
- Add unit, integration, and end-to-end feature scenarios.

6. Hardening
- Add observability, error taxonomy, and operator runbook notes.

## Validation Checklist
1. Positive flow validated against acceptance criteria.
2. Negative flow and retry behavior validated.
3. Audit records present for critical actions.
4. Cross-feature compatibility verified.

## Definition of Done
1. Code merged with automated tests passing.
2. Feature docs updated across requirements and design.
3. Operations and support notes are complete.

## Feature-Specific Execution Notes
- Implementation should be sequenced with state anchor CASE_CREATED in mind.
- Exposed interfaces must align with: /cases webhooks adapters.
- Tag all test cases and tasks with feature ID F01.

## Work Breakdown
1. Create adapter interface and provider implementation for MyCase baseline.
2. Add webhook endpoint, signature verification, and event dedupe.
3. Implement outbound status/document push with retries and dead-letter path.
4. Add sync health endpoint and case-level last_sync metadata.
5. Add tests: duplicate webhook, provider timeout, partial push failure.
