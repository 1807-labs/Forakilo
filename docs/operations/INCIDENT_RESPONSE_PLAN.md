# Incident Response Plan

Purpose: define how Forakilo responds to incidents.
Scope: security, privacy, data, model, trading, provider, and infrastructure incidents.
Audience: operators, security reviewers, maintainers, legal counsel, and product owners.
Assumptions: no production incident process exists yet.
Dependencies: [Alerting](ALERTING_AND_ESCALATION.md), [Security Policy](../../SECURITY.md), [Business Continuity](BUSINESS_CONTINUITY.md).
Unresolved decisions: incident commander roster, communications channels, and legal notification thresholds.

## Phases

1. Detect and triage.
2. Assign severity and incident commander.
3. Contain by disabling risky actions, revoking credentials, suspending models, or activating kill switch.
4. Preserve evidence and audit logs.
5. Eradicate root cause.
6. Recover through verified deploy, restore, reconciliation, or rollback.
7. Communicate to affected users, providers, regulators, or partners if required.
8. Run post-incident review and create follow-up work.

## Trading Safety

Any incident affecting provider credentials, account state, data freshness, order state, model integrity, risk controls, or audit logging MUST block new live execution until resolved.
