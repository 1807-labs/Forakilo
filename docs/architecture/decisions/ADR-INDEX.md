# Architecture Decision Record Index

Purpose: list accepted architectural decisions for the pre-development baseline.
Scope: major technology, architecture, security, ML, data, provider, and operations choices.
Audience: maintainers, reviewers, and future implementers.
Assumptions: decisions are reversible through new ADRs; no production code exists yet.
Dependencies: [Technology Evaluation](../../research/TECHNOLOGY_EVALUATION.md), [Sources](../../research/SOURCES.md).
Unresolved decisions: final hosting, paid provider contracts, and exact package versions remain open.

## Accepted ADRs

| ADR | Decision | Status |
| --- | --- | --- |
| [ADR-0001](ADR-0001-modular-monolith-first.md) | Modular monolith first | Accepted |
| [ADR-0002](ADR-0002-python-api-stack.md) | Python FastAPI API stack | Accepted |
| [ADR-0003](ADR-0003-dashboard-stack.md) | Next.js dashboard stack | Accepted |
| [ADR-0004](ADR-0004-storage-baseline.md) | PostgreSQL-centered storage baseline | Accepted |
| [ADR-0005](ADR-0005-cache-and-messaging.md) | Valkey cache and NATS messaging | Accepted |
| [ADR-0006](ADR-0006-data-quality-and-lineage.md) | Point-in-time data quality and lineage | Accepted |
| [ADR-0007](ADR-0007-mlops-stack.md) | Self-hostable MLOps baseline | Accepted |
| [ADR-0008](ADR-0008-backtesting-and-simulation.md) | Dual research and event-driven backtesting path | Accepted |
| [ADR-0009](ADR-0009-provider-integration-strategy.md) | Direct provider integration strategy | Accepted |
| [ADR-0010](ADR-0010-secure-sdlc-and-supply-chain.md) | Secure SDLC and supply-chain baseline | Accepted |
| [ADR-0011](ADR-0011-python-311-lean-boundary.md) | Python 3.11 lean boundary | Accepted |
| [ADR-0012](ADR-0012-provider-neutral-bot-integration.md) | Provider-neutral bot integration | Accepted |
| [ADR-0013](ADR-0013-durable-notification-outbox.md) | Durable notification outbox | Accepted |
| [ADR-0014](ADR-0014-read-only-bot-command-boundary.md) | Read-only bot command boundary | Accepted |
| [ADR-0015](ADR-0015-telegram-local-delivery.md) | Telegram local delivery | Accepted |
| [ADR-0016](ADR-0016-discord-interaction-model.md) | Discord interaction model | Accepted |
| [ADR-0017](ADR-0017-noesis-compatible-contracts.md) | Noesis-compatible contracts | Accepted |
