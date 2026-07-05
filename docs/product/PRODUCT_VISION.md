# Product Vision

Purpose: define what Forakilo is intended to become.
Scope: product intent, safety posture, and success boundaries before implementation.
Audience: product owners, engineers, reviewers, risk approvers, and legal counsel.
Assumptions: Forakilo starts as a Canada-first, pre-development platform with no implemented trading capability.
Dependencies: [Scope and Non-Goals](SCOPE_AND_NON_GOALS.md), [Delivery Roadmap](../roadmap/DELIVERY_ROADMAP.md).
Unresolved decisions: operating model, approved providers, and live trading eligibility require legal and product approval.

## Vision

Forakilo is intended to become an authenticated AI-assisted quantitative market-analysis and trading-risk platform for cryptocurrency and foreign-exchange markets. It should help a user research market data, evaluate strategies, monitor model behavior, and operate paper trading before any controlled live execution is considered.

## Product Promise

Forakilo MUST prioritize capital preservation, operational correctness, traceability, controlled risk, privacy, and truthful performance reporting.

Forakilo MUST NOT promise returns, eliminate financial risk, or describe research results as proof of future performance.

## Governing Principles

- Protect capital before optimizing returns.
- Fail closed when execution safety is uncertain.
- Paper trading precedes live trading.
- Deterministic risk controls outrank model output.
- No model controls unrestricted capital.
- Point-in-time correctness outranks larger datasets.
- Reproducibility outranks impressive one-off results.
- Auditability outranks hidden automation.
- Security and privacy are product requirements.
- No withdrawal access in the initial product scope.

## Success Outcomes

- An authenticated user can safely connect approved sandbox or demo credentials.
- Market data is validated, time-stamped, lineage-tracked, and replayable.
- Strategies and models produce auditable signals with expiry and confidence metadata.
- Risk controls can reject unsafe orders independently of AI output.
- Paper trading can simulate order, fill, balance, position, fee, and reconciliation state.
- Candidate model retraining can be triggered and evaluated without silent live promotion.

## Current Reality

The repository is pre-development. It has documentation, backlog items, and a GPL-3.0 license, but no application code, dashboard, data pipeline, model pipeline, broker integration, tests, CI, or production deployment.
