# FKL-006: Data Quality Validation and Quarantine

Epic: Data
Priority: P0
Target release phase: MVP
Status: Planned
Estimate: 8

## User Story

As a risk-conscious user, I want bad or stale market data quarantined so that unsafe signals and orders are not produced from untrusted inputs.

## Business Value

Prevents data failures from becoming trading failures.

## Context

Data-quality rules are required before model or strategy work.

## In Scope

Schema checks, missing data, duplicates, out-of-order events, stale quotes, impossible values, quarantine, and alerts.

## Out of Scope

Complex anomaly detection beyond MVP rules.

## Acceptance Criteria

- Invalid data fails contract validation.
- Blocking failures quarantine data.
- Downstream signals expire when required data is stale.
- Quality events are visible to dashboard and audit.

## Negative Acceptance Criteria

- Quarantined data is not used for training, backtesting, or inference.

## Security Requirements

Quality events do not leak secrets or unrelated user data.

## Privacy Requirements

Tenant/user scoping is preserved in quality records.

## Data Requirements

Quality result schema and reason codes.

## Model Requirements

Model training requires passing data-quality reports.

## Risk Controls

Data-quality failure blocks new execution.

## Observability Requirements

Quality pass/warn/quarantine/fail-closed metrics.

## Accessibility Requirements

Dashboard warnings must be understandable without color alone.

## Dependencies

FKL-005.

## Assumptions

GX Core is available for declarative suites.

## Edge Cases

Late events, revised macro data, clock skew, delisting.

## Test Notes

Data-quality fixture suite.

## Documentation Impact

Update data quality documentation.

## Definition of Ready

Initial contracts and failure policies exist.

## Definition of Done

Quality gates block downstream unsafe data.
