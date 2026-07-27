# ADR 0011: Deferred LEAN boundary verification and low-resource development path

**Status: Accepted**

**Date:** 2026-07-27

**Approver:** Uchenna Emmanuel Anozie, Product Owner

## Context

Phase 1A-R accurately ended as `BLOCKED_RESOURCE`: the workstation had insufficient free disk for the approved local container/LEAN-build gate, and Docker and .NET were unavailable. That result prevented an executable LEAN/QuantConnect.pythonnet test but did not invalidate the runtime-independent architecture.

Chainna's deterministic core is intentionally separated from LEAN, pythonnet and brokerage infrastructure. Requiring the full LEAN boundary before any repository or domain-foundation work would unnecessarily couple independent phases.

## Decision

1. Preserve Phase 1A-R as `BLOCKED_RESOURCE`.
2. The blocked executable LEAN/pythonnet verification does not block runtime-independent product development.
3. Authorize a later Phase 1B for the repository and deterministic Python foundation, subject to its entry gates and a separate start instruction.
4. Phase 1B uses Python 3.11.11 through `uv` and remains compatible with Python `>=3.11,<3.13`.
5. The Phase 1B domain core must not import QuantConnect, pythonnet, LEAN or brokerage packages.
6. Docker is not required for Phase 1B or the deterministic harmonic core.
7. Real pinned LEAN/pythonnet boundary verification is deferred to a mandatory Phase 3 entrance gate; it is not waived.
8. Phase 3 cannot be accepted until the exact pinned boundary succeeds twice reproducibly in an approved Linux/container environment.
9. Verification may run on the local workstation when resources permit, a controlled remote Linux host, or a version-pinned CI runner.
10. An unrelated latest LEAN image is unacceptable evidence.
11. The 25 GiB free-space threshold applies only to local container, LEAN-build and data-intensive work.
12. Runtime-independent Phase 1 work requires at least 10 GiB free locally, with 12 GiB preferred.
13. Below 10 GiB, dependency installation and test runs must stop.
14. Phase 1B prohibits LEAN integration, market-data acquisition, trading backtests, OANDA dependencies, broker credentials, broker connections and order execution.
15. Chainna 0.1 still ends after Phase 3; this ADR changes sequencing, not the release boundary.

## Reasons

The deterministic package boundary permits useful repository and domain work without embedding the trading runtime. Deferring executable verification concentrates LEAN-specific cost and evidence at the phase that consumes it while keeping the gate mandatory.

## Consequences

- Phase 1B may start only after its resource and repository gates pass.
- Phase 1B code and tests must remain runtime-independent.
- Python 3.11.11 is the local foundation interpreter; Python 3.12 remains CI compatibility coverage.
- Phase 3 planning must budget an approved Linux/container executor and exact pinned build provenance.
- Phase 3 remains blocked until two equivalent successful boundary probes exist.

## Risks

- A late LEAN incompatibility could require adapter or runtime adjustments after the core exists.
- Enforcing the import boundary requires dependency and test controls.
- Ten GiB is an operational floor, not a guarantee that every development tool will fit.
- Remote/CI evidence can drift unless runner, image, commit and artifacts are immutably pinned.

## Alternatives rejected

- Treating Phase 1A-R as a failed architecture is rejected; the architecture was not the failed resource.
- Waiving the LEAN boundary test is rejected.
- Requiring Docker for the pure core is rejected as unnecessary coupling.
- Using an unrelated latest LEAN image is rejected because it cannot prove the accepted pin.
- Lowering the local Phase 1 floor below 10 GiB is rejected due to disk-exhaustion risk.

## Phase gates

### Phase 1B entrance

- At least 10 GiB free locally; 12 GiB preferred.
- Clean canonical repositories at accepted commits.
- No secrets, broker dependencies or broker credentials.
- Exact Python 3.11.11 provisioned through `uv`.
- Scope limited to repository/safety tooling and deterministic runtime-independent Python foundations.

If free space falls below 10 GiB, stop dependency installation and test execution.

### Phase 3 entrance

- Exact LEAN source commit and resulting build/image provenance recorded.
- Approved Linux/container environment, locally, remotely or on pinned CI.
- Canonical Python 3.11.11 runtime.
- QuantConnect.pythonnet and relevant QuantConnect types initialize.
- The external read-only Chainna probe imports outside the LEAN tree.
- No data, brokerage or order path is required by the boundary probe.
- Two reproducible successful runs with equivalent important outputs.

## Explicit implementation impact

This ADR authorizes sequencing only. It does not start Phase 1B, create product files, install dependencies or authorize LEAN, data, backtest or broker work.
