# U08 Forms Workspace and Completion Management - UI UX Detailed Design

## Screen Purpose
Manage route-aware forms, unresolved fields, previews, and exports

## Information Architecture
1. Header: title, stage, sync health, last update.
2. Main content: task-focused data area and primary workflow controls.
3. Side context: blockers, dependencies, activity hints.

## Layout and Components
1. Core components required for form list, field completion, preview, export.
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
1. Forms sidebar with completion counters.
2. Main panel for field groups and unresolved warnings.
3. Preview tab for official form layout representation.
4. Action bar for regenerate, export, and send-to-review actions.

## State Design
1. Generating state with progress indicators.
2. Ready state with unresolved warning count.
3. Approved state with locked fields and export evidence.
