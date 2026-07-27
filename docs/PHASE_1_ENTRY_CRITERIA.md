# Phase 1 entry criteria

## Purpose

Phase 1 is limited to the repository and safety foundation described in `IMPLEMENTATION_PLAN.md`. Meeting these criteria does not itself begin Phase 1; explicit Product Owner authorization is still required.

## Mandatory pre-entry checklist

- [ ] **Clean repository status:** intended Phase 0 documentation is committed or otherwise explicitly reviewed, with no unexplained changes or artifacts.
- [ ] **Accepted ADRs:** ADR-0001 through ADR-0009 are `Accepted`, dated 2026-07-26 and attributed to Uchenna Emmanuel Anozie, Product Owner.
- [x] **Workspace location:** the canonical workspace is outside OneDrive at `C:\Users\Wildf\chainna`, as recorded in `WORKSPACE_LOCATION.md`.
- [ ] **No secrets:** repository and relevant untracked files pass secret review; no tokens, passwords, private keys, account IDs or credential-bearing configuration is present.
- [ ] **No broker dependencies:** no OANDA or other brokerage implementation/client dependency is installed, vendored, locked or referenced as an executable dependency.
- [ ] **No broker credentials:** no Practice or Live credentials, secret-provider bindings or account allowlists are introduced.
- [ ] **Protected repositories clean:** `engine/lean/` and `legacy/chains/` have clean repository status and remain unmodified.
- [ ] **Compatibility spike resolved:** following ADR-0010, exact Python 3.11.11 is the required LEAN-facing candidate and Python 3.12.4 is secondary. The external-package and real QuantConnect.pythonnet boundary must be verified reproducibly without Chainna product source, market data, backtests or broker components. Phase 1A-R is currently `BLOCKED_RESOURCE`.
- [ ] **Narrow Phase 1 scope:** work is limited to repository/tooling and safety foundation: approved package/tool configuration, locking, lint/type/test framework, CI, secret/dependency/license controls, mode schema, initial domain/event schemas and tests proving execution is unavailable.
- [ ] **No broker execution:** Phase 1 explicitly does not implement brokerage adapters, OANDA connectivity, order submission, practice execution or live execution.

## Compatibility-spike plan requirement

Before Phase 1 authorization, record a bounded plan that identifies:

- the pinned LEAN commit and existing build/runtime provenance to inspect;
- the Python 3.11.11 canonical boundary and secondary Python 3.12.4 compatibility question;
- read-only or disposable test steps;
- Windows host and Linux portability considerations;
- success/failure evidence;
- cleanup expectations; and
- a stop condition before any product scaffolding if compatibility fails.

The spike is evidence for ADR-0010 and ADR-0005. Python 3.11.11 is required for LEAN/release validation; future CI must also test Python 3.12. It is not a LEAN build authorization unless the Product Owner separately expands the task and the 25 GiB resource gate passes.

## Phase 1 prohibited work

- Strategy or Sandy implementation.
- LEAN adapter implementation or backtests.
- Market-data acquisition.
- Docker/Phase 3 integration work beyond documenting future requirements.
- Signal-only services, notification adapters or operational databases.
- Approval UI or risk/execution workflows.
- Broker package selection/installation, credentials, connectivity or orders.

## Entry approval record

When all checklist items pass, record:

- repository commit/status evidence;
- workspace path or exception;
- compatibility-spike plan reference;
- scope confirmation;
- approval date and approver; and
- the explicit Product Owner instruction authorizing Phase 1.

Until that record exists, implementation remains unauthorized.
