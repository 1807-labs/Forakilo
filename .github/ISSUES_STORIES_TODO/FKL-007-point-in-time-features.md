# FKL-007: Point-in-Time Feature Engineering

Epic: Intelligence
Priority: P1
Target release phase: MVP
Status: Planned
Estimate: 8

## User Story

As a quantitative developer, I want point-in-time feature engineering so that models and backtests do not use future or revised information.

## Business Value

Reduces leakage and misleading performance reports.

## Context

Feature generation must follow data-quality and lineage controls.

## In Scope

Feature definitions, feature versioning, freshness, lineage, leakage checks, and feature-ready datasets.

## Out of Scope

Full feature store and deep learning.

## Acceptance Criteria

- Each feature has ID, version, source data, window, null policy, and freshness rule.
- Features are reproducible from source lineage.
- Leakage tests fail centered windows or future data usage.
- Feature generation records code and environment versions.

## Negative Acceptance Criteria

- Revised macro data cannot be used without vintage-time correctness.

## Security Requirements

Feature data respects tenant boundaries.

## Privacy Requirements

Personal data is excluded unless specifically approved.

## Data Requirements

Feature contract and feature catalogue entries.

## Model Requirements

Models reference feature version.

## Risk Controls

Stale features force signal abstention or expiry.

## Observability Requirements

Feature freshness and failure metrics.

## Accessibility Requirements

None.

## Dependencies

FKL-005, FKL-006.

## Assumptions

Initial features are market and risk features only.

## Edge Cases

Missing windows, daylight-saving changes, instrument rename.

## Test Notes

Leakage, reproducibility, and time-boundary tests.

## Documentation Impact

Update data feature catalogue.

## Definition of Ready

Feature definitions and source contracts are approved.

## Definition of Done

Features pass leakage and lineage checks.
