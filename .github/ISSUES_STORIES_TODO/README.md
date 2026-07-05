# Forakilo Story Backlog

Purpose: hold normalized pre-development stories before GitHub issues are created.
Scope: foundation and MVP backlog candidates.
Audience: product owners, engineers, QA, security reviewers, and risk reviewers.
Assumptions: these stories are not GitHub issues yet; estimates are planning estimates only.
Dependencies: [User Story Audit](../../docs/product/USER_STORY_AUDIT.md), [Traceability Matrix](../../docs/product/REQUIREMENTS_TRACEABILITY_MATRIX.md).
Unresolved decisions: final sprint sequencing and owners.

## Story Inventory

| ID | File | Epic | Priority | Phase | Estimate | Status |
| --- | --- | --- | --- | --- | --- | --- |
| FKL-001 | [FKL-001-account-registration.md](FKL-001-account-registration.md) | Identity | P0 | Foundation/MVP | 8 | Planned |
| FKL-002 | [FKL-002-session-mfa-lifecycle.md](FKL-002-session-mfa-lifecycle.md) | Identity | P0 | MVP | 8 | Planned |
| FKL-003 | [FKL-003-provider-credential-vault.md](FKL-003-provider-credential-vault.md) | Security | P0 | MVP | 13 | Planned |
| FKL-004 | [data_io.md](data_io.md) | Provider Integration | P0 | MVP | 13 | Planned |
| FKL-005 | [FKL-005-immutable-market-data-ingestion.md](FKL-005-immutable-market-data-ingestion.md) | Data | P0 | MVP | 8 | Planned |
| FKL-006 | [FKL-006-data-quality-quarantine.md](FKL-006-data-quality-quarantine.md) | Data | P0 | MVP | 8 | Planned |
| FKL-007 | [FKL-007-point-in-time-features.md](FKL-007-point-in-time-features.md) | Intelligence | P1 | MVP | 8 | Planned |
| FKL-008 | [ai_and_strategy.md](ai_and_strategy.md) | Intelligence | P1 | MVP | 13 | Planned |
| FKL-009 | [FKL-009-signal-lifecycle.md](FKL-009-signal-lifecycle.md) | Trading | P0 | MVP | 8 | Planned |
| FKL-010 | [execution_risk_management.md](execution_risk_management.md) | Risk | P0 | MVP | 13 | Planned |
| FKL-011 | [FKL-011-paper-execution-simulator.md](FKL-011-paper-execution-simulator.md) | Trading | P0 | MVP | 13 | Planned |
| FKL-012 | [FKL-012-order-reconciliation.md](FKL-012-order-reconciliation.md) | Trading | P0 | MVP | 13 | Planned |
| FKL-013 | [FKL-013-dashboard-global-status.md](FKL-013-dashboard-global-status.md) | Dashboard | P1 | MVP | 13 | Planned |
| FKL-014 | [FKL-014-model-registry-promotion.md](FKL-014-model-registry-promotion.md) | MLOps | P1 | MVP | 8 | Planned |
| FKL-015 | [FKL-015-observability-audit.md](FKL-015-observability-audit.md) | Operations | P0 | MVP | 8 | Planned |
| FKL-016 | [backtest_engine.md](backtest_engine.md) | Quant Validation | P0 | MVP | 13 | Planned |

## Definition of Ready

A story is ready when it has stable ID, actor, value, dependencies, acceptance criteria, security/privacy/data/risk/observability impacts, test notes, and release phase.

## Definition of Done

A story is done when implementation, tests, docs, traceability, security review where relevant, and operational evidence are complete. Live trading stories also require paper-to-live gates.
