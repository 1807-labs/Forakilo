# FKL-012: Order, Fill, Balance, and Position Reconciliation

Epic: Trading
Priority: P0
Target release phase: MVP
Status: Planned
Estimate: 13

## User Story

As an operator, I want reconciliation of orders, fills, balances, and positions so that Forakilo can detect unknown or unsafe account state.

## Business Value

Prevents repeated execution while state is uncertain.

## Context

Reconciliation applies to paper/sandbox first and live only after gates.

## In Scope

Expected-vs-authoritative state comparison, mismatch detection, reconciliation IDs, blocking policy, and audit events.

## Out of Scope

Tax reporting and full accounting ledger.

## Acceptance Criteria

- Each order lifecycle triggers reconciliation.
- Mismatches block new execution according to policy.
- Reconciliation records link orders, fills, balances, positions, and provider responses.
- Unknown provider outcome is resolved before retry.

## Negative Acceptance Criteria

- New execution cannot proceed with stale or mismatched account state.

## Security Requirements

Reconciliation data access is least-privilege.

## Privacy Requirements

Account state is scoped and redacted where needed.

## Data Requirements

Reconciliation schemas and reason codes.

## Model Requirements

Model output is suspended for affected account/instrument during unsafe reconciliation state.

## Risk Controls

Reconciliation mismatch is a circuit breaker.

## Observability Requirements

Reconciliation success, mismatch, latency, and blocked-execution metrics.

## Accessibility Requirements

Dashboard must clearly show reconciliation state.

## Dependencies

FKL-011 and provider adapter contracts.

## Assumptions

Paper reconciliation is implemented before live provider reconciliation.

## Edge Cases

Provider timeout, duplicate fill, late cancellation, REST/WebSocket disagreement.

## Test Notes

State-machine and failure-mode tests.

## Documentation Impact

Update order execution docs and runbook index.

## Definition of Ready

State contracts are approved.

## Definition of Done

Unsafe mismatch blocks execution with audited evidence.
