# Product Requirements Document

Purpose: define Forakilo requirements for implementation planning and acceptance.
Scope: foundation, MVP, controlled beta, and post-MVP product requirements.
Audience: product owners, engineers, testers, risk reviewers, and legal counsel.
Assumptions: users keep accounts with approved third-party providers; Forakilo does not hold funds or provide personalized financial advice in the MVP.
Dependencies: [Product Vision](PRODUCT_VISION.md), [Non-Functional Requirements](NON_FUNCTIONAL_REQUIREMENTS.md), [Requirements Traceability Matrix](REQUIREMENTS_TRACEABILITY_MATRIX.md).
Unresolved decisions: final user segment, provider contracts, risk limits, and legal permissions.

## Product Goals

| ID | Goal | Verification |
| --- | --- | --- |
| PG-001 | Provide authenticated access before protected services. | Auth tests reject unauthenticated API/dashboard access. |
| PG-002 | Provide validated market and macro data for research and paper trading. | Data quality reports and lineage checks pass. |
| PG-003 | Generate auditable strategy/model signals. | Signal records include user, strategy, model, data, confidence, expiry, and risk context. |
| PG-004 | Apply deterministic risk controls before execution. | Risk test fixtures reject unsafe orders independent of model output. |
| PG-005 | Support paper trading before live trading. | Paper mode can reconcile simulated orders, fills, balances, and positions. |
| PG-006 | Govern candidate retraining without silent live promotion. | Promotion workflow requires documented approval gates. |

## Functional Requirements

| ID | Requirement | Priority | Release |
| --- | --- | --- | --- |
| FR-001 | Users MUST register, verify email, authenticate, log out, and manage sessions. | Must | Foundation/MVP |
| FR-002 | High-impact actions MUST require step-up authentication. | Must | MVP |
| FR-003 | Exchange credentials MUST be encrypted, scoped, rotatable, revocable, and never logged. | Must | MVP |
| FR-004 | Market data connectors MUST persist raw immutable payloads before normalization. | Must | MVP |
| FR-005 | Data contracts MUST version schemas for market, feature, signal, order, fill, balance, and position events. | Must | Foundation/MVP |
| FR-006 | The dashboard MUST show global mode, kill switch, data freshness, connectivity, reconciliation, model, risk, execution, and alerts. | Must | MVP |
| FR-007 | Backtests MUST use chronological splits, point-in-time data, costs, spread, slippage, and walk-forward evaluation. | Must | MVP |
| FR-008 | Models MUST support abstention via `HOLD` when confidence, calibration, or data quality is insufficient. | Must | MVP |
| FR-009 | Paper trading MUST be the default and live trading MUST be disabled until gates pass. | Must | MVP |
| FR-010 | Every order decision MUST be attributable to user, strategy, model, signal, risk decision, and execution event. | Must | Controlled beta |

## Non-Functional Requirements

See [Non-Functional Requirements](NON_FUNCTIONAL_REQUIREMENTS.md) for security, privacy, reliability, accessibility, observability, data quality, and performance requirements.

## Acceptance Boundary

Forakilo is not ready for live trading until [Paper to Live Trading Gate](../trading/PAPER_TO_LIVE_TRADING_GATE.md) is satisfied.
