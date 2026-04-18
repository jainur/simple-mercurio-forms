# Phase 2 Architecture Decisions

## ADR-01 Workflow Engine
Decision: Use Temporal for long-lived workflow orchestration.
Reason: Durable state, timers, retries, and explicit human wait points.

## ADR-02 Legal Grounding
Decision: Use Neo4j-driven GraphRAG for eligibility and recommendation grounding.
Reason: Requirement-level traceability and reduced hallucination risk.

## ADR-03 Certificate Strategy
Decision: Keep certificate private keys local-first with encrypted handling and purge.
Reason: Security and practical portal constraints.

## ADR-04 API Evolution
Decision: Move to versioned API modules under /v1 with tenant context and idempotency.
Reason: Safer parallel delivery and long-term maintainability.

## ADR-05 Extensibility Model
Decision: Use Protocol + registry plugin architecture.
Reason: Provider swaps without core code changes.

## ADR-06 Human Gates
Decision: Keep mandatory review points for extraction, form quality, and submission decision.
Reason: Legal risk control and explainability.
