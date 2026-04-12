# U09 Lawyer Review Console - UI UX Detailed Design

## Screen Purpose
Focus lawyer decisions on legal risks, contradictions, and sign-off actions

## Information Architecture
1. Header: title, stage, sync health, last update.
2. Main content: task-focused data area and primary workflow controls.
3. Side context: blockers, dependencies, activity hints.

## Layout and Components
1. Core components required for risk summary, source comparison, decision actions.
2. List/table cards where users need scanning and triage.
3. Detail drawers/modals for focused edits and approvals.

## User Journey Design
1. Entry points for assistant, lawyer, and admin roles.
2. Happy path steps with visible completion checkpoints.
3. Exception path steps with explicit recovery actions.

## Interaction Design
1. Primary CTA and enabling conditions.
2. Inline validation and blocking validation behavior.
3. Confirmation patterns for irreversible actions.

## Data and API Binding Design
1. Required data contracts and refresh triggers.
2. Local UI state vs server state responsibilities.
3. Error mapping from backend codes to user-facing messages.

## Accessibility Design
1. Landmark regions and semantic structure.
2. Keyboard navigation map for primary interactions.
3. Live region announcements for asynchronous updates.

## Testability Design
1. Component-level test hooks and deterministic selectors.
2. Journey-level test checkpoints and expected outcomes.
3. Visual regression checkpoints for key states.

## Screen Blueprint
1. Summary card: eligibility posture, key risks, unresolved items.
2. Contradiction table with severity and evidence links.
3. Side-by-side source comparison viewer.
4. Decision footer with rationale input and action buttons.

## State Design
1. Awaiting review state.
2. Returned-for-corrections state.
3. Approved-for-filing state.
