# ADR-0010: Secure SDLC and Supply Chain

Status: Accepted
Date: 2026-07-04

Purpose: select security and supply-chain controls for future implementation.
Scope: code, dependencies, builds, artifacts, containers, secrets, CI/CD, and releases.
Audience: maintainers, security reviewers, and release owners.
Assumptions: no CI/CD or code exists yet; controls must be introduced before production code and releases.
Dependencies: [Secure SDLC](../../security/SECURE_SDLC.md), [Supply Chain Security](../../security/SUPPLY_CHAIN_SECURITY.md), [Quality Gates](../../engineering/QUALITY_GATES.md).
Unresolved decisions: CI runner model, registry, artifact signing policy, and hosting environment.

## Decision

Adopt NIST SSDF, OWASP ASVS/API guidance, SLSA provenance goals, CycloneDX SBOMs, secret scanning, SAST, dependency vulnerability scanning, container scanning, and Sigstore/Cosign signing when release artifacts exist.

## Rationale

Forakilo will handle credentials, personal data, model artifacts, financial decisions, and trading events. Security must be a product requirement, not a later hardening pass.

## Consequences

- Security gates MUST block releases when critical findings lack approved exceptions.
- Secrets MUST never be committed, logged, or exposed after initial entry.
- SBOMs and provenance MUST be generated for release artifacts once build pipelines exist.

## Alternatives Rejected

- Relying on manual review only: rejected because dependency and artifact risk require automated evidence.
- Single scanning tool: rejected because no one tool covers code, secrets, dependencies, containers, and provenance.
