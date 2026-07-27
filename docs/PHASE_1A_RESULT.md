# Phase 1A result

## Current outcome

**BLOCKED_RESOURCE**

Phase 1A-R on 2026-07-27 stopped at the mandatory resource gate: 7.19 GiB was free on the workspace drive, below the Chainna 25 GiB threshold. Docker and .NET were also absent. No runtime environments, container or build were provisioned.

ADR-0011 preserves this result while clarifying that it was not a failed architecture. The remaining executable verification is deferred, not waived. Runtime-independent Phase 1B may proceed only after its separate entry criteria pass because the product core is designed not to depend on LEAN or pythonnet. Phase 3 remains blocked until the executable boundary succeeds twice reproducibly.

ADR-0010 nevertheless resolves the architecture decision: Python 3.11.11 is canonical for LEAN/release work; Chainna supports `>=3.11,<3.13`; Python 3.12 is secondary.

## Original Phase 1A outcome

**BLOCKED: environment or dependency problem prevented a conclusion.**

Python 3.12.4 and `uv 0.11.32` successfully created and recreated an isolated environment and imported a trivial local package outside the LEAN tree. Static inspection shows that the pinned LEAN runtime officially uses Python 3.11.11, .NET 10 and `QuantConnect.pythonnet` 2.0.64.

The decisive LEAN/pythonnet boundary was not runnable because:

- this Windows host has no .NET SDK or runtime;
- the LEAN checkout has no authorized prebuilt boundary selected for this test;
- building LEAN is prohibited in Phase 1A;
- Docker is absent; and
- installing an arbitrary upstream `pythonnet` package would not represent the pinned QuantConnect fork.

The task explicitly forbids marking `PASS` from static evidence alone. `BLOCKED` is therefore the only defensible outcome.

## What passed

- All three repositories were clean at entry.
- LEAN matched accepted commit `cd52034dd`.
- No broker-related environment variables were present.
- `uv` installed successfully for the permitted isolated environment.
- Python 3.12.4 environment creation succeeded.
- Import of an external non-product package succeeded.
- Clear/recreate repeatability succeeded.

## What remains unproven

- Python 3.12 with `QuantConnect.pythonnet` 2.0.64.
- Python 3.12 embedded by the .NET 10 launcher.
- LEAN's `python-venv` activation against a `uv` environment.
- `AlgorithmImports`/assembly loading from an external Chainna package.
- Windows/Linux parity.

## ADR disposition

ADR-0010 supersedes ADR-0001's Python-version portion. Python 3.11.11 is canonical for the LEAN adapter, release and container; 3.12 remains a secondary compatibility target.

## Safety confirmation

- No product implementation began.
- No `src/chainna` files, strategy, Sandy, risk, signal, order or broker code was created.
- No market data was downloaded and no backtest was run.
- No OANDA or brokerage dependency was installed.
- No broker credential was introduced.
- No broker connection was attempted.
- No order or trade occurred.
- `engine/lean/` and `legacy/chains/` remained unmodified.

Phase 1A stops here. The Phase 1 repository scaffold and safety foundation have not begun.

ADR-0011 subsequently authorized the sequencing of a later Phase 1B, not its immediate start.
