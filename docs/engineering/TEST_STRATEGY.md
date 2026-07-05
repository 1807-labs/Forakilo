# Test Strategy

Purpose: define risk-based testing for Forakilo.
Scope: documentation, backend, dashboard, data, ML, trading, security, operations, and releases.
Audience: engineers, QA, security reviewers, risk reviewers, and release owners.
Assumptions: no tests exist yet.
Dependencies: [Quality Gates](QUALITY_GATES.md), [Backtesting Standard](../trading/BACKTESTING_AND_VALIDATION_STANDARD.md).
Unresolved decisions: test frameworks and coverage thresholds.

## Required Test Types

Unit, property-based, contract, integration, database, migration, API, authentication, authorization, security, dashboard, accessibility, data-quality, replay, model, leakage, backtesting, execution simulation, sandbox provider, reconciliation, chaos, performance, load, recovery, backup-restore, dependency, supply-chain, end-to-end, paper-trading acceptance, and live-readiness tests.

## High-Risk Fixtures

Stale data, duplicate ticks, out-of-order provider events, revised macro data, partial fills, timeout after possible order acceptance, precision rejection, insufficient margin, provider rate limits, model drift, calibration failure, credential revocation, session theft, and reconciliation mismatch.

## Determinism

Tests SHOULD use deterministic clocks, seeded randomness, fixed provider fixtures, and isolated storage.
