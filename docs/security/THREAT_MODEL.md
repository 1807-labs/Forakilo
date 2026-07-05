# Threat Model

Purpose: identify Forakilo-specific threats and required controls.
Scope: account, API, credential, data, model, trading, dashboard, CI/CD, dependency, and operations threats.
Audience: security reviewers, engineers, risk reviewers, and operators.
Assumptions: STRIDE plus misuse-case analysis is used; no implementation controls exist yet.
Dependencies: [Security Requirements](SECURITY_REQUIREMENTS.md), [Trust Boundaries](../architecture/TRUST_BOUNDARIES.md), [Sources](../research/SOURCES.md).
Unresolved decisions: owner assignments and residual-risk acceptance process.

## Method

Forakilo uses STRIDE for spoofing, tampering, repudiation, information disclosure, denial of service, and elevation of privilege, supplemented by financial misuse cases.

## Threat Register

| ID | Threat | Asset | Actor | Boundary | Impact | Required control | Test/monitoring |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TM-001 | Account takeover | User account | External attacker | Browser/API | Credential and trading abuse | MFA/passkeys, rate limits, anomaly detection | Auth abuse tests |
| TM-002 | Broken object authorization | User data/orders | Authenticated attacker | API | Cross-user data leak | Server-side object checks | BOLA tests |
| TM-003 | API-key theft | Provider credentials | External/insider | Credential vault | Unauthorized trading | Encryption, masking, no logs, revocation | Secret scans and audit |
| TM-004 | Dataset poisoning | Market/model data | Provider/attacker | Data ingestion | Unsafe model | Validation, anomaly checks, provenance | Data-quality alerts |
| TM-005 | Model artifact tampering | Model registry | Insider/supply chain | Registry | Bad signals | Fingerprints, approvals, signing | Artifact verification |
| TM-006 | Order manipulation | Trading state | External/insider | Trading API | Financial loss | Idempotency, authz, risk checks, audit | Execution tests |
| TM-007 | Replay/duplicate events | Orders/fills | Provider/network | Provider adapter | Duplicate orders | Idempotency and reconciliation | Failure simulation |
| TM-008 | Dashboard manipulation | UI state | XSS/attacker | Browser | Misleading decisions | CSP, output encoding, ASVS controls | SAST/DAST/UI tests |
| TM-009 | CI/CD compromise | Build artifacts | Supply-chain attacker | CI | Tampered release | SLSA, protected branches, signing | Provenance checks |
| TM-010 | Dependency compromise | Runtime | Supply-chain attacker | Dependencies | Code execution | Lockfiles, SBOM, scanning | Dependency gates |
| TM-011 | Prompt injection | Future LLM feature | External content | LLM boundary | Operator misinformation | LLM isolation, no execution authority | LLM red-team if added |
| TM-012 | Audit tampering | Evidence | Insider | Database/admin | Loss of accountability | Append-only audit, restricted admin | Audit integrity checks |

## Residual Risk

Residual risk MUST be documented for any accepted exception before live trading can be enabled.
