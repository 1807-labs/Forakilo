$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Lock = Get-Content -LiteralPath (Join-Path $Root "third_party\lean\LEAN.lock.json") -Raw | ConvertFrom-Json
$Target = Join-Path $Root $Lock.checkout_directory
if (-not (Test-Path -LiteralPath $Target)) {
    git clone --filter=blob:none --no-checkout $Lock.source_repository $Target
}
git -C $Target fetch origin $Lock.commit
git -C $Target checkout --detach $Lock.commit
uv run python (Join-Path $Root "scripts\verify_lean.py")

