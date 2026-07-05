# Privacy Policy Draft

This is a working technical draft for product planning and is not a substitute for qualified legal advice.

Purpose: outline personal-data handling for Forakilo.
Scope: account data, authentication data, provider metadata, trading records, telemetry, and support data.
Audience: product owners, legal counsel, privacy reviewers, and engineers.
Assumptions: Forakilo will collect personal information only as needed for account, security, operations, and compliance purposes.
Dependencies: [Data Retention Policy](DATA_RETENTION_POLICY.md), [PIPEDA research](JURISDICTION_RESEARCH.md).
Unresolved decisions: subprocessors, hosting regions, cookie use, analytics vendors, and exact retention periods.

## Draft Data Categories

- Account identifiers such as email and profile settings.
- Authentication, MFA/passkey, recovery, session, and device metadata.
- Provider connection metadata and encrypted credential material.
- Paper/live trading records, risk decisions, audit events, and user acknowledgements.
- Support communications and incident records.
- Security and operational telemetry, with secrets redacted.

## Draft Rights and Controls

Forakilo SHOULD support access, correction, export, deletion subject to legal retention, consent management where required, breach notification workflow, and clear contact paths for privacy questions.

## Minimization

Forakilo MUST NOT collect withdrawal credentials in the MVP and MUST minimize sensitive provider/account data.
