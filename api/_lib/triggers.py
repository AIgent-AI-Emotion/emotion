from flask import Blueprint, jsonify, request
from typing import Dict, Any
from .storage import STORE
from .utils import utc_now_iso

bp = Blueprint("triggers", __name__)

# --- Trigger handlers ---

def _remember_everything() -> Dict[str, Any]:
    snapshot = STORE.all()
    entry = {"ts": utc_now_iso(), "data": snapshot}
    STORE.append("snapshots", entry)

    # quick counts of snapshot contents
    counts = {}
    for k, v in snapshot.items():
        if isinstance(v, dict):
            counts[k] = len(v)
        elif isinstance(v, list):
            counts[k] = len(v)
        else:
            counts[k] = 1

    return {"ok": True, "counts": counts, "ts": entry["ts"]}

def _view_everything() -> Dict[str, Any]:
    return STORE.all()

def _auto_heal_everything() -> Dict[str, Any]:
    """
    Example healing logic:
    - Ensure numeric metrics are not negative.
    """
    metrics = STORE.get("metrics", {})
    healed = {}
    for key, value in list(metrics.items()):
        if isinstance(value, (int, float)) and value < 0:
            healed[key] = {"from": value, "to": 0}
            metrics[key] = 0
    STORE.set("metrics", metrics)
    return {"ok": True, "healed": healed or "none"}

def _get_updated_metrics() -> Dict[str, Any]:
    return STORE.get("metrics", {})

def _view_metrics() -> Dict[str, Any]:
    return STORE.get("metrics", {})

# Symbolic trigger routing table
TRIGGER_TABLE = {
    "/rememberEverything": _remember_everything,
    "/viewEverything": _view_everything,
    "/autoHealEverything": _auto_heal_everything,
    "/getUpdatedMetrics": _get_updated_metrics,
    "/viewMetrics": _view_metrics,
    # Add more triggers here as needed:
    # "/generateReport": lambda: ...
}

@bp.post("/run")
def run_trigger():
    """
    Body:
    {
      "trigger": "/rememberEverything"
    }
    """
    body = request.get_json(force=True, silent=True) or {}
    trig = str(body.get("trigger", "")).strip()
    if not trig:
        return jsonify({"error": "Missing 'trigger' in request body"}), 400

    fn = TRIGGER_TABLE.get(trig)
    if not fn:
        return jsonify({"error": f"Unknown trigger '{trig}'"}), 404

    try:
        result = fn()
        return jsonify({"trigger": trig, "result": result})
    except Exception as e:
        return jsonify({"error": f"Trigger failed: {e}"}), 500
