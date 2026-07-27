# Phase 1A repository preflight

Preflight date: 2026-07-26.

Phase 1A-R verification on 2026-07-27 confirmed the canonical workspace is `C:\Users\Wildf\chainna`, all expected commits still matched, and all repositories were clean. Current host/resource details and the `BLOCKED_RESOURCE` outcome are recorded in `PHASE_1A_RERUN.md`.

## Repository gates

| Repository | Root | Branch | HEAD | Initial status |
|---|---|---|---|---|
| Chainna | `C:\Users\Wildf\chainna\forex-engine` | `master` | `3869433ce1a195c5cd00f15992336487895fd7f6` | Clean |
| LEAN | `C:\Users\Wildf\chainna\engine\lean` | `master` | `cd52034ddf55c0c9aa57264d2a148e563924100f` | Clean |
| Legacy Chains | `C:\Users\Wildf\chainna\legacy\chains` | `main` | `6ada073d6793431c376b942ef45a73000fe781f2` | Clean |

There were no modified, staged or untracked files in any repository. The LEAN HEAD exactly matches the accepted pin. The workspace is outside OneDrive, although `PHASE_1_ENTRY_CRITERIA.md` names an older expected path (`C:\webbaby\chainna`); the actual root is recorded above.

## Host

- OS: Microsoft Windows 11 Home, version `10.0.26200`, build `26200`.
- Architecture: x64.
- Disk `C:`: 237.20 GiB total, 5.22 GiB free at preflight. This low free-space condition is a material constraint for a future .NET/LEAN/container installation.

## Toolchain

Installed Python interpreters:

| Version | Executable |
|---|---|
| 3.13.1 | `C:\Python313\python.exe` |
| 3.12.4 | `C:\Users\Wildf\AppData\Local\Programs\Python\Python312\python.exe` |
| 3.10.0 | `C:\Program Files\Python310\python.exe` |

- Default `python`: Python 3.10.0.
- `uv` at initial preflight: absent.
- `uv` after permitted isolated-environment retrieval: `0.11.32`.
- .NET SDK: absent from `PATH`.
- .NET runtime: absent from `PATH`.
- Docker CLI: absent.
- Docker Compose: absent.
- Docker daemon status was not required or queried.

## Broker and credential gate

Environment-variable names were inspected using a case-insensitive match for OANDA, broker, trading, account ID, access/API token or key, and private key. No matching variable names were present. Values were never printed.

A filename-only scan outside `docs/` found no credential-shaped assignment/configuration files. No broker credential, account identifier or secret was discovered.

## Gate decision

Repository and credential stop conditions did not trigger. The compatibility investigation was allowed to proceed. Missing .NET/Docker and low disk did not dirty a protected repository, but they constrain the executable boundary test and final result.

## Commands executed

```text
git -C <repo> branch --show-current
git -C <repo> rev-parse HEAD
git -C <repo> status --short
git -C <repo> status --porcelain=v2
Get-ChildItem Env: | filter broker/credential-shaped names
Get-CimInstance Win32_OperatingSystem
py -0p
py -3.13/-3.12/-3.10 interpreter probes
python --version
where.exe python
uv --version / where.exe uv
dotnet --info / --list-sdks / --list-runtimes
docker --version
docker compose version
Get-CimInstance Win32_LogicalDisk
filename-only credential-pattern scan
```

No command contacted a broker, used market data, built LEAN or ran a backtest.
