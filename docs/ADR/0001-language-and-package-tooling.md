# ADR 0001: Language and package tooling

**Status: Accepted**  
**Approval date:** 2026-07-26  
**Approver:** Uchenna Emmanuel Anozie, Product Owner

## Context

Chainna needs one deterministic product package usable from research, a thin Python LEAN algorithm adapter and later services. No package files may be created during Phase 0.

## Decision being considered

Use Python 3.12 for Chainna strategy/orchestration code outside LEAN, with a modern locked dependency workflow, Ruff, strict static typing and pytest.

## Available options

| Option | Strengths | Trade-offs |
|---|---|---|
| `uv` | Fast resolver/installer, lockfile, Python/version/environment management, workspace support, simple CI path | Newer ecosystem tool; team familiarity and LEAN/pythonnet compatibility must be verified |
| Poetry | Mature project metadata, lockfile, packaging and environments, broad familiarity | More opinionated packaging workflow; slower; can complicate non-package/app and special binary dependency cases |
| pip-tools | Small layer over pip; transparent requirement inputs and compiled locks | Environment/Python management is separate; multiple platform/extra lock workflows require more convention and tooling |
| C# product core | Native LEAN ecosystem and strong typing | Slower parity/research iteration and less direct notebook reuse; still needs service/tooling decisions |

## Recommended option

Python 3.12 with `uv` as the lock, sync and environment workflow. Require Ruff, Pyright strict and pytest after Phase 1 is authorized. The initial developer host is Windows; CI and runtime portability include Linux. Docker is not required for the initial domain foundation but is mandatory before Phase 3 LEAN integration. Produce platform-aware locked dependencies and pin Python. Keep LEAN as a separately pinned runtime.

## Reasons

This offers the lowest-friction route between deterministic Python domain code, QuantBook research and thin LEAN Python entry points while giving one reproducible dependency workflow. `uv` covers more of the environment lifecycle than pip-tools without Poetry's packaging conventions.

## Consequences

Phase 1 would create package/tool configuration, a lockfile and CI checks. Binary/runtime compatibility with LEAN's Python environment must be proven. Research notebooks import the product package; they never own strategy logic.

## Risks

Python 3.12 may not match the pinned LEAN image/pythonnet stack. A newer dependency tool introduces operational learning and lock portability questions. Strict typing can be weakened by LEAN's dynamic Python boundary unless adapter types are isolated.

## Alternatives rejected

Poetry and pip-tools are not technically unsuitable; they are rejected only as the starting recommendation. C# is rejected as the primary product language because the current research/parity path benefits more from Python. Ad hoc `pip install` and unpinned requirements are rejected.

## Questions requiring human approval

None. The Product Owner approved Python 3.12, `uv`, Ruff, pytest, Pyright strict, Windows development with Linux portability, and the Docker timing stated above.

## Evidence required before acceptance

Acceptance is conditional on execution evidence at the appropriate phase. The first Phase 1 activity must be a no-product-code compatibility spike showing that the pinned LEAN runtime can load the chosen Python version/environment. Later evidence includes lock reproducibility on Windows and Linux, dependency/license review and documented CI sync behavior.

## Explicit implementation impact

If accepted and Phase 1 is separately authorized, it determines `pyproject.toml`, lockfile, source layout, CI and developer commands. It creates no authority to add them now.
