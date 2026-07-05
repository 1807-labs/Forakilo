# FKL-011: Paper Execution Simulator

Epic: Trading
Priority: P0
Target release phase: MVP
Status: Planned
Estimate: 13

## User Story

As a user, I want paper execution that simulates order behavior so that I can evaluate strategies without risking real capital.

## Business Value

Supports paper-first development and live-readiness evidence.

## Context

Paper state must never be confused with live state.

## In Scope

Paper orders, order state, simulated fills, fees, spread, slippage, partial fills, cancellations, rejections, balances, positions, and portfolio updates.

## Out of Scope

Live provider order submission.

## Acceptance Criteria

- Paper orders require risk approval.
- Simulator produces order/fill/balance/position records.
- Costs and slippage assumptions are recorded.
- Paper state is labeled distinctly in API and UI.

## Negative Acceptance Criteria

- Paper execution cannot use live credentials.
- Paper balances cannot be represented as provider balances.

## Security Requirements

Paper APIs still require authentication and authorization.

## Privacy Requirements

Paper records are scoped to user/account.

## Data Requirements

Paper execution contracts and replayable fixtures.

## Model Requirements

Model signals can only affect paper orders through risk engine.

## Risk Controls

Risk engine remains mandatory.

## Observability Requirements

Paper order lifecycle and simulation assumption metrics.

## Accessibility Requirements

Paper mode is visually distinct.

## Dependencies

FKL-010.

## Assumptions

Initial simulator is conservative and documents limitations.

## Edge Cases

Partial fill, rejected order, stale quote, insufficient simulated balance.

## Test Notes

Execution simulation and replay tests.

## Documentation Impact

Update trading and dashboard docs.

## Definition of Ready

Paper execution schema and assumptions approved.

## Definition of Done

Paper orders reconcile under test fixtures.
