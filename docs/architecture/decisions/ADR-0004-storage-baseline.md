# ADR-0004: Storage Baseline

Status: Accepted
Date: 2026-07-04

Purpose: select storage systems for transactional, time-series, cache, and artifact data.
Scope: MVP storage architecture.
Audience: data engineers, backend engineers, operations, and security reviewers.
Assumptions: initial volume is unknown; correctness and auditability outrank premature scale.
Dependencies: [Data Architecture](../../data/DATA_ARCHITECTURE.md), [Technology Evaluation](../../research/TECHNOLOGY_EVALUATION.md).
Unresolved decisions: managed database provider, backup tooling, and exact retention classes.

## Decision

Use PostgreSQL as the relational system of record. Use PostgreSQL partitioning for initial time-series storage and evaluate Apache-licensed TimescaleDB features only if volume and query patterns justify them. Use S3-compatible object storage for artifacts and immutable datasets.

## Rationale

PostgreSQL supports transactional integrity, auditing, relational constraints, and broad operations tooling. A PostgreSQL-centered baseline reduces moving parts while preserving a path to time-series optimization.

## Consequences

- Audit, account, order, fill, risk, and reconciliation records MUST be persisted transactionally.
- Raw market data MUST be immutable after ingestion except for explicit correction records.
- TimescaleDB Community features MUST NOT be used without license review.

## Alternatives Rejected

- InfluxDB as primary store: rejected because account, order, and audit data need relational integrity.
- Local filesystem as artifact store: rejected beyond local development because lineage and backup controls would be weaker.
