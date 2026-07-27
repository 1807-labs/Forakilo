# ADR 0008: Risk ceilings and promotion policy

**Status: Accepted**  
**Approval date:** 2026-07-26  
**Approver:** Uchenna Emmanuel Anozie, Product Owner

## Context

Structural safety rules can be chosen before performance research; defensible numeric ceilings cannot. Placeholder numbers risk becoming accidental production defaults.

## Decision being considered

Approve structural controls, the numeric-limit governance model and measurable walk-forward/promotion categories.

## Available options

- Structural rules now; evidence-based numeric values later with fail-closed absence.
- Choose conservative-looking placeholder numbers now.
- Permit operator discretion without hard ceilings.
- Let optimizer results automatically choose limits and promotion.

## Recommended option

Approve these structural controls now: execution disabled by default; a protective stop for every future risk-increasing order with no initial exception; no martingale, grid trading or averaging down; no automatic parameter promotion; fail-closed health; reconciliation before entries; immutable proposal/approval; idempotent submission; stale-signal rejection; durable scoped/global kill switches; no live profile.

Every required numeric limit is mandatory but unset until researched, pre-registered and approved. Absence rejects execution.

| Ceiling | Unit | Future configuration location | Absolute maximum | Evidence required to select value | Safe behavior when absent |
|---|---|---|---|---|---|
| Risk per trade | % reconciled equity and account-currency amount | Versioned risk policy | `REQUIRES PRE-REGISTRATION BEFORE HOLDOUT` | Stop-aware loss distribution, costs, drawdown simulations, broker constraints | Reject proposal |
| Gross leverage | Gross notional / equity | Account risk policy | `REQUIRES PRE-REGISTRATION BEFORE HOLDOUT` | Margin/stress scenarios and broker rules | Reject exposure increase |
| Daily loss | %/amount from UTC or approved session start equity | Durable account limits | `REQUIRES PRE-REGISTRATION BEFORE HOLDOUT` | OOS loss tails and incident tolerance | Halt entries |
| Weekly loss | %/amount from approved week boundary | Durable account limits | `REQUIRES PRE-REGISTRATION BEFORE HOLDOUT` | OOS/stress loss clustering | Halt entries |
| Drawdown | % from durable equity high-water mark | Durable account limits | `REQUIRES PRE-REGISTRATION BEFORE HOLDOUT` | OOS/stress maximum drawdown | Halt entries; reduce only per policy |
| Exposure | Gross/net units and account-currency notional by pair/currency/strategy | Portfolio risk policy | `REQUIRES PRE-REGISTRATION BEFORE HOLDOUT` | Correlation, conversion and stress analysis | Reject proposal |
| Spread | Pips and bps of reference/modeled range | Instrument/session policy | `REQUIRES PRE-REGISTRATION BEFORE HOLDOUT` | Historical bid/ask distribution by session/regime | Reject proposal |
| Slippage | Pips/bps and price collar | Order policy | `REQUIRES PRE-REGISTRATION BEFORE HOLDOUT` | Conservative fill scenarios/practice observations | Reject or use non-marketable bounded order |
| Signal age | Elapsed seconds/bars from `known_time` | Strategy/execution policy | `REQUIRES PRE-REGISTRATION BEFORE HOLDOUT` | Decay/latency study and H1 workflow | Expire signal/proposal |
| Margin buffer | % free margin/equity and currency amount | Account risk policy | `REQUIRES PRE-REGISTRATION BEFORE HOLDOUT` | Broker margin rules and stress moves | Reject exposure increase |
| Simultaneous positions | Integer open + risk-increasing pending entries | Portfolio risk policy | `REQUIRES PRE-REGISTRATION BEFORE HOLDOUT` | Dependency/exposure and operational capacity analysis | Reject new entry |
| Turnover | Account-currency notional per day/week | Account/strategy policy | `REQUIRES PRE-REGISTRATION BEFORE HOLDOUT` | Cost, churn and capacity analysis | Halt further entries |

“Absolute maximum” means a code/config hard ceiling that an operator cannot override at runtime. It is intentionally unresolved until pre-registration; it is not optional.

Walk-forward promotion must use chronological train/validation/final holdout, with purge and embargo at least covering maximum signal/position overlap and finalized before runs. Pre-register minimum trade-count sufficiency; positive net expectancy after all modeled costs; drawdown bound; stability across validation windows; adverse spread/slippage sensitivity; parameter stability; pair/session/regime concentration; simple baseline comparisons; and aggregation rules.

Record every experiment. The final holdout is one-use: after inspection it is consumed, and any later strategy change requires a new untouched holdout. Reject promotion if a single exceptional run/window dominates aggregate results, thresholds fail, material results depend on optimistic costs, or chosen parameters are unstable. Every unresolved threshold is labeled `REQUIRES PRE-REGISTRATION BEFORE HOLDOUT`.

## Reasons

This prevents invented numbers from gaining authority and makes absence safe. It separates engineering completion from trading merit.

## Consequences

No practice proposal can pass until every applicable value and hard maximum is approved. Research may conclude the strategy should not progress. Pre-registration adds deliberate review overhead.

## Risks

Overly strict or poorly evidenced limits can prevent useful evaluation; weak pre-registration can still permit researcher degrees of freedom. Mandatory stops can experience gaps/slippage and are not loss guarantees.

## Alternatives rejected

Placeholder defaults, discretionary overrides and optimizer-led promotion are rejected because they create hidden authorization and selection bias.

## Questions requiring human approval

The Product Owner approved all structural controls, fail-closed missing limits, no runtime override of absolute maxima and the one-use holdout policy. Numeric values still require evidence, pre-registration and Product Owner approval before use.

## Evidence required before acceptance

Signed risk taxonomy; proposed policy schema; walk-forward protocol; holdout governance; historical/stress methodology; safety-test plan; explicit approval authority and reset process.

## Explicit implementation impact

If accepted later, risk schemas must represent “unset” distinctly and the gateway must reject it. CI/safety tests cover structural bans. Promotion tooling enforces pre-registered windows/criteria and records all trials. No numeric default or risk code is created now.
