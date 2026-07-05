# Backtesting and Validation Standard

Purpose: prevent misleading trading performance claims.
Scope: research, model validation, strategy validation, and paper-readiness.
Audience: quantitative researchers, ML engineers, risk reviewers, and QA.
Assumptions: historical performance is not evidence of future returns.
Dependencies: [Model Validation](../ml/MODEL_VALIDATION.md), [Risk Management Policy](RISK_MANAGEMENT_POLICY.md).
Unresolved decisions: benchmark selection and numeric thresholds per strategy.

## Required Methodology

Backtests MUST include chronological splits, walk-forward evaluation, purging when labels overlap, embargo periods where appropriate, out-of-sample testing, point-in-time data, reproducible seeds where applicable, multiple regimes, simple baselines, champion comparison, stress testing, sensitivity analysis, and capacity/liquidity assumptions.

## Required Execution Modeling

Backtests MUST model fees, spread, slippage, partial fills, rejections, rate limits, latency, funding, borrowing, margin, liquidation, minimum order size, tick size, quantity precision, price precision, order-book depth where relevant, venue downtime, data gaps, market closures, and execution uncertainty.

## Required Reporting

Reports MUST include total return, annualized return where meaningful, volatility, Sharpe ratio with assumptions, Sortino ratio, maximum drawdown, Calmar ratio, profit factor, expectancy, hit rate, average win/loss, turnover, exposure, tail loss, VaR/Expected Shortfall where appropriate, trade count, regime-specific results, fee sensitivity, slippage sensitivity, and confidence intervals.

## Claim Control

No strategy may receive approval or readiness status based only on in-sample results.
