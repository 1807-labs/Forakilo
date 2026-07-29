"""Verify that an external LEAN checkout matches the committed pin."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LOCK = ROOT / "third_party" / "lean" / "LEAN.lock.json"


def main() -> int:
    lock = json.loads(LOCK.read_text(encoding="utf-8"))
    checkout = ROOT / lock["checkout_directory"]
    if not checkout.is_dir():
        print(f"LEAN checkout missing: {checkout}", file=sys.stderr)
        return 2
    if (checkout / ".git").is_dir() and checkout.is_relative_to(ROOT):
        # .external is intentionally ignored; this protects against accidental vendoring.
        pass
    actual = subprocess.run(
        ["git", "-C", str(checkout), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    if actual != lock["commit"]:
        print(f"LEAN commit mismatch: expected {lock['commit']}, found {actual}", file=sys.stderr)
        return 1
    print(f"LEAN pin verified: {actual}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
