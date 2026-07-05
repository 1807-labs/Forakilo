# Quality Gates

Purpose: define gates that block unsafe changes.
Scope: documentation, code, data, models, containers, infrastructure, and releases.
Audience: maintainers, engineers, QA, security reviewers, and release owners.
Assumptions: CI is not implemented yet.
Dependencies: [CI/CD Strategy](CI_CD_STRATEGY.md), [Secure SDLC](../security/SECURE_SDLC.md).
Unresolved decisions: exact tooling and thresholds.

## Gates

| Gate | Blocks on |
| --- | --- |
| Documentation | Broken links, invalid Mermaid, placeholders, misleading status, unsupported claims. |
| Application code | Failing tests, lint/type errors, auth/security regressions. |
| Data pipeline | Contract failure, quality failure, lineage gap, replay failure. |
| Model | Leakage, poor baseline comparison, calibration failure, missing model card. |
| Trading | Risk-control failure, idempotency failure, reconciliation failure. |
| Security | Critical vulnerability, secret leak, missing audit for high-impact action. |
| Container/release | Failed scan, missing SBOM/provenance/signature where required. |
| Live readiness | Any incomplete paper-to-live gate. |
