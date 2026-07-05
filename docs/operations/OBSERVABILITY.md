# Observability

Purpose: define logs, metrics, traces, and events required for Forakilo.
Scope: authentication, dashboard, data, models, signals, risk, execution, reconciliation, alerts, and audit.
Audience: engineers, operators, security reviewers, and risk reviewers.
Assumptions: OpenTelemetry is the portable baseline.
Dependencies: [Sources](../research/SOURCES.md), [Service Level Objectives](SERVICE_LEVEL_OBJECTIVES.md).
Unresolved decisions: observability backend and retention periods.

## Required Context Fields

Telemetry MUST include correlation ID, environment, paper/live mode, user/tenant context where allowed, strategy version, model version, dataset version, feature version, signal ID, order ID, provider order ID, reconciliation ID, decision outcome, risk rejection reason, data freshness, latency, error type, and provider name.

## Redaction

Logs, metrics, traces, screenshots, and exported diagnostics MUST NOT contain secrets, full provider credentials, password material, recovery codes, full tokens, or unnecessary personal data.

## Signals

- Auth success/failure and suspicious-login events.
- Provider connection status and rate limits.
- Data freshness, gaps, quarantine, and contract failures.
- Model drift, calibration, performance, and suspension.
- Signal creation, expiry, rejection, and consumption.
- Risk approval/rejection and circuit breakers.
- Order lifecycle, provider responses, fills, cancellations, and unknown outcomes.
- Reconciliation success/failure.
- Kill switch and incident events.
