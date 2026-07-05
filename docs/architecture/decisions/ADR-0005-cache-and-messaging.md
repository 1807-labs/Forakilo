# ADR-0005: Cache and Messaging

Status: Accepted
Date: 2026-07-04

Purpose: select initial cache and message transport.
Scope: local development and MVP event transport.
Audience: backend engineers, data engineers, and operations.
Assumptions: MVP throughput is moderate; ordering and replay needs exist but Kafka-scale operations are not yet justified.
Dependencies: [Integration Architecture](../INTEGRATION_ARCHITECTURE.md), [Technology Evaluation](../../research/TECHNOLOGY_EVALUATION.md).
Unresolved decisions: exact stream retention and replay partitions need implementation tests.

## Decision

Use Valkey for cache and ephemeral coordination. Use NATS JetStream for internal event transport and replayable MVP streams.

## Rationale

Valkey preserves a permissive open-source posture. NATS is lightweight, operationally simple, and sufficient for early internal eventing.

## Consequences

- Cache MUST NOT be the sole store for orders, fills, balances, positions, credentials, or audit records.
- Event consumers MUST be idempotent.
- Kafka MAY be evaluated later if retention, throughput, connectors, or ecosystem requirements exceed NATS.

## Alternatives Rejected

- Redis 7.4+ as default: rejected due source-available licensing concerns.
- Kafka as default: rejected until volume or ecosystem requirements justify its operational cost.
