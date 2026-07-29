# Telegram bot setup

1. Create a dedicated bot with BotFather and retain the token outside the repository.
2. Add the bot only to the intended private test chat and determine its numeric chat ID.
3. Copy `.env.example` to a local ignored `.env` file.
4. Set `FORAKILO_TELEGRAM_ENABLED=true`, the token, and a comma-separated chat allowlist.
5. Verify the bot identity with Telegram `getMe` before starting delivery.
6. Start with paper-only notifications and exercise `/health` and `/help`.

The adapter uses Telegram's HTTPS Bot API, escaped HTML, bounded message chunks, explicit chat
allowlisting, and retry classification. It does not contain long-lived secrets in source code
and does not expose any trading mutation command.

## Safely identify a chat

Send a harmless message to the test chat, call `getUpdates` from a local secret-aware client,
and copy only `message.chat.id` into the allowlist. Do not paste the full response into an issue
or log because it can include names and message text. Channels commonly use a negative ID.

## Local smoke test and shutdown

Keep `FORAKILO_DISCORD_ENABLED=false`, start the local application, verify `getMe`, then send a
paper-only health notification to the allowlisted test chat. Confirm that a denied chat fails
without retry. Disable the provider by setting `FORAKILO_TELEGRAM_ENABLED=false` and restart.

For delivery problems, check provider health, the numeric allowlist, bot membership, and Telegram
rate limits using redacted status output. Never print the request URL because it contains the
token. Rotate a token through BotFather, update the local secret, and restart the worker.
