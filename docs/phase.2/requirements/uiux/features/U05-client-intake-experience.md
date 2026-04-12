# U05 Client Intake Experience - UI UX Detailed Requirements

## Objective
Guide client through low-stress intake with progress, save resume, and consent

## Primary Users
- Assistant
- Lawyer
- Admin/Ops
- Client (where applicable)

## UX Outcomes
1. Reduce ambiguity around next action.
2. Reduce duplicate data entry.
3. Increase confidence through source and sync visibility.

## Functional Requirements
1. The screen or workflow must support: wizard, upload prompts, consent, progress.
2. UI must show state progression and actionable status labels.
3. UI must support explicit handling of exceptions and unresolved items.
4. UI must provide traceability to source data and workflow events.
5. UI must support role-appropriate actions and hide unauthorized actions.

## Interaction Requirements
1. Primary action, secondary action, and safe-cancel behavior must be explicit.
2. Loading, empty, error, and partial-data states must be designed.
3. Destructive or irreversible actions must require confirmation.

## Content and Information Requirements
1. Labels must use legal-operations terminology consistent with Phase 2 docs.
2. Helper text must explain why input is needed and what happens next.
3. Important statuses must include timestamp and actor when available.

## Accessibility and Usability Requirements
1. Keyboard-only flow must cover all core actions.
2. Focus order and focus visibility must remain logical in dialogs and side panels.
3. Screen reader labels must be present for all controls and status chips.

## Acceptance Criteria
1. User can complete primary task without leaving this feature.
2. User can identify unresolved items and next action in under 10 seconds.
3. Error state explains recovery path.
4. Audit-relevant actions are visible in timeline/log surfaces.

## Dependencies
- Backend endpoints and workflow states that supply feature data
- Shared design system components and role-based authorization

## Feature-Specific UI Requirements
1. Intake wizard must support route-aware question sets and save-resume.
2. Client must see progress, expected time, and required evidence hints.
3. Consent and declaration checkpoints must be explicit before completion.
4. Missing information requests must deep-link client to exact section.

## User Journey Requirements
1. Client completes intake in multiple sessions without losing progress.
2. Assistant sends clarification request and client resolves it from secure link.
