# ADR-0002: Python API Stack

Status: Accepted
Date: 2026-07-04

Purpose: select the backend technology baseline.
Scope: API, validation, persistence access, migrations, and configuration.
Audience: backend engineers and reviewers.
Assumptions: Python ML and data tooling are central to Forakilo; exact versions will be pinned when manifests are created.
Dependencies: [Technology Evaluation](../../research/TECHNOLOGY_EVALUATION.md), [Sources](../../research/SOURCES.md).
Unresolved decisions: background-job library and workflow orchestrator require implementation spikes.

## Decision

Use Python 3.13, FastAPI, Pydantic v2, SQLAlchemy 2.x, Alembic, and typed settings for the backend modular monolith.

## Rationale

This stack aligns API development with Python-native data and ML libraries, provides OpenAPI documentation, and supports explicit schema validation.

## Consequences

- Code MUST be typed and linted once implementation begins.
- API models MUST distinguish public response schemas from persistence models.
- Database migrations MUST be reviewed and tested.

## Alternatives Rejected

- Django: strong framework, but heavier than needed for the initial API-centric system.
- Flask: flexible, but requires assembling more security and schema conventions.
- Raw SQL only: useful for critical queries, but not as the default access strategy.
