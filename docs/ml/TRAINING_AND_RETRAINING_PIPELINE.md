# Training and Retraining Pipeline

Purpose: define the model training and candidate retraining process.
Scope: datasets, training, evaluation, registration, shadow, paper, and promotion gates.
Audience: ML engineers, data engineers, risk reviewers, and operators.
Assumptions: automated retraining can create candidates but cannot silently promote them to live execution.
Dependencies: [Model Registry and Promotion](MODEL_REGISTRY_AND_PROMOTION.md), [Data Lineage](../data/DATA_LINEAGE_AND_RETENTION.md).
Unresolved decisions: orchestration tool and compute environment.

## Pipeline Stages

1. Select approved point-in-time dataset.
2. Verify data contract, quality, lineage, and feature freshness.
3. Build labels without leakage.
4. Train baselines and candidate models with reproducible environment metadata.
5. Evaluate temporal splits, walk-forward results, costs, calibration, stability, and tail risk.
6. Register artifacts, metrics, model card, and fingerprints in MLflow.
7. Compare candidate to baseline and champion.
8. Deploy to shadow or paper only after approval.
9. Promote to live eligibility only through documented gates.

## Retraining Triggers

Each trigger MUST define metric, baseline, threshold, minimum sample, evaluation window, persistence requirement, cooldown, false-positive handling, action, escalation, and rollback condition.

| Trigger | Metric | Action |
| --- | --- | --- |
| Data drift | Feature distribution shift | Create candidate retraining job after persistence threshold. |
| Concept drift | Degraded labeled performance | Escalate and train candidate; do not auto-promote. |
| Calibration decay | Calibration error exceeds policy | Suspend model for affected strategy if severe. |
| Regime collapse | Regime-specific performance breach | Restrict model to approved regimes or abstain. |
| Data quality breach | Freshness/quality failure | Expire signals and block retraining until data is repaired. |
