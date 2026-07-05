# ADR-0007: MLOps Stack

Status: Accepted
Date: 2026-07-04

Purpose: select the initial model lifecycle tooling.
Scope: baseline models, experiments, registry, monitoring, retraining, and promotion.
Audience: ML engineers, risk reviewers, and operators.
Assumptions: simple and interpretable models should precede complex models; automated retraining is allowed but direct live promotion is not.
Dependencies: [Model Strategy](../../ml/MODEL_STRATEGY.md), [Model Registry and Promotion](../../ml/MODEL_REGISTRY_AND_PROMOTION.md).
Unresolved decisions: exact artifact store, GPU strategy, and model-serving process.

## Decision

Use scikit-learn for baseline models, XGBoost as the primary tabular gradient-boosting candidate, MLflow for experiment tracking and model registry, Evidently for monitoring evaluation, and Optuna only after leakage-safe validation exists. PyTorch is deferred.

## Rationale

The MVP needs reproducible baselines, calibration, abstention, and conservative promotion gates more than model complexity.

## Consequences

- Candidate models MUST beat simple baselines under walk-forward validation before paper deployment.
- Automated retraining MAY create and evaluate candidates but MUST NOT silently promote candidates into live capital execution.
- Model cards MUST be produced for every registered candidate.

## Alternatives Rejected

- Reinforcement learning in MVP: rejected due validation and safety complexity.
- Deep learning first: rejected until tabular/rules-based baselines prove insufficient.
- Hosted LLM trading intelligence: rejected for real-time market, risk, and execution paths.
