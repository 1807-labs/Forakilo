# Discord bot setup

1. Create a dedicated Discord application and bot in the developer portal.
2. Grant only the permissions required to view and send messages in a private test channel.
3. Record the application ID, guild ID, and channel ID; keep the bot token outside the repo.
4. Copy `.env.example` to a local ignored `.env` file and enable Discord explicitly.
5. Configure both guild and channel allowlists, then verify the bot identity with `/users/@me`.
6. Register only the read-only commands in [BOT_COMMANDS.md](BOT_COMMANDS.md).

The adapter sends bounded embeds and validates both guild and channel. A permission failure is
permanent until configuration changes; rate limits and network failures are retryable.

## Minimal installation and IDs

Use OAuth2 scopes `bot` and `applications.commands`. Grant View Channel and Send Messages only in
the selected test channel; add Embed Links if embeds are retained. Message Content intent is not
required. Enable Developer Mode locally to copy the guild and channel IDs, and do not publish
them with installation metadata.

## Local smoke test and shutdown

Keep Telegram disabled, verify `/users/@me`, send a paper-only health notification to the
allowlisted channel, and confirm a second channel is denied. Set
`FORAKILO_DISCORD_ENABLED=false` and restart to disable the integration.

For failures, inspect redacted provider health, channel membership, overwrite permissions, the
guild/channel allowlists, and retry-after status. Rotate the token in the developer portal,
replace the local secret, and restart; never paste an authorization header into logs or issues.
