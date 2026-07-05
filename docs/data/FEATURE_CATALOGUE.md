# Data Feature Catalogue

Purpose: define initial feature groups for research and model development.
Scope: market, portfolio, risk, macro, and model-health features.
Audience: quantitative researchers, ML engineers, data engineers, and reviewers.
Assumptions: features are planned and not implemented; all features require leakage review.
Dependencies: [Model Strategy](../ml/MODEL_STRATEGY.md), [Data Quality](DATA_QUALITY_AND_VALIDATION.md).
Unresolved decisions: approved feature sets per strategy.

## Feature Groups

| ID | Feature group | Examples | Controls |
| --- | --- | --- | --- |
| FG-001 | Price returns | log returns, rolling returns, range metrics | Point-in-time windows only. |
| FG-002 | Volatility | realized volatility, ATR-like ranges, drawdown | Stable window definitions. |
| FG-003 | Liquidity/spread | bid/ask spread, depth, volume, turnover | Provider sequencing and stale quote checks. |
| FG-004 | Momentum | moving averages, RSI-like indicators, trend slopes | No future bars or centered windows. |
| FG-005 | Regime | volatility clusters, trend/range labels | Walk-forward validation. |
| FG-006 | Portfolio/risk | exposure, concentration, margin, daily loss | Paper/live separation. |
| FG-007 | Macro | rates, inflation, employment releases | Vintage-time correctness using ALFRED when relevant. |
| FG-008 | Model health | drift, calibration, error, abstention rate | Monitoring windows and thresholds. |

## Feature Approval

A feature MUST NOT enter training or inference until it has a contract, source lineage, leakage test, freshness rule, null policy, precision policy, and owner approval.
