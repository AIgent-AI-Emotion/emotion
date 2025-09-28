"""
Flask entrypoint for Vercel (Serverless Function).

- Exposes:
    - GET  /api                -> Service info + endpoint index
    - GET  /api/health         -> Health check
    - GET  /api/metrics        -> Read metrics
    - POST /api/metrics        -> Upsert metrics
    - GET  /api/matrix/kwords  -> List K-WORD entries
    - POST /api/matrix/kwords  -> Create K-WORD entry
    - POST /api/triggers/run   -> Run symbolic triggers
    - POST /api/reports/generate -> Generate a summary report
    - GET  /api/python         -> Legacy hello route (kept for continuity)

- Vercel requirement: `app` must be defined at module scope.
"""

import os
from flask import Flask, jsonify
from flask_cors import CORS

# Blueprints (these modules will be added next)
from _lib.health import bp as health_bp
from _lib.metrics import bp as metrics_bp
from _lib.matrix import bp as matrix_bp
from _lib.triggers import bp as triggers_bp
from _lib.reports import bp as reports_bp


def create_app() -> Flask:
    app = Flask(__name__)

    # Allow the Next.js frontend to call the API (adjust origins as needed)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # --- Root service index ---
    @app.get("/api")
    def root_index():
        return jsonify({
            "service": "kword-api",
            "status": "ok",
            "version": os.getenv("VERCEL_GIT_COMMIT_SHA", "dev"),
            "endpoints": [
                "/api/health",
                "/api/metrics",
                "/api/matrix/kwords",
                "/api/triggers/run",
                "/api/reports/generate",
                "/api/python"  # legacy hello route
            ]
        })

    # --- Legacy hello route (kept from your original) ---
    @app.get("/api/python")
    def hello_world():
        return "<p>Hello, World!</p>"

    # --- Register blueprints with clear URL prefixes ---
    # NOTE: The blueprints themselves define relative routes:
    #   health_bp   -> defines '/health'            (prefix '/api')
    #   metrics_bp  -> defines '/' (GET/POST)       (prefix '/api/metrics')
    #   matrix_bp   -> defines '/kwords'            (prefix '/api/matrix')
    #   triggers_bp -> defines '/run'               (prefix '/api/triggers')
    #   reports_bp  -> defines '/generate'          (prefix '/api/reports')
    app.register_blueprint(health_bp,   url_prefix="/api")
    app.register_blueprint(metrics_bp,  url_prefix="/api/metrics")
    app.register_blueprint(matrix_bp,   url_prefix="/api/matrix")
    app.register_blueprint(triggers_bp, url_prefix="/api/triggers")
    app.register_blueprint(reports_bp,  url_prefix="/api/reports")

    return app


# Vercel looks for `app` at module scope
app = create_app()

# Local dev: `python api/index.py`
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5000")), debug=True)
