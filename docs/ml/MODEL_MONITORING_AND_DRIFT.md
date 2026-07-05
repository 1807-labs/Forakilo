# Model Monitoring and Drift

Purpose: define monitoring for deployed and evaluated models.
Scope: shadow, paper, and future live model monitoring.
Audience: ML engineers, operators, risk reviewers, and security reviewers.
Assumptions: drift detection is advisory unless tied to explicit risk policy.
Dependencies: [Observability](../operations/OBSERVABILITY.md), [Training Pipeline](TRAINING_AND_RETRAINING_PIPELINE.md).
Unresolved decisions: exact thresholds and monitoring storage.

## Monitoring Signals

- Data drift, prediction drift, label drift, and concept drift.
- Calibration error and confidence distribution.
- Abstention rate and signal expiry rate.
- Feature freshness and missing-feature rate.
- Live-to-backtest divergence.
- Regime-specific performance and collapse.
- Data poisoning and anomalous provider behavior indicators.
- Performance degradation, drawdown, turnover, and risk rejection rates.

## Actions

| Condition | Action |
| --- | --- |
| Mild drift | Alert and annotate model dashboard. |
| Persistent drift | Create candidate retraining job. |
| Severe calibration failure | Suspend affected model for new signals. |
| Data quality failure | Expire signals and fail closed. |
| Model-service failure | Use no model output; risk engine rejects model-dependent orders. |

## Observability Fields

Model events MUST include model version, dataset version, feature version, strategy version, environment, paper/live mode, correlation ID, decision outcome, confidence, calibration state, drift status, and owner.
