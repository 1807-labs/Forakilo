# Deployment Architecture

Purpose: define deployment direction without creating infrastructure.
Scope: local development, MVP staging, and future production patterns.
Audience: engineers, operations, security, and release owners.
Assumptions: no infrastructure is currently provisioned; deployment must start locally and progress through gated environments.
Dependencies: [Environment Strategy](ENVIRONMENT_STRATEGY.md), [CI/CD Strategy](../engineering/CI_CD_STRATEGY.md).
Unresolved decisions: cloud provider, region, registry, secrets manager, and managed database services.

## Target Environments

- Local: developer workstation with local services and fake/sandbox providers.
- Test: automated CI environment with deterministic fixtures and no live credentials.
- Staging: production-like environment using sandbox/demo credentials.
- Production: disabled until legal, security, risk, operations, and provider approvals exist.

## Deployment Shape

For MVP, the deployable unit SHOULD be a backend modular monolith, dashboard web app, PostgreSQL, Valkey, NATS, object storage, observability collector, and background worker process.

## Production Controls

- Secrets MUST come from an approved secrets manager.
- Public ingress MUST terminate TLS.
- Admin and operator access MUST use least privilege and MFA/passkeys.
- Release artifacts SHOULD include SBOM, provenance, signatures, and deployment approval evidence.
- Production live trading MUST remain unavailable until [Paper to Live Trading Gate](../trading/PAPER_TO_LIVE_TRADING_GATE.md) is complete.
