# Chainna 0.1 Phase 0 scope

## Purpose

Phase 0 defines the reviewable scope and proposed architectural decisions for Chainna 0.1. It produces documentation only. Implementation, package scaffolding, dependency installation, data download, backtesting and broker activity are not authorized.

## Approved Chainna 0.1 outcome

Chainna 0.1 ends after Phase 3. It is a deterministic, reproducible harmonic-pattern research baseline with narrow LEAN backtest parity. It is an engineering and characterization release, not a claim of profitability and not an execution product.

### In scope

- Repository and safety foundation from Phase 1.
- A deterministic harmonic research core in Phase 2.
- An immutable `sandy_parity_v1` characterization strategy reproducing Sandy's point-target Gartley, Bat and Butterfly classification rules while preventing action before `known_time`.
- Explicit, versioned handling of pivot normalization, simultaneous pivots, candidate retention and signal selection.
- EUR_USD only at one-hour resolution as the first engineering baseline.
- Completed, bid/ask-aware Forex QuoteBars.
- Synthetic committed fixtures for timing, numeric and parity cases.
- Licensed historical data only when its terms and provenance are approved; no data is acquired in Phase 0.
- A thin LEAN research/backtest adapter outside `engine/lean/`.
- Reproducible immutable run manifests and content-addressed artifacts.
- Initial experiment analysis using Parquet and DuckDB if ADR-0004 is accepted.
- Chronological walk-forward design and promotion criteria, without assuming the strategy will pass.
- Execution-disabled modes and safety invariants from the start.

### Explicitly out of scope

- Live-money trading or a live broker profile.
- OANDA credentials, plugin installation, broker connectivity or practice orders in version 0.1's initial research/backtest scope.
- Practice execution before the Phase 7 review gate.
- Signal-only services and notifications.
- PostgreSQL operational services.
- Manual-approval UI.
- OANDA connectivity or any brokerage dependency.
- Controlled automation before a separate later approval.
- AI/ML trading predictions.
- Unbounded optimizer searches or automatic parameter promotion.
- Martingale, grid trading or averaging down.
- Sandy's drawn PRZ or target lines as execution rules.
- Stops/targets without separate researched and approved strategy/risk semantics.
- Additional currency pairs or resolutions before the complete EUR_USD H1 data, timing and parity pipeline passes.
- A mobile application.
- A public signal-selling service.
- Public release of the private product repository.
- Production code in `engine/lean/` or imports from `legacy/chains/`.

## Repository and runtime boundaries

- `forex-engine/` owns Chainna product logic and documentation.
- `engine/lean/` remains a clean, pinned external runtime.
- `legacy/chains/` remains read-only reference material.
- LEAN configuration will eventually be generated into isolated run directories.
- OANDA access, if later approved, must pass through a separately pinned LEAN brokerage plugin. Strategy code may never call OANDA directly.

## Version 0.1 release boundary

Version 0.1 ends after Phase 3 and includes repository safety, deterministic `sandy_parity_v1`, EUR_USD H1, synthetic fixtures, reproducible manifests and LEAN backtest parity. Signal-only begins no earlier than Phase 5. Practice-manual and practice-auto are later gated capabilities and are not 0.1 acceptance criteria.

## Success criteria

Success means:

- the same inputs and manifest produce the same candidates and artifacts;
- no candidate acts before the closed confirmation bar's `known_time`;
- Sandy parity and intentional corrections are separately versioned and explained;
- EUR_USD H1 direct replay and LEAN adapter agree on core candidates;
- all data, code, LEAN, dependency, parameter and cost assumptions are traceable;
- tests demonstrate execution is unavailable;
- the research result may be “not suitable for promotion” without making the engineering release a failure.

## Expansion gates

An additional pair or resolution requires:

1. validated licensed bid/ask data and symbol metadata;
2. the full timing/parity pipeline passing unchanged;
3. pre-registered reason and evaluation criteria;
4. cost/liquidity/session assumptions for that market;
5. no use of the final holdout to choose the expansion; and
6. an updated manifest and strategy/universe version.

Any later signal-only scope remains restricted to the approved EUR_USD H1 universe until a new approved, pre-registered universe version exists. It requires a durable event/read model, outbox, health controls, restart idempotency and proof that no execution dependency or credential is present.

Practice-manual requires separate ADR acceptance, evidence-based numeric ceilings, authenticated approval, reconciliation, kill switches and verified OANDA Practice integration.

## Phase 0 exit criteria

- Scope is approved or amended by the product owner.
- ADR-0001 through ADR-0009 are Accepted, dated and attributed.
- Answered approval questions are closed; deferred decisions remain explicitly recorded.
- Numeric risk and promotion thresholds that lack evidence are labeled `REQUIRES PRE-REGISTRATION BEFORE HOLDOUT`.
- No implementation is inferred from documentation approval; Phase 1 needs explicit authorization.
