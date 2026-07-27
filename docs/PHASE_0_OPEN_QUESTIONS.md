# Phase 0 deferred questions

All Phase 0 architecture decisions were approved on 2026-07-26 by Uchenna Emmanuel Anozie, Product Owner. The following items are deliberately deferred and do not reopen the accepted release boundary.

## Before historical-data use

1. Which licensed bid/ask historical source will be selected?
2. Does its license permit local storage, derived artifacts and any committed samples?
3. What exact EUR_USD H1 market calendar, timezone metadata and bar-boundary convention will be registered?

Only synthetic fixtures may be committed initially. Historical data selection is a later evidence task; no data may be downloaded under Phase 0 authority.

## Before holdout evaluation or numeric risk policy

4. What pre-registered numerical thresholds will govern trade-count sufficiency, expectancy, drawdown, stability, cost sensitivity and concentration?
5. What absolute numeric risk maxima will the Product Owner approve after evidence?
6. What new untouched holdout will be reserved after any strategy change made following inspection of a consumed holdout?

Missing required numeric limits reject execution. Absolute maxima have no runtime override.

## Before Phase 7 entrance

7. What minimum evidence duration and order-sample requirements must the isolated OANDA Practice integration satisfy?

This question must be answered in a pre-registered Phase 7 entrance decision. It does not authorize plugin selection, installation, credentials, connectivity or orders now.
