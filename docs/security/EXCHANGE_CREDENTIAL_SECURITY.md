# Exchange Credential Security

Purpose: define secure handling of broker and exchange credentials.
Scope: API keys, tokens, scopes, validation, rotation, revocation, masking, logging, and compromise response.
Audience: backend engineers, security reviewers, risk reviewers, and operators.
Assumptions: provider credentials can enable financial actions and must be treated as high-impact secrets.
Dependencies: [Secrets and Key Management](SECRETS_AND_KEY_MANAGEMENT.md), [Provider Matrix](../research/API_AND_DATA_PROVIDER_MATRIX.md).
Unresolved decisions: final secrets manager and provider-specific scope mappings.

## Credential Rules

- Credentials MUST be encrypted at rest using an approved secrets manager or envelope encryption design.
- Full secrets MUST never be logged, returned, displayed after entry, exported, or included in telemetry.
- Credentials MUST be masked in UI and audit records.
- Sandbox/demo and live credentials MUST be separate.
- Withdrawal permission MUST NOT be requested or stored.
- Read/trade permissions SHOULD be separated when providers support safe scopes.
- Every credential create, validate, use, rotate, revoke, and failure event MUST be audited.

## Provider Validation

Before enabling a provider connection, Forakilo MUST verify account identity, environment, permissions, supported markets, account mode, rate-limit access, and whether live trading is disabled or enabled.

## Compromise Response

On suspected credential compromise, Forakilo MUST disable provider connection, revoke local credential material, notify user/operator, audit the event, block new execution, and require fresh credential validation.
