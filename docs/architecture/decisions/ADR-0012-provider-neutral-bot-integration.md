# ADR-0012: Provider-neutral bot integration

- Status: Accepted
- Date: 2026-07-29

## Decision

Foreightkillo exposes versioned application event and query contracts to a
provider-neutral bot gateway. Telegram, Discord, local testing, and future
Noesis adapters depend inward on those contracts. Trading, risk, strategy,
signal, and paper-execution modules never import provider libraries.

Outgoing delivery is asynchronous through a durable outbox. Incoming commands
are authenticated, allowlisted, permission-checked, and read-only. Chat
messages cannot authorize proposals, execute orders, change risk, or promote
models. Tokens are environment secrets and integrations are disabled by
default.

The bot gateway remains part of the modular monolith. No external AI service or
microservice is required.
