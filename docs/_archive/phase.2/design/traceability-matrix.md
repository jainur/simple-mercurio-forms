# Phase 2 Traceability Matrix

## Purpose
Map features to UI surfaces, APIs, data entities, integrations, capabilities, and security controls.

| Feature | UI UX Feature | API Groups | Key Data Entities | Integrations | Capabilities | Security Controls |
|---|---|---|---|---|---|---|
| F01 PMS Sync | U02 U04 U12 | A07 A08 | D05 D16 D17 E05 | I01 I02 | C06 | S-tenant-scope S-audit-sync |
| F02 Intake Canonical | U05 U07 | A02 A03 | D06 D07 D08 | I03 | C01 C03 | S-role-assistant S-pii-encryption |
| F03 Procedure Scoping | U03 U08 | A01 A04 | D05 R01 R02 | I01 | C02 C03 | S-state-guard |
| F04 Eligibility | U07 U09 | A04 | D09 D10 | I02 | C02 | S-citation-audit |
| F05 Document Intelligence | U06 U07 | A02 A03 | D07 D08 D10 | I03 | C01 C02 | S-pii-redaction |
| F06 Form Assembly | U08 | A05 | D11 D12 | I04 | C04 | S-role-state-gate |
| F07 Certificate Mgmt | U10 | A06 | D18 | I04 | C05 C07 | S-cert-encryption S-cert-purge |
| F08 HITL Gates | U07 U09 U10 | A03 A05 | E02 E08 D19 | I02 | C03 C04 | S-approval-nonrepudiation |
| F09 Workflow | U03 U11 | A01 A06 | E08 D19 | I02 I04 | C03 | S-state-authorization |
| F10 Submission Monitoring | U10 U11 | A06 | D13 D14 D15 | I04 I01 | C05 C06 | S-audit-submission |
| F11 API Multi-Tenancy | U12 | A01-A08 | D01 D02 D03 D04 | I01 I02 I03 | C06 C07 | S-tenant-scope S-rbac |
| F12 Plugin Architecture | U12 | A08 | R11 R12 E06 | I01 I02 I04 | C01-C06 | S-plugin-policy |
| F13 Observability Security | U01 U11 U12 | A08 | E01 E03 E04 E06 E07 | I01-I04 | C07 | S-monitoring S-retention |

## Security Control Key
- S-tenant-scope: enforce tenant/workspace isolation
- S-rbac: enforce role-based permissions
- S-state-guard: enforce workflow-state mutation guards
- S-pii-encryption: encrypt sensitive data at rest
- S-pii-redaction: redact sensitive values in logs
- S-cert-encryption: encrypt certificate artifacts
- S-cert-purge: secure certificate purge after use
- S-approval-nonrepudiation: immutable approval evidence
- S-audit-sync: immutable sync activity trail
- S-audit-submission: immutable submission evidence trail
- S-plugin-policy: plugin registration and execution policy checks
- S-monitoring: security observability and alerts
- S-retention: retention and purge policy enforcement
