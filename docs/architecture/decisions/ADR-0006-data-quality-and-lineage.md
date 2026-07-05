# ADR-0006: Data Quality and Lineage

Status: Accepted
Date: 2026-07-04

Purpose: establish point-in-time data correctness as a core architecture decision.
Scope: ingestion, validation, datasets, features, training, backtesting, and inference.
Audience: data engineers, ML engineers, quantitative researchers, and reviewers.
Assumptions: misleading data can directly cause unsafe trading decisions.
Dependencies: [Data Architecture](../../data/DATA_ARCHITECTURE.md), [Data Quality and Validation](../../data/DATA_QUALITY_AND_VALIDATION.md).
Unresolved decisions: exact data-contract format and quality tooling configuration.

## Decision

Forakilo will use explicit data zones, schema versions, quality thresholds, lineage metadata, content fingerprints, and time semantics for every market, macro, feature, dataset, model, signal, and execution record.

## Rationale

Trading and model validation require reproducible point-in-time datasets. Forakilo must prevent leakage, training-serving skew, stale quotes, revised macro data misuse, and cross-tenant data exposure.

## Consequences

- Every record SHOULD capture event time, provider time, ingestion time, and processing time where available.
- Macro features MUST use vintage/effective time when revisions are relevant.
- Failed data quality checks MUST quarantine data and fail closed for dependent signals.

## Alternatives Rejected

- Ad hoc CSV and notebook datasets: rejected because they cannot provide durable lineage or auditability.
- Feature store first: deferred until feature reuse and serving scale justify it.
