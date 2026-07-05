# Data Lineage and Retention

Purpose: define lineage, retention, archival, deletion, backup, and restore requirements.
Scope: provider data, datasets, features, models, user data, audit data, and reconciliation records.
Audience: data engineers, privacy reviewers, operations, and legal counsel.
Assumptions: provider terms may impose retention and redistribution limits; personal data is subject to privacy obligations.
Dependencies: [Data Retention Policy](../legal/DATA_RETENTION_POLICY.md), [Backup and Disaster Recovery](../operations/BACKUP_AND_DISASTER_RECOVERY.md).
Unresolved decisions: final retention periods and legal hold process.

## Lineage Requirements

Every dataset, feature set, model artifact, signal, and backtest report MUST reference:

- Source provider, endpoint, instrument, and request window.
- Raw data version or content fingerprint.
- Contract version and validation result.
- Code version and environment version.
- Processing time and operator/job identity.
- Approval and retention class.

## Retention Classes

| Class | Examples | Default stance |
| --- | --- | --- |
| User personal data | profile, auth metadata, preferences | Minimize and retain only as needed. |
| Credential metadata | masked key metadata, validation history | Retain for audit; never store plaintext. |
| Raw provider data | market payloads, macro records | Retain only if terms permit. |
| Audit and trading records | orders, fills, risk decisions, approvals | Retain for compliance evidence subject to legal review. |
| Model artifacts | models, metrics, cards, datasets | Retain by lifecycle and rollback needs. |

## Restore Testing

Backups MUST be periodically restored into isolated environments and verified for referential integrity, audit readability, and secret redaction.
