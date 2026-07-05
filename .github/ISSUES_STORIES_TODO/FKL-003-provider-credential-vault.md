# FKL-003: Provider Credential Vault

Epic: Security
Priority: P0
Target release phase: MVP
Status: Planned
Estimate: 13

## User Story

As a user, I want to store approved sandbox or demo provider credentials securely so that Forakilo can connect without exposing my secrets.

## Business Value

Enables provider integration while controlling financial and credential risk.

## Context

Withdrawal permissions are prohibited.

## In Scope

Encrypted storage, masking, validation, rotation, revocation, environment separation, scope checks, and audit events.

## Out of Scope

Live trading enablement and withdrawal permissions.

## Acceptance Criteria

- Credentials are encrypted at rest.
- Full secret values are never returned after submission.
- Sandbox/demo and live credentials are stored separately.
- Provider scope validation rejects withdrawal-capable credentials where detectable.
- Rotation and revocation are audited.

## Negative Acceptance Criteria

- Secrets do not appear in logs, traces, metrics, errors, screenshots, or exports.
- A user cannot access another user's credential metadata.

## Security Requirements

Step-up authentication, least privilege, encryption, secret redaction, and private compromise response.

## Privacy Requirements

Store minimum provider account metadata.

## Data Requirements

Credential metadata schema, audit events, and key rotation metadata.

## Model Requirements

None.

## Risk Controls

Provider connection is disabled on failed validation, revocation, suspected compromise, or environment mismatch.

## Observability Requirements

Emit credential create, validate, rotate, revoke, and failure events without secrets.

## Accessibility Requirements

Credential forms must explain scopes clearly without relying on color alone.

## Dependencies

FKL-001, FKL-002, secrets manager decision.

## Assumptions

Initial credentials are sandbox/demo only.

## Edge Cases

Provider scope cannot be verified, token expires, key is revoked externally, validation endpoint rate-limits.

## Test Notes

Secret scanning, redaction, authz, and provider fake tests.

## Documentation Impact

Update exchange credential security and provider matrix.

## Definition of Ready

Secret storage design is approved.

## Definition of Done

No secret leakage in tests and audit evidence is complete.
