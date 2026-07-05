# ADR-0001: Modular Monolith First

Status: Accepted
Date: 2026-07-04

Purpose: define the initial application architecture.
Scope: runtime structure before production implementation.
Audience: maintainers and engineering leads.
Assumptions: no source code exists; one small team is expected initially; safety boundaries can be expressed inside a modular monolith.
Dependencies: [System Architecture](../SYSTEM_ARCHITECTURE.md), [Technology Evaluation](../../research/TECHNOLOGY_EVALUATION.md).
Unresolved decisions: future service extraction boundaries depend on measured load, compliance isolation, and team ownership.

## Decision

Forakilo will start as a modular monolith with explicit internal planes: control, data, intelligence, trading, and governance/operations.

## Rationale

The repository has no implemented services and no evidence requiring independent deployment, scaling, or fault isolation yet. A modular monolith reduces operational complexity while still requiring strong internal interfaces, audit trails, and trust boundaries.

## Consequences

- Internal modules MUST enforce ownership boundaries.
- Live trading, credential storage, model promotion, and admin actions MUST have explicit authorization and audit controls.
- Service extraction MAY occur later for high-throughput ingestion, model training, or execution adapters if evidence justifies it.

## Alternatives Rejected

- Microservices by default: rejected due lack of implementation evidence and unnecessary operational burden.
- Single unstructured app: rejected because trading, ML, data, and credential boundaries are safety-critical.
