# F08 Human-in-the-Loop Review Gates - Implementation Plan

## Objective
Deliver Human-in-the-Loop Review Gates for Phase 2 with testable milestones.

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
- Expose endpoints/interfaces: /extractions /forms/{id}/approve /submit-decision

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
- Implementation should be sequenced with state anchor FORM_REVIEW_PENDING in mind.
- Exposed interfaces must align with: /extractions /forms/{id}/approve /submit-decision.
- Tag all test cases and tasks with feature ID F08.

## Work Breakdown
1. Implement extraction review APIs and validation rules.
2. Implement form review APIs and correction history recording.
3. Implement submit decision endpoint with submit/decline branches.
4. Wire signals and transitions to enforce required human gates.
5. Add tests: unauthorized approval, decline branch, repeated approval idempotency.
