# FKL-009: Auditable Signal Lifecycle

Epic: Trading
Priority: P0
Target release phase: MVP
Status: Planned
Estimate: 8

## User Story

As a risk administrator, I want every strategy or model signal to be versioned, expiring, and auditable so that no stale or duplicate signal can silently drive execution.

## Business Value

Creates the control point between intelligence and trading.

## Context

Signals are not orders and must pass risk checks.

## In Scope

Signal IDs, lifecycle states, expiry, deduplication, context, model references, data freshness, and audit events.

## Out of Scope

Provider order submission.

## Acceptance Criteria

- Signal records include strategy, model, feature, data, confidence, calibration, expiry, and environment.
- Signals expire on stale data, model suspension, provider degradation, or risk-policy change.
- Duplicate active signals are prevented or explicitly versioned.
- Signal consumption creates an audit event.

## Negative Acceptance Criteria

- Expired, rejected, or cancelled signals cannot create order plans.

## Security Requirements

Signal access is scoped to authorized users and services.

## Privacy Requirements

Signals do not expose unrelated user account data.

## Data Requirements

Signal contract and state transitions.

## Model Requirements

Model-dependent signals reference model and feature versions.

## Risk Controls

Risk engine remains mandatory after signal creation.

## Observability Requirements

Signal created, expired, rejected, consumed, and duplicate metrics.

## Accessibility Requirements

Dashboard labels distinguish signal from order.

## Dependencies

FKL-008 or approved rules-based strategy.

## Assumptions

Initial signals are paper-only.

## Edge Cases

Clock skew, duplicate job run, stale feature, model suspension.

## Test Notes

State-machine and expiry tests.

## Documentation Impact

Update signal lifecycle docs.

## Definition of Ready

Signal contract is approved.

## Definition of Done

Signal cannot bypass risk or expiry controls.
