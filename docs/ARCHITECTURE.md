# Chainna architecture

## Product boundary

`forex-engine/` is the private product repository and source of truth for Chainna. It owns strategy logic, schemas, experiment definitions, product workflows, risk policy, approval policy, operational services, documentation, and tests.

`engine/lean/` is a pinned runtime dependency. Do not place Chainna algorithms in LEAN's `Algorithm.Python` tree and do not edit LEAN configuration in place. Consume a tagged/commit-pinned build or container, mount/copy Chainna algorithm artifacts and generated run configuration into an isolated run directory, and keep any necessary LEAN patch as a small, reviewed upstreamable patch set. The default expectation is zero LEAN patches.

`legacy/chains/` is reference-only. Strategy parity tests may be derived from Sandy and designs may be derived from ChainCrawlr, subject to its license, but runtime imports are prohibited.

## Logical architecture

```text
Market data / historical files / OANDA practice stream
                         |
                  LEAN runtime adapter
                         |
              normalized bars and clock
                         |
         harmonic detector + strategy policy
                         |
               immutable SignalCandidate
                         |
             validation and risk gateway
                         |
            +------------+-------------+
            |                          |
      signal-only sink           OrderProposal
                                       |
                              approval workflow
                                       |
                             execution permission
                                       |
                                LEAN order API
                                       |
                            brokerage adapter/plugin
                                       |
                               OANDA practice

All stages -> event ledger -> reconciliation -> metrics/alerts/audit UI
```

The signal/risk core must be deterministic and side-effect free. Runtime-specific code translates LEAN `QuoteBar`/`Slice` data into the core and translates approved intents back into LEAN orders. FX bars must use bid/ask-aware prices; midpoint-only research assumptions must be explicit.

## Proposed repository layout

```text
forex-engine/
  docs/
  src/chainna/
    domain/          # versioned events, values, enums, state machines
    strategy/
      harmonics/     # pivot normalization, XABCD ratios, PRZ, signal policy
    risk/            # sizing, limits, gates, kill-switch policy
    portfolio/       # product ledger and currency exposure views
    workflows/       # proposal, approval, expiry, execution lifecycle
    notifications/   # outbox and channel adapters
    monitoring/      # health probes, metrics, incident state
    storage/         # event/experiment repositories and migrations
    adapters/
      lean/          # QCAlgorithm shell, event/result bridge
      oanda/         # configuration/reconciliation policy, no raw direct trading
  research/          # notebooks/scripts using the same strategy package
  algorithms/lean/   # thin Chainna QCAlgorithm entry points
  configs/
    base/
    research/
    backtest/
    signal/
    practice/
  experiments/       # immutable manifests; no secrets
  tests/
    unit/
    parity/
    integration/
    regression/
    safety/
  schemas/
  scripts/           # build/run wrappers and config generation
  deploy/            # containers/services; execution profiles isolated
```

This is a design, not authorization to create implementation files.

## Core contracts

### `SignalCandidate`

Required fields:

- `signal_id`, `schema_version`, `strategy_id`, `strategy_version`;
- symbol, market, resolution and direction;
- `event_time`, `known_time`, `created_at`, and expiry;
- X/A/B/C/D prices and times, pivot confirmation width, ratios, tolerance and pattern;
- proposed entry basis, invalidation/stop, targets, confidence/quality;
- data snapshot/hash, parameter-set ID and run ID;
- status (`observed`, `eligible`, `rejected`, `expired`).

### `OrderProposal`

Contains the signal reference, account/environment, side, units, order type, limit/stop prices, time-in-force, protective orders, estimated spread/slippage/margin, risk checks and expiry. It is not executable until it has an approval or an explicitly enabled automation policy.

### `ApprovalDecision`

Contains proposal ID, approve/reject, actor, authentication context, timestamp, optional modifications/reason, proposal hash, and expiry. Approval is single-use. Any material proposal change invalidates it.

### Execution events

`OrderAuthorized`, `OrderSubmitted`, `OrderAccepted`, `OrderRejected`, `OrderPartiallyFilled`, `OrderFilled`, `OrderCanceled`, and `PositionReconciled` are separate immutable records with correlation/idempotency keys.

## Operating modes

| Mode | LEAN role | Orders allowed | Broker |
|---|---|---:|---|
| Research | QuantBook/history or offline data access | No | None |
| Backtest | Deterministic simulation | Simulated only | Backtesting brokerage |
| Walk-forward | Repeated train/validate backtests | Simulated only | Backtesting brokerage |
| Signal-only | Live or replayed data and signal emission | No | None/read-only data |
| Practice-manual | Live data, proposal, approval, execution | Approved only | OANDA Practice |
| Practice-auto | Controlled policy-based execution | Explicitly enabled later | OANDA Practice |
| Live | Future mode; absent initially | No | None |

Use separate deployable profiles. A signal-only process must not contain brokerage credentials or load an execution adapter. A backtest configuration cannot select a live handler. `mode` must be an enum, not a loose collection of booleans.

## Historical research and backtesting

- Use LEAN `QuantBook`/Research for exploration, with notebooks calling the same versioned harmonic core as production.
- Use a thin `QCAlgorithm` adapter for event-driven backtests.
- Pin data vendor, data version/hash, timezone, resolution, symbol properties, spread model, fee model, slippage model, warm-up, parameters, code commit and LEAN commit in an experiment manifest.
- Model the Sandy confirmation delay exactly: D becomes actionable after the right pivot window closes.
- Produce machine-readable results plus a Chainna run summary. Preserve rejected signals as well as trades.
- Never promote notebook-only logic. Promotion requires package code and tests.

## Walk-forward validation

The walk-forward coordinator belongs in Chainna and invokes LEAN backtests as isolated child runs:

1. Declare chronological training, embargo/purge, validation, and final untouched holdout windows.
2. Fit/select parameters using training data only.
3. Freeze parameters before each validation window.
4. Carry only explicitly modeled state across boundaries; otherwise reset.
5. Aggregate out-of-sample results without selecting on the same windows.
6. Compare against simple baselines and account for spread, slippage, financing, latency, and multiple testing.
7. Store every attempted parameter set and failure, not only winners.

LEAN Optimizer can execute parameter searches, but Chainna must own window scheduling, leakage prevention, selection policy, manifests, and aggregate acceptance gates.

## LEAN integration

The inspected fork provides:

- Python and C# algorithm loading via `algorithm-location`;
- filesystem historical feed/backtesting handlers;
- `QuantBook` research support;
- optimizer launcher and constraints;
- Forex `QuoteBar` support and OANDA market/brokerage model;
- launcher environments for backtest, paper, and `live-oanda`;
- OANDA Practice/account/token configuration keys.

The checkout does **not** contain the OANDA brokerage implementation/factory; it contains the model and runtime hooks. Treat the compatible OANDA brokerage plugin/package as a separately pinned runtime dependency. Verify its license, version compatibility, provenance and checksums before practice testing. Do not add its source to the LEAN fork merely for convenience.

Integration mechanics:

- Build/pin LEAN independently.
- Generate per-run configuration outside the LEAN checkout.
- Provide algorithm location, data/output directories and parameters through the supported launcher/CLI surface.
- Keep secrets in an external secret provider/environment injection; never generate them into committed config.
- Consume LEAN result JSON/log/order events through an adapter.
- Use LEAN's order API and brokerage transaction handler for practice execution; do not call OANDA's order endpoint from strategy code.
- Reconcile LEAN state with broker account/orders/positions before enabling entries and continuously thereafter.

## Manual approval

The proposed practice workflow is:

1. Strategy emits a signal.
2. Risk engine creates or rejects an immutable proposal.
3. Notifier/UI displays entry, stop, target, units, risk, spread, expiry and rationale.
4. An authenticated operator approves or rejects the exact proposal hash.
5. Execution gateway re-runs time-sensitive risk checks.
6. Only then is the one-time authorization delivered to the algorithm/execution service.
7. Submission and fills are reconciled and reported.

Approval expires on stale price, excessive spread, session loss of health, kill-switch activation, changed quantity/price/protection, or elapsed TTL.

## Controlled automation later

Automation is a separate capability, not “manual approval off.” It requires a signed policy identifying strategies, instruments, sessions, account, maximum size/risk, allowed order types and validity window. Enablement requires two explicit gates (deployment capability plus runtime arming), a practice account allowlist, successful startup reconciliation, and all controls in `RISK_CONTROLS.md`. There is no live-account mode in the initial architecture.
