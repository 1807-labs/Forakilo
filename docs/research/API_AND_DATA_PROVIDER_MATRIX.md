# API and Data Provider Matrix

Purpose: evaluate external APIs and data providers before implementation.
Scope: crypto, FX, macroeconomic, economic calendar, licensed news, sentiment, status, and metadata providers.
Audience: engineering, product, legal, risk, and operations.
Assumptions: provider terms and availability can change; Canada is the first research jurisdiction; no provider contract has been approved.
Dependencies: [Sources](SOURCES.md), [Integration Architecture](../architecture/INTEGRATION_ARCHITECTURE.md), [Exchange Credential Security](../security/EXCHANGE_CREDENTIAL_SECURITY.md).
Unresolved decisions: approved venues, paid data subscriptions, account eligibility, and redistribution permissions require owner and legal review.

## Provider Decision Summary

| Provider | Role | Initial decision | Reason | Key limits |
| --- | --- | --- | --- | --- |
| OANDA v20 | FX demo and possible later live FX/CFD integration | Candidate for MVP sandbox/demo spike | Official REST/stream endpoints and practice environment; Canadian account availability appears documented by OANDA. | Token grants broad sub-account access; leveraged FX/CFD rules require legal and risk review. |
| Coinbase Advanced Trade | Crypto API candidate | Candidate for Canada-first crypto route, subject to legal and account review | CSA list includes Coinbase Canada Inc.; REST and WebSocket docs exist. | Sandbox responses may be static and not realistic for execution validation. |
| Kraken | Crypto market data and possible execution candidate | Candidate for public/authorized-market evaluation | REST, WebSocket, FIX, and status docs exist; Canadian restrictions must be checked. | Product availability and sandbox coverage require review. |
| Binance | Crypto data/execution | Not approved for initial Canadian trading scope | API docs are strong, but Binance exited the Canadian market. | May be used only for public API pattern research if terms permit. |
| FRED/ALFRED | Macroeconomic data and point-in-time macro revisions | Candidate for research data | Official API and vintage service. | Terms restrict storage, caching, archiving, and redistribution; must be reviewed before persistence. |
| Alpha Vantage | Market/macro fallback | Evaluation-only candidate | Broad API coverage. | Free tier too limited for production; terms and premium cost must be reviewed. |
| Nasdaq Data Link | Licensed datasets | Later paid-data candidate | API supports free and premium datasets. | Licensing, redistribution, and fees vary per dataset. |
| Licensed news/sentiment vendors | News and sentiment | Deferred | MVP does not need licensed sentiment. | Requires contract, redistribution, latency, and model-risk review. |

## Evaluation Criteria

Every provider integration MUST record:

- Markets, instruments, country availability, and account prerequisites.
- REST, WebSocket, FIX, and streaming support where applicable.
- Sandbox/demo support and realism limits.
- Authentication method, API-key scopes, rotation, expiry, and withdrawal-permission controls.
- Rate limits, pagination, sequencing, timestamp semantics, and reconnection behavior.
- Terms, licensing, retention, caching, redistribution, and data-derived-work restrictions.
- Provider status endpoint, maintenance history, incident behavior, and fallback approach.
- Fees, slippage, spread, margin, funding, and product restrictions.

## Provider Capability Matrix

| Capability | OANDA v20 | Coinbase Advanced Trade | Kraken | FRED/ALFRED | Alpha Vantage |
| --- | --- | --- | --- | --- | --- |
| Primary market | FX/CFD | Crypto spot | Crypto spot/derivatives depending jurisdiction | Macro | Multi-asset data |
| Real-time transport | Pricing stream | WebSocket | WebSocket | No | Varies |
| Historical data | Candles/prices | Products and market data endpoints | Market data endpoints | Yes, with revisions via ALFRED | Yes, API-dependent |
| Sandbox/demo | Practice environment | Static sandbox responses for Advanced Trade | Requires endpoint-specific verification | Not applicable | Not applicable |
| Auth | Personal access token | CDP/API keys | API keys | API key | API key |
| Key scope concern | Token may cover all sub-accounts | Scope model must be verified | Scope model must be verified | Data key only | Data key only |
| Canadian suitability | Candidate, subject to account/legal review | Candidate, subject to CSA/platform terms | Candidate, restrictions reviewed per product | Research source | Fallback only |
| MVP use | FX demo spike | Crypto contract-shape and provider spike | Crypto market data spike | Macro research with vintage controls | Low-volume fallback research |

## Anti-Scraping Rule

Forakilo MUST prefer official or licensed APIs. Scraping MAY be proposed only when terms permit automated access, robots/access controls are respected, licensing permits the intended use, official APIs are unavailable, legal risk is documented, and rate limiting plus attribution requirements are implemented.

## Fallback Strategy

- If live provider connectivity is degraded, Forakilo MUST fail closed for new execution.
- If market data is stale, signals MUST expire and pre-trade risk MUST reject orders.
- If provider account state disagrees across REST and streaming channels, reconciliation MUST block new orders until resolved.
