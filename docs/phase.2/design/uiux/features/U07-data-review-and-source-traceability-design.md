# U07 Data Review and Source Traceability - UI UX Detailed Design

## Screen Purpose
Validate canonical profile once with source trace and inconsistency handling

## Information Architecture
1. Header: title, stage, sync health, last update.
2. Main content: task-focused data area and primary workflow controls.
3. Side context: blockers, dependencies, activity hints.

## Layout and Components
1. Core components required for entity panels, source badges, inconsistency queue.
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
1. Domain tabs for canonical profile sections.
2. Field rows with value, source badge, confidence, and edit control.
3. Inconsistency side queue with jump-to-field links.
4. Save bar with section status and validation summary.

## State Design
1. High-confidence auto-populated state.
2. Low-confidence review-required state.
3. Conflict-heavy state with blocked approval.
