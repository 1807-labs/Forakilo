# Data Architecture

Purpose: define Forakilo's point-in-time data architecture.
Scope: market data, macro data, normalized data, features, datasets, inference inputs, audit records, and artifacts.
Audience: data engineers, ML engineers, quantitative researchers, and reviewers.
Assumptions: provider data may be incomplete, delayed, revised, or restricted by terms.
Dependencies: [Data Flow](../architecture/DATA_FLOW.md), [Data Quality](DATA_QUALITY_AND_VALIDATION.md), [Sources](../research/SOURCES.md).
Unresolved decisions: exact table schemas, object-store layout, and provider-specific retention limits.

## Storage Zones

| Zone | Purpose | Mutability |
| --- | --- | --- |
| Raw immutable | Store original provider payloads and metadata. | Append-only with correction records. |
| Validated | Store payloads that passed contract checks. | Append-only. |
| Normalized | Store canonical market/account/event records. | Versioned corrections only. |
| Feature-ready | Store inputs approved for feature calculation. | Rebuildable from lineage. |
| Training datasets | Store point-in-time datasets and labels. | Immutable by version. |
| Backtesting datasets | Store replayable data with cost assumptions. | Immutable by version. |
| Live inference inputs | Store latest approved inputs and freshness state. | Mutable with audit trail. |
| Audit/reconciliation | Store order, fill, balance, position, risk, and user events. | Append-only. |
| Model artifacts | Store models, metrics, cards, and signatures/fingerprints. | Immutable by version. |

## Time Semantics

Every relevant record SHOULD capture event time, provider time, exchange time, ingestion time, processing time, effective time, and revision/vintage time when applicable.

## Data Safety Rules

- Point-in-time correctness MUST be enforced for training and backtesting.
- Provider terms MUST be checked before caching, archiving, or redistributing data.
- Raw data MUST be auditable back to provider, endpoint, credentials/environment, request, and response metadata.
- Cross-tenant leakage MUST be prevented by tenant/user scoping and authorization checks.
