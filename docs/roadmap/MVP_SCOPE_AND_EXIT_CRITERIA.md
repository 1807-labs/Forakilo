# MVP Scope and Exit Criteria

Purpose: define MVP boundaries and completion evidence.
Scope: MVP only.
Audience: product owners, engineers, QA, risk reviewers, and legal counsel.
Assumptions: MVP is paper/sandbox first and does not require live trading.
Dependencies: [PRD](../product/PRODUCT_REQUIREMENTS_DOCUMENT.md), [Quality Gates](../engineering/QUALITY_GATES.md).
Unresolved decisions: exact provider and first strategy.

## MVP Scope

- Authentication and account lifecycle.
- Sandbox/demo provider credential management.
- Market data ingestion and quality checks.
- Dashboard status and paper trading views.
- One baseline strategy/model.
- Signal lifecycle and deterministic risk controls.
- Paper/sandbox execution and reconciliation.
- Model training, evaluation, registry, and manual promotion gates.
- Observability, audit, and kill switch.

## Exit Criteria

- All MVP stories meet Definition of Done.
- Data, model, trading, auth, security, dashboard, and reconciliation tests pass.
- Paper trading demonstrates safe execution and reconciliation under failure fixtures.
- Legal review items for user-facing launch are resolved or explicitly deferred.
- Live trading remains disabled unless beta gates are separately approved.
