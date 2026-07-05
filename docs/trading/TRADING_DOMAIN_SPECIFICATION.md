# Trading Domain Specification

Purpose: define core trading domain entities and invariants.
Scope: signals, strategies, portfolios, risk, orders, fills, positions, balances, fees, and reconciliation.
Audience: trading engineers, backend engineers, QA, risk reviewers, and operators.
Assumptions: paper trading is default; live trading is unavailable until gates pass.
Dependencies: [Signal Lifecycle](SIGNAL_LIFECYCLE.md), [Risk Management Policy](RISK_MANAGEMENT_POLICY.md), [Order Execution](ORDER_EXECUTION_AND_RECONCILIATION.md).
Unresolved decisions: first venue, instruments, order types, and risk limits.

## Core Entities

- Instrument: provider, symbol, base/quote, precision, tick size, lot size, status, and venue rules.
- Strategy: approved policy that transforms data/model state into proposed signals.
- Signal: auditable recommendation with action, confidence, expiry, and context.
- Risk decision: deterministic approval or rejection of an order plan.
- Order plan: intended order before provider submission.
- Order: provider or paper execution request with idempotency key.
- Fill: execution event with price, quantity, fee, and provider reference.
- Position: instrument exposure and average price.
- Balance: asset/currency quantity and availability.
- Portfolio: aggregate balances, positions, equity, margin, exposure, and risk utilization.
- Reconciliation: comparison between expected and authoritative account state.

## Invariants

- Every order MUST trace to user, strategy, signal, model where applicable, risk decision, and execution event.
- Every signal MUST expire.
- A risk rejection MUST prevent order submission.
- Paper state MUST never be represented as live state.
- Provider uncertainty MUST block new execution until reconciled.
