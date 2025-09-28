import os
from flask import Blueprint, jsonify

bp = Blueprint("health", __name__)

@bp.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "service": "kword-api",
        "version": os.getenv("VERCEL_GIT_COMMIT_SHA", "dev"),
        "runtime": "python"
    })
