# Service Level Objectives

Purpose: define initial reliability objectives for future implementation.
Scope: MVP and controlled beta services.
Audience: product owners, engineers, operators, and risk reviewers.
Assumptions: targets are proposed design objectives, not current measured performance.
Dependencies: [Observability](OBSERVABILITY.md), [Alerting](ALERTING_AND_ESCALATION.md).
Unresolved decisions: final targets after measurement and staffing review.

## Initial SLOs

| Area | User impact | Measurement | Initial target | Alert threshold | Degraded behavior |
| --- | --- | --- | --- | --- | --- |
| Authentication | Users cannot access platform | Successful auth requests excluding invalid credentials | 99.5% over 30 days for MVP service | Error spike over 5 minutes | Block protected actions and show status. |
| Dashboard freshness | User sees stale state | Age of latest displayed state | Key status under 30 seconds in paper mode | Freshness exceeds policy | Mark stale and disable actions. |
| Market data freshness | Unsafe signals | Provider event age | Instrument-specific freshness policy | Freshness breach | Expire signals and reject orders. |
| Signal generation | No new strategy decisions | Successful signal jobs | 99% scheduled runs in paper mode | Missed job window | Alert and keep previous signals expired. |
| Risk evaluation | Unsafe or blocked orders | Risk decision latency and errors | Decision success for valid paper requests | Error > policy | Reject execution. |
| Reconciliation | Unknown portfolio state | Reconciliation age and mismatch count | Reconcile after every execution event | Missed reconciliation | Block new execution. |
| Audit logging | Lost evidence | Durable audit write success | 99.9% for high-impact events | Any high-impact audit failure | Block high-impact action. |

## Error Budgets

Error budgets MUST NOT be used to justify unsafe trading. Any execution safety breach overrides availability goals.
