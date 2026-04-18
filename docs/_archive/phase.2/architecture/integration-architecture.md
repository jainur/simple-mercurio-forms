# Phase 2 Integration Architecture

## Objective
Define how the application integrates with external systems while keeping external PMS as system of record and this app as workflow system.

## Integration Domains
1. PMS connectors
- MyCase connector baseline
- Adapter model for additional PMS providers

2. Filing and legal ops channels
- OpenClaw connector for workflow/event interoperability
- Email/SMS notification channels for client and staff communication

3. Government portal interaction
- Browser automation through Playwright
- Local certificate constrained execution path

## Integration Patterns
1. Event ingress
- Webhook receivers with signature verification
- Polling workers for systems without push support

2. Event egress
- Publish-back queue for status, notes, documents, and milestones
- Retry with backoff and dead-letter handling

3. Data synchronization
- Field-level mapping catalog
- Conflict detection and resolution ledger
- Provenance stamp on all synchronized fields

## Reliability Design
1. Idempotency keys for mutating external writes
2. Replay-safe inbound event dedupe by source event ID
3. Circuit breaker and fallback channel strategy
4. Observability: connector latency, failure rate, retry depth

## Integration Security
1. Connector credentials stored in secrets manager
2. Scoped API tokens by tenant and connector
3. Signed webhook payloads and timestamp drift validation
4. Full audit trail for sync and conflict decisions
