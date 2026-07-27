# ADR 0004: Data and experiment storage

**Status: Accepted**  
**Approval date:** 2026-07-26  
**Approver:** Uchenna Emmanuel Anozie, Product Owner

## Context

Research must be reproducible without committing unlicensed market data or treating notebooks as strategy sources.

## Decision being considered

Define historical data requirements, normalization/error policy and staged experiment storage.

## Available options

- JSON/CSV files only.
- Parquet datasets, immutable JSON manifests, content-addressed artifacts and DuckDB analysis.
- Put all data/results in PostgreSQL.
- Cloud object store and warehouse from the start.

## Recommended option

Require source-identified completed bid and ask OHLC bars. Midpoint may be derived and labeled, never substituted silently. Normalize timestamps to UTC while retaining source timezone, market timezone, DST/calendar and bar-boundary metadata. Record source/version/license, acquisition timestamp, raw and normalized hashes, schema, symbol-properties version and transformation code version.

Reject a run on out-of-order or conflicting duplicate bars. Exact duplicates may be deterministically collapsed and counted. Missing bars reject the run by default. Fill-forward is permitted only when explicitly pre-registered, versioned and recorded in the run manifest with explicit flags. Validate bid/ask ordering and price precision.

Use synthetic fixtures initially. Licensed historical fixtures may be committed only when redistribution is explicitly permitted and provenance is recorded; otherwise store generation recipes/expected hashes, not data.

Store one immutable JSON manifest per experiment; content-address configuration/results/log summaries; use Parquet for normalized market data and large tables; use DuckDB for local queries/aggregates. Every run records product Git commit, LEAN commit/build, data hash, parameter set, dependency-lock hash, platform, random seed, cost models and window definition. Notebooks are disposable analysis clients, never production strategy sources.

Spread uses actual bid/ask where present. Fees, slippage, financing and latency are explicit scenario/model versions. No zero-cost implicit default is allowed.

## Reasons

This design is local, portable and auditable without premature service infrastructure. Columnar data and DuckDB suit research scale; manifests and hashes preserve lineage.

## Consequences

Data ingestion must be strict and licensed data may live outside Git. Artifact retention and schema migration policies are needed. Cost scenarios may produce multiple results per strategy run.

## Risks

Content-addressed stores need garbage-collection/retention rules. DuckDB concurrency is unsuitable for operational state. Vendor revisions can invalidate hashes and comparisons.

## Alternatives rejected

CSV/JSON-only is inefficient and weakly typed for large data. PostgreSQL is unnecessary for immutable research datasets. Cloud-first infrastructure is premature.

## Questions requiring human approval

The storage stack, synthetic-first fixture policy, missing-bar default and controlled fill-forward exception are approved. Historical source/license selection and cost scenarios remain later pre-registered evidence decisions.

## Evidence required before acceptance

Data-source/license matrix, proposed schemas/manifests, hash procedure, DST/bar-boundary examples, anomaly policy examples and cost-model inventory.

## Explicit implementation impact

If accepted later, this determines ingestion validation, artifact paths, manifest schemas and research queries. No data, database or storage artifact is created in Phase 0.
