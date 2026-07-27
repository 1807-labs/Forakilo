# Legacy reuse matrix

Ratings:

- **Reuse**: preserve the concept/contract, then implement inside Chainna with tests.
- **Adapt**: useful algorithmic seed, but semantics or coupling require substantial redesign.
- **Reference**: study or use as a parity fixture; do not import at runtime.
- **Reject**: crypto-specific, unsafe, obsolete, generated, or non-product material.

| Legacy source | Capability | Disposition | Chainna target | Reason / required change |
|---|---|---|---|---|
| `sandy.pine` pivot detection | Confirmed symmetric pivots | Adapt | `strategy/harmonics` | Preserve right-window confirmation and known-time delay; normalize alternating pivots and closed-bar behavior. |
| `sandy.pine` ratios/patterns | Gartley/Bat/Butterfly seed rules | Adapt | `strategy/harmonics` | Make rules data-driven; decide point targets versus ranges; add fixtures and numeric precision policy. |
| `sandy.pine` drawings/TP/PRZ | Visualization | Reference | research/reporting | Targets are display-only and PRZ is not true confluence. Never infer execution rules from drawings. |
| `sandy.pine` alert logic | Alert trigger | Reject | signal emitter | `db == bar_index` is impossible after required pivot delay. Use first-confirmed immutable signal IDs. |
| `interface/signal_payloads.py` | Trade/risk/system event separation | Reuse | `domain`, `schemas` | Version schemas; split signal/proposal/approval/order/fill; add stable IDs, UTC and provenance. |
| `interface/signal_payloads.py` | Explorer links/token fields | Reject | — | Blockchain-specific presentation. |
| `interface/notifier.py` | Queued multi-channel delivery | Adapt | `notifications` | Durable bounded outbox, stable dedupe, per-channel status, dead-letter queue, async rate limiting and metrics. |
| `utils/telegram_handler.py`, `discord_handler.py` | Channel adapters | Reference | `notifications/adapters` | Patterns are useful; APIs, error handling, redaction and secret handling need replacement. |
| `utils/logger.py` | Structured/enriched logs and rotation | Adapt | `monitoring` | Use standard structured telemetry, correlation IDs and secret redaction; remove crypto enrichment. |
| `utils/caching.py` | Cache abstraction | Reference | infrastructure | JSON cache is not durable workflow state and has unsafe semantics for execution dedupe. |
| `core/portfolio_manager.py:Position` | Entry, amount, high-water, trailing and exit state | Reuse | `portfolio` | Replace token identity with FX position/account/currency exposure model and append-only ledger. |
| `PortfolioManager` sizing | Risk-based sizing idea | Adapt | `risk/sizing` | Base size on stop distance, pip value, conversion rates, equity, margin and exposure caps; fail closed on missing data. |
| `PortfolioManager` metrics | P&L, win rate, best/worst/recent | Adapt | analytics | Add drawdown, expectancy, costs, exposure, risk-adjusted and out-of-sample metrics; distinguish realized/unrealized. |
| `PortfolioManager` JSON persistence/cache | State storage | Reject | storage | Race-prone and non-transactional; not authoritative or broker-reconciled. |
| `core/auto_exit.py` | Stop, target, time and trailing policies | Adapt | `risk/exits` | Pure fill-aware rules, consistent units, partial exits, broker-side protection and exact state transitions. |
| `AutoExit.active_positions` | Per-position concurrency guard | Reuse | workflows | Use durable idempotency/leases, not an in-memory token-address dictionary. |
| `AutoExit` cached exit result | Execution deduplication | Reject | execution ledger | Can falsely close state from stale cached success. Reconcile by broker/order IDs and idempotency key. |
| `AutoExit` rug/fallback transfer | Emergency exit | Reject | — | Crypto-specific and not equivalent to closing exposure. |
| `main.py` initialization order | Notifier/infra before dependent workers | Reuse | service composition | Add dependency injection, readiness gates and rollback; never restore initialized process state from cache. |
| `main.py` worker loops | Scanner/exit/dashboard separation | Adapt | workflows/services | Supervised cancellable tasks with bounded queues and heartbeats; remove nested infinite loops. |
| `main.py` SIGINT/SIGTERM | Graceful process stop | Reuse | runtime | Stop entries, drain/persist events, preserve protective orders, then terminate cleanly. |
| `main.py` health taxonomy | Balance, connection, component checks | Adapt | monitoring | Measure freshness/liveness/reconciliation rather than object existence; failures gate execution. |
| `main.py` emergency flag/state record | Kill-switch concept | Reuse | risk/control plane | Durable, externally operable, idempotent state with separate entry-stop/cancel/reduce/flatten actions. |
| `main.py` optional `liquidate_all` | Universal emergency reaction | Reject | — | Bookkeeping close is not broker flattening; blanket liquidation may increase risk. |
| `interface/dashboard.py` | Operational visibility concept | Adapt | operator UI | Read from authoritative event/read models; authenticated approval, control state and audit trail are required. |
| `config/config.py` | Validated centralized config idea | Reuse | typed config | Use strict schemas and environment profiles; current object/dict and schema mismatches make code unusable. |
| `config/settings.yaml` | Separated operational parameters/secrets references | Reference | `configs` | Replace crypto fields; notifications disabled safely unless configured; never label a default profile production. |
| `core/token_scanner.py` | Discovery loop | Reject | — | Token/DEX-specific; FX universe and schedule come from product configuration/LEAN. |
| `core/sniper.py` | Immediate entry execution | Reject | — | Crypto-specific and bypasses proposal/approval/risk separation. |
| `core/anti_rug.py` | Risk screening concept | Reject for code | — | Contract/honeypot/holder/liquidity checks do not map to FX. General pre-trade risk is redesigned. |
| `dex_clients/*` | Venue adapters | Reject | — | Uniswap/Raydium/Jupiter only. OANDA is reached through the pinned LEAN brokerage adapter. |
| `utils/helpers.py` gas/address/token methods | Utilities | Reject | — | Crypto-only. Generic time/decimal helpers should use standard libraries or be rewritten narrowly. |
| `chaincrawler.js`, `CCmermaid.js`, `CC.txt`, `cr.py` | Earlier prototypes/scaffolds | Reference | docs/history | Superseded/incomplete; useful only for design history. |
| `comment_removal.ts` | Source rewriting utility | Reject | — | Not part of product behavior. |
| logs, PNG, `__pycache__` | Artifacts | Reject | — | No source reuse; logs may contain operational data and should not be copied. |

## LEAN reuse matrix

| LEAN surface | Disposition | Chainna usage |
|---|---|---|
| Engine event loop, time, subscriptions and consolidators | Reuse as dependency | Run strategy adapter without modifying LEAN. |
| Forex `QuoteBar`, symbol properties and market hours | Reuse as dependency | Normalize bid/ask-aware FX inputs. |
| Backtesting handlers, fills, fees, slippage and result output | Reuse as dependency | Configure per run; Chainna pins assumptions and archives artifacts. |
| `QuantBook` research runtime | Reuse as dependency | Exploratory history access with product strategy package. |
| Optimizer | Adapt/orchestrate | LEAN runs searches; Chainna owns walk-forward splits, leakage policy and promotion gates. |
| Algorithm Framework abstractions | Optional | Use only where they simplify the thin adapter; domain contracts remain LEAN-independent. |
| OANDA brokerage model and launcher hooks | Reuse as dependency | Model/backtest configuration and runtime discovery. |
| OANDA brokerage implementation | External dependency | Not present in this checkout; pin a compatible trusted plugin/package for practice only. |
| `Launcher/config.json` | Reference/template | Never edit in place; generate isolated run config with secrets injected at runtime. |
| LEAN source/fork | Do not modify initially | Pin commit/build; carry only unavoidable, reviewed patches later. |
