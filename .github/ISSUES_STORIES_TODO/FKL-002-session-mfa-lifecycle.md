# FKL-002: Session, MFA, Passkey, and Recovery Lifecycle

Epic: Identity
Priority: P0
Target release phase: MVP
Status: Planned
Estimate: 8

## User Story

As a user, I want to manage sessions, devices, MFA or passkeys, and recovery so that I can protect and recover my account safely.

## Business Value

Reduces account takeover risk for a platform that may later control trading actions.

## Context

High-impact actions require step-up authentication.

## In Scope

Session listing/revocation, expiration, suspicious-login detection, MFA/passkey enrollment, recovery codes, recovery flow, and step-up foundation.

## Out of Scope

Administrative support tooling and provider credentials.

## Acceptance Criteria

- User can view and revoke active sessions.
- Sessions expire according to policy.
- MFA/passkey enrollment and recovery codes are audited.
- Step-up authentication can be required for high-impact routes.
- Recovery flows are rate-limited and audited.

## Negative Acceptance Criteria

- Recovery cannot bypass rate limits.
- Revoked sessions cannot be used.
- Recovery codes are not retrievable after creation.

## Security Requirements

Use NIST 800-63-4-informed controls, server-side session checks, device metadata, and anomaly logging.

## Privacy Requirements

Device/session metadata is minimized and retained only as needed.

## Data Requirements

Session, device, authenticator, recovery, and audit schemas.

## Model Requirements

None.

## Risk Controls

Step-up gate must support future credential, risk, model, and live trading actions.

## Observability Requirements

Metrics for suspicious login, MFA changes, session revocations, and recovery attempts.

## Accessibility Requirements

MFA and recovery flows must support accessible forms and error states.

## Dependencies

FKL-001.

## Assumptions

Passkeys may be phased in after MFA if implementation complexity requires.

## Edge Cases

Lost device, stolen session, simultaneous revocation, expired step-up.

## Test Notes

Auth, session fixation, rate-limit, and recovery abuse tests.

## Documentation Impact

Update account lifecycle and security requirements.

## Definition of Ready

MFA/passkey provider approach is selected.

## Definition of Done

Security tests and audit evidence pass.
