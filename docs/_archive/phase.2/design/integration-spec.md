# Phase 2 Integration Specification

## Connectors

## I01 PMS Connector (MyCase baseline)
Capabilities
1. Inbound matter and contact sync
2. Outbound status, notes, deadlines, and document publish-back
3. Field mapping for standard and custom fields

Contract
1. Inbound: webhook and polling modes
2. Outbound: queued publish API calls with retry and dedupe
3. Sync visibility: case-level sync health and history

## I02 OpenClaw Connector
Capabilities
1. Case workflow event exchange
2. Task and milestone interoperability
3. Optional document metadata synchronization

Contract
1. Event schema versioned with correlation_id
2. Ack and retry protocol for delivery guarantees
3. Conflict strategy aligned with internal conflict ledger

## I03 Notification Channels
1. Email, SMS, and in-app messages
2. Template and locale support
3. Delivery status tracking and retry

## I04 Government Portal Automation Channel
1. Submission preparation and optional submission execution
2. Receipt and status scraping
3. Evidence artifact capture (screenshots, html snapshots)

## Integration State Model
1. CONNECTED
2. DEGRADED
3. DISCONNECTED
4. RETRYING
5. CONFLICTED

## Conflict Resolution Rules
1. Critical legal fields require explicit human resolution.
2. Non-critical metadata may auto-resolve by configured precedence.
3. Every resolution creates audit and integration delivery log entries.

## Operational Controls
1. Connector health checks with latency and error rate metrics.
2. Dead-letter queues with replay controls.
3. Per-tenant connector toggles and scoped credentials.
