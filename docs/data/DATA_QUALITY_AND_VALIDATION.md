# Data Quality and Validation

Purpose: define quality controls for data used by Forakilo.
Scope: market data, macro data, provider account data, features, datasets, and inference inputs.
Audience: data engineers, ML engineers, QA, and risk reviewers.
Assumptions: bad data can cause financial loss and invalid model evaluation.
Dependencies: [Data Contracts](DATA_CONTRACTS_AND_SCHEMAS.md), [Model Validation](../ml/MODEL_VALIDATION.md).
Unresolved decisions: exact quality thresholds per provider and instrument.

## Required Checks

- Missing candles, missing ticks, duplicate records, out-of-order events, late events, and replay duplication.
- Revised macro observations and vintage-time correctness.
- Incorrect symbol mappings, instrument renames, delistings, and provider schema changes.
- Time-zone errors, daylight-saving errors, clock skew, and stale quotes.
- Negative or impossible prices, volumes, balances, fees, or quantities.
- Price spikes, inconsistent decimals, precision loss, corrupt payloads, and training-serving skew.
- Cross-tenant leakage and unauthorized dataset access.

## Quality Outcomes

| Outcome | Meaning | System behavior |
| --- | --- | --- |
| Pass | Data meets contract and freshness thresholds. | Data may flow to downstream systems. |
| Warn | Data has non-blocking anomaly. | Surface alert and record quality event. |
| Quarantine | Data violates blocking rule. | Stop downstream use until reviewed or corrected. |
| Fail closed | Data is unsafe for trading. | Expire signals and reject new execution. |

## Validation Tooling

Great Expectations GX Core is selected for declarative data-quality suites. Custom validators MAY be added for provider sequencing, financial precision, point-in-time leakage, and trading-specific checks.

## Verification

Quality suites MUST run in CI for fixtures, during ingestion for provider data, before dataset creation, before model training, and before live/paper inference.
