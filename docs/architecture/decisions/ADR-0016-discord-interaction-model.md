# ADR-0016: Discord interaction model

- Status: Accepted
- Date: 2026-07-29

Discord is an optional provider adapter owned by the deployment operator.
Outbound messages and read-only slash commands use allowlisted guilds and
channels with minimal permissions. The adapter does not request unrestricted
message-content access. Provider embeds, response codes, limits, and identity
types do not cross into the application core.

