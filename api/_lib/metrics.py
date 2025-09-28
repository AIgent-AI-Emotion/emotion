from flask import Blueprint, jsonify, request
from typing import Dict, Any
from .storage import STORE
from .utils import ensure_dict

bp = Blueprint("metrics", __name__)

@bp.get("/")
def get_metrics():
    metrics: Dict[str, Any] = STORE.get("metrics", {})
    return jsonify(metrics)

@bp.post("/")
def upsert_metrics():
    """
    Upsert metrics as a plain JSON object.
    Example:
    {
      "Clarity": 0.98,
      "Integrity": 1.0,
      "Notes": "System synced"
    }
    """
    payload = ensure_dict(request.get_json(force=True, silent=True))
    if not isinstance(payload, dict):
        return jsonify({"error": "Request body must be a JSON object"}), 400

    metrics: Dict[str, Any] = STORE.get("metrics", {})
    metrics.update(payload)
    STORE.set("metrics", metrics)

    return jsonify({"ok": True, "metrics": metrics})
