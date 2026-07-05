# Forakilo

Forakilo is a pre-development repository for an authenticated AI-assisted quantitative market-analysis and paper-trading platform for cryptocurrency and foreign-exchange markets.

The project is currently a documentation and planning baseline. No production application code, dashboard, trading engine, market-data connector, model pipeline, broker/exchange integration, CI workflow, tests, or deployed service is implemented in this repository yet.

## Purpose

Forakilo is intended to help users research market data, validate strategies, monitor model behavior, and operate paper trading before any controlled live execution is considered.

The product direction emphasizes:

- Capital preservation before return optimization.
- Paper trading before live trading.
- Deterministic risk controls before any order.
- Complete auditability of significant user, data, model, risk, and execution events.
- Point-in-time data correctness.
- Truthful reporting of implementation status and performance limits.

## Safety Position

Forakilo must not promise returns, trade quality, prediction accuracy, or elimination of financial risk. Historical or simulated performance must not be presented as proof of future results.

Live trading is disabled until explicit legal, security, data, model, risk, operations, provider, and human approval gates are satisfied. Automated retraining may create candidate models, but MVP and initial live releases must not silently promote a candidate model into live capital execution.

## Current Repository State

Verified on 2026-07-04:

- Present: documentation baseline, normalized planning backlog, GPL-3.0 license.
- Missing: application source, tests, dependency manifests, workflows, Docker files, infrastructure, secrets, model artifacts, provider accounts, and deployments.

See [Repository Evidence Inventory](docs/research/REPOSITORY_EVIDENCE_INVENTORY.md).

## Architecture Direction

The selected initial architecture is a modular monolith with explicit internal planes:

- Control Plane
- Data Plane
- Intelligence Plane
- Trading Plane
- Governance and Operations Plane

See [System Architecture](docs/architecture/SYSTEM_ARCHITECTURE.md) and [ADR Index](docs/architecture/decisions/ADR-INDEX.md).

## Documentation

Start with [DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md). Key documents:

- [Product Vision](docs/product/PRODUCT_VISION.md)
- [Product Requirements Document](docs/product/PRODUCT_REQUIREMENTS_DOCUMENT.md)
- [Delivery Roadmap](docs/roadmap/DELIVERY_ROADMAP.md)
- [MVP Scope and Exit Criteria](docs/roadmap/MVP_SCOPE_AND_EXIT_CRITERIA.md)
- [Paper to Live Trading Gate](docs/trading/PAPER_TO_LIVE_TRADING_GATE.md)
- [Security Policy](SECURITY.md)
- [Contributing](CONTRIBUTING.md)

## Development Status

There is no verified functional setup yet because no application code or dependency manifest exists. Setup instructions will be added only after a working local development path is implemented and tested.

## Risk and Non-Advisory Notice

Forakilo documentation is not financial, investment, legal, tax, or trading advice. Cryptocurrency, FX, CFDs, derivatives, and margin products can involve substantial loss. Users remain responsible for provider terms, market risk, tax obligations, and their own decisions.

## License

This repository contains a GPL-3.0 license in [LICENSE](LICENSE).
