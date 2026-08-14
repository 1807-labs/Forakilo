$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
if (-not (Test-Path -Path '.venv')) {
    python -m venv .venv
}
$py = Join-Path $Root '.venv\Scripts\python.exe'
& $py -m pip install --upgrade pip
& $py -m pip install -r requirements-dev.txt
Write-Host 'Dev environment ready. Activate with: .\.venv\Scripts\Activate.ps1'