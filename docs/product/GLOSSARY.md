# Glossary

Purpose: define terms used across Forakilo documentation.
Scope: product, trading, data, ML, security, and operations terms.
Audience: all contributors and reviewers.
Assumptions: terms may be refined as implementation reveals better domain language.
Dependencies: [Documentation Index](../../DOCUMENTATION_INDEX.md).
Unresolved decisions: provider-specific terminology mappings.

## Normative Language

- MUST: required for implementation or approval.
- SHOULD: strongly recommended unless a documented exception is approved.
- MAY: optional capability or allowed implementation choice.
- MUST NOT: prohibited unless a later documented decision explicitly reverses it.

## Terms

- Abstention: model decision to produce `HOLD` or no actionable signal when confidence, calibration, data quality, or risk criteria are insufficient.
- Audit event: immutable record of a significant user, model, data, risk, security, or execution state transition.
- Backtest: historical simulation of a strategy using point-in-time data and realistic cost assumptions.
- Champion model: currently approved model for a given strategy/environment.
- Challenger model: candidate model evaluated against the champion.
- Concept drift: change in the relationship between features and target.
- Data drift: change in the distribution of input data.
- Deterministic risk control: rule-based control that can reject execution without relying on model approval.
- Event time: time at which the market or provider event occurred.
- Ingestion time: time at which Forakilo received the event.
- Kill switch: control that stops new execution and may trigger protective operational actions.
- Live trading: trading against real capital through an approved provider.
- Model promotion: change that moves a model to a higher-impact stage such as shadow, paper, or live eligibility.
- Paper trading: simulated trading with no real capital at risk.
- Point-in-time correctness: using only information available at the relevant historical time.
- Provider time: timestamp supplied by an exchange, broker, or data provider.
- Shadow deployment: model runs beside approved logic without controlling execution.
- Step-up authentication: fresh stronger authentication required before high-impact action.
- Training-serving skew: difference between features used in training and features available during inference.
