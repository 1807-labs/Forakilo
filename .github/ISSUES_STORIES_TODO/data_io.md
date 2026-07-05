# FKL-004: Provider Connection and Market Data Contract

Epic: Provider Integration
Priority: P0
Target release phase: MVP
Status: Planned
Estimate: 13

## User Story

As a trader, I want Forakilo to connect to approved sandbox/demo market-data providers so that paper strategies can receive validated real-time and historical data.

## Business Value

Creates the external data foundation without implying live execution readiness.

## Context

The original story mentioned Binance and live order execution. The normalized version limits MVP work to approved providers and sandbox/demo or public market data.

## In Scope

Provider adapter interface, OANDA practice spike, Coinbase/Kraken evaluation spike, status endpoint checks, rate-limit handling, reconnect behavior, and normalized data contracts.

## Out of Scope

Live trading, withdrawal credentials, scraping, and unsupported providers.

## Acceptance Criteria

- Adapter fetches or receives approved market data in sandbox/demo/public mode.
- Raw provider payloads are captured before normalization.
- Normalized records include provider, instrument, timestamps, and contract version.
- Connection drops use bounded retry and degraded status.
- Provider status and rate-limit events are surfaced.

## Negative Acceptance Criteria

- Binance is not treated as an initial Canada-first live provider.
- Data is not used downstream when freshness or contract checks fail.

## Security Requirements

Provider credentials use FKL-003; logs redact secrets and sensitive account data.

## Privacy Requirements

Provider account metadata is minimized.

## Data Requirements

Market data contracts, timestamp semantics, quality checks, and lineage.

## Model Requirements

Downstream models receive only validated feature-ready data.

## Risk Controls

Provider degradation expires signals and blocks execution.

## Observability Requirements

Emit connection, freshness, rate-limit, retry, and provider status metrics.

## Accessibility Requirements

Dashboard provider status must not rely on color alone.

## Dependencies

FKL-003, data contracts, provider legal review.

## Assumptions

OANDA practice is the first FX demo candidate; Coinbase and Kraken remain crypto candidates.

## Edge Cases

Reconnect loop, rate limit, stale stream, REST/WebSocket disagreement, provider maintenance.

## Test Notes

Provider fake contract tests and replay fixtures.

## Documentation Impact

Update API provider matrix and integration architecture.

## Definition of Ready

Provider spike plan and data contract draft exist.

## Definition of Done

Contract tests, data quality checks, docs, and observability pass.
