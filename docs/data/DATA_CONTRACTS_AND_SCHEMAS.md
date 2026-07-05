# Data Contracts and Schemas

Purpose: define data-contract expectations before implementation.
Scope: provider payloads, normalized market data, features, datasets, signals, orders, fills, positions, balances, and audit events.
Audience: data engineers, backend engineers, ML engineers, and QA.
Assumptions: schema evolution is unavoidable and must be versioned.
Dependencies: [Data Architecture](DATA_ARCHITECTURE.md), [Quality Gates](../engineering/QUALITY_GATES.md).
Unresolved decisions: contract format, registry location, and schema compatibility tooling.

## Contract Requirements

Every contract MUST include:

- Stable contract ID and semantic version.
- Owner and approval status.
- Field names, types, units, precision, nullability, and allowed values.
- Timestamp semantics and timezone.
- Provider/source mapping.
- Validation rules and quarantine behavior.
- Backward/forward compatibility notes.
- Example valid and invalid records as fixtures.

## Core Contracts

| Contract ID | Entity | Required checks |
| --- | --- | --- |
| DC-001 | Instrument | Symbol mapping, venue, status, precision, lot size, min order size. |
| DC-002 | Candle | OHLCV types, monotonic time, non-negative volume, valid high/low/open/close relationships. |
| DC-003 | Tick/trade | Trade ID, price, quantity, provider time, ordering, duplicate handling. |
| DC-004 | Order book | Sequence, bid/ask ordering, spread, depth, timestamp. |
| DC-005 | Feature vector | Feature version, source data versions, freshness, leakage guard. |
| DC-006 | Signal | Strategy/model IDs, confidence, expiry, input references, action. |
| DC-007 | Order | Idempotency key, side, quantity, price, order type, risk decision. |
| DC-008 | Fill | Provider fill ID, order ID, quantity, price, fee, liquidity flag where available. |
| DC-009 | Balance/position | Instrument, quantity, valuation time, source, reconciliation status. |
| DC-010 | Audit event | Actor, action, target, time, outcome, reason, correlation ID. |

## Compatibility Policy

Breaking schema changes MUST require migration notes, replay impact analysis, and approval from affected component owners.
