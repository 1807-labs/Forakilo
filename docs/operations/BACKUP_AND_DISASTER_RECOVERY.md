# Backup and Disaster Recovery

Purpose: define backup and recovery expectations.
Scope: databases, object storage, model artifacts, configuration, audit records, and documentation.
Audience: operations, engineers, security reviewers, and product owners.
Assumptions: production infrastructure is not selected.
Dependencies: [Data Retention Policy](../legal/DATA_RETENTION_POLICY.md), [Business Continuity](BUSINESS_CONTINUITY.md).
Unresolved decisions: RPO/RTO targets, backup tooling, encryption keys, and restore schedule.

## Requirements

- Backups MUST be encrypted and access-controlled.
- Restore tests MUST be performed in isolated environments.
- Audit and trading records MUST be restorable with referential integrity.
- Secret material MUST be restored through approved secrets processes, not from logs.
- Model artifacts and datasets MUST retain lineage and fingerprints after restore.

## Recovery Priorities

1. Credential and account safety.
2. Audit and trading evidence.
3. User access and dashboard status.
4. Data ingestion and reconciliation.
5. Model and paper trading workflows.
