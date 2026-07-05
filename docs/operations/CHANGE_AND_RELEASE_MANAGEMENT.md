# Change and Release Management

Purpose: define how changes and releases are controlled.
Scope: documentation, application code, data pipelines, models, containers, infrastructure, and releases.
Audience: maintainers, release owners, security reviewers, risk approvers, and operators.
Assumptions: no release automation exists yet.
Dependencies: [CI/CD Strategy](../engineering/CI_CD_STRATEGY.md), [Quality Gates](../engineering/QUALITY_GATES.md).
Unresolved decisions: versioning scheme and release approval owners.

## Change Rules

- Changes MUST go through review.
- High-risk changes MUST include security, data, model, risk, and operations impact notes.
- Model promotion and live-trading enablement MUST use approval gates.
- Releases SHOULD include changelog, test results, SBOM, provenance, deployment plan, rollback plan, and monitoring plan.

## Release Types

Documentation baseline, application release, data pipeline release, model candidate release, container release, infrastructure release, and emergency fix.
