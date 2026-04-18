# F04 Eligibility and Legal Grounding (GraphRAG) - Implementation Plan

## Objective
Deliver Eligibility and Legal Grounding (GraphRAG) for Phase 2 with testable milestones.

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
- Expose endpoints/interfaces: /reasoning /eligibility

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
- Implementation should be sequenced with state anchor ELIGIBILITY_ASSESSMENT_READY in mind.
- Exposed interfaces must align with: /reasoning /eligibility.
- Tag all test cases and tasks with feature ID F04.

## Work Breakdown
1. Implement requirement-level scoring with confidence and status classes.
2. Attach citation references for each recommendation and risk.
3. Generate missing evidence recommendations per unsatisfied requirement.
4. Implement multi-procedure compare API and ranking output.
5. Add tests: missing citation rejection and conflicting requirement evidence.
