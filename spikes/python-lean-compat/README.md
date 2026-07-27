# Python/LEAN compatibility spike

## Scope

This is a non-product Phase 1A probe. It contains no strategy, domain, risk, signal, order or brokerage code. It tests only an isolated Python 3.12 environment and import of a trivial package located outside the LEAN repository.

## Files

- `outside-package/chainna_spike_probe/__init__.py`: trivial external-package marker.
- `probe.py`: prints interpreter metadata and the imported marker.
- `.venv/`: ignored disposable environment.

## Commands and observed results

The host did not initially have `uv`. It was installed for the isolated development environment:

```powershell
py -3.12 -m pip install --user uv
```

Result: `uv 0.11.32`.

First environment creation and import:

```powershell
py -3.12 -m uv venv `
  --python C:\Users\Wildf\AppData\Local\Programs\Python\Python312\python.exe `
  spikes\python-lean-compat\.venv
$env:PYTHONPATH = 'C:\Users\Wildf\chainna\forex-engine\spikes\python-lean-compat\outside-package'
spikes\python-lean-compat\.venv\Scripts\python.exe `
  spikes\python-lean-compat\probe.py
```

Observed:

```json
{"executable":"...\\.venv\\Scripts\\python.exe","marker":"chainna-phase-1a-external-package","python":"3.12.4"}
```

Repeatability was tested by clearing/recreating the environment with `uv venv --clear` and rerunning the same probe. The second result was identical in version and marker.

## Boundary result

The `uv` and outside-LEAN package-import portions passed twice. The actual LEAN/pythonnet import could not be executed because this Windows host has no .NET SDK/runtime and the checkout has no prebuilt launcher output. LEAN was not built because Phase 1A explicitly prohibited it. No substitute upstream `pythonnet` wheel was installed because LEAN expects QuantConnect's fork and random binary pinning would not be valid evidence.

The authoritative result is therefore `BLOCKED`, as documented in `docs/PHASE_1A_RESULT.md`.
