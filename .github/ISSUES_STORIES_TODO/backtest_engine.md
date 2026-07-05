# FKL-016: Backtesting and Walk-Forward Validation

Epic: Quant Validation
Priority: P0
Target release phase: MVP
Status: Planned
Estimate: 13

## User Story

As a risk-conscious trader, I want point-in-time backtesting with realistic costs and walk-forward validation so that I can evaluate a paper strategy before any live gate is considered.

## Business Value

Prevents misleading performance claims and supports paper-first evidence.

## Context

The original story focused on profitability metrics. The normalized story forbids in-sample-only approval and requires execution assumptions.

## In Scope

Chronological splits, walk-forward evaluation, costs, spread, slippage, partial fills, latency assumptions, baselines, drawdown, tail risk, reproducible report, and lineage.

## Out of Scope

Live trading and claims of future performance.

## Acceptance Criteria

- Backtest uses point-in-time data and records data/model/strategy versions.
- Report includes required performance, risk, cost, and sensitivity metrics.
- Walk-forward and out-of-sample results are separated from in-sample results.
- Baseline and champion comparisons are included where available.
- Report states limitations and assumptions.

## Negative Acceptance Criteria

- In-sample-only results cannot mark a strategy ready.
- Strategy cannot receive readiness approval from a backtest alone.

## Security Requirements

Backtest inputs and reports are scoped to authorized users.

## Privacy Requirements

Reports exclude unnecessary personal data.

## Data Requirements

Point-in-time datasets and cost assumption records.

## Model Requirements

Model validation report links to backtest report.

## Risk Controls

Backtest must include risk-limit simulation and drawdown analysis.

## Observability Requirements

Backtest job status, duration, failure, and report metrics.

## Accessibility Requirements

Reports and charts are accessible in dashboard.

## Dependencies

FKL-005, FKL-006, FKL-007.

## Assumptions

VectorBT is used for vectorized research; event-driven simulator path is evaluated.

## Edge Cases

Data gap, market closure, low liquidity, fee change, delisting, overlapping labels.

## Test Notes

Deterministic backtest fixtures and leakage checks.

## Documentation Impact

Update backtesting standard.

## Definition of Ready

Dataset and strategy contracts exist.

## Definition of Done

Report is reproducible and cannot be mistaken for live-readiness approval.
