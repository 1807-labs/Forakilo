# Personas and User Journeys

Purpose: define the users and journeys Forakilo must support.
Scope: MVP and controlled-beta personas.
Audience: product, design, engineering, testing, and risk reviewers.
Assumptions: initial users are technically capable and willing to review risk disclosures; consumer suitability still requires legal review.
Dependencies: [Dashboard Specification](DASHBOARD_SPECIFICATION.md), [Account Lifecycle](../security/ACCOUNT_AND_SESSION_LIFECYCLE.md).
Unresolved decisions: exact target customer eligibility and onboarding checks.

## Personas

| ID | Persona | Need | Risk |
| --- | --- | --- | --- |
| P-001 | Research-focused retail trader | Evaluate data, backtests, and paper strategies before risking capital. | May over-trust historical performance. |
| P-002 | Quantitative developer | Build and validate features, models, and strategies. | May optimize into leakage or overfit results. |
| P-003 | Risk administrator | Configure limits, gates, and kill switches. | Misconfiguration can allow unsafe exposure. |
| P-004 | Operator | Monitor data, execution, model, provider, and system health. | Missed alerts can leave trading in degraded state. |
| P-005 | Security administrator | Manage sensitive access, keys, and incident response. | Privilege abuse or account compromise. |
| P-006 | Read-only auditor | Review audit trails, approvals, and compliance evidence. | Incomplete evidence weakens accountability. |

## MVP User Journey

1. User registers, verifies email, enables MFA or passkey, and accepts risk disclosures.
2. User connects approved sandbox or demo credentials with no withdrawal permission.
3. Forakilo validates provider connectivity and account state.
4. User selects an approved instrument and paper strategy.
5. Market data is ingested, validated, and shown on the dashboard.
6. Strategy/model produces a signal with confidence, expiry, and model/data versions.
7. Deterministic risk controls approve or reject the proposed paper order.
8. Paper execution simulates fills and updates portfolio state.
9. Reconciliation compares expected and observed paper account state.
10. User reviews performance, risk, data health, model health, and audit history.

## High-Impact Journey

High-impact actions such as adding credentials, enabling live trading, increasing risk limits, disabling a kill switch, promoting a model, changing execution policy, exporting sensitive data, or deleting an account MUST require step-up authentication and audit capture.
