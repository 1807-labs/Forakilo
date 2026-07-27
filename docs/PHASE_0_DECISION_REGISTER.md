# Phase 0 decision register

Phase 0 decisions were approved by the Product Owner on 2026-07-26. Acceptance finalizes architecture and scope only; it does not authorize implementation or begin Phase 1.

| Decision ID | Subject | Recommendation | Alternatives | Status | Human decision required | Blocking phase | Evidence | Final approval date | Approver |
|---|---|---|---|---|---|---|---|---|---|
| ADR-0001 | Language and package tooling | Original Python 3.12 decision, `uv`, Ruff, Pyright strict and pytest; Python-version portion superseded by ADR-0010 | Poetry; pip-tools; C# core | Accepted; amended in part | See ADR-0010 | Phase 1 | Phase 1A found official LEAN baseline Python 3.11.11; real boundary remains unverified | 2026-07-26 | Uchenna Emmanuel Anozie, Product Owner |
| ADR-0002 | Harmonic semantics | Immutable `sandy_parity_v1`; more-extreme normalization; ambiguous simultaneous pivots ineligible; retain all candidates; parity-only Sandy precedence | Reject adjacent pivots; preserve raw Sandy behavior; ranges/confluence immediately | Accepted | None | Phase 2 | Synthetic/golden cases and written parity differences | 2026-07-26 | Uchenna Emmanuel Anozie, Product Owner |
| ADR-0003 | Initial market universe | EUR_USD H1 only across research, backtest and later signal-only; completed bid/ask-aware QuoteBars | More pairs; lower/higher resolution; midpoint bars | Accepted | None | Phase 2/3 | Data availability/licensing and pipeline validation plan | 2026-07-26 | Uchenna Emmanuel Anozie, Product Owner |
| ADR-0004 | Data and experiment storage | Synthetic committed fixtures; bid/ask data; UTC Parquet; immutable JSON manifests; DuckDB; missing-bar rejection by default | CSV/JSON datasets; database-first; cloud object store first | Accepted | None | Phase 3 | Vendor/license assessment and manifest/schema review | 2026-07-26 | Uchenna Emmanuel Anozie, Product Owner |
| ADR-0005 | LEAN runtime boundary | Commit/build-pinned external LEAN; thin adapters; isolated config; zero initial patches; optional CLI; containerized by Phase 3 | Embed product in LEAN; fork customization; direct broker integration | Accepted | None | Phase 1/3 | Compatibility spike, build provenance and containerized reproducibility | 2026-07-26 | Uchenna Emmanuel Anozie, Product Owner |
| ADR-0006 | Operational state | Append-only audit/domain events plus transactional current state; PostgreSQL later; SQLite non-execution only | Full event sourcing; SQLite operational service; JSON/cache state | Accepted | None | Phase 5/6 | Event schema, transaction/idempotency and restore/reconciliation design | 2026-07-26 | Uchenna Emmanuel Anozie, Product Owner |
| ADR-0007 | Notifications and approval | Telegram first optional notifier; authenticated local web approval later; separate trust boundaries | Discord first; chat approval; CLI approval; hosted UI first | Accepted | None | Phase 5/6 | Threat model, redaction rules and operator workflow | 2026-07-26 | Uchenna Emmanuel Anozie, Product Owner |
| ADR-0008 | Risk ceilings and promotion | Structural controls accepted; mandatory protective stops; no runtime maximum overrides; missing limits fail closed; one-use holdout | Placeholder defaults; discretionary promotion; optimizer-led promotion | Accepted | Numeric values remain subject to evidence and Product Owner pre-approval | Phase 1/4/6 | Research protocol, safety tests and signed ceiling register | 2026-07-26 | Uchenna Emmanuel Anozie, Product Owner |
| ADR-0009 | OANDA Practice plugin selection | OANDA Practice first; official QuantConnect/OANDA sources only; isolated identity/profile; formal later verification | Install now; direct OANDA client; another broker | Accepted | Phase 7 evidence duration and order-sample requirements remain deferred | Phase 7 | Verified candidate dossier and pre-registered Phase 7 entrance decision | 2026-07-26 | Uchenna Emmanuel Anozie, Product Owner |
| ADR-0010 | Python runtime baseline amendment | Python 3.11.11 LEAN/release baseline; package `>=3.11,<3.13`; CI on 3.11/3.12; no 3.12-only product requirements | Keep 3.12 canonical; support 3.11 only; patch LEAN | Accepted | None | Phase 1/3 | Phase 1A static evidence plus later executable Python 3.11 boundary proof | 2026-07-27 | Uchenna Emmanuel Anozie, Product Owner |
| ADR-0011 | Deferred LEAN verification and low-resource development | Permit runtime-independent Phase 1B at >=10 GiB free; defer mandatory twice-reproducible pinned LEAN boundary to Phase 3 entrance | Block all work on LEAN; waive boundary; require Docker for core | Accepted | None | Phase 1B/3 | Import-boundary controls in Phase 1B; pinned Linux/container boundary evidence before Phase 3 | 2026-07-27 | Uchenna Emmanuel Anozie, Product Owner |

## Approval rule

The accepted ADRs govern later work. Evidence and phase gates still apply:

1. every approval question in that ADR has an explicit answer;
2. required evidence is attached or referenced;
3. consequences and residual risks are acknowledged;
4. the approver and date are recorded; and
5. dependent ADRs do not contradict the decision.

Acceptance does not begin Phase 1. Phase 1 requires explicit authorization after `PHASE_1_ENTRY_CRITERIA.md` is satisfied.
