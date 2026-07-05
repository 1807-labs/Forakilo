# Secrets and Key Management

Purpose: define how Forakilo stores and uses secrets.
Scope: application secrets, provider credentials, API tokens, signing keys, encryption keys, and CI secrets.
Audience: engineers, security reviewers, operators, and release owners.
Assumptions: no secrets should exist in the repository.
Dependencies: [Exchange Credential Security](EXCHANGE_CREDENTIAL_SECURITY.md), [Supply Chain Security](SUPPLY_CHAIN_SECURITY.md).
Unresolved decisions: final secrets manager and key-rotation schedule.

## Requirements

- Secrets MUST be stored in an approved secrets manager or encrypted vault.
- Secrets MUST NOT be committed to Git, stored in issue text, printed in logs, or exposed in telemetry.
- Secrets MUST be rotatable without code changes.
- Production secrets MUST be unavailable to local development and CI pull-request workflows.
- Key access MUST be least-privilege and audited.
- Encryption keys SHOULD use envelope encryption where supported.

## Secret Classes

| Class | Examples | Required handling |
| --- | --- | --- |
| Provider credentials | OANDA, Coinbase, Kraken keys/tokens | Encrypted, masked, scoped, revocable. |
| Application secrets | Session, CSRF, JWT/signing keys if used | Rotatable and environment-specific. |
| CI/CD secrets | Registry tokens, deployment credentials | Protected environments and minimal scope. |
| Artifact signing | Cosign keys or OIDC identity | Prefer keyless signing when feasible. |
