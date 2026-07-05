# Requirements Traceability Matrix

Purpose: map product goals to requirements, components, stories, tests, risks, and release phases.
Scope: foundation and MVP baseline.
Audience: product owners, engineers, QA, risk reviewers, and auditors.
Assumptions: mappings will grow as implementation and tests are added.
Dependencies: [PRD](PRODUCT_REQUIREMENTS_DOCUMENT.md), [Story Backlog](../../.github/ISSUES_STORIES_TODO/README.md).
Unresolved decisions: exact test IDs after test suite creation.

| Goal/Requirement | Feature | Component | Story | Risk control | Test evidence | Release |
| --- | --- | --- | --- | --- | --- | --- |
| PG-001/FR-001 | Account registration | Identity | FKL-001 | Auth boundary | Auth API tests | MVP |
| FR-002 | Step-up auth | Identity | FKL-002 | High-impact gate | Step-up tests | MVP |
| FR-003 | Credential vault | Credential Vault | FKL-003 | No withdrawal keys | Secret/redaction tests | MVP |
| FR-004/FR-005 | Provider data | Provider/Data Plane | FKL-004, FKL-005 | Freshness fail-closed | Contract/replay tests | MVP |
| NFR-005 | Data quality | Data Plane | FKL-006 | Quarantine | Data quality tests | MVP |
| PG-003 | Features/model | Intelligence | FKL-007, FKL-008 | Abstention | Leakage/model tests | MVP |
| PG-004 | Risk controls | Risk Engine | FKL-009, FKL-010 | Deterministic rejection | Risk fixtures | MVP |
| PG-005 | Paper trading | Paper Execution | FKL-011, FKL-012 | Reconciliation block | Simulator/recon tests | MVP |
| FR-006 | Dashboard | Dashboard | FKL-013 | Mode separation | UI/a11y tests | MVP |
| PG-006 | Model governance | Model Registry | FKL-014 | No auto live promotion | Promotion tests | MVP |
| NFR-007 | Auditability | Governance | FKL-015 | Durable audit | Audit tests | MVP |
| FR-007 | Backtesting | Quant Validation | FKL-016 | Point-in-time validation | Backtest tests | MVP |
