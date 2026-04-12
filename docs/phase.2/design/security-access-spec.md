# Phase 2 Security and Access Specification

## Roles
1. Assistant
- Manage intake, documents, data review, and form preparation

2. Lawyer
- Review legal risks and approve or return decisions

3. Client
- Complete intake, upload documents, respond to clarifications

4. Admin/Ops
- Manage connectors, templates, mappings, and user permissions

## Permission Model
1. Resource-action model
- case.read, case.update, extraction.approve, form.approve, filing.decide, sync.resolve, admin.manage

2. Guard conditions
- Some actions require both role permission and workflow state eligibility
- Critical actions require confirmation and rationale capture

## Role Permission Matrix

| Permission | Assistant | Lawyer | Client | Admin/Ops |
|---|---|---|---|---|
| case.read | allow | allow | scoped-self | allow |
| case.update | allow | limited | none | allow |
| intake.submit | assist-proxy | none | allow-scoped | allow |
| document.upload | allow | limited | allow-scoped | allow |
| extraction.review | allow | read-only | none | allow |
| extraction.approve | allow | allow | none | allow |
| eligibility.view | allow | allow | limited-summary | allow |
| form.edit | allow | limited | none | allow |
| form.approve | propose | allow | none | allow |
| filing.decide | none | allow | none | allow |
| certificate.upload | allow | allow | none | allow |
| sync.view | allow | allow | none | allow |
| sync.resolve | propose | approve | none | allow |
| admin.manage | none | none | none | allow |

Notes
1. scoped-self means client is limited to their own intake/document resources.
2. limited means read-heavy access with controlled write surfaces.
3. propose means action requires downstream lawyer or admin approval.

## Workflow State Guard Matrix

| Action | Allowed States | Guard Result if Invalid |
|---|---|---|
| extraction.approve | EXTRACTION_REVIEW_PENDING | FORBIDDEN_STATE |
| form.edit | FORM_REVIEW_PENDING, FORM_FILLING_IN_PROGRESS | FORBIDDEN_STATE |
| form.approve | FORM_REVIEW_PENDING | FORBIDDEN_STATE |
| filing.decide | FORM_APPROVED | FORBIDDEN_STATE |
| certificate.upload | AWAITING_DIGITAL_CERTIFICATE, FORM_APPROVED | FORBIDDEN_STATE |
| sync.conflict.resolve | any non-closed state | FORBIDDEN_STATE |
| case.withdraw | any non-closed state | FORBIDDEN_STATE |

## Authorization Decision Flow
1. Validate token and signature.
2. Resolve tenant and workspace scope.
3. Check role permission against resource-action.
4. Check workflow-state guard for mutating action.
5. Check ownership guard for client-scoped resources.
6. Emit authorization audit event.

## Authentication and Session
1. OIDC login and JWT access token
2. Token includes tenant_id, workspace scopes, roles
3. Session timeout and refresh token rotation policies

## Authorization Checks
1. API gateway checks token validity and tenant scoping
2. Endpoint authorization middleware enforces resource-action permissions
3. Domain layer checks workflow-state guards for mutation commands

## User Management
1. Admin-managed invites and role assignment
2. Optional SSO group mapping to roles
3. Role recertification cadence and dormant account controls

## User Lifecycle
1. Provisioning
- Invite, accept, verify identity, assign role and workspace scope.

2. Active management
- Role changes are versioned and audited.
- Privileged role grants require second approver policy.

3. Suspension and deactivation
- Immediate token revocation on suspension.
- Deactivated users remain in audit trails with immutable actor references.

4. Offboarding
- Remove active assignments and rotate integration secrets if required.
- Trigger access review for impacted workflows and approvals.

## Sensitive Data Controls
1. Encryption for PII and certificate references
2. Secrets manager for connector credentials
3. PII redaction in logs and support tooling

## Data Classification
1. Public operational metadata: low sensitivity
2. Internal workflow metadata: medium sensitivity
3. PII and legal evidence data: high sensitivity
4. Secrets and private key material: critical sensitivity

## Session and Token Policies
1. Access token TTL: short-lived
2. Refresh token rotation with revocation list
3. Device/session listing and remote logout for privileged users
4. Step-up authentication for irreversible actions (submission decision, admin policy changes)

## Audit Controls
1. Approval actions must include actor, rationale, timestamp
2. Sync conflict resolutions must include selected strategy and evidence
3. Security policy changes must create immutable audit entries

## Security Events and Alerts
1. Repeated authorization failures per actor or IP range
2. Abnormal connector error burst and replay loops
3. Privilege escalation and role-change anomalies
4. Suspicious automation behavior during filing workflows

## Minimum Security Test Suite
1. Tenant isolation tests for read and write paths.
2. Permission matrix enforcement tests for all roles.
3. Workflow-state guard tests for protected actions.
4. Token expiry and refresh misuse tests.
5. Audit completeness tests for critical operations.
