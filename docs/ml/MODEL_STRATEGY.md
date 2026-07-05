# Model Strategy

Purpose: define Forakilo's initial model approach.
Scope: prediction targets, baselines, candidates, abstention, explainability, and lifecycle.
Audience: ML engineers, quantitative researchers, risk reviewers, and product owners.
Assumptions: simple validated models are preferred before complex models; model output is advisory to deterministic controls.
Dependencies: [AI Risk Register](AI_RISK_REGISTER.md), [Model Validation](MODEL_VALIDATION.md), [ADR-0007](../architecture/decisions/ADR-0007-mlops-stack.md).
Unresolved decisions: first instrument, horizon, label, and strategy policy.

## Objective

The initial model objective is to produce calibrated, auditable probability estimates or regime labels that may inform paper-trading signals. The model MUST be able to abstain with `HOLD`.

## Target Definition

Every model must define:

- Market and instruments.
- Forecast horizon.
- Label construction.
- Baseline models.
- Candidate models.
- Features and exclusions.
- Transaction-cost assumptions.
- Evaluation metrics and calibration methods.
- Intended and prohibited use.

## Model Order

1. Rules-based and naive baselines.
2. scikit-learn interpretable baselines.
3. XGBoost tabular models if baselines justify complexity.
4. PyTorch only after a documented need and safe validation path.

## Prohibited MVP Model Behavior

- No reinforcement learning in MVP.
- No direct live order control by any model.
- No live promotion without human and gate approval.
- No hosted general-purpose LLM in trading, risk, or execution path.
