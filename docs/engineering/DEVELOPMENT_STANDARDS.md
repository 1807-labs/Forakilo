# Development Standards

Purpose: define engineering standards for future Forakilo work.
Scope: code, docs, tests, reviews, security, data, ML, and trading changes.
Audience: contributors, maintainers, and reviewers.
Assumptions: standards will evolve as code is added.
Dependencies: [Contributing](../../CONTRIBUTING.md), [Secure SDLC](../security/SECURE_SDLC.md).
Unresolved decisions: exact formatter/type-checker configuration.

## Standards

- Keep implementation aligned with the ADRs unless a new ADR changes the decision.
- Separate planned capability from implemented capability in docs and UI.
- Write tests proportional to risk and blast radius.
- Preserve point-in-time data correctness.
- Do not log secrets or sensitive payloads.
- Use least privilege for permissions and service identities.
- Add audit events for significant state transitions.
- Treat trading, credentials, model promotion, and privacy changes as high-risk.
- Update traceability and docs when requirements or behavior changes.
