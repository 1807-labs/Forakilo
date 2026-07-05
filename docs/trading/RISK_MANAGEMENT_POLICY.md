# Risk Management Policy

Purpose: define deterministic risk controls for Forakilo.
Scope: paper trading, sandbox trading, and future live trading.
Audience: risk administrators, trading engineers, QA, and operators.
Assumptions: risk limits are conservative until product-owner and risk approvals set exact values.
Dependencies: [Paper to Live Gate](PAPER_TO_LIVE_TRADING_GATE.md), [Service Level Objectives](../operations/SERVICE_LEVEL_OBJECTIVES.md).
Unresolved decisions: numeric limits by market, venue, and user eligibility.

## Required Controls

Forakilo MUST implement deterministic controls independent of model output:

- Maximum risk per trade.
- Maximum account, instrument, and correlated exposure.
- Maximum leverage, open positions, order size, daily loss, and drawdown.
- Maximum trade frequency.
- Maximum acceptable spread and slippage.
- Minimum market liquidity.
- Quote/data freshness limits.
- Volatility, provider-error, reconciliation, and model-health circuit breakers.
- Model confidence and calibration floors where model output is used.
- Manual global kill switch and automated fail-closed switch.
- Emergency credential revocation.

## Risk Decision Output

Every risk decision MUST record approved/rejected status, rule IDs, inputs, thresholds, model/signal context, policy version, actor, environment, and timestamp.

## Fail-Closed Conditions

New execution MUST be rejected when account state is stale, positions are unreconciled, data freshness fails, provider status is degraded, model is suspended, risk policy is unknown, or order outcome is uncertain.
