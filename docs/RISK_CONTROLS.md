# Mandatory risk controls

## Safety invariant

Chainna starts with **all broker execution disabled**. The initial permitted modes are research, backtest, walk-forward and signal-only. OANDA Practice execution requires a later reviewed milestone and explicit practice-only enablement. Live-money execution is out of scope and must have no usable configuration profile, credential path or account allowlist.

Fail closed: missing, stale, inconsistent or unhealthy input rejects new risk. Logging an error and continuing is not an acceptable execution policy.

## Capability gates

Every order requires all gates to pass:

1. Build permits execution (`execution_capability=practice`); default build/deployment is `none`.
2. Runtime mode is exactly `practice-manual` or, later, approved `practice-auto`.
3. Account ID is allowlisted as OANDA Practice and environment is exactly `Practice`.
4. A durable global kill switch is disarmed and strategy/instrument/session switches permit entry.
5. Startup and current reconciliation show no unknown orders/positions.
6. Market data, broker connection, clock and storage/outbox health are current.
7. Signal is unexpired and based only on information known by its `known_time`.
8. Pre-trade risk checks pass.
9. Manual mode has a valid, unexpired, single-use approval for the exact proposal hash.
10. Execution gateway revalidates price, spread, units, margin and protection immediately before submission.

Unknown account environment, missing account metadata, or ambiguous configuration must prevent adapter initialization.

## Pre-trade controls

Values are configurable only within hard ceilings established after research; no production defaults should be invented during implementation.

- Risk per trade capped as a fraction of current reconciled equity.
- Position size derived from stop distance, pip/tick value, quote/account-currency conversion and estimated costs.
- Mandatory protective stop or explicit approved alternative; stop must be valid and transmitted/confirmed.
- Maximum gross leverage and margin usage.
- Maximum aggregate open risk (sum of stop-based loss estimates).
- Maximum net and gross exposure per currency, pair, correlated group and strategy.
- Maximum simultaneous positions and pending entries.
- Maximum order units/notional and maximum daily turnover.
- Daily and rolling loss limits; peak-to-trough drawdown limit.
- Consecutive-loss/cooldown rule.
- Maximum spread, slippage estimate, price deviation, quote age and signal age.
- Trading-session, rollover/financing, weekend/holiday and scheduled-news restrictions.
- Minimum available margin buffer.
- Duplicate-signal/order prevention using stable idempotency keys.
- Price/quantity precision, minimum size and brokerage constraint validation.
- Self-trade/conflicting-order and unintended hedging/netting checks.
- Strategy, parameter set, symbol and timeframe allowlists.

Rejected checks produce a durable reasoned event. No override is implicit; any operator override is separately authorized, bounded and audited.

## Order and execution controls

- Strategy code cannot directly possess or use broker credentials.
- Only the execution gateway can consume an authorization.
- Order intent, authorization, submission and fill have distinct IDs and states.
- Submission is idempotent; uncertainty triggers reconciliation, not blind retry.
- Protective orders are monitored until broker-acknowledged.
- Partial fills update remaining risk before any further action.
- Cancellations and amendments are acknowledged/reconciled.
- Maximum slippage and price collars are enforced where order type permits.
- Market orders require explicit policy; practice-manual proposals show worst-case assumptions.
- Stale approvals automatically expire.
- A material edit to units, side, pair, price, stop, target or order type invalidates approval.
- Disconnect behavior is defined per state: never create new exposure; preserve broker-held protection; reconcile on recovery.

## Portfolio and loss controls

- Broker account, open orders, fills, cash, margin and positions are reconciled at startup and continuously.
- Unknown broker state places the system in `HALTED_RECONCILIATION`.
- Local state never marks a position closed solely because an exit request was sent.
- Realized and unrealized P&L include spread, commission and financing where available.
- Equity high-water mark and loss limits are durable across restarts.
- Breaching a loss/exposure limit stops new entries immediately and follows a configured reduce/cancel policy.
- Resetting a breached limit requires authenticated operator action and an audit reason; process restart cannot reset it.

## Harmonic-strategy controls

- Pivots are actionable only after the right confirmation window and a closed known bar.
- `event_time` and `known_time` are stored and tested.
- Same-direction adjacent pivots are normalized or rejected deterministically.
- Pattern definitions, tolerance units, PRZ definition and invalidation are versioned.
- One D pivot can produce multiple candidates internally; deterministic selection/deduplication policy is explicit.
- Stops and targets are strategy/risk rules, not copied from Sandy's drawings.
- Warm-up is sufficient to establish pivot and strategy state.
- Backtest fills occur no earlier than the first tradable event after `known_time`.

## Data and model-risk controls

- Historical/live source, timezone, resolution, data hash/version and symbol-properties version are recorded.
- Missing/out-of-order/duplicate bars and stale bid/ask data are detected.
- Clock synchronization is monitored.
- Bid/ask spread, slippage, fees, financing and latency are modeled conservatively.
- Train/validation/holdout periods are chronological with purge/embargo where signals overlap boundaries.
- All attempted experiments are logged to limit selection bias.
- Promotion uses out-of-sample criteria, stability across windows/pairs/regimes, and capacity/cost sensitivity—not a single Sharpe optimum.
- The production package and tests are the source of strategy logic; notebooks cannot be deployed.

## Health controls

Required health signals:

- market-data freshness and sequence;
- broker/API session and rate-limit status;
- account/order/position reconciliation age;
- order acknowledgement and fill-event latency;
- system clock drift;
- worker heartbeat and queue/outbox depth/age;
- storage write/read health and disk capacity;
- notification channel delivery health;
- exception/error rate and restart count;
- protective-order coverage;
- credential expiry/rotation status without exposing secret values.

Critical health failure blocks entries. Notifications are secondary: a failed notifier must not hide or undo a halt.

## Kill switches and emergency states

Controls must be durable, authenticated, observable and idempotent:

| Control | Required behavior |
|---|---|
| Global halt | Reject all new order authorizations. |
| Strategy/pair halt | Reject new exposure for scoped strategy/instrument. |
| Cancel entries | Cancel pending entry orders; preserve protective exits. |
| Reduce-only | Allow only actions that do not increase gross risk. |
| Cancel all | Cancel all cancellable orders with reconciliation. |
| Flatten practice | Explicit operator action; close practice positions with bounded policy and verify fills. |
| Credential disable | Remove execution service access independently of application state. |

Process termination alone is not a kill switch. Conversely, automatic flattening on every software exception is prohibited: it can worsen exposure during bad prices or connectivity loss.

## Manual approval controls

- Strong operator authentication and least-privilege roles.
- Approval view shows account/environment, pair, side, units, estimated loss at stop, equity risk %, spread, order type, entry, stop, targets, expiry and signal evidence.
- Approver cannot unknowingly approve a changed proposal.
- Approval and execution actors/policies are attributable.
- Single-use nonce, proposal hash, UTC timestamp and reason are stored.
- Approval TTL is short and revalidation mandatory.
- Reject/expire is the safe default on UI, network or storage failure.

## Secrets and environments

- No secrets in Git, manifests, logs, alerts, notebooks, command history or result artifacts.
- Practice and any future live credentials use separate identities and secret paths.
- Signal-only and research deployments receive no execution secret.
- Outbound network access is restricted to required endpoints per deployment.
- Logs redact tokens, account identifiers as appropriate, headers and payload secrets.
- Dependency provenance, hashes, vulnerabilities and licenses are checked, especially the external OANDA brokerage plugin.

## Promotion gates

Practice-manual may be considered only after deterministic tests, Sandy parity characterization, leakage tests, realistic cost backtests, walk-forward acceptance, safety test suite, restart/reconciliation tests, and operator runbooks pass.

Practice-auto additionally requires sustained practice-manual evidence, chaos/failure tests, durable kill switches, approval of hard ceilings, monitored canary sizing and a rollback drill.

Live trading remains disabled and requires a separate future architecture/risk review. Passing practice gates does not authorize it.
