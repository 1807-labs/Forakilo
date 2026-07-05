# Order Execution and Reconciliation

Purpose: define safe order execution and reconciliation behavior.
Scope: paper, sandbox, and future live order flows.
Audience: trading engineers, backend engineers, QA, risk reviewers, and operators.
Assumptions: paper trading is the only initially available execution mode.
Dependencies: [Trading Domain](TRADING_DOMAIN_SPECIFICATION.md), [Failure Modes](FAILURE_MODES_AND_EDGE_CASES.md).
Unresolved decisions: provider-specific order types and reconciliation endpoints.

## Execution Flow

1. Signal is active and unexpired.
2. Order plan is created with idempotency key.
3. Risk engine approves or rejects.
4. Provider adapter validates precision, size, order type, account state, and rate limits.
5. Paper/sandbox/live adapter submits or simulates order.
6. Provider/paper response is persisted.
7. Reconciliation compares expected order, fill, balance, and position state.
8. Audit and observability events are emitted.

## Reconciliation Requirements

- Reconcile orders, fills, cancelled orders, rejected orders, fees, balances, positions, margin, and realized/unrealized P&L.
- Treat provider state as authoritative for live accounts but verify against local expectations.
- Block new execution when reconciliation mismatch exceeds policy.
- Preserve idempotency and duplicate-submission evidence.

## Unknown Order Outcome

If a timeout occurs after an order may have been accepted, Forakilo MUST query provider state using idempotency/client order ID and block duplicate submissions until outcome is resolved.
