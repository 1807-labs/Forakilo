# FKL-014: Model Registry and Promotion Gates

Epic: MLOps
Priority: P1
Target release phase: MVP
Status: Planned
Estimate: 8

## User Story

As a risk approver, I want model registry and promotion gates so that candidates can be evaluated without silently entering live execution.

## Business Value

Prevents uncontrolled model lifecycle changes.

## Context

Automated retraining may create candidates but cannot auto-promote to live.

## In Scope

MLflow registry metadata, model cards, approval states, shadow/paper promotion, suspension, rollback metadata, and audit events.

## Out of Scope

Live model promotion automation.

## Acceptance Criteria

- Registered model includes artifact fingerprint, dataset, feature, code, environment, metrics, owner, and stage.
- Promotion to shadow or paper requires approval evidence.
- Live eligibility is blocked unless paper-to-live gates pass.
- Suspension and rollback metadata are available.

## Negative Acceptance Criteria

- Retraining job cannot change champion live model directly.

## Security Requirements

Registry writes are authorized and audited.

## Privacy Requirements

Model cards avoid unnecessary personal data.

## Data Requirements

Registry and model-card schemas.

## Model Requirements

Validation report and calibration required.

## Risk Controls

Risk approval required for paper/live eligibility.

## Observability Requirements

Model stage change, suspension, rollback, and approval metrics.

## Accessibility Requirements

Model status is readable on dashboard.

## Dependencies

FKL-008.

## Assumptions

MLflow is available locally or in controlled environment.

## Edge Cases

Artifact missing, fingerprint mismatch, stale candidate, rollback model unavailable.

## Test Notes

Registry permission, promotion-state, and rollback tests.

## Documentation Impact

Update model registry docs.

## Definition of Ready

Promotion state machine approved.

## Definition of Done

No candidate can bypass approval gates.
