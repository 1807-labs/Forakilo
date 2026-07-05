# Dashboard Specification

Purpose: define the Forakilo dashboard experience before implementation.
Scope: authenticated dashboard for MVP and controlled beta.
Audience: product, design, frontend, backend, QA, risk, and operations.
Assumptions: dashboard data is read-only by default; high-impact commands require step-up authentication; paper and live modes must be visually distinct.
Dependencies: [Authentication and Authorization](../security/AUTHENTICATION_AND_AUTHORIZATION.md), [Observability](../operations/OBSERVABILITY.md), [Risk Management Policy](../trading/RISK_MANAGEMENT_POLICY.md).
Unresolved decisions: exact visual design, component library packaging, and chart interaction details.

## Global Status

The dashboard MUST always display:

- Paper/live mode, environment, trading-enabled state, and kill-switch state.
- Data freshness, exchange/broker connectivity, and last successful reconciliation.
- Active alerts, current model version, current strategy version, and deployment version.
- Clear visual separation between paper and live trading.

## Portfolio View

Show balances, equity, available margin, used margin, exposure, asset allocation, realized and unrealized P&L, fees, funding, drawdown, and risk utilization. Values MUST identify whether they are simulated, sandbox, or live.

## Trading View

Show open positions, pending orders, recent fills, rejected orders, cancelled orders, strategy signals, signal confidence, signal expiry, risk rejection reason, execution slippage, and order latency.

## Market Intelligence View

Show instruments, price charts, volume, spread, volatility, regime classification, data gaps, event/macro context, model predictions, confidence intervals, calibration information, and feature freshness.

## Model Operations View

Show champion model, challenger models, training runs, dataset version, feature version, drift status, calibration status, degradation, retraining triggers, retraining jobs, evaluation reports, promotion history, rollback history, and suspended models.

## Risk View

Show per-trade risk, exposure limits, position limits, daily-loss limit, drawdown limit, concentration, correlation exposure, volatility limits, spread limits, slippage limits, trade-frequency limits, and circuit-breaker status.

## Audit and Operations View

Show user actions, strategy decisions, model decisions, risk decisions, order events, provider errors, incidents, security events, and configuration changes. Sensitive values MUST be redacted.

## Accessibility and UX Requirements

- UI MUST target WCAG 2.2 AA.
- Commands MUST use clear controls, disabled states, confirmations, and step-up authentication when required.
- Profit-focused or manipulative design patterns MUST NOT be used.
- Data freshness and degraded modes MUST be visible without relying on color alone.
