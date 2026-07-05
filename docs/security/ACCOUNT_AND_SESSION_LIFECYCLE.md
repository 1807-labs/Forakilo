# Account and Session Lifecycle

Purpose: define account and session lifecycle behavior.
Scope: registration, verification, login, recovery, devices, sessions, suspension, deletion, export, and incident recovery.
Audience: backend engineers, security reviewers, QA, support, and product owners.
Assumptions: account recovery is a high-risk attack path.
Dependencies: [Authentication and Authorization](AUTHENTICATION_AND_AUTHORIZATION.md), [Abuse and Fraud Controls](ABUSE_AND_FRAUD_CONTROLS.md).
Unresolved decisions: exact recovery-channel policy and customer-support workflow.

## Lifecycle

1. Registration with email verification.
2. Password or passkey setup.
3. MFA enrollment and recovery-code generation where enabled.
4. Login with rate limiting and suspicious-login detection.
5. Session creation, listing, expiration, revocation, and logout.
6. Device registration, review, and revocation.
7. Password reset or passkey recovery with abuse prevention.
8. Profile, notification, and risk-preference management.
9. Account suspension for abuse, fraud, legal, security, or user request.
10. Personal-data export.
11. Account deletion subject to legal, audit, and trading-record retention.
12. Security incident recovery and forced credential/session rotation.

## Required Audit Events

Registration, verification, login, logout, failed login threshold, MFA changes, recovery events, device changes, session revocation, role changes, credential changes, export, deletion, suspension, and support/admin access MUST be audited.

## Recovery Abuse Prevention

Recovery flows MUST rate limit attempts, notify users of sensitive changes, block immediate high-risk actions after recovery where appropriate, and require stronger review for privileged accounts.
