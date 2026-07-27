"""Verify Python version and import a local package outside the LEAN tree."""

from __future__ import annotations

import json
import platform
import sys

from chainna_spike_probe import MARKER


print(
    json.dumps(
        {
            "executable": sys.executable,
            "marker": MARKER,
            "python": platform.python_version(),
            "pythonpath_head": sys.path[:3],
        },
        sort_keys=True,
    )
)
