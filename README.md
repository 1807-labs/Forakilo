# For8killo

For8killo is a self-hosted, evidence-led market-intelligence and paper-practice platform.
Foreight is its conversational research agent. The canonical Python namespace is
`foreightkillo`, and the command-line entry point is `for8killo`.

## Working MVP

The current MVP includes:

- deterministic market-structure, liquidity-sweep, imbalance, volatility, and regime analysis;
- explainable trend, momentum, breakout, mean-reversion, harmonic, and multi-timeframe research;
- cost-, freshness-, exposure-, regime-, and uncertainty-aware signal ranking;
- synthetic local FX, commodity, and crypto data for deterministic development;
- point-in-time backtesting with next-bar fills, explicit friction, sizing, and drawdown metrics;
- fail-closed risk gates, idempotent paper orders, and authorized practice-account routing;
- portfolio accounting, realized/unrealized performance, and broker reconciliation;
- governed model-version registration, validation evidence, manual promotion, and audit history;
- persistent conversation memory, approved-source research ingestion, and grounded explanations;
- scoped API-key authentication, signed webhooks, persistent kill switch, and operational audit;
- an authenticated browser console plus read-only Telegram and Discord integration foundations;
- executable behavior specifications under [`features/`](features/).

Live-money execution does not exist in this release. Messaging cannot mutate trading state. No
profitability, accuracy, or return is promised.

## Run locally

Python 3.11 or 3.12 and [uv](https://docs.astral.sh/uv/) are required.

```powershell
uv sync --all-groups
$env:FOR8KILLO_API_KEY="local.replace-with-at-least-24-random-characters"
uv run for8killo
```

Open `http://127.0.0.1:8000/`. Enter the same `key-id.secret` value in the operator console. The
OpenAPI interface is available at `/docs`; the unauthenticated liveness endpoint is `/health`.
Runtime state defaults to `.state/`, which is excluded from Git. See [`.env.example`](.env.example)
for optional integration settings.

## Run in Docker

```powershell
docker build -t for8killo:local .
docker run --rm -p 8000:8000 -e FOR8KILLO_API_KEY="local.replace-with-at-least-24-random-characters" for8killo:local
```

The image runs as a non-root user and stores SQLite operational state under `/app/.state`. Mount
that directory as a volume when persistence across containers is required.

## Validate

```powershell
uv run ruff format --check .
uv run ruff check .
uv run pytest -q
uv run behave
uv run pyright
uv run pip-audit --progress-spinner off
```

The bundled provider is synthetic and identifies itself as such. Install an approved, licensed
market-data provider before using the system for real decisions. Practice-broker execution still
requires a matching unexpired proposal, approving deterministic risk decision, and one-time human
authorization.

## Documentation

Start with the [documentation index](DOCUMENTATION_INDEX.md),
[implementation evidence](docs/product/MVP_IMPLEMENTATION_EVIDENCE.md),
[system architecture](docs/architecture/SYSTEM_ARCHITECTURE.md),
[risk policy](docs/trading/RISK_MANAGEMENT_POLICY.md),
[MVP exit criteria](docs/roadmap/MVP_SCOPE_AND_EXIT_CRITERIA.md), and
[security policy](SECURITY.md).

## License

For8killo is distributed under [GPL-3.0](LICENSE).
