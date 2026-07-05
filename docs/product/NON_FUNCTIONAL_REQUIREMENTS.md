# Non-Functional Requirements

Purpose: define measurable quality attributes for Forakilo.
Scope: security, privacy, reliability, accessibility, observability, data quality, performance, and maintainability.
Audience: engineers, QA, security, risk, operations, and product owners.
Assumptions: exact SLO numbers will be refined after implementation baselines are measured.
Dependencies: [Service Level Objectives](../operations/SERVICE_LEVEL_OBJECTIVES.md), [Security Requirements](../security/SECURITY_REQUIREMENTS.md).
Unresolved decisions: production hosting, staffing model, and compliance commitments.

## Requirements

| ID | Requirement | Verification |
| --- | --- | --- |
| NFR-001 | Protected services MUST require authentication and authorization. | Auth and BOLA tests. |
| NFR-002 | High-impact actions MUST require step-up authentication and audit records. | Security acceptance tests. |
| NFR-003 | Secrets MUST be encrypted, redacted, rotatable, and excluded from logs. | Secret-scanning and logging tests. |
| NFR-004 | Dashboard MUST target WCAG 2.2 AA. | Automated and manual accessibility tests. |
| NFR-005 | Market data MUST expose freshness, quality, and lineage. | Data quality reports and dashboard checks. |
| NFR-006 | Model outputs MUST include model version, dataset version, feature version, confidence, calibration, and abstention state. | Model inference contract tests. |
| NFR-007 | Execution decisions MUST be auditable end to end. | Traceability and audit-query tests. |
| NFR-008 | New execution MUST fail closed during unsafe provider, data, model, risk, or reconciliation state. | Failure-mode simulations. |
| NFR-009 | Builds MUST be reproducible enough to generate dependency locks, SBOMs, and provenance. | CI release gates once code exists. |
| NFR-010 | Personal data MUST be minimized, retained only as needed, exportable, and deletable subject to legal holds. | Privacy workflow tests. |

## Performance Position

Forakilo MUST NOT claim latency-sensitive trading capability without measured evidence, provider access, infrastructure design, and market-data rights. MVP latency targets should be conservative and based on measured paper/sandbox behavior.
