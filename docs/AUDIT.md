# Chainna workspace audit

## Scope and guardrails

Audit date: 2026-07-26.

The workspace contains three repository boundaries:

- `forex-engine/`: newly initialized private product repository; empty at audit start.
- `legacy/chains/`: clean legacy repository at commit `6ada073`, containing Sandy and ChainCrawlr.
- `engine/lean/`: clean LEAN fork at commit `cd52034dd` (`vebbaybi/Lean`).

This audit was read-only outside `forex-engine/`. No broker connection, credential use, order submission, or trade execution occurred. `engine/lean/` and `legacy/chains/` are reference/upstream inputs, not product code locations.

## Sandy (`legacy/chains/sandy.pine`)

### What it does

Sandy is a Pine Script v6 overlay indicator. It:

1. Confirms swing highs and lows with `ta.pivothigh/high` and `ta.pivotlow/low`, using equal left/right windows (`minLegLength`, default 5).
2. Stores confirmed pivot price, original bar, and high/low type in newest-first arrays, capped by `swingDepth`.
3. Examines every contiguous five-pivot window as X-A-B-C-D.
4. Requires chronological bar order, a direction/type shape, and simple price inequalities.
5. Computes:
   - `AB / XA`
   - `BC / AB`
   - `CD / BC`
   - `XD / XA`
6. Classifies bullish or bearish Gartley, Bat, or Butterfly patterns using fixed Fibonacci targets and an absolute ratio tolerance (default ±0.03).
7. Back-plots the XABCD legs and D label; optionally plots two targets at 38.2% and 61.8% of `|X-D|`, and a D-centered display zone of `±(|X-D| × tolerance)`.

Pattern rules in the script are:

| Pattern | AB/XA | BC/AB | CD/BC | XD/XA |
|---|---:|---:|---:|---:|
| Gartley | 0.618 | 0.382 or 0.886 | 1.27 or 1.618 | 0.786 |
| Bat | 0.382 or 0.5 | 0.382 or 0.886 | 1.618 or 2.618 | 0.886 |
| Butterfly | 0.786 | 0.382 or 0.886 | 1.618 or 2.24 | 1.27 |

These are point-target tests, not conventional inclusive Fibonacci ranges. A value between the listed endpoints does not pass unless it lies near one endpoint.

### Pivot-confirmation delay

With `ta.pivot*(source, L, L)`, a pivot attributed to bar `t` becomes knowable only on bar `t + L`. Sandy correctly stores the pivot at `bar_index - minLegLength`, but the signal is therefore available `minLegLength` completed bars after D. At the default, a label drawn on D appears five bars in the past when first confirmed.

Any Chainna port must represent both:

- `event_time`: the D pivot's bar time.
- `known_time`: the bar close at which D became confirmed.

Backtests and walk-forward studies must act no earlier than `known_time`; using `event_time` as the order time creates look-ahead bias.

### Repainting and hindsight

- Confirmed pivots do not ordinarily change after the right-side window completes, so Sandy does not use an unconfirmed, continuously moving D.
- The drawing is nevertheless visually hindsight-biased because it is placed on historical D after the confirmation delay.
- On a still-forming confirmation bar, Pine can recalculate as high/low changes. Production signals should require a closed confirmation bar (`barstate.isconfirmed` semantics in a Pine comparison).
- Historical discovery loops can find an older pattern on a later bar. A research port must record the actual first-known time, not infer it from the plotted D bar.
- Deduplication uses only `d_bar`, so two valid pattern types sharing D collapse into one. Detection order makes Gartley win over Bat, and Bat over Butterfly.
- The high/low-type test permits adjacent same-type C and D pivots (`C low, D low` bullish; `C high, D high` bearish) rather than enforcing a strictly alternating zigzag. This can admit malformed XABCD sequences. A port needs explicit pivot normalization (replace a same-direction pivot with the more extreme one, or reject the sequence).
- If both a high and low confirm on one bar, both are inserted with the same source bar. Chronology then rejects windows containing both, but array ordering is incidental and should not become strategy semantics.

Other correctness concerns:

- `lastPatternBar` is unused.
- Pattern retention is pruned only every ten bars and by detection count, while drawing objects are not deleted.
- The “PRZ” is only a display band around D. It is not a confluence calculation from independent XA/BC projections and must not be treated as a validated harmonic PRZ.
- Targets have no stop/invalidation rule and are visualization only.

### Broken alert condition

The alert cannot fire for the intended newly confirmed pattern:

```pine
if db == bar_index
    alertBarTriggered := true
```

`db` is D's original pivot bar. D is only added after `minLegLength` right-side bars, so on first detection `db == bar_index - minLegLength`, never the current bar for the allowed `minLegLength >= 1`. `alertBarTriggered` is also reset on every calculation. The alert message says “detected on current bar,” which conflicts with delayed confirmation.

The future port should emit an immutable signal when a previously unseen `(symbol, timeframe, D time, pattern, direction, parameter version)` first becomes confirmed. A Pine repair, if ever made separately, would trigger on new detection at the confirmation bar, not compare D's historical bar with `bar_index`.

## ChainCrawlr (`legacy/chains/CC/`)

### Source shape

The relevant implementation is the Python package:

- `core/`: scanner, sniper, anti-rug checks, portfolio manager, auto-exit.
- `dex_clients/`: Uniswap, Raydium, and Jupiter adapters.
- `interface/`: payloads, queued notifier, Streamlit-style dashboard.
- `utils/`: structured logging, notification handlers, cache, chain helpers.
- `config/`: JSON/YAML configuration.
- `main.py`: threaded lifecycle and health orchestration.

`chaincrawler.js`, `CCmermaid.js`, `CC.txt`, `cr.py`, and `comment_removal.ts` are earlier prototypes, generated/scaffolding material, or utilities. `__pycache__/`, the PNG, and the log are artifacts, not reusable source. There is no test suite.

### Reusable concepts

#### Signal contracts

`interface/signal_payloads.py` separates `TradeSignal`, `RiskAlert`, and `SystemAlert`, with severity and timestamps. Reuse the separation and typed-event idea, not the crypto fields or mutable dataclasses. The new contract needs stable IDs, schema/version, symbol, asset class, timeframe, event/known times, direction, confidence, pattern evidence, proposed entry/stop/targets, strategy/config/data versions, expiry, and lifecycle status. “Signal generated,” “order proposed,” “approved,” “submitted,” “filled,” and “closed” must be distinct events.

#### Portfolio concepts

`Position` and `PortfolioManager` contain useful ideas: position ledger, entry/exit state, realized history, high-water price, trailing state, risk-based sizing, portfolio valuation, and performance metrics. Rebuild around FX quantities, base-currency conversion, account equity, margin, net exposure by currency, realized/unrealized P&L, broker reconciliation, and an append-only ledger. JSON files and token-address keys are insufficient.

#### Notifier architecture

The notifier usefully separates event creation from channel delivery and includes priority, deduplication, rate limiting, retry, severity formatting, and multi-channel dispatch. Rebuild it with a bounded durable outbox, stable event IDs, per-channel delivery records, dead-letter handling, non-blocking rate limits, redaction, and health metrics. Notifications must never be the authoritative state store or part of the order-authorization path.

#### Execution orchestration

`main.py` expresses useful startup ordering, independent workers, graceful signal handling, a main supervisor loop, and emergency state. Preserve explicit lifecycle/state-machine concepts. Replace direct construction and unbounded daemon loops with dependency injection, supervised services, cancellation, readiness/liveness checks, idempotent commands, and durable workflow state.

#### Auto-exit

Useful policies include stop-loss, percentage target, time-based exit, trailing state, one-at-a-time position evaluation, exit history, and emergency escalation. Separate pure exit decisions from execution. Partial/ladder exits, broker-side protective orders, fill-aware quantities, gap/slippage handling, and reconciliation are required.

#### Health monitoring

Balance, connectivity, component, scanner, exit, dashboard, and initialization alerts are a useful starting taxonomy. Production checks must measure fresh market data, clock drift, broker session, account reconciliation, order/fill lag, event queue age, database/outbox health, error budgets, and worker heartbeats—not merely whether an object is non-null.

#### Emergency controls

SIGINT/SIGTERM handling, a stop flag, critical alert, persisted shutdown marker, and optional liquidation express the right concerns. Chainna needs separate controls for:

- stop new entries;
- cancel pending entries;
- cancel all cancellable orders;
- maintain protective exits;
- reduce-only mode;
- flatten practice positions;
- disable execution credentials/service.

“Emergency stop” must fail closed and be idempotent. Automatic liquidation must not be the default response to every process failure.

### Defects that prevent direct reuse

- `load_config()` returns a `ChainCrawlrConfig` object, while callers subscript it as a dictionary.
- The settings validator requires sections absent from `settings.yaml`; wallet and dashboard shapes also disagree with callers.
- Several constructor calls do not match their class signatures.
- The scanner method name used by `main.py` does not match the implementation.
- Initialization can be skipped from a cached success even though in-memory components are absent.
- Infinite loops are nested (`_run_auto_exit` calls `monitor_positions`, which itself loops forever), weakening shutdown.
- Notifier priority-queue entries can compare payload objects when priorities tie, causing runtime errors.
- Rate limiting sleeps the caller; delivery failures can be swallowed inside dispatch and then cached as sent.
- Exit caching can close a position again based on a prior cached success without broker reconciliation.
- Global stop-loss units are inconsistent: a default `0.1` is compared to a percentage P&L, effectively 0.1%, while comments/config imply fractional or larger percentage values.
- The trailing-exit formula tests whether a newly calculated trail exceeds stored trail; it does not test whether price fell through an updated trailing stop.
- `liquidate_all()` calls bookkeeping-oriented `close_position()` and is not a reliable flatten workflow.
- Direct RPC/broker/DEX calls, credentials, state mutation, and policy decisions are tightly coupled.
- Broad exception handling frequently logs and continues, making fail-open behavior possible.

## Crypto-specific versus reusable

Crypto-specific code that should remain quarantined:

- token discovery/sniping;
- contract addresses, token decimals, EVM/Solana wallet/key handling;
- Web3/Solana RPC checks;
- gas, gas price, lamports, nonce construction;
- Uniswap/Raydium/Jupiter clients and swap routes;
- anti-rug contract verification, honeypot, ownership, holder, liquidity-lock checks;
- blockchain explorers and transaction hashes;
- emergency token transfer to a fallback wallet;
- `chains.json` DEX/RPC topology and crypto dependencies.

Reusable only after redesign:

- typed domain events and severity;
- signal lifecycle and deduplication;
- portfolio/position ledger concepts;
- sizing and performance concepts;
- notifier/outbox/channel abstraction;
- supervised orchestration and health taxonomy;
- pure exit policies;
- kill-switch state and graceful shutdown;
- structured logs, correlation IDs, retries, and caching patterns.

No legacy execution adapter, wallet code, or cache implementation should be imported into the forex product.

## Audit conclusion

Sandy is valuable as a strategy specification and parity fixture, not production signal code. ChainCrawlr is valuable as a catalog of domain concepts and operational failure cases, not as a base framework. LEAN should supply the mature quantitative runtime. Chainna should own all product policy and integration code in `forex-engine/`, with live execution disabled by construction until later gates are passed.
