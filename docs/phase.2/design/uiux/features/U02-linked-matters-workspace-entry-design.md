# U02 Linked Matters Workspace Entry - UI UX Detailed Design

## Screen Purpose
Start from externally linked PMS matters and open immigration workspace

## Information Architecture
1. Header: title, stage, sync health, last update.
2. Main content: task-focused data area and primary workflow controls.
3. Side context: blockers, dependencies, activity hints.

## Layout and Components
1. Core components required for linked matter list, filters, status chips.
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
1. Header: linked matters title, connector status, create-link action.
2. Toolbar: search, filters, sort, saved views.
3. Table: external ID, client, procedure, stage, sync health, assignee.
4. Row actions: open workspace, view sync log, remap link.

## State Design
1. No linked matters empty state.
2. Connector offline warning banner.
3. Partial sync badge with field-level discrepancy count.
