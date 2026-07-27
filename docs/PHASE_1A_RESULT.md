# Phase 1A result

## Outcome

**BLOCKED: environment or dependency problem prevents a conclusion.**

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

## ADR 0001 disposition

ADR 0001 does **not yet require amendment**, because Python 3.12 did not fail at the LEAN boundary; that boundary was unavailable. Python 3.12 may be retained for runtime-independent Phase 1 domain/tooling work only.

Before Phase 3, a separately authorized containerized compatibility test must compare:

1. the official Python 3.11.11 baseline; and
2. Python 3.12 against the exact pinned QuantConnect pythonnet/LEAN build.

If 3.12 cannot pass without patching LEAN or undocumented binary pins, ADR 0001 must be amended so the LEAN adapter runtime uses Python 3.11.

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
