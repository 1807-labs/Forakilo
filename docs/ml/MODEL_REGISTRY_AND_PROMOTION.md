# Model Registry and Promotion

Purpose: define registry, approval, promotion, rollback, suspension, and retirement controls.
Scope: model artifacts from research through live eligibility.
Audience: ML engineers, risk approvers, security reviewers, and operators.
Assumptions: MLflow is the baseline registry; approval workflows are not yet implemented.
Dependencies: [Model Card Template](MODEL_CARD_TEMPLATE.md), [Paper to Live Gate](../trading/PAPER_TO_LIVE_TRADING_GATE.md).
Unresolved decisions: exact approval tool and artifact signing method.

## Registry Metadata

Each model artifact MUST include:

- Model ID, version, owner, stage, status, and approval history.
- Code version, environment version, dataset version, feature version, and artifact fingerprint.
- Intended use, prohibited use, supported markets, supported regimes, and limitations.
- Training/evaluation data, metrics, calibration, risk controls, and failure modes.
- Rollback target and retirement criteria.

## Promotion Gates

| Stage | Required gate |
| --- | --- |
| Research | Reproducible training and data lineage. |
| Registered | Model card, metrics, and artifact fingerprint. |
| Shadow | Validation report and security review. |
| Paper | Risk approval, backtest report, and paper-execution plan. |
| Live eligible | Full paper-to-live gate, human approval, rollback, and monitoring. |

## Rollback and Suspension

Any model can be suspended by risk, security, operations, or automated severe-failure policy. Rollback MUST be immediate for live-eligible models.
