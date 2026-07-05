# FKL-010: Deterministic Risk Engine

Epic: Risk
Priority: P0
Target release phase: MVP
Status: Planned
Estimate: 13

## User Story

As a risk administrator, I want deterministic pre-trade controls so that model output cannot create orders outside approved risk limits.

## Business Value

Protects capital and creates auditable safety decisions.

## Context

The original story assumed OCO orders. The normalized story requires provider capability checks and does not depend on OCO support.

## In Scope

Position sizing, exposure, leverage, open positions, order size, daily loss, drawdown, frequency, spread, slippage, liquidity, freshness, provider status, reconciliation, model confidence/calibration floors, and kill-switch checks.

## Out of Scope

Live trading and provider-specific bracket/OCO implementation.

## Acceptance Criteria

- Risk engine returns approved or rejected with rule IDs and reason codes.
- Risk decisions are independent of model approval.
- Stale data, stale account state, model suspension, or reconciliation mismatch rejects execution.
- Kill switch rejects new execution.
- Risk decisions are audited.

## Negative Acceptance Criteria

- No order plan can bypass risk evaluation.
- A high model confidence cannot override a hard risk limit.

## Security Requirements

Risk policy changes require authorization, step-up authentication, and audit.

## Privacy Requirements

Risk logs avoid unnecessary personal data.

## Data Requirements

Risk input and decision schemas.

## Model Requirements

Model confidence and calibration are inputs only, not authority.

## Risk Controls

This story implements the MVP risk-control foundation.

## Observability Requirements

Risk approval/rejection rates, rule hits, latency, and circuit-breaker metrics.

## Accessibility Requirements

Dashboard risk reasons must be human-readable.

## Dependencies

FKL-009, portfolio/account state fixtures.

## Assumptions

Initial numeric thresholds are conservative defaults approved for paper only.

## Edge Cases

Extreme spread, stale balance, clock skew, delisting, rate-limit degraded state.

## Test Notes

Property-based and fixture-based risk tests.

## Documentation Impact

Update risk management policy.

## Definition of Ready

Risk rule list and schemas are approved.

## Definition of Done

Every unsafe fixture is rejected with auditable reason.
