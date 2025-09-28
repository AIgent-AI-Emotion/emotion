from flask import Blueprint, jsonify, request
from typing import Dict, Any, List
from uuid import uuid4
from .storage import STORE
from .utils import ensure_dict, utc_now_iso

bp = Blueprint("matrix", __name__)

@bp.get("/kwords")
def list_kwords():
    kwords: List[Dict[str, Any]] = STORE.get("kwords", [])
    return jsonify({"kwords": kwords})

@bp.post("/kwords")
def add_kword():
    """
    Create a K-WORD entry.

    Example body:
    {
      "name": "×Kevin Michael Norman",
      "tags": ["+Founder","÷Architect","@AIgent"],
      "attributes": {
        "§Principles": ["§Reality","§Magick"],
        "%Metrics": {"Clarity": 0.98}
      }
    }
    """
    data = ensure_dict(request.get_json(force=True, silent=True))
    if not data:
        return jsonify({"error": "Invalid or empty JSON body"}), 400

    # Normalize and validate minimal fields
    name = str(data.get("name", "")).strip()
    if not name:
        return jsonify({"error": "Field 'name' is required"}), 400

    tags = data.get("tags") or []
    if not isinstance(tags, list):
        return jsonify({"error": "Field 'tags' must be a list"}), 400

    attributes = data.get("attributes") or {}
    if not isinstance(attributes, dict):
        return jsonify({"error": "Field 'attributes' must be an object"}), 400

    item = {
        "id": str(uuid4()),
        "name": name,
        "tags": tags,
        "attributes": attributes,
        "created_at": utc_now_iso()
    }

    STORE.append("kwords", item)
    return jsonify({"created": item}), 201
