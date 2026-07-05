# Trust Boundaries

Purpose: identify trust boundaries that shape security and safety controls.
Scope: users, dashboard, APIs, credentials, providers, data, models, execution, and operations.
Audience: security reviewers, engineers, risk reviewers, and operators.
Assumptions: all external input is untrusted; provider data can be stale, malformed, delayed, or manipulated.
Dependencies: [Threat Model](../security/THREAT_MODEL.md), [System Architecture](SYSTEM_ARCHITECTURE.md).
Unresolved decisions: network segmentation and hosting controls.

## Boundaries

| Boundary | Crossing | Required controls |
| --- | --- | --- |
| Browser to API | User requests, sessions, commands | Authentication, authorization, CSRF controls where relevant, rate limits, input validation. |
| API to credential vault | Secret creation and use | Encryption, least privilege, masking, audit, step-up authentication. |
| Forakilo to providers | Market data, account data, orders | Provider-specific validation, rate limits, idempotency, status checks, retries, reconciliation. |
| Raw to normalized data | Untrusted payload processing | Schema validation, quarantine, provenance, timestamp normalization. |
| Research to model registry | Candidate artifacts | Reproducibility, signatures/fingerprints, evaluation reports, approval status. |
| Model to trading | Signals | Confidence, calibration, expiry, risk checks, abstention. |
| Paper to live | Execution environment change | Release gates, user authorization, risk approval, security review, kill switch. |
| Operations/admin | Privileged changes | Least privilege, MFA/passkeys, step-up, approval, immutable audit. |

## Boundary Policy

No boundary crossing may rely solely on client-side checks or model output.
