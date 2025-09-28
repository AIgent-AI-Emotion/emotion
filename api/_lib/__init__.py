"""
Internal library for the K‑WORD API.

Modules:
- storage.py  : Ephemeral in-memory storage (replace with DB later)
- health.py   : /api/health
- metrics.py  : /api/metrics (GET/POST)
- matrix.py   : /api/matrix/kwords (GET/POST)
- triggers.py : /api/triggers/run (POST)
- reports.py  : /api/reports/generate (POST)
- utils.py    : Shared helpers (timestamps, validation stubs)
"""
__all__ = [
    "storage",
    "health",
    "metrics",
    "matrix",
    "triggers",
    "reports",
    "utils",
]
