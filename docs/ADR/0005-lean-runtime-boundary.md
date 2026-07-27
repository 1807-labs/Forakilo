# ADR 0005: LEAN runtime boundary

**Status: Accepted**  
**Approval date:** 2026-07-26  
**Approver:** Uchenna Emmanuel Anozie, Product Owner

## Context

The pinned LEAN fork supplies event-driven market runtime, backtesting and order infrastructure. Product logic inside the fork would make upgrades and audit boundaries harder. The checkout has OANDA model/configuration hooks but not the OANDA brokerage implementation.

## Decision being considered

Define ownership and integration mechanics between Chainna and LEAN.

## Available options

- Keep LEAN external with thin Chainna adapters.
- Put Chainna algorithms/product code in LEAN's source tree.
- Maintain a heavily customized LEAN fork.
- Avoid LEAN and call data/broker APIs directly.

## Recommended option

Keep LEAN at a pinned commit and pin the resulting build provenance; keep it initially unmodified. Lean CLI is optional. Containerized reproducibility is mandatory before Phase 3 is accepted. Chainna owns strategy, candidate/signal identity, risk, proposal, approval, audit, experiment and promotion semantics. LEAN owns event scheduling, subscriptions, normalized runtime data, historical/backtest handlers, simulated fills/results and later broker order infrastructure.

A thin input adapter converts completed LEAN Forex QuoteBars and clock metadata into Chainna domain inputs. A separate later execution adapter converts only authorized Chainna intents into LEAN order API calls. Strategy code cannot call OANDA directly.

Generate LEAN configuration into per-run isolated directories; never edit `engine/lean/Launcher/config.json` in place. Mount/copy Chainna artifacts into the run environment and ingest results through documented files/events. Keep the OANDA brokerage plugin separately sourced, verified and pinned.

## Reasons

This preserves an upgradeable runtime boundary, keeps private product policy in one repository and allows the deterministic core to run without LEAN.

## Consequences

Adapters and compatibility tests become explicit product responsibilities. LEAN and plugin versions appear in every manifest. Any unavoidable patch needs its own ADR, tests and upstream/rebase plan.

## Risks

Python/runtime type differences, timestamp/bar semantics and plugin discovery can cause adapter drift. External builds and generated configuration add operational tooling.

## Alternatives rejected

Embedding product code in LEAN and heavy fork customization are rejected due to coupling. Direct broker integration is rejected because it bypasses LEAN's order infrastructure and the approved boundary.

## Questions requiring human approval

None. Zero initial patches, commit plus build provenance, optional Lean CLI and containerized reproducibility before Phase 3 are approved. Any future LEAN patch requires a separate ADR and Product Owner approval.

## Evidence required before acceptance

A documented isolated-run design; QuoteBar/time mapping specification; result-contract inventory; reproducible build provenance; and a compatibility plan for the pinned LEAN commit.

## Explicit implementation impact

If accepted later, Chainna creates adapters and run-config generation only in `forex-engine/`. `engine/lean/` remains clean. This ADR does not authorize a build, backtest or adapter implementation.
