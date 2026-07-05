# CI/CD Strategy

Purpose: define CI/CD direction before implementation.
Scope: documentation checks, application checks, model/data checks, container checks, and release evidence.
Audience: engineers, release owners, security reviewers, and operations.
Assumptions: GitHub Actions may be used, but no workflow exists yet.
Dependencies: [Quality Gates](QUALITY_GATES.md), [Supply Chain Security](../security/SUPPLY_CHAIN_SECURITY.md).
Unresolved decisions: final CI provider, runner trust model, and branch protection rules.

## Proposed Pipelines

- Documentation: Markdown lint, link check, Mermaid validation, placeholder/claim search.
- Backend: uv sync, Ruff, type checks, unit/property/API tests, dependency scan.
- Frontend: package manager install, lint, type check, unit/UI/accessibility tests.
- Data: schema contract tests, data-quality fixtures, replay tests.
- ML: leakage tests, validation report generation, model-card check.
- Trading: risk fixtures, execution simulation, reconciliation tests.
- Security: secret scan, SAST, dependency scan, container scan.
- Release: build, SBOM, provenance, signing, changelog, approval evidence.

## Deployment

CI MUST NOT deploy live trading capabilities automatically. Production deployment and live enablement require separate approvals.
