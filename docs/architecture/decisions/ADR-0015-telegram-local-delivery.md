# ADR-0015: Telegram local delivery

- Status: Accepted
- Date: 2026-07-29

Telegram is an optional provider adapter using the Bot API behind Foreightkillo
contracts. Deployment owners create and own bots and supply tokens through the
environment. Destinations are allowlisted. Local command receiving may use
long polling; a public webhook is not required. Formatting, size limits,
rate-limit responses, invalid chats, blocked bots, health, and normalized
failures stay inside the adapter.

