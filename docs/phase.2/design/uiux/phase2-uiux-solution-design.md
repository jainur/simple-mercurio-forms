# Phase 2 UI UX Solution Design

## Design Model
Use a two-level navigation model:
1. Product-level sidebar for cross-matter functions.
2. Matter-level tabs for in-case execution.

## Global Navigation
- Dashboard
- Linked Matters
- Intake
- Documents
- Data Review
- Forms
- Review
- Filing
- Timeline
- Sync Center
- Templates
- Admin

## Matter Header Standard
Every matter page includes:
1. External PMS badge and matter ID.
2. Stage rail with current and next states.
3. Sync health chip and last sync timestamp.
4. Primary next action button and blocker summary.

## Global Interaction Patterns
1. Right-side context panel for blockers, sync status, and next actions.
2. Status chips with consistent semantics: approved, waiting, blocked, needs review.
3. Source badges for editable fields: PMS, Intake, OCR, Manual.
4. Review gates use explicit decision dialogs with rationale capture.

## Shared Screen States
1. Loading skeletons for list and detail views.
2. Empty states with action-oriented recovery paths.
3. Conflict states with compare-and-choose controls.
4. Failure states with retry, diagnostics, and escalation options.

## UX Telemetry Design
Track events for:
1. Task completion time per feature.
2. Correction frequency and rejection rates.
3. Sync issue detection and resolution time.
4. Lawyer approval cycle time.
