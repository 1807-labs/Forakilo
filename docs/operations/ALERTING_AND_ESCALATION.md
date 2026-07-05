# Alerting and Escalation

Purpose: define alert categories and escalation behavior.
Scope: security, provider, data, model, risk, execution, reconciliation, infrastructure, and compliance alerts.
Audience: operators, engineers, security reviewers, and risk owners.
Assumptions: on-call staffing is not yet defined.
Dependencies: [Incident Response](INCIDENT_RESPONSE_PLAN.md), [Service Level Objectives](SERVICE_LEVEL_OBJECTIVES.md).
Unresolved decisions: paging vendor, rotation, severity names, and escalation contacts.

## Severity

| Severity | Meaning | Response |
| --- | --- | --- |
| SEV-1 | Live-capital, credential, security, or data-integrity emergency | Immediate escalation, freeze risky actions, incident commander. |
| SEV-2 | Paper/sandbox execution safety, provider outage, major model/data failure | Prompt response and stakeholder notification. |
| SEV-3 | Degraded service or warning threshold | Triage during support hours. |
| SEV-4 | Informational trend | Backlog or monitoring review. |

## Required Alerts

Account takeover indicators, credential compromise, secret leak, provider outage, stale data, model suspension, risk circuit breaker, kill switch, unknown order outcome, reconciliation mismatch, audit write failure, backup failure, CI supply-chain failure, and incident notification deadline risk.
