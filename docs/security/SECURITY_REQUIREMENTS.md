# Security Requirements

Purpose: define Forakilo security requirements for future implementation.
Scope: application, API, data, model, trading, infrastructure, and operations security.
Audience: engineers, QA, security reviewers, and release owners.
Assumptions: OWASP ASVS Level 2 is the default target; higher controls apply to credential and trading-impact actions.
Dependencies: [Threat Model](THREAT_MODEL.md), [Secure SDLC](SECURE_SDLC.md), [Sources](../research/SOURCES.md).
Unresolved decisions: exact ASVS requirement mapping and security tooling configuration.

## Requirements

| ID | Requirement | Verification |
| --- | --- | --- |
| SEC-001 | Enforce authentication and authorization on protected routes. | Auth and BOLA tests. |
| SEC-002 | Protect against credential stuffing, brute force, recovery abuse, and session theft. | Abuse tests and monitoring. |
| SEC-003 | Validate all inputs at trust boundaries. | Unit, API, and fuzz/property tests. |
| SEC-004 | Prevent XSS, CSRF where relevant, injection, SSRF, path traversal, insecure deserialization, and IDOR. | SAST, DAST, and integration tests. |
| SEC-005 | Encrypt provider secrets and sensitive data at rest and in transit. | Architecture review and secret tests. |
| SEC-006 | Redact secrets and sensitive payloads from logs, traces, metrics, screenshots, and exports. | Telemetry tests. |
| SEC-007 | Require least privilege for users, admins, service identities, and CI/CD. | Access review. |
| SEC-008 | Generate immutable audit events for high-impact actions. | Audit tests. |
| SEC-009 | Use dependency locking, vulnerability scanning, SBOMs, and provenance. | CI gates. |
| SEC-010 | Maintain incident response, disclosure, and recovery processes. | Tabletop and runbook tests. |
