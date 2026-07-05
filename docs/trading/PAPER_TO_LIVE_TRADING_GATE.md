# Paper to Live Trading Gate

Purpose: define mandatory gates before live trading can be enabled.
Scope: transition from paper/sandbox to limited live trading.
Audience: product owners, risk approvers, security reviewers, legal counsel, operators, and engineers.
Assumptions: live trading is disabled by default and unavailable until every gate passes.
Dependencies: [Risk Management Policy](RISK_MANAGEMENT_POLICY.md), [Model Registry and Promotion](../ml/MODEL_REGISTRY_AND_PROMOTION.md), [Legal Review Checklist](../legal/LEGAL_REVIEW_CHECKLIST.md).
Unresolved decisions: live provider, capital limits, instrument set, and approval owners.

## Required Gates

| Gate | Requirement |
| --- | --- |
| Legal | Product classification, jurisdiction, provider terms, disclosures, and user consent reviewed. |
| Security | Auth, authorization, credential vault, secrets, threat model, and incident process approved. |
| Data | Data quality, lineage, point-in-time correctness, and freshness controls passing. |
| Model | Validation, calibration, model card, drift monitoring, and rollback passing. |
| Backtest | Walk-forward, costs, slippage, spread, fees, partial fills, latency, and baseline comparison passing. |
| Paper | Paper/sandbox trading demonstrates order, fill, balance, position, fee, and reconciliation correctness. |
| Risk | Conservative limits, circuit breakers, kill switch, and fail-closed behavior tested. |
| Operations | Observability, alerts, runbooks, backup, incident response, and escalation ready. |
| Human approval | Product owner, risk approver, security approver, and operator sign-off recorded. |

## Initial Live Constraints

If approved, live trading MUST be limited to one approved venue, limited instruments, limited capital, limited exposure, no withdrawal permission, manual model promotion, and immediate kill-switch availability.
