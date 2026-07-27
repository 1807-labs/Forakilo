# Phase 1B entry criteria

## Purpose

Phase 1B is limited to the repository, safety tooling and deterministic runtime-independent Python foundation described in `IMPLEMENTATION_PLAN.md`. ADR-0011 permits this work before the LEAN boundary test, but meeting these criteria does not itself start Phase 1B; an explicit start instruction is still required.

## Mandatory pre-entry checklist

- [ ] **Clean repository status:** intended Phase 0 documentation is committed or otherwise explicitly reviewed, with no unexplained changes or artifacts.
- [ ] **Accepted ADRs:** ADR-0001 through ADR-0009 are `Accepted`, dated 2026-07-26 and attributed to Uchenna Emmanuel Anozie, Product Owner.
- [x] **Workspace location:** the canonical workspace is outside OneDrive at `C:\Users\Wildf\chainna`, as recorded in `WORKSPACE_LOCATION.md`.
- [ ] **No secrets:** repository and relevant untracked files pass secret review; no tokens, passwords, private keys, account IDs or credential-bearing configuration is present.
- [ ] **No broker dependencies:** no OANDA or other brokerage implementation/client dependency is installed, vendored, locked or referenced as an executable dependency.
- [ ] **No broker credentials:** no Practice or Live credentials, secret-provider bindings or account allowlists are introduced.
- [ ] **Protected repositories clean:** `engine/lean/` and `legacy/chains/` have clean repository status and remain unmodified.
- [ ] **Local resource floor:** at least 10 GiB free before dependency installation or test execution; 12 GiB is preferred. If free space falls below 10 GiB, stop both activities. The 25 GiB threshold applies only to local container, LEAN-build and data-intensive work.
- [ ] **Python baseline:** exact Python 3.11.11 is provisioned through `uv`; package compatibility remains `>=3.11,<3.13`, with future CI coverage for 3.11 and 3.12.
- [ ] **Runtime-independent boundary:** Phase 1B domain code and dependencies do not import QuantConnect, pythonnet, LEAN or brokerage packages.
- [ ] **Narrow Phase 1B scope:** work is limited to repository/tooling and safety foundation plus deterministic runtime-independent Python foundations.
- [ ] **No broker execution:** Phase 1B does not implement brokerage adapters, OANDA connectivity, order submission, practice execution or live execution.

## Deferred LEAN verification

The Phase 1A-R `BLOCKED_RESOURCE` result is preserved and does not block Phase 1B. Its remaining executable test is deferred, not waived. Before Phase 3 entrance, record and execute a bounded plan that identifies:

- the pinned LEAN commit and existing build/runtime provenance to inspect;
- the Python 3.11.11 canonical boundary and secondary Python 3.12.4 compatibility question;
- read-only or disposable test steps;
- Windows host and Linux portability considerations;
- success/failure evidence;
- cleanup expectations; and
- a stop condition before any product scaffolding if compatibility fails.

The spike is evidence for ADR-0010, ADR-0011 and ADR-0005. Python 3.11.11 is required for LEAN/release validation. The exact pinned LEAN boundary must succeed twice reproducibly on an approved Linux/container environment before Phase 3 can be accepted.

## Phase 1B prohibited work

- Strategy or Sandy implementation.
- LEAN adapter implementation or backtests.
- Market-data acquisition.
- LEAN or pythonnet integration.
- Docker/Phase 3 integration beyond documenting future requirements.
- Trading backtests.
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
- the explicit instruction authorizing Phase 1B.

Until that record exists, Phase 1B implementation remains unauthorized. At the current measured 7.72 GiB free, the 10 GiB resource criterion does not pass.
