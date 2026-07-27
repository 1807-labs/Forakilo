# ADR 0003: Initial market universe and timeframes

**Status: Accepted**  
**Approval date:** 2026-07-26  
**Approver:** Uchenna Emmanuel Anozie, Product Owner

## Context

Multiple pairs and resolutions multiply data, session, spread, timing and selection-bias problems before the parity pipeline is validated.

## Decision being considered

Choose the first research universe and expansion criteria.

## Available options

- EUR_USD H1 only.
- A basket of major FX pairs at H1.
- EUR_USD across several resolutions.
- Start at minute resolution for more observations.

## Recommended option

Use only EUR_USD at one-hour resolution with completed, bid/ask-aware QuoteBars across research, backtest and any later signal-only mode. Treat it as an engineering baseline, not a trading recommendation or profitability claim. Expansion requires a new approved universe version and pre-registered process.

## Reasons

A single liquid pair and moderate resolution constrain integration variables, make confirmation timing reviewable and reduce premature multiple testing.

## Consequences

Initial findings do not generalize to other pairs or resolutions. Trade counts may be too low; that is evidence, not justification to widen scope after seeing holdout results.

## Risks

EUR_USD H1 may not generate enough candidates or economic value. Concentration can overfit market-specific behavior.

## Alternatives rejected

Broader baskets and multiple resolutions are deferred because they obscure whether discrepancies arise from logic, data or market metadata. Minute data is deferred due to greater cost/latency sensitivity.

## Questions requiring human approval

The universe and signal-only restriction are approved. Exact market/session calendar and H1 boundary metadata remain a data-registration evidence item before historical-data use, not an open universe decision.

## Evidence required before acceptance

Licensed bid/ask data availability, symbol-properties/market-hours review, deterministic bar-boundary definition and a pre-registered expansion procedure.

## Explicit implementation impact

If accepted later, fixtures, manifests, subscriptions, validation and reports must reject other symbols/resolutions until an approved universe version adds them.
