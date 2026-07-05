# Feature Catalogue

Purpose: list product features and release intent.
Scope: foundation through later releases.
Audience: product owners, engineers, testers, and roadmap reviewers.
Assumptions: features marked planned are not implemented.
Dependencies: [PRD](PRODUCT_REQUIREMENTS_DOCUMENT.md), [Epic and Release Map](EPIC_AND_RELEASE_MAP.md).
Unresolved decisions: detailed feature sequencing after MVP acceptance tests are written.

| ID | Feature | Release | Status | Verification |
| --- | --- | --- | --- | --- |
| F-001 | Account registration and login | MVP | Planned | Auth acceptance tests |
| F-002 | MFA/passkeys and recovery controls | MVP | Planned | Security tests and recovery abuse tests |
| F-003 | Exchange credential vault | MVP | Planned | Secret storage and audit tests |
| F-004 | Provider connection manager | MVP | Planned | Sandbox/demo contract tests |
| F-005 | Market data ingestion | MVP | Planned | Data-quality and replay tests |
| F-006 | Point-in-time feature pipeline | MVP | Planned | Leakage and lineage tests |
| F-007 | Baseline model training | MVP | Planned | Reproducible training reports |
| F-008 | Signal lifecycle | MVP | Planned | Signal expiry and idempotency tests |
| F-009 | Deterministic risk engine | MVP | Planned | Risk fixture tests |
| F-010 | Paper trading simulator | MVP | Planned | Execution simulation tests |
| F-011 | Reconciliation engine | MVP | Planned | Order/fill/balance/position reconciliation tests |
| F-012 | Dashboard global status | MVP | Planned | UI and accessibility tests |
| F-013 | Model registry and promotion gates | MVP/Beta | Planned | Approval workflow tests |
| F-014 | Observability and audit log | MVP | Planned | OTel and audit queries |
| F-015 | Controlled live trading | Beta | Planned | Live gate evidence |
| F-016 | Licensed sentiment sources | Later | Planned | Contract and model-risk review |
