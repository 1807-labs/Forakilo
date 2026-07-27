# ADR 0010: Python runtime baseline amendment

**Status: Accepted**

**Date:** 2026-07-27

**Approver:** Uchenna Emmanuel Anozie, Product Owner

## Context

ADR 0001 accepted Python 3.12 as the Chainna language baseline, subject to the mandatory Phase 1A compatibility spike. Phase 1A established that pinned LEAN commit `cd52034dd` officially documents and packages Python 3.11.11, while the real QuantConnect.pythonnet boundary could not be verified on the Windows host because .NET and Docker were absent.

The original decision remains part of the audit trail. This ADR supersedes only its Python-version portion.

## Decision

- Canonical LEAN-facing runtime: Python 3.11.11.
- Chainna package compatibility range: Python `>=3.11,<3.13`.
- Future CI must test Python 3.11 and Python 3.12.
- Release, LEAN adapter and container validation use Python 3.11.11.
- Product code may not require Python 3.12-only syntax, APIs or semantics.
- Python 3.12 remains a secondary development compatibility target.
- `uv` remains the accepted dependency and environment workflow.
- Ruff, pytest and Pyright strict remain accepted.
- LEAN remains a separately pinned external runtime.

## Reasons

The accepted LEAN pin explicitly uses Python 3.11.11 in its local documentation and official foundation/container configuration. Aligning the release-facing interpreter minimizes unsupported pythonnet, native-wheel and Windows/Linux differences while preserving 3.12 compatibility as useful forward coverage.

## Consequences

- Phase 1 package metadata will eventually declare `>=3.11,<3.13`.
- The lowest Python version governs syntax and standard-library use.
- CI must exercise both supported minor versions.
- LEAN/container evidence is valid only against exact Python 3.11.11 unless a later ADR changes the baseline.
- A developer may use Python 3.12, but release and LEAN adapter conclusions cannot rely solely on it.

## Risks

- Supporting two minor versions expands testing.
- The current host does not have Python 3.11.11 installed, so the accepted runtime has not yet been provisioned locally.
- QuantConnect.pythonnet still needs an executable boundary test; version alignment reduces but does not eliminate that risk.
- Python 3.11 reaches end of upstream support before newer versions, so a future planned migration will be needed.

## Alternatives rejected

- Retaining Python 3.12 as the canonical LEAN runtime is rejected because the pinned runtime does not officially evidence it.
- Supporting only Python 3.11 is rejected because 3.12 remains a valuable compatibility target for runtime-independent Chainna code.
- Patching LEAN or pinning undocumented binary combinations to force 3.12 is rejected.
- Installing arbitrary PyPI pythonnet as a substitute for QuantConnect.pythonnet is rejected.

## Evidence and follow-up gates

The amendment is an accepted product-owner decision. Runtime evidence remains required:

1. provision exact isolated Python 3.11.11 and 3.12.4 environments with `uv`;
2. repeat the external-package probe in both;
3. build/use a runtime tied to LEAN commit `cd52034dd`;
4. initialize .NET, QuantConnect.pythonnet and Python 3.11.11;
5. import the external read-only probe and relevant QuantConnect types twice reproducibly; and
6. keep LEAN and legacy repositories clean.

Phase 1A-R could not execute these steps because the host failed the 25 GiB disk gate. That is a resource blocker, not a reversal of this decision.

## Explicit implementation impact

This ADR changes runtime metadata and future CI/runtime selection only. It does not authorize package scaffolding, product code, LEAN builds, data acquisition, backtests or broker integration.
