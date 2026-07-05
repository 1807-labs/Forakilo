# Supply Chain Security

Purpose: define dependency, build, artifact, and release integrity controls.
Scope: Python, TypeScript, containers, CI/CD, SBOMs, provenance, signing, and dependency risk.
Audience: maintainers, security reviewers, release owners, and operations.
Assumptions: no build pipeline exists yet; controls are required before production releases.
Dependencies: [Secure SDLC](SECURE_SDLC.md), [ADR-0010](../architecture/decisions/ADR-0010-secure-sdlc-and-supply-chain.md), [Sources](../research/SOURCES.md).
Unresolved decisions: package registries, container registry, and CI runner trust model.

## Requirements

- Dependencies MUST be lockfile-managed.
- Pull requests MUST run linting, tests, secret scanning, SAST, and dependency scanning once code exists.
- Release artifacts SHOULD include CycloneDX SBOMs.
- Container images SHOULD be scanned and signed before deployment.
- Provenance SHOULD target SLSA-aligned attestations.
- Dependency exceptions MUST document severity, exploitability, compensating controls, owner, and expiry.

## Initial Tooling Direction

Use uv for Python locking, package manager lockfiles for TypeScript, Ruff for linting, Semgrep CE with license review, pip-audit or equivalent for Python dependencies, npm audit or equivalent for frontend dependencies, gitleaks for secrets, Trivy/Grype for containers, CycloneDX for SBOM, and Sigstore Cosign for signing.
