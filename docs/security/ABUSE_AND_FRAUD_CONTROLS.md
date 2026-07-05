# Abuse and Fraud Controls

Purpose: define controls against account, credential, provider, and trading abuse.
Scope: registration, login, recovery, API use, provider credentials, trading controls, and cost abuse.
Audience: security, product, support, operations, and engineers.
Assumptions: Forakilo may be targeted for credential abuse and automated financial misuse.
Dependencies: [Account Lifecycle](ACCOUNT_AND_SESSION_LIFECYCLE.md), [Threat Model](THREAT_MODEL.md).
Unresolved decisions: exact fraud signals and support escalation process.

## Controls

- Rate limiting for registration, login, recovery, MFA, credential validation, and provider API operations.
- Credential stuffing detection and suspicious-login notifications.
- Step-up authentication for high-impact actions.
- Cooldowns after recovery before enabling high-risk changes.
- Provider credential validation that rejects withdrawal permission.
- Trading frequency limits and automated fail-closed circuit breakers.
- Abuse monitoring for excessive API cost, repeated failed provider requests, and unusual account changes.

## Support Safety

Support or administrative actions MUST be least-privilege, audited, and unable to reveal provider secrets.
