# FKL-013: Dashboard Global Status and Core Views

Epic: Dashboard
Priority: P1
Target release phase: MVP
Status: Planned
Estimate: 13

## User Story

As a user, I want a dashboard that shows market, account, strategy, model, risk, execution, and system health so that I can understand Forakilo's current state.

## Business Value

Makes safety and operational state visible.

## Context

Paper/live mode confusion is a critical UI risk.

## In Scope

Global status, portfolio, trading, market intelligence, model operations, risk, audit, and operations views for MVP data.

## Out of Scope

Marketing landing page and mobile-native app.

## Acceptance Criteria

- Dashboard shows paper/live mode, environment, trading enabled, kill switch, data freshness, connectivity, reconciliation, alerts, model version, and strategy version.
- Paper and live states are visually distinct.
- Core views show the fields defined in dashboard specification.
- Protected dashboard requires authentication.

## Negative Acceptance Criteria

- Dashboard does not imply profit certainty or hide risk state.
- Stale data is not displayed as fresh.

## Security Requirements

Server-side authorization for all dashboard data.

## Privacy Requirements

Sensitive data is redacted and scoped.

## Data Requirements

Dashboard read models and freshness timestamps.

## Model Requirements

Model status includes version, calibration, drift, and suspension.

## Risk Controls

Risk and kill-switch state is always visible.

## Observability Requirements

Dashboard load, data freshness, and client error metrics.

## Accessibility Requirements

WCAG 2.2 AA target, keyboard navigation, color-independent status.

## Dependencies

FKL-001, FKL-004, FKL-010, FKL-012.

## Assumptions

Next.js stack is selected by ADR-0003.

## Edge Cases

Stale API response, disconnected provider, unreadable chart labels, long instrument names.

## Test Notes

UI, API, accessibility, and authz tests.

## Documentation Impact

Update dashboard specification if implementation narrows scope.

## Definition of Ready

Dashboard data contracts exist.

## Definition of Done

Accessible dashboard displays safe status without overlap or stale ambiguity.
