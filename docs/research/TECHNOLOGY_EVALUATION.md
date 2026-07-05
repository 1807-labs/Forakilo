# Technology Evaluation

Purpose: select initial technologies for Forakilo before implementation.
Scope: application, dashboard, storage, data engineering, ML, backtesting, infrastructure, and DevSecOps choices.
Audience: maintainers, engineering leads, security reviewers, and product owners.
Assumptions: Forakilo starts as a pre-development repository; local development on Windows is expected; production hosting is not selected; open-source and self-hostable options are preferred.
Dependencies: [Sources](SOURCES.md), [ADR Index](../architecture/decisions/ADR-INDEX.md).
Unresolved decisions: exact package versions, hosting provider, paid data vendors, and final broker/exchange integration require later spikes and approvals.

## Selection Summary

| Responsibility | Primary choice | Rejected or deferred alternatives | Decision |
| --- | --- | --- | --- |
| Python runtime | Python 3.13 | Python 3.11/3.12 | Current active runtime with longer remaining support than 3.11/3.12. Compatibility must be re-tested when manifests are added. |
| API framework | FastAPI | Django, Flask | Typed async API, OpenAPI support, good fit for a modular monolith. Django is heavier for service APIs; Flask needs more assembly. |
| Validation/schema | Pydantic v2 | Marshmallow, attrs-only | Strong type-driven validation and JSON schema support. |
| ORM/database access | SQLAlchemy 2.x | Django ORM, raw SQL only | Mature Python database layer with async support and Alembic integration. |
| Migrations | Alembic | Flyway, custom scripts | Python-native SQLAlchemy migration tool. |
| Background jobs | Taskiq or FastAPI-integrated workers, final choice deferred | Celery, RQ | Keep MVP simple; select after concrete job needs are implemented. |
| Workflow orchestration | Prefect, deferred until pipelines exist | Airflow, Dagster | Prefect is simpler for Python-first workflows; no orchestrator is needed before pipelines exist. |
| Streaming/API updates | WebSocket/SSE via FastAPI for MVP | GraphQL subscriptions | Native dashboard update path; broker-backed fanout can follow. |
| Configuration | Pydantic Settings plus environment variables | ad hoc `.env` parsing | Typed, auditable configuration. Secrets are never committed. |
| Dashboard framework | Next.js with TypeScript and React | Vite SPA, Remix | Strong React ecosystem, server/client flexibility, and established accessibility tooling. |
| UI system | Tailwind CSS plus Radix/shadcn-style primitives | Material UI, custom CSS only | Accessible primitives with local control; avoid theme lock-in. |
| Charts | Apache ECharts | TradingView commercial widgets, Chart.js only | Rich candlestick and time-series support under Apache-2.0. TradingView licensing needs separate review. |
| Server state | TanStack Query | Redux-only, raw fetch | Strong data-fetching and cache invalidation model. |
| Relational database | PostgreSQL | MySQL, SQLite-only | Reliable system of record and strong ecosystem. SQLite remains a dev/test substitute only. |
| Time-series | PostgreSQL partitioning first; Apache-licensed TimescaleDB features optional | InfluxDB | Keep relational consistency and avoid license ambiguity until volume requires extension features. |
| Cache | Valkey | Redis 7.4+ | Valkey keeps a permissive open-source posture after Redis licensing changes. |
| Message transport | NATS JetStream | Kafka, Redpanda | Lightweight single-binary path fits MVP; Kafka is deferred until throughput/retention needs justify it. |
| Object/artifact storage | S3-compatible storage such as MinIO locally | Local filesystem only | Supports future model artifacts, datasets, and backups with cloud portability. |
| Data frames | pandas and Polars | pandas-only | pandas ecosystem breadth plus Polars performance for larger analytical workloads. |
| Data quality | Great Expectations GX Core | custom validators only | Declarative suites, docs, and repeatable checks. |
| Dataset lineage/versioning | MLflow artifacts plus content fingerprints first; DVC optional | full feature store first | Avoid premature feature-store complexity while preserving reproducibility. |
| Baseline ML | scikit-learn | deep learning first | Simple, interpretable baselines before complex models. |
| Gradient boosting | XGBoost primary candidate; LightGBM alternative | TensorFlow, RL | Strong tabular baseline candidate; LightGBM kept as alternative due packaging/licensing review. |
| Deep learning | PyTorch deferred | TensorFlow | Only after baselines prove a need; not in MVP core path. |
| Hyperparameter optimization | Optuna, gated | manual-only | Useful after leakage-safe validation exists. |
| Experiment/model registry | MLflow | Weights & Biases SaaS, custom registry | Self-hostable, broad ecosystem, registry support. |
| Model monitoring | Evidently plus custom trading metrics | vendor-only monitors | Self-hostable model/data monitoring starter. |
| Backtesting | VectorBT for vectorized research; event-driven engine spike with NautilusTrader | Backtrader primary | Avoid relying on one engine for all truth. Backtrader rejected as primary due GPL and maintenance risk. |
| Dependency management | uv | Poetry, pip-tools | Fast Python project management and lockfile support. |
| Lint/format | Ruff | Flake8 + Black + isort stack | Single fast tool for many checks. |
| Type checking | Pyright or mypy, final choice deferred | none | Required gate once code exists. |
| Security scanning | Semgrep CE, pip-audit, gitleaks, Trivy/Grype | single scanner only | Layered checks for code, dependencies, secrets, and containers. |
| SBOM | CycloneDX | SPDX-only | Strong application-security ecosystem and VEX path. |
| Provenance/signing | SLSA provenance and Sigstore Cosign | unsigned artifacts | Required before release artifacts exist. |
| Observability | OpenTelemetry | vendor SDK only | Portable metrics, logs, traces, and correlation IDs. |

## MVP Technology Principles

- The system SHOULD begin as a modular monolith with clear internal planes.
- Trading intelligence SHOULD be implemented in Forakilo-controlled code and infrastructure where practical.
- Hosted general-purpose LLM APIs MUST NOT be in the real-time market-analysis, risk-control, or order-execution path.
- Deterministic risk controls MUST operate independently of model output.
- Paper trading MUST be the default execution mode.
- Live trading MUST remain disabled until legal, security, risk, data, model, operations, and human approval gates pass.

## Rejected MVP Ideas

- Microservices as a default architecture: rejected because no scaling, ownership, or isolation evidence exists yet.
- Reinforcement learning in the MVP: rejected because it adds safety and validation complexity without a proven advantage.
- Scraping economic calendars by default: rejected unless terms, robots, licensing, attribution, and operational risk are approved.
- Binance as an initial Canadian live provider: rejected for initial scope because Canadian availability and regulatory status are unsuitable for a Canada-first product baseline.
- Redis 7.4+ as default cache: rejected in favor of Valkey due source-available licensing concerns.
