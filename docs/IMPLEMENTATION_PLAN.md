# Chainna implementation plan

## Status

This is a proposed, review-gated plan. The audit phase ends with these documents. **Do not begin implementation until the audit is reviewed and approved.**

## Principles

- Product code lives only in `forex-engine/`.
- LEAN stays pinned and unmodified unless a documented integration gap proves otherwise.
- Legacy code is a specification/reference, never an execution dependency.
- One deterministic strategy core serves research, backtest, signal and practice modes.
- Execution capability is absent by default and added only behind explicit gates.
- Each phase produces evidence and has a stop/go review.

## Phase 0 — audit review and decisions

Review these documents and decide:

- language/package approach for the LEAN adapter and domain core (Python is the shortest path to the inspected Python algorithm/research surfaces);
- exact harmonic definitions: endpoint versus range ratios, pivot normalization, multi-match precedence, true PRZ, invalidation, entry timing, stops and targets;
- initial FX pairs, resolutions, sessions and data source;
- experiment store and operational state store;
- local container/CLI approach and supported host environment;
- notification/approval UI scope;
- hard risk ceilings and walk-forward acceptance criteria;
- trusted source/version for the compatible OANDA brokerage plugin.

Deliverable: signed architecture decision records and an approved scope. No code before this gate.

## Phase 1 — repository and safety foundation

- Establish package, lint/type/test tooling and dependency locking.
- Add secret scanning, dependency/license checks and CI.
- Define strict environment/mode schema with only research, backtest, walk-forward and signal-only enabled.
- Define versioned event schemas, IDs, UTC/time semantics and experiment manifest.
- Add a build-time safety test proving no practice/live adapter or credential is loaded by default.
- Add repository rules that reject secrets and generated run outputs.

Exit criteria: reproducible clean build; schemas validated; safety tests prove orders cannot be submitted.

## Phase 2 — harmonic core and Sandy characterization

- Implement pure pivot confirmation and normalized zigzag logic.
- Implement data-driven Gartley/Bat/Butterfly rules.
- Preserve `event_time` and calculate `known_time`.
- Create golden fixtures from synthetic XABCD paths and manually characterized Sandy outputs.
- Test tolerance boundaries, equal prices, adjacent same-type pivots, simultaneous pivots, multiple pattern matches, deduplication and bar-close timing.
- Implement signal evidence and rejection reasons.

Exit criteria: deterministic cross-run results, full boundary tests, and an explicit parity report explaining every intentional difference from Sandy.

## Phase 3 — LEAN research/backtest adapter

- Pin LEAN commit/build/container and record it in manifests.
- Create thin Chainna algorithm entry points outside the LEAN tree.
- Generate isolated backtest configuration and parameter injection.
- Map Forex `QuoteBar` data to the core; use correct bid/ask semantics.
- Map candidates to simulated decisions/orders only where the test strategy calls for it.
- Archive LEAN result/order/log artifacts plus Chainna signal/rejection output.
- Add realistic spread, slippage, fee/financing and latency assumptions.
- Add integration tests that fail if action occurs before D's `known_time`.

Exit criteria: reproducible baseline backtests from a single documented command, no modifications in `engine/lean/`, and identical core signals between direct replay and LEAN adapter.

## Phase 4 — walk-forward research

- Implement chronological window manifests, purge/embargo and untouched holdout.
- Use LEAN Optimizer or isolated backtest runs for training searches.
- Freeze chosen parameters for each validation window.
- Track all trials, failures and selection decisions.
- Aggregate out-of-sample metrics, stability, cost sensitivity and baseline comparisons.
- Define promotion report and rejection thresholds before viewing the holdout.

Exit criteria: automated leakage tests, reproducible report, and acceptance criteria met without using holdout feedback for tuning.

## Phase 5 — signal-only service

- Run the same core against live/replayed market data without an order path.
- Implement durable event ledger/read model and notifier outbox.
- Add signal expiry/deduplication and operational dashboard.
- Add data freshness, clock, process, queue, storage and notifier health checks.
- Exercise restart/recovery and high-availability/idempotency behavior.

Exit criteria: extended shadow run with no order capability, no duplicate signals after restart, measured alert reliability and complete audit trail.

## Phase 6 — proposal, risk and manual approval

- Build portfolio/account read models using simulated or read-only practice snapshots.
- Implement sizing, exposure, drawdown, spread/staleness and session gates.
- Implement immutable proposals, proposal hashing, authentication, approve/reject/expire and single-use authorization.
- Add durable global/scoped halts, cancel-entry and reduce-only state.
- Keep the execution adapter mocked; run adversarial safety and authorization tests.

Exit criteria: all controls in `RISK_CONTROLS.md` have automated tests or an explicit verified operational control; no authorization bypass exists.

## Phase 7 — OANDA Practice, manual only

- Obtain and pin the compatible trusted OANDA brokerage plugin outside the LEAN fork.
- Verify package provenance, license, checksum and compatibility in an isolated build.
- Add a practice-only deployment with account/environment allowlist and secret injection.
- Use LEAN brokerage/order interfaces; no direct OANDA order calls from strategy code.
- Implement startup/continuous reconciliation, idempotent submission, partial-fill/cancel/amend handling and broker-acknowledged protection.
- Start with smallest permitted units and manual approval for every proposal.
- Drill disconnect, stale data, restart, uncertain submission, kill switch, cancel and flatten-practice scenarios.

Exit criteria: sustained reconciled practice operation, zero unexplained orders/positions, incident/runbook review and explicit approval to continue. This gate does not enable automation or live trading.

## Phase 8 — controlled practice automation (later)

- Define signed automation policy allowlisting strategy, pairs, sessions, sizes and order types.
- Require deployment capability plus runtime arming and durable operator-visible state.
- Canary at minimum size with tighter limits than manual practice.
- Add automatic de-arming on health, loss, drift or reconciliation breach.
- Continue periodic manual reconciliation and rollback drills.

Exit criteria: separate risk and architecture approval. Live remains unavailable.

## Future live-trading gate

Live-money support is not an implementation phase in the current plan. It requires a new threat model, regulatory/operational review, broker/account isolation, capital and loss limits, on-call/incident procedures, evidence from practice automation, and an explicit user decision. No configuration alias may silently convert Practice to Live.

## Verification checklist for every phase

- Unit, property, integration, regression and safety tests proportional to the change.
- Deterministic timestamps/timezones and no look-ahead.
- Run manifest records code, LEAN, data, dependencies, configuration and parameters.
- No secrets or account credentials in artifacts.
- Execution-disabled default remains proven in CI.
- Failure behavior is fail-closed and reconciliation-driven.
- Documentation and operator runbooks updated.
- `engine/lean/` and `legacy/chains/` remain clean unless a later separately approved task changes scope.

## Deferred items

The following are deliberately not started by this audit:

- repository scaffolding beyond the requested documents;
- harmonic implementation;
- LEAN builds/config generation;
- data acquisition;
- backtests or optimizer runs;
- notifier/approval UI;
- OANDA plugin installation or credentials;
- broker connections, practice orders, automation or live trading.
