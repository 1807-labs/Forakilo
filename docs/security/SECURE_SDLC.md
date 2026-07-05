# Secure SDLC

Purpose: define secure software development lifecycle controls.
Scope: planning, design, implementation, review, testing, release, vulnerability response, and maintenance.
Audience: maintainers, engineers, security reviewers, QA, and release owners.
Assumptions: NIST SSDF is the baseline framework.
Dependencies: [Quality Gates](../engineering/QUALITY_GATES.md), [Supply Chain Security](SUPPLY_CHAIN_SECURITY.md), [Sources](../research/SOURCES.md).
Unresolved decisions: exact CI provider, branch protections, and release process.

## Required Practices

- Threat modeling for high-risk features before implementation.
- Security requirements in user stories and acceptance criteria.
- Code review for every change.
- Static analysis, dependency scanning, secret scanning, and tests in CI.
- Secure defaults for authentication, authorization, sessions, CORS, CSP, cookies, and logging.
- Vulnerability intake, triage, remediation, disclosure, and backport policy.
- Release evidence including tests, SBOM, provenance, and approval.

## Definition of Done Security Additions

A story touching user data, credentials, model promotion, risk controls, or execution is not done until security tests, audit events, logging redaction, and operational alerts are reviewed.
