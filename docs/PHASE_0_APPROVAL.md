# Phase 0 approval

## Approval record

- **Decision:** Chainna Phase 0 architecture and scope package
- **Status:** Approved
- **Approval date:** 2026-07-26
- **Approver:** Uchenna Emmanuel Anozie, Product Owner
- **Release boundary:** Chainna 0.1 ends after Phase 3

This approval accepts ADR-0001 through ADR-0009 and the version 0.1 scope. It does not authorize implementation, Phase 1, dependency installation, LEAN builds, data acquisition, broker connectivity or trading.

## Accepted decisions

1. Python 3.12, `uv`, Ruff, pytest and Pyright strict. Windows is the initial development host; Linux portability is required. Docker becomes mandatory before Phase 3.
2. `sandy_parity_v1` uses more-extreme adjacent-pivot replacement, earliest retention for equal extremes, diagnostic/ineligible simultaneous pivots, all-candidate retention, parity-only Gartley > Bat > Butterfly eligibility precedence, canonical Decimal identities, closed bars and distinct event/known times.
3. EUR_USD H1 is the sole universe for research, backtest and later signal-only until a new approved universe version.
4. Immutable JSON manifests, Parquet datasets and DuckDB queries. Initially committed fixtures are synthetic. Missing bars reject by default; fill-forward must be pre-registered and recorded. Midpoint never silently substitutes for bid/ask.
5. LEAN remains commit/build-pinned, external and initially zero-patch. Lean CLI is optional. Containerized reproducibility is required before Phase 3 acceptance. Future patches require a separate ADR.
6. Future operational services use append-only audit/domain events plus transactional current-state tables in PostgreSQL. Full event sourcing is not mandatory. SQLite is non-execution only; JSON/cache is never authoritative operational state.
7. Telegram is the first optional notifier; Discord is deferred. Future practice approval uses an authenticated local web interface. Notifications and approvals are separate trust boundaries, and external notifications exclude sensitive account/broker information.
8. Structural risk controls are accepted: mandatory protective stops, no martingale/grid/averaging down, no runtime override of absolute maxima, fail-closed missing limits, Product Owner approval of evidenced/pre-registered numeric limits, and one-use final holdouts.
9. OANDA Practice is the first broker target. Initially trusted sources are official QuantConnect and OANDA only. Any later integration uses isolated Practice identity, credentials, deployment and account allowlist.

## Chainna 0.1 contents

Version 0.1 includes:

- repository and safety foundation;
- deterministic `sandy_parity_v1`;
- EUR_USD H1;
- synthetic fixtures;
- reproducible manifests;
- a thin external LEAN backtest adapter; and
- direct-versus-LEAN backtest parity evidence.

Version 0.1 excludes signal-only services, notifications, PostgreSQL operational services, approval UI, OANDA connectivity, practice trading, AI/ML and live trading.

## Deferred decisions

- Historical bid/ask source, license and exact H1 calendar/bar-boundary registration.
- Pre-registered numeric risk maxima and walk-forward/promotion thresholds.
- A new untouched holdout after any post-inspection strategy change.
- Exact Phase 7 OANDA Practice evidence duration and order-sample requirements.

These are recorded in `PHASE_0_OPEN_QUESTIONS.md`. The Phase 7 evidence question must remain explicit until a pre-registered Phase 7 entrance decision resolves it.

## Authorization boundary

Phase 0 is complete when this package passes document validation. Phase 1 may begin only after:

1. `PHASE_1_ENTRY_CRITERIA.md` is satisfied; and
2. the Product Owner gives a separate explicit instruction to begin Phase 1.

No ADR acceptance implicitly grants broker or trading authority.
