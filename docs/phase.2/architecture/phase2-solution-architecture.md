# Phase 2 Solution Architecture

## Objective
Describe the target architecture for Phase 2 delivery across product, platform, data, and operations layers.

## Architecture Layers
1. Experience Layer
- Web client for client intake, assistant operations, and lawyer review.
- Local desktop agent for certificate-bound portal execution.

2. API and Integration Layer
- FastAPI gateway exposes versioned endpoints.
- PMS adapters handle webhooks, polling, schema mapping, and status pushback.

3. Workflow Layer
- Temporal orchestrates durable workflows, timers, retries, human gates, and status queries.

4. Intelligence Layer
- LangGraph supervisor and workers for extraction, eligibility, and readiness.
- Structured JSON outputs with confidence and citations.

5. Knowledge Layer
- Neo4j legal graph with hybrid retrieval support.
- Requirement-evidence relationships and citation anchors.

6. Data Layer
- Postgres for transactional operations and workflow state.
- Object storage for uploaded and generated artifacts.

7. Automation Layer
- Playwright-based submission and monitoring automation.
- Online execution coupled with certificate handling constraints.

8. Cross-Cutting Layer
- Multi-tenancy, RBAC, observability, data governance, and plugin registry.

## Core Runtime Flows
1. New case intake and procedure setup
2. Document extraction and review
3. Eligibility matrix and missing evidence strategy
4. Form generation and review
5. Online submission decision and execution
6. Monitoring, resolution processing, and outcome closure

## Architecture Decisions
1. PMS remains system of record; this platform is operational overlay.
2. Private keys remain local via desktop agent certificate strategy.
3. Workflow durability is mandatory for long-running legal cases.
4. Extensibility uses Protocol plus registry plugin pattern.

## Quality Attributes
- Security: encryption, RBAC, auditability
- Reliability: retries, idempotency, safe blocker handling
- Scalability: queue-driven execution and stateless API layer
- Maintainability: feature boundaries and typed adapter interfaces
