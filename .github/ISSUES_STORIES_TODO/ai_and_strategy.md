# FKL-008: Baseline Model and Strategy Evaluation

Epic: Intelligence
Priority: P1
Target release phase: MVP
Status: Planned
Estimate: 13

## User Story

As a quantitative developer, I want to train and evaluate a simple baseline model or strategy so that Forakilo can generate auditable paper-trading signals without overclaiming performance.

## Business Value

Provides the first intelligence path while prioritizing reproducibility and model risk controls.

## Context

The original story referenced high-probability signals and deep-learning options. The normalized story requires simple baselines first.

## In Scope

Baseline rules, scikit-learn baseline, XGBoost candidate only if justified, evaluation report, calibration, abstention, model card, and registration.

## Out of Scope

Reinforcement learning, deep learning, hosted LLM trading intelligence, and live promotion.

## Acceptance Criteria

- Training uses approved point-in-time datasets.
- Baseline and candidate metrics are reported with uncertainty and costs.
- Model outputs `BUY`, `SELL`, or `HOLD` only through a documented signal policy.
- Low confidence, poor calibration, drift, or stale features produce `HOLD`.
- Model card and registry metadata are created.

## Negative Acceptance Criteria

- In-sample results alone cannot approve a model.
- Candidate model cannot promote directly into live execution.

## Security Requirements

Model artifacts have fingerprints and access controls.

## Privacy Requirements

Training data excludes unnecessary personal data.

## Data Requirements

Dataset, feature, label, and environment lineage.

## Model Requirements

Validation, calibration, baseline comparison, and model card.

## Risk Controls

Deterministic risk controls remain separate from model output.

## Observability Requirements

Training run, metrics, drift, calibration, and abstention telemetry.

## Accessibility Requirements

Model results displayed in dashboard must be understandable without misleading profit emphasis.

## Dependencies

FKL-007, FKL-016.

## Assumptions

First model is paper-only.

## Edge Cases

Class imbalance, regime collapse, unstable feature importance, label leakage.

## Test Notes

Leakage, validation, reproducibility, and model-card tests.

## Documentation Impact

Update model docs and AI risk register.

## Definition of Ready

Prediction target, horizon, and label policy are approved.

## Definition of Done

Model candidate has reproducible evaluation and cannot bypass gates.
