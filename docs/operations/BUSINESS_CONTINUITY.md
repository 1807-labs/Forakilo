# Business Continuity

Purpose: define continuity expectations for Forakilo operations.
Scope: provider outages, cloud outages, staffing gaps, data failures, security incidents, and legal restrictions.
Audience: operators, product owners, risk reviewers, and legal counsel.
Assumptions: Forakilo must remain able to halt risky actions before maintaining feature availability.
Dependencies: [Incident Response](INCIDENT_RESPONSE_PLAN.md), [Backup and Disaster Recovery](BACKUP_AND_DISASTER_RECOVERY.md).
Unresolved decisions: continuity staffing, provider alternatives, and customer communications.

## Continuity Principles

- Preserve user capital safety before service availability.
- Disable live/paper execution if state is unsafe.
- Keep users informed about degraded data, provider outages, and disabled actions.
- Maintain private security and legal escalation channels.
- Document provider exit strategies for every approved third-party dependency.

## Continuity Scenarios

Provider outage, cloud region outage, database loss, credential compromise, model registry corruption, data provider terms change, legal restriction, key staff unavailability, and CI/CD compromise.
