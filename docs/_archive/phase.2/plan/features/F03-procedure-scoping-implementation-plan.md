# F03 Procedure Scoping - Implementation Plan

## Objective
Deliver Procedure Scoping for Phase 2 with testable milestones.

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
- Expose endpoints/interfaces: /cases /procedure/requirements

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
- Implementation should be sequenced with state anchor PROCEDURE_CANDIDATES_READY in mind.
- Exposed interfaces must align with: /cases /procedure/requirements.
- Tag all test cases and tasks with feature ID F03.

## Work Breakdown
1. Add migration for procedure_id and version snapshot.
2. Implement direct graph query path for explicit procedure selection.
3. Implement fallback inference when procedure_id missing.
4. Add requirements endpoint returning documents, fees, deadlines, channels.
5. Add tests: explicit override precedence and graph query fallback behavior.
