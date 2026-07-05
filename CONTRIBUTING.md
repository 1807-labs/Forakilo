# Contributing to Forakilo

Purpose: define contribution expectations for the pre-development repository.
Scope: documentation, backlog, and future code contributions.
Audience: contributors and maintainers.
Assumptions: Forakilo is pre-development and safety-critical features require extra review.
Dependencies: [Development Standards](docs/engineering/DEVELOPMENT_STANDARDS.md), [Secure SDLC](docs/security/SECURE_SDLC.md).
Unresolved decisions: maintainer roster and branch protection configuration.

## Ground Rules

- Distinguish planned capability from implemented capability.
- Do not add secrets, credentials, personal data, provider keys, or live trading configuration.
- Do not describe strategy or model results as proof of future returns.
- Update documentation and traceability when requirements change.
- Treat authentication, credentials, data lineage, model promotion, risk controls, and execution as high-risk areas.

## Contribution Flow

1. Open or update a normalized story in `.github/ISSUES_STORIES_TODO/` unless work is purely documentation cleanup.
2. Keep changes scoped.
3. Add or update tests when code exists.
4. Update affected docs and ADRs.
5. Use the pull request template.

## Review Expectations

High-risk changes require reviewers for security, data/model correctness, trading risk, and operations impact.
