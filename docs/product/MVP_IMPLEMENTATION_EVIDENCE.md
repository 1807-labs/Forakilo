# MVP Implementation Evidence

This matrix maps the requested For8killo MVP outcomes to current authoritative implementation and
verification evidence. “External gate” means the product-side capability exists but an operator
must provide a licensed account, credentials, or approval outside this repository.

| Requirement | State | Runtime evidence | Verification evidence |
| --- | --- | --- | --- |
| For8killo and Foreight naming | Implemented | `pyproject.toml`, canonical `src/foreightkillo/` package and environment configuration | `tests/unit/test_branding.py` |
| FX, commodity, and crypto market data | Implemented with deterministic synthetic provider; licensed live feed is an external gate | `src/foreightkillo/marketdata/` | `tests/unit/test_provider_adapters.py`, executable market scenarios |
| Market structure, liquidity, volatility, and regime | Implemented | `src/foreightkillo/intelligence/market.py` | `tests/unit/test_market_intelligence.py` |
| Trend, momentum, breakout, mean-reversion, harmonic, and multi-timeframe research | Implemented | `src/foreightkillo/intelligence/strategies.py`, `/api/v1/strategy-research/{symbol}` | `tests/unit/test_technical_strategies.py`, executable strategy scenario |
| Complete signal lifecycle and comparative ranking | Implemented | `src/foreightkillo/signals/` | `tests/unit/test_signal_pipeline.py`, ranking scenario |
| Point-in-time backtesting with costs | Implemented | `src/foreightkillo/backtesting/` | `tests/unit/test_backtesting.py` |
| Deterministic fail-closed risk | Implemented | `src/foreightkillo/risk/` | `tests/unit/test_safety_core.py` |
| Paper execution | Implemented | `src/foreightkillo/execution/paper.py` | safety and application lifecycle tests |
| Practice execution | Implemented; approved practice provider account is an external gate | `src/foreightkillo/execution/practice.py`, provider-neutral broker contract | `tests/unit/test_practice_execution.py`, executable denial scenario |
| Positions, P&L, performance, reconciliation | Implemented | `src/foreightkillo/portfolio/`, `/api/v1/portfolio` | `tests/unit/test_portfolio_ledger.py`, query tests |
| Grounded natural-language interaction and memory | Implemented; optional hosted language model is an external gate | `src/foreightkillo/intelligence/conversation.py`, `/api/v1/conversations/ask` | `tests/unit/test_conversation.py`, executable refusal scenario |
| Approved web/news/macro/sentiment research | Provider-neutral ingestion implemented; approved feeds are external gates | `src/foreightkillo/intelligence/research.py` | `tests/unit/test_research_providers.py` |
| Telegram ingress and delivery | Implemented; bot account is an external gate | `src/foreightkillo/bot/adapters/telegram.py`, polling runtime | bot runtime and provider-adapter tests |
| Discord commands and delivery | Implemented; Discord application is an external gate | `src/foreightkillo/bot/adapters/discord.py`, interaction runtime | bot runtime and provider-adapter tests |
| Secure API, webhooks, and dashboard | Implemented | `src/foreightkillo/api.py`, `security/`, `dashboard.py` | API security and application tests |
| Kill switch, audit, health, and model governance | Implemented | `src/foreightkillo/operations/`, `src/foreightkillo/models/` | operational-control and model-registry tests |
| Deployment and CI | Implemented for self-hosted container | `Dockerfile`, `.github/workflows/ci.yml` | local image build/startup and GitHub Python 3.11/3.12 jobs |
| Live-money trading | Intentionally unavailable | no live mode or adapter exists | safety tests reject live mode; beta gates remain separate |

## Release invariants

1. Market or language-model output never bypasses deterministic risk evaluation.
2. A signal never automatically becomes an order.
3. Messaging and conversation remain read-only for trading and model governance.
4. Missing operational state fails closed.
5. Secrets and third-party accounts are never committed.
6. Live-money execution requires a separate product, security, legal, and operational approval.
