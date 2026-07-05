# AI Risk Register

Purpose: identify and control AI/model risks specific to Forakilo.
Scope: data, model, retraining, monitoring, promotion, and user interpretation risks.
Audience: ML engineers, risk reviewers, security reviewers, product owners, and operators.
Assumptions: NIST AI RMF is used as the organizing framework.
Dependencies: [Sources](../research/SOURCES.md), [Model Strategy](MODEL_STRATEGY.md), [Risk Management Policy](../trading/RISK_MANAGEMENT_POLICY.md).
Unresolved decisions: risk appetite thresholds and approval owners.

| ID | Risk | Impact | Control | Test/monitoring |
| --- | --- | --- | --- | --- |
| AIR-001 | Look-ahead leakage | Misleading model performance | Point-in-time datasets and leakage tests | Validation gate |
| AIR-002 | Overfitting | Unsafe strategy confidence | Baselines, walk-forward splits, complexity limits | Model validation report |
| AIR-003 | Poor calibration | Oversized risk based on false confidence | Calibration checks and confidence floors | Calibration dashboard |
| AIR-004 | Drift | Model degrades in new regime | Drift monitoring and retraining triggers | Evidently/custom metrics |
| AIR-005 | Data poisoning | Manipulated signals | Provider anomaly checks and quarantine | Data-quality alerts |
| AIR-006 | Automated promotion error | Unsafe live model | Human and risk approval gates | Promotion workflow tests |
| AIR-007 | Explainability gap | Unreviewable decisions | Model cards and feature importance/stability | Review checklist |
| AIR-008 | Feedback loop | Self-generated labels contaminate training | Dataset isolation and lineage | Dataset audit |
| AIR-009 | LLM prompt injection | Operator misinformation if LLM added | LLM isolation and no execution authority | Threat-model test |
| AIR-010 | User over-trust | Financial harm | Risk disclosure and conservative dashboard copy | UX/content review |
