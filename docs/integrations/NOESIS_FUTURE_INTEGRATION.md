# Future Noesis integration

Noesis is a future consumer, not a privileged execution path. The current boundary exposes
versioned, provider-neutral contracts for event subscriptions, typed queries, acknowledgements,
correlation IDs, and idempotency keys.

An implementation should authenticate an installation, authorize the requested visibility,
negotiate a supported schema version, and project the same internal events used by local bot
providers. It must preserve truthful `NOT_AVAILABLE` query results and must not bypass the
read-only command policy. Provider-native objects and credentials stay outside core event,
projection, query, and outbox modules.
