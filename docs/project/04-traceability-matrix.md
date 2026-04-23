# Traceability Matrix — abogados-cowork

Last updated: 2026-04-18  
Status: Approved

## Purpose

Provide end-to-end traceability from requirements to features, user stories, design, standards, and implementation planning artifacts.

## Matrix

| Requirement Area | Feature Coverage | User Story Coverage | Design Coverage | Standards Coverage | Implementation Coverage |
|---|---|---|---|---|---|
| FR-001 to FR-004 (case/workflow basics) | F01, F10, F14 | US-001, US-002, US-003 | 6.1, 5.1, 5.2, 6.10 | 6, 8, 11, 12 | Sprint 1, Sprint 2 gates |
| FR-010 to FR-015 (intake/doc capture) | F02, F03 | US-010, US-011, US-012 | 6.2 | 6, 7, 10 | Sprint 3 gates |
| FR-020 to FR-021b, FR-024 (extraction/provenance) | F04 | US-013, US-014 | 4.2, 6.3 | 9, 11, 12 | Sprint 3 gates |
| FR-025 to FR-030c (GraphRAG/legal validation) | F05, F06 | US-020, US-021, US-022, US-023, US-024 | 6.4 | 9, 12 | Sprint 4 gates |
| FR-031 to FR-034 (forms and EX scope) | F07 | US-030, US-031, US-032, US-032a | 4.3, 6.5 | 14, 15 | Sprint 5, Sprint 7 gates |
| FR-040 to FR-042 (approval controls) | F08, F14 | US-033, US-043 | 6.6, 6.10 | 8.3, 11.4 | Sprint 5 gates |
| FR-050 to FR-053 (submission support) | F09a, F09b | US-034, US-035, US-036 | 5.1, 6.7 | 6.4, 8.4, 11.3 | Sprint 6 gates |
| FR-060 to FR-062 (tenant/admin) | F11, F12 | US-040, US-041 | 6.8 | 6.5, 7, 11 | Sprint 1, Sprint 8 gates |
| FR-070 to FR-072 (i18n) | F13 | US-042 | 6.9 | 10.2 | Sprint 8 checks |
| FR-080 to FR-087 (extensibility/DI) | Extensibility (DI-based) (+F05/F07/F09 integration) | US-024, US-032a, US-036, US-044 | 6.11, 7.4 | 4.4, 8.5, 9.5, 15.2a | Sprint 2, Sprint 4-6 gates |
| NFR-001 to NFR-005 (security/privacy) | F12, F14, F19 | US-040, US-043, US-044 | 9 | 11, 13 | Sprint 8 gates |
| NFR-010 to NFR-012 (reliability/durability) | F10, F09a | US-034, US-036 | 5.3, 10 | 8.4, 12, 15 | Sprint 6, Sprint 8 gates |
| NFR-020 to NFR-022 (observability/audit) | F14, F18, F19 | US-043, US-103 | 11, 6.10, 6.11 | 12, 11.4 | Sprint 8 gates |
| NFR-040 to NFR-042 (deployability) | F09b, F11 | US-035, US-041 | 3.1, 6.7, 7.3 | 3, 13, 15.2 | Sprint 8 gates |
| DGR-001 to DGR-004 (data governance) | F04, F14, F11 | US-013, US-043, US-041 | 4, 7.1, 6.10 | 7.4, 11, 12 | Sprint 3, Sprint 8 gates |

## Maintenance Rule

Any new requirement, feature, or P0 user story must update this matrix before release sign-off.

**Note:** For MVP, the product is delivered as a desktop application (Tauri) only. All extensibility and alternate implementations are handled via dependency injection (DI), not plugins. The web application and runtime plugin model are deferred until after MVP.
