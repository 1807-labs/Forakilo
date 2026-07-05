# Forakilo Documentation Index

Purpose: provide the pre-development documentation map for Forakilo.
Scope: repository foundation, product intent, architecture, security, data, ML, trading, compliance, operations, engineering, roadmap, and backlog documents.
Audience: maintainers, product owners, engineers, reviewers, risk approvers, security reviewers, and legal counsel.
Assumptions: Forakilo is pre-development; Canada is the initial research jurisdiction; live trading is out of scope until gates are met.
Dependencies: [README.md](README.md), [docs/research/SOURCES.md](docs/research/SOURCES.md), [docs/product/GLOSSARY.md](docs/product/GLOSSARY.md).
Unresolved decisions: legal operating permissions, provider contracts, hosting region, and final commercial licensing model require owner or counsel input.

## Repository Status

Forakilo currently contains documentation and backlog artifacts only. No production application code, tests, dependency manifests, workflows, containers, deployed infrastructure, brokerage accounts, or exchange integrations were verified as implemented on 2026-07-04.

## Start Here

- [Product Vision](docs/product/PRODUCT_VISION.md)
- [Product Requirements Document](docs/product/PRODUCT_REQUIREMENTS_DOCUMENT.md)
- [Scope and Non-Goals](docs/product/SCOPE_AND_NON_GOALS.md)
- [System Architecture](docs/architecture/SYSTEM_ARCHITECTURE.md)
- [Delivery Roadmap](docs/roadmap/DELIVERY_ROADMAP.md)
- [Security Policy](SECURITY.md)
- [Completion Report](COMPLETION_REPORT.md)

## Research and Decisions

- [Repository Evidence Inventory](docs/research/REPOSITORY_EVIDENCE_INVENTORY.md)
- [Sources](docs/research/SOURCES.md)
- [Technology Evaluation](docs/research/TECHNOLOGY_EVALUATION.md)
- [API and Data Provider Matrix](docs/research/API_AND_DATA_PROVIDER_MATRIX.md)
- [ADR Index](docs/architecture/decisions/ADR-INDEX.md)

## Product

- [Personas and User Journeys](docs/product/PERSONAS_AND_USER_JOURNEYS.md)
- [Feature Catalogue](docs/product/FEATURE_CATALOGUE.md)
- [Dashboard Specification](docs/product/DASHBOARD_SPECIFICATION.md)
- [Use Cases and Edge Cases](docs/product/USE_CASES_AND_EDGE_CASES.md)
- [Non-Functional Requirements](docs/product/NON_FUNCTIONAL_REQUIREMENTS.md)
- [User Story Audit](docs/product/USER_STORY_AUDIT.md)
- [Backlog Gap Analysis](docs/product/BACKLOG_GAP_ANALYSIS.md)
- [Requirements Traceability Matrix](docs/product/REQUIREMENTS_TRACEABILITY_MATRIX.md)
- [Epic and Release Map](docs/product/EPIC_AND_RELEASE_MAP.md)
- [Glossary](docs/product/GLOSSARY.md)

## Architecture

- [System Context](docs/architecture/SYSTEM_CONTEXT.md)
- [Component Responsibilities](docs/architecture/COMPONENT_RESPONSIBILITIES.md)
- [Data Flow](docs/architecture/DATA_FLOW.md)
- [Trust Boundaries](docs/architecture/TRUST_BOUNDARIES.md)
- [Deployment Architecture](docs/architecture/DEPLOYMENT_ARCHITECTURE.md)
- [Environment Strategy](docs/architecture/ENVIRONMENT_STRATEGY.md)
- [Integration Architecture](docs/architecture/INTEGRATION_ARCHITECTURE.md)

## Security

- [Authentication and Authorization](docs/security/AUTHENTICATION_AND_AUTHORIZATION.md)
- [Account and Session Lifecycle](docs/security/ACCOUNT_AND_SESSION_LIFECYCLE.md)
- [Exchange Credential Security](docs/security/EXCHANGE_CREDENTIAL_SECURITY.md)
- [Threat Model](docs/security/THREAT_MODEL.md)
- [Security Requirements](docs/security/SECURITY_REQUIREMENTS.md)
- [Secrets and Key Management](docs/security/SECRETS_AND_KEY_MANAGEMENT.md)
- [Secure SDLC](docs/security/SECURE_SDLC.md)
- [Abuse and Fraud Controls](docs/security/ABUSE_AND_FRAUD_CONTROLS.md)
- [Supply Chain Security](docs/security/SUPPLY_CHAIN_SECURITY.md)

## Data, ML, and Trading

- [Data Architecture](docs/data/DATA_ARCHITECTURE.md)
- [Data Contracts and Schemas](docs/data/DATA_CONTRACTS_AND_SCHEMAS.md)
- [Data Quality and Validation](docs/data/DATA_QUALITY_AND_VALIDATION.md)
- [Data Lineage and Retention](docs/data/DATA_LINEAGE_AND_RETENTION.md)
- [Data Feature Catalogue](docs/data/FEATURE_CATALOGUE.md)
- [Model Strategy](docs/ml/MODEL_STRATEGY.md)
- [Training and Retraining Pipeline](docs/ml/TRAINING_AND_RETRAINING_PIPELINE.md)
- [Model Validation](docs/ml/MODEL_VALIDATION.md)
- [Model Monitoring and Drift](docs/ml/MODEL_MONITORING_AND_DRIFT.md)
- [Model Registry and Promotion](docs/ml/MODEL_REGISTRY_AND_PROMOTION.md)
- [Model Card Template](docs/ml/MODEL_CARD_TEMPLATE.md)
- [AI Risk Register](docs/ml/AI_RISK_REGISTER.md)
- [Trading Domain Specification](docs/trading/TRADING_DOMAIN_SPECIFICATION.md)
- [Backtesting and Validation Standard](docs/trading/BACKTESTING_AND_VALIDATION_STANDARD.md)
- [Signal Lifecycle](docs/trading/SIGNAL_LIFECYCLE.md)
- [Risk Management Policy](docs/trading/RISK_MANAGEMENT_POLICY.md)
- [Order Execution and Reconciliation](docs/trading/ORDER_EXECUTION_AND_RECONCILIATION.md)
- [Paper to Live Trading Gate](docs/trading/PAPER_TO_LIVE_TRADING_GATE.md)
- [Failure Modes and Edge Cases](docs/trading/FAILURE_MODES_AND_EDGE_CASES.md)

## Legal and Operations

- [Product Classification and Regulatory Assumptions](docs/legal/PRODUCT_CLASSIFICATION_AND_REGULATORY_ASSUMPTIONS.md)
- [Jurisdiction Research](docs/legal/JURISDICTION_RESEARCH.md)
- [Risk Disclosure](docs/legal/RISK_DISCLOSURE.md)
- [Terms of Service Draft](docs/legal/TERMS_OF_SERVICE_DRAFT.md)
- [Privacy Policy Draft](docs/legal/PRIVACY_POLICY_DRAFT.md)
- [Acceptable Use Policy](docs/legal/ACCEPTABLE_USE_POLICY.md)
- [Data Retention Policy](docs/legal/DATA_RETENTION_POLICY.md)
- [Legal Review Checklist](docs/legal/LEGAL_REVIEW_CHECKLIST.md)
- [Observability](docs/operations/OBSERVABILITY.md)
- [Service Level Objectives](docs/operations/SERVICE_LEVEL_OBJECTIVES.md)
- [Alerting and Escalation](docs/operations/ALERTING_AND_ESCALATION.md)
- [Incident Response Plan](docs/operations/INCIDENT_RESPONSE_PLAN.md)
- [Backup and Disaster Recovery](docs/operations/BACKUP_AND_DISASTER_RECOVERY.md)
- [Business Continuity](docs/operations/BUSINESS_CONTINUITY.md)
- [Runbook Index](docs/operations/RUNBOOK_INDEX.md)
- [Change and Release Management](docs/operations/CHANGE_AND_RELEASE_MANAGEMENT.md)

## Engineering and Backlog

- [Test Strategy](docs/engineering/TEST_STRATEGY.md)
- [Quality Gates](docs/engineering/QUALITY_GATES.md)
- [CI/CD Strategy](docs/engineering/CI_CD_STRATEGY.md)
- [Development Standards](docs/engineering/DEVELOPMENT_STANDARDS.md)
- [Story Backlog](.github/ISSUES_STORIES_TODO/README.md)
- [Contributing](CONTRIBUTING.md)
- [Support](SUPPORT.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Changelog](CHANGELOG.md)
