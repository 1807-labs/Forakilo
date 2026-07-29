# Bot security

- Providers are disabled by default and require explicit destination allowlists.
- Tokens come from environment variables. Never commit, print, or paste a live token.
- Use a dedicated least-privilege bot identity and rotate a token after suspected exposure.
- Telegram chat IDs and Discord guild/channel IDs must match installation-local allowlists.
- Actor and destination identifiers are protected or hashed in command audit records.
- Provider error details are bounded and must be redacted before durable storage.
- Commands are read-only. Live-money and order mutation paths are intentionally absent.
- Outbound delivery uses idempotency keys, bounded retry, leases, expiry, and dead letters.

Before enabling a provider, verify its identity endpoint, review its allowlist, and test in a
non-production destination. To disable delivery, set the provider's enabled flag to `false`,
stop the worker, and revoke the provider token if compromise is suspected.
