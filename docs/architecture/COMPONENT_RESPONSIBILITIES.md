# Component Responsibilities

Purpose: define component ownership and responsibilities.
Scope: target modular monolith components.
Audience: engineers, reviewers, and maintainers.
Assumptions: components are logical modules before code exists.
Dependencies: [System Architecture](SYSTEM_ARCHITECTURE.md), [Trust Boundaries](TRUST_BOUNDARIES.md).
Unresolved decisions: exact package/module names.

| Component | Plane | Responsibilities | Must not do |
| --- | --- | --- | --- |
| Identity | Control | Users, credentials, MFA/passkeys, sessions, roles, recovery. | Submit orders or access provider secrets directly. |
| Provider Credential Vault | Control/Security | Encrypt, rotate, validate, mask, revoke, and audit provider credentials. | Request withdrawal permissions. |
| Provider Gateway | Data/Trading | Normalize provider APIs, rate limits, status, errors, and idempotency. | Hide provider-specific execution semantics. |
| Market Data Ingestion | Data | Raw capture, normalization, validation, gap detection, replay. | Mutate raw records without correction history. |
| Feature Pipeline | Intelligence | Point-in-time features and feature freshness. | Use future or revised data incorrectly. |
| Model Training | Intelligence | Baselines, candidates, metrics, artifacts, model cards. | Promote to live without gates. |
| Signal Service | Intelligence/Trading | Signal generation, expiry, deduplication, confidence, context. | Bypass risk controls. |
| Risk Engine | Trading | Position sizing, exposure, spread, slippage, drawdown, circuit breakers. | Depend solely on model confidence. |
| Paper Execution | Trading | Simulated orders, fills, balances, positions, fees, and reconciliation. | Represent simulated state as live state. |
| Audit Log | Governance | Immutable evidence for significant events. | Store secrets or mutable business state only. |
| Observability | Governance | Metrics, logs, traces, alerts, dashboards. | Log secrets or sensitive payloads. |
