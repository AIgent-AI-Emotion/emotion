from flask import Blueprint, jsonify, request
from typing import Dict, Any, List
from .storage import STORE
from .utils import utc_now_iso

bp = Blueprint("reports", __name__)

@bp.post("/generate")
def generate_report():
    """
    Generates a lightweight summary of current state.
    """
    data: Dict[str, Any] = STORE.all()
    kwords: List[Dict[str, Any]] = data.get("kwords", [])
    metrics: Dict[str, Any] = data.get("metrics", {})
    snapshots: List[Dict[str, Any]] = data.get("snapshots", [])

    latest_snapshot_ts = snapshots[-1]["ts"] if snapshots else None

    report = {
        "generated_at": utc_now_iso(),
        "summary": {
            "kwords_count": len(kwords),
            "metrics_count": len(metrics),
            "snapshots_count": len(snapshots),
            "latest_snapshot_ts": latest_snapshot_ts
        },
        "recent_metrics": metrics,
        "latest_kwords": kwords[-5:],
    }
    return jsonify({"report": report})
