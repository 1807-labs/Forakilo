# Phase 1A-R rerun

Rerun date: 2026-07-27.

## Outcome

**BLOCKED_RESOURCE**

The pinned LEAN/pythonnet probe did not start because the canonical workspace drive had 7.19 GiB free, below the Chainna operational threshold of 25 GiB.

ADR-0011 preserves this history. Phase 1A-R was not a failed architecture: its executable verification is deferred to the Phase 3 entrance gate and is not waived. Runtime-independent Phase 1B has a separate 10 GiB local floor (12 GiB preferred); the 25 GiB threshold applies only to local container, LEAN-build and data-intensive work.

## Mandatory repository verification

| Repository | Resolved path | Branch | HEAD | Status |
|---|---|---|---|---|
| Chainna | `C:\Users\Wildf\chainna\forex-engine` | `master` | `c82667230b9b56597009960b05aaa128b63929b7` | Clean |
| LEAN | `C:\Users\Wildf\chainna\engine\lean` | `master` | `cd52034ddf55c0c9aa57264d2a148e563924100f` | Clean |
| Legacy Chains | `C:\Users\Wildf\chainna\legacy\chains` | `main` | `6ada073d6793431c376b942ef45a73000fe781f2` | Clean |

There were no modified, staged or untracked files at entry. No broker-related environment-variable names were present.

## Host and resource gate

- Windows 11 Home `10.0.26200`, build `26200`, x64.
- RAM: 5.94 GiB total; approximately 0.39 GiB available at inspection.
- `C:`: 237.20 GiB total; 7.19 GiB free before task documentation.
- Threshold: 25 GiB free before a LEAN container pull/build.
- WSL: 2.7.11.0, default version 2, kernel 6.18.33.2-2.
- WSL distributions: none installed.
- Docker Desktop: not found in uninstall registry inventory.
- Docker client/server/Compose: unavailable.
- Docker engine/Linux-container health: unavailable because Docker is absent.
- .NET SDK/runtime: unavailable from `PATH`.
- Python launcher reports 3.13, 3.12 and 3.10; Python 3.11.11 is not installed.
- `uv`: 0.11.32.

The disk gate takes precedence. No container, toolchain, Python interpreter or dependency was downloaded or installed.

## Read-only disk investigation

Two read-only recursive size scans were attempted. They were stopped without deleting anything because traversal of the large/cloud-backed user profile was excessively slow and available RAM was critically low.

Likely categories for owner-reviewed reclamation include:

- Windows Storage temporary files and update cleanup;
- `%LOCALAPPDATA%\Temp`;
- user `Downloads`;
- OneDrive offline/local copies;
- language/build caches such as `.gradle`, `.cargo`, `.cache` and Python caches;
- global `node_modules`;
- unused virtual environments;
- old container data if Docker is installed later; and
- build outputs in unrelated projects.

These are candidates, not deletion recommendations. No size claim was made where traversal did not complete, and nothing was removed. The owner should use Windows Storage settings or a trusted disk analyzer and preserve at least 25 GiB free before rerunning.

## Runtime amendment

ADR-0010 was accepted by the Product Owner:

- Python 3.11.11 is canonical for LEAN/release/container validation.
- Chainna supports Python `>=3.11,<3.13`.
- CI must test 3.11 and 3.12.
- Product code cannot require 3.12-only behavior.
- `uv`, Ruff, pytest and Pyright strict remain accepted.

## Python environment rerun

Not attempted. The resource-gate instruction allowed only read-only disk investigation and documentation after failure.

| Candidate | Result |
|---|---|
| Python 3.11.11 | Not installed; environment not provisioned |
| Python 3.12.4 | Installed globally, but new disposable environment not provisioned |

The prior Phase 1A Python 3.12.4 `uv` probe remains historical evidence only.

## Docker/LEAN provenance and boundary probes

- Pinned LEAN source: `cd52034ddf55c0c9aa57264d2a148e563924100f`.
- Supported definitions remain `Dockerfile`, `DockerfileLeanFoundation` and `DockerfileJupyter` in the pinned checkout.
- Image build: not attempted.
- Image ID/digest: none.
- Build duration/result: not applicable.
- QuantConnect.pythonnet boundary run 1: not attempted.
- QuantConnect.pythonnet boundary run 2: not attempted.
- Repeatability conclusion: no conclusion; prerequisite gate failed.

Phase 3 remains blocked until both reproducible boundary runs succeed using the exact pinned runtime on an approved Linux/container environment.

No unrelated/latest image was used as evidence.

## Commands executed

- Git existence, branch, HEAD, status, modified/staged/untracked checks for all three repositories.
- Broker-related environment-variable name inspection without values.
- Windows OS, architecture, memory and disk queries.
- `wsl --status`, `wsl --version`, and `wsl -l -v`.
- Docker installation/path, client/server/Compose and engine-health queries.
- .NET SDK/runtime path and version queries.
- Python launcher and `uv` version queries.
- Read-only disk-size investigations, stopped when they became resource-intensive.

## Safety confirmation

- No `src/chainna` or product implementation was created.
- No Sandy, signal, risk, order, portfolio or broker code was created.
- No market data was downloaded.
- No trading backtest was run.
- No OANDA/broker dependency or credential was introduced.
- No broker connection, order or trade occurred.
- LEAN and Legacy Chains remained unmodified.
