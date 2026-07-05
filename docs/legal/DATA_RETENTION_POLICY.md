# Data Retention Policy

This is a working technical draft for product planning and is not a substitute for qualified legal advice.

Purpose: define retention principles for user, trading, audit, data, and model records.
Scope: repository planning and future product implementation.
Audience: legal counsel, privacy reviewers, data engineers, operations, and product owners.
Assumptions: exact periods require legal and provider-term review.
Dependencies: [Data Lineage and Retention](../data/DATA_LINEAGE_AND_RETENTION.md), [Privacy Policy Draft](PRIVACY_POLICY_DRAFT.md).
Unresolved decisions: retention schedule, legal hold process, deletion exceptions, and provider-specific obligations.

## Principles

- Retain personal data only as long as needed for stated purposes, security, legal, audit, or operational obligations.
- Retain audit and trading records long enough to support dispute, compliance, incident, and reconciliation needs, subject to legal review.
- Delete or anonymize data when retention purpose expires unless legal hold applies.
- Respect provider terms for market-data caching, archiving, derived works, and redistribution.
- Test backup restore and deletion workflows.

## Retention Schedule Status

Exact retention periods are intentionally unresolved and MUST be approved before production launch.
