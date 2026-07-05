# Use Cases and Edge Cases

Purpose: define user and system behaviors that need implementation and testing.
Scope: authentication, data, models, signals, paper trading, risk, execution, and operations.
Audience: engineers, QA, product, and risk reviewers.
Assumptions: most edge cases should fail closed until reviewed.
Dependencies: [Failure Modes](../trading/FAILURE_MODES_AND_EDGE_CASES.md), [Test Strategy](../engineering/TEST_STRATEGY.md).
Unresolved decisions: provider-specific edge cases after adapter spikes.

## Core Use Cases

| ID | Use case | Primary actor | Acceptance signal |
| --- | --- | --- | --- |
| UC-001 | Register and log in | User | Protected endpoints reject unauthenticated access. |
| UC-002 | Add sandbox credential | User | Credential is encrypted, validated, masked, and audited. |
| UC-003 | Ingest market data | System | Raw and normalized records pass schema and freshness checks. |
| UC-004 | Run backtest | Quantitative developer | Report includes costs, drawdown, walk-forward splits, and lineage. |
| UC-005 | Generate signal | Strategy/model | Signal includes version, confidence, expiry, and data references. |
| UC-006 | Reject unsafe order | Risk engine | Rejection includes deterministic reason and audit event. |
| UC-007 | Simulate paper execution | Paper engine | Orders, fills, fees, positions, and balances reconcile. |
| UC-008 | Trigger retraining | Model monitor | Candidate is evaluated without live promotion. |
| UC-009 | Activate kill switch | Risk admin | New execution stops and event is audited. |

## Edge Cases

- Stale quotes, missing candles, duplicate ticks, out-of-order events, late events, revised macro observations, and symbol renames.
- Provider timeout after an order may have been accepted.
- Duplicate order submission due retry.
- REST and WebSocket disagreement.
- Partial fills, precision rejection, insufficient funds, insufficient margin, and provider maintenance.
- Model service unavailable, poor calibration, low confidence, drift, and regime mismatch.
- Database, cache, queue, or clock failure.
- Account takeover, session theft, credential stuffing, recovery abuse, and API-key leakage.

## Edge-Case Policy

If Forakilo cannot determine whether state is safe, it MUST fail closed for new execution and surface an operator alert.
