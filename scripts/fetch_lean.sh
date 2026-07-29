#!/usr/bin/env sh
set -eu
ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
COMMIT="$(python -c 'import json; print(json.load(open("third_party/lean/LEAN.lock.json"))["commit"])')"
TARGET="$ROOT/.external/lean"
if [ ! -d "$TARGET" ]; then
  git clone --filter=blob:none --no-checkout https://github.com/vebbaybi/Lean.git "$TARGET"
fi
git -C "$TARGET" fetch origin "$COMMIT"
git -C "$TARGET" checkout --detach "$COMMIT"
python "$ROOT/scripts/verify_lean.py"

