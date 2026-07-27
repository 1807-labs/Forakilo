# Python and LEAN compatibility at `cd52034dd`

## Runtime decision amendment

ADR-0010, accepted 2026-07-27, supersedes only the Python-version portion of ADR-0001:

- LEAN/release baseline: Python 3.11.11.
- Chainna compatibility: Python `>=3.11,<3.13`.
- CI: Python 3.11 and 3.12.
- Python 3.12: secondary development compatibility target.
- Product code: no Python 3.12-only syntax, APIs or semantics.

The original Phase 0 Python 3.12 decision is retained in ADR-0001 and the decision register as amended history.

## Conclusion

This pinned LEAN checkout documents Python 3.11.11 and uses it in the official foundation/CI image. Python 3.11.11 is now the accepted canonical boundary. Python 3.12 remains unproven at the QuantConnect.pythonnet boundary, not failed. Phase 1A-R could not rerun either boundary because the host had only 7.19 GiB free, below the 25 GiB operational threshold.

## Evidence from the pinned checkout

### Supported Python and official runtime

- LEAN's local setup heading explicitly says Python 3.11 and specifies Windows Python 3.11.11: `engine/lean/Algorithm.Python/readme.md:32-42`.
- Linux setup downloads the Python 3.11 Miniconda installer, creates a 3.11.11 environment and points `PYTHONNET_PYDLL` at `libpython3.11.so`: `engine/lean/Algorithm.Python/readme.md:72-90`.
- The x64 foundation image uses `PYTHONNET_PYDLL=/opt/miniconda3/lib/libpython3.11.so` and a `py311` Miniconda installer: `engine/lean/DockerfileLeanFoundation:26-35`.
- The ARM foundation does the same: `engine/lean/DockerfileLeanFoundationARM:22-29`.
- CI jobs run inside `quantconnect/lean:foundation`, for example `engine/lean/.github/workflows/gh-actions.yml:14-19` and `virtual-environments.yml:14-19`. CI therefore practically exercises the image's Python 3.11, not 3.12.

There is no pinned-checkout evidence of official Python 3.12 testing.

### pythonnet and .NET

- Core LEAN projects target `.NET 10.0`: `engine/lean/Engine/QuantConnect.Lean.Engine.csproj:1-8` and `Launcher/QuantConnect.Lean.Launcher.csproj:1-12`.
- The engine references `QuantConnect.pythonnet` version `2.0.64`: `engine/lean/Engine/QuantConnect.Lean.Engine.csproj:43-48`. This is QuantConnect's enhanced fork, not evidence that an arbitrary PyPI `pythonnet` wheel is interchangeable; the distinction is documented at `Algorithm.Python/readme.md:111-127`.
- The foundation installs .NET SDK 10: `engine/lean/DockerfileLeanFoundation:412-419`.
- Research starts CoreCLR through `clr-loader`, then imports LEAN assemblies and initializes LEAN's Python bridge: `engine/lean/Research/start.py:20-42`.
- The research image pins `clr-loader==0.2.9`: `engine/lean/DockerfileJupyter:24-25`; research CI installs the same version at `.github/workflows/research-regression-tests.yml:24-32`.

### Interpreter and virtual-environment model

LEAN embeds CPython in the .NET launcher for Python algorithms:

- `PythonEngine.Initialize()` is called by `PythonInitializer`: `engine/lean/Common/Python/PythonInitializer.cs:51-69`.
- `PYTHONNET_PYDLL` must identify the base interpreter DLL; LEAN then prepends virtual-environment storage: `PythonInitializer.cs:187-249`.
- Launcher activates the job's configured Python virtual environment: `engine/lean/Launcher/Program.cs:78-80`.
- `python-venv` is a supported launcher option: `engine/lean/Configuration/LeanArgumentParser.cs:55-70` and `Launcher/config.json:31-32`.

Research reverses the direction: Python starts CoreCLR with `clr-loader` and loads LEAN assemblies (`Research/start.py:20-42`). The official container provides the interpreter, native Python library and compiled dependencies.

### External Chainna package loading

Product source need not live in LEAN:

- Python algorithm location is configured as a filesystem `.py` path: `engine/lean/Algorithm.Python/readme.md:98-107` and `Launcher/config.json:14-19`.
- The job queue reads `algorithm-location`, adds its directory to Python's path and stores the virtual-environment setting: `engine/lean/Queues/JobQueue.cs:89`, `268-282`, and `177/244`.
- `PythonInitializer.AddPythonPaths` inserts external paths into `sys.path`: `engine/lean/Common/Python/PythonInitializer.cs:98-152`.
- The algorithm directory is deliberately placed first: `PythonInitializer.cs:125-175`.

Lowest-risk Phase 3 configuration is an isolated generated launcher config with:

- `algorithm-language=Python`;
- an absolute `algorithm-location` outside the LEAN checkout;
- `python-venv` pointing to the compatible environment; and
- a controlled `PYTHONPATH` or adapter directory that exposes the installed Chainna package.

A `uv` environment is technically a standard virtual environment (`pyvenv.cfg` and `site-packages`), which matches LEAN's activation logic. This must still be proven with the actual embedded interpreter.

## Answers to the Phase 1A questions

1. **Python 3.12 support:** not officially evidenced by this pin. Official/practical baseline is 3.11.11. A plain 3.12 `uv` environment works, but the LEAN boundary is unverified.
2. **Official container/CI Python:** Python 3.11 via `Miniconda3-py311_24.9.2-0`; local docs specify 3.11.11.
3. **pythonnet version:** NuGet `QuantConnect.pythonnet` `2.0.64`; research additionally uses `clr-loader` `0.2.9`.
4. **Interpreter provision:** embedded system/Conda CPython for the launcher, with `PYTHONNET_PYDLL`; container-provided in official images. Research starts CoreCLR from Python.
5. **External `uv` package:** structurally yes; the local import probe passed twice and LEAN supports external paths/venvs. End-to-end proof remains blocked.
6. **Path/config supply:** external `algorithm-location`, `python-venv`, and controlled `PYTHONPATH`/algorithm-directory import. Generate config outside the LEAN tree.
7. **Binary conflicts:** likely risk. The official image pins many compiled packages against Python 3.11, including NumPy/SciPy/Pandas and ML libraries (`DockerfileLeanFoundation:46-140`). Wheels/native ABI availability can differ under 3.12.
8. **Windows versus Linux:** materially different. Windows needs a matching `python311.dll`/`PYTHONNET_PYDLL` and locally installed .NET; official CI/container is Ubuntu/Conda with `libpython3.11.so`. Windows site-package discovery is a documented issue (`Algorithm.Python/readme.md:135-138`).
9. **Lowest-risk arrangement:** Phase 1 domain work may use isolated Python 3.12 `uv` without LEAN imports. Before Phase 3, use the official Linux/container Python 3.11 baseline, pin image/build provenance, and prove external-package loading. Test 3.12 only in a separate evidence matrix.
10. **Runtime decision:** ADR-0010 now makes Python 3.11.11 canonical for LEAN/release work and supports `>=3.11,<3.13` for Chainna. Python 3.12 is secondary and cannot determine release compatibility.

## Phase 1A-R resource gate

On 2026-07-27 the canonical host had:

- 7.19 GiB free on `C:` (threshold: 25 GiB);
- 5.94 GiB total RAM and approximately 0.39 GiB available at inspection;
- WSL 2 installed, but no Linux distribution;
- no Docker Desktop/client/server/Compose;
- no .NET SDK/runtime; and
- no installed Python 3.11 interpreter.

No Python environments, container, .NET toolchain or LEAN build were provisioned. The outcome is `BLOCKED_RESOURCE`.

## Windows host findings

The host has Python 3.12.4 but no .NET SDK/runtime, no Docker and only 5.22 GiB free. It cannot execute the pinned LEAN bridge as configured. Installing .NET or building LEAN was not authorized. Container verification is already required before Phase 3 and remains the safest integration proof.

## Spike evidence

`uv 0.11.32` created a Python 3.12.4 virtual environment. A trivial package under `forex-engine/spikes/python-lean-compat/outside-package` imported successfully through `PYTHONPATH`. Clearing/recreating the environment with `uv venv --clear` produced the same result.

No PyPI `pythonnet` was installed: it would not test the pinned QuantConnect fork. No `AlgorithmImports`/LEAN assembly import was attempted because the required .NET/build artifacts were absent.
