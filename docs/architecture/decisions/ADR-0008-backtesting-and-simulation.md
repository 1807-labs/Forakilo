# ADR-0008: Backtesting and Simulation

Status: Accepted
Date: 2026-07-04

Purpose: define the backtesting approach before strategy implementation.
Scope: vectorized research, event-driven simulation, paper trading, and validation.
Audience: quantitative researchers, ML engineers, risk reviewers, and operators.
Assumptions: historical performance can be misleading without realistic costs, temporal splits, and execution uncertainty.
Dependencies: [Backtesting and Validation Standard](../../trading/BACKTESTING_AND_VALIDATION_STANDARD.md), [Technology Evaluation](../../research/TECHNOLOGY_EVALUATION.md).
Unresolved decisions: final event-driven engine choice requires a spike with target providers and data models.

## Decision

Use VectorBT for fast vectorized research and require an event-driven simulation path, with NautilusTrader as the primary spike candidate, before any strategy can advance to paper or live gates.

## Rationale

Vectorized research is efficient for broad exploration but can hide execution assumptions. Event-driven simulation is needed for partial fills, latency, order state, retries, and reconciliation behavior.

## Consequences

- No model or strategy may be called validated from in-sample or vectorized-only results.
- Backtests MUST include fees, spread, slippage, latency, rejections, and realistic precision constraints.
- Paper trading MUST be the first execution environment.

## Alternatives Rejected

- Backtrader as primary engine: rejected because GPL dependency implications and maintenance concerns are not desirable for the baseline.
- Custom engine first: deferred unless existing engines cannot satisfy safety requirements.
