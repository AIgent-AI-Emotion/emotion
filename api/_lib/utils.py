from datetime import datetime, timezone
from typing import Any, Dict


def utc_now_iso() -> str:
    """Return current UTC time in ISO 8601 format with 'Z'."""
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def ensure_dict(obj: Any) -> Dict:
    """Return a dict if obj is a dict, else empty dict."""
    return obj if isinstance(obj, dict) else {}
