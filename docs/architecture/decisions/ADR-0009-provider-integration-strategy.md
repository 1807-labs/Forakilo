# ADR-0009: Provider Integration Strategy

Status: Accepted
Date: 2026-07-04

Purpose: define how Forakilo integrates with external brokers, exchanges, and data providers.
Scope: market data, account data, order execution, status, and provider abstraction.
Audience: backend engineers, trading engineers, security reviewers, legal counsel, and operators.
Assumptions: provider terms, account eligibility, and API behavior differ materially by market and jurisdiction.
Dependencies: [API and Data Provider Matrix](../../research/API_AND_DATA_PROVIDER_MATRIX.md), [Integration Architecture](../INTEGRATION_ARCHITECTURE.md).
Unresolved decisions: approved provider list and contracts require legal and product-owner approval.

## Decision

Forakilo will prefer direct provider adapters for approved venues and use unifying libraries only after endpoint-level behavior, terms, and risk controls are verified. OANDA v20, Coinbase Advanced Trade, and Kraken are candidates for early evaluation. Binance is not an initial Canadian live-trading provider.

## Rationale

Unified libraries can simplify access but may hide exchange-specific order semantics, scopes, precision rules, and failure modes. Trading safety requires provider-specific controls.

## Consequences

- Every provider adapter MUST implement idempotency, rate-limit handling, reconciliation, status checks, timestamp normalization, and safe degraded behavior.
- Withdrawal permissions MUST NOT be requested.
- Sandbox credentials MUST be separated from live credentials and environments.

## Alternatives Rejected

- CCXT as sole abstraction: rejected because exchange-specific execution behavior must be verified directly.
- Scraping as default: rejected due terms, licensing, reliability, and compliance risk.
