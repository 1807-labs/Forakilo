# Model Validation

Purpose: define validation standards for Forakilo models.
Scope: baselines, candidates, champion comparison, leakage, calibration, robustness, and paper evaluation.
Audience: ML engineers, quantitative researchers, risk reviewers, and QA.
Assumptions: no model is valid merely because it performs well in sample.
Dependencies: [Backtesting Standard](../trading/BACKTESTING_AND_VALIDATION_STANDARD.md), [Model Strategy](MODEL_STRATEGY.md).
Unresolved decisions: metric thresholds by market and strategy.

## Required Validation

- Chronological train/validation/test splits.
- Walk-forward evaluation.
- Purging and embargo where labels overlap.
- Leakage tests for features, labels, revisions, and symbol survivorship.
- Baseline comparisons against naive and simple rules-based models.
- Champion comparison.
- Transaction cost, fee, spread, slippage, latency, and partial-fill assumptions.
- Calibration and confidence analysis.
- Regime-specific performance analysis.
- Drawdown, tail loss, turnover, exposure, and fee sensitivity.
- Shadow and paper-trading results before live eligibility.

## Overfitting and Underfitting Evidence

Validation reports MUST address training/validation divergence, poor baseline performance, excessive complexity, unstable feature importance, poor calibration, regime-specific collapse, live-to-backtest divergence, class imbalance, and feedback-loop risk.

## Approval Result

A model may be:

- Rejected.
- Registered for research only.
- Approved for shadow evaluation.
- Approved for paper trading.
- Eligible for live gate review.
- Suspended.
- Retired.
