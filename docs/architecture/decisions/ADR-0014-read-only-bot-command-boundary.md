# ADR-0014: Read-only bot command boundary

- Status: Accepted
- Date: 2026-07-29

Bot commands are authenticated by provider identity and destination
allowlists, then authorized through installation-local roles. The milestone
supports queries only. There are no buy, sell, approval, execution, risk-change
or model-promotion commands. Unknown or mutation-like commands fail closed and
are audited.

Chat content is never an order authorization or source of market truth.

