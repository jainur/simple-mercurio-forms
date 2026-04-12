# Phase 2 UI UX Requirements Overview

## Purpose
Define detailed user interface and user journey requirements for Phase 2 in an integration-first operating model.

## Product UX Principles
1. PMS remains system of record and must be visible in the UI.
2. Immigration workspace is system of workflow and must be task-first.
3. Users must always see provenance of critical fields: PMS, intake, OCR, or manual edit.
4. Lawyer approval gates must be explicit and irreversible actions must be clearly separated.
5. Sync trust must be first-class: status, conflicts, retries, and audit context are visible.

## Persona Coverage
- Assistant: primary operator for intake, docs, exceptions, and packet readiness.
- Lawyer: focused reviewer for legal risk, unresolved conflicts, and sign-off.
- Client: guided intake, uploads, clarification responses, and progress view.
- Admin/Ops: integration setup, mappings, template governance, and team controls.

## Global UI Functional Requirements
1. UI must provide a linked-matter-first journey, not local matter creation as default.
2. UI must expose both product-level navigation and matter-level navigation.
3. UI must present stage progression and next action for every matter.
4. UI must present sync health and unresolved conflicts at matter and global levels.
5. UI must support exception-driven workflows to reduce manual repetition.

## Global UX Quality Requirements
1. Accessibility: WCAG AA contrast, keyboard navigation, semantic labeling, and focus states.
2. Responsiveness: desktop-first for staff and mobile-safe for client intake.
3. Performance: key screens must load summary state quickly with progressive detail rendering.
4. Consistency: shared status language across dashboard, matter pages, and timeline.
5. Explainability: every critical decision surface includes source and rationale context.

## Feature Set
- U01 to U12 in ./features

## Master Acceptance Criteria
1. End-to-end assistant journey from linked matter to lawyer review is executable in UI.
2. Client journey from invite to upload and clarification loop is executable in UI.
3. Lawyer journey from exception-focused review to approval/return is executable in UI.
4. Sync issues can be identified, triaged, retried, and audited through UI surfaces.
