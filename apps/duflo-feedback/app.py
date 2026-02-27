"""
Duflo Feedback Web Application

Flask app that lets students input their experimental design and receive
feedback from either:
  1. A parametric scoring model (rule-based, instant)
  2. An LLM with Esther Duflo persona (qualitative, API-dependent)
"""

import json
import os

from flask import Flask, render_template, request, jsonify

from parametric_model import score_experiment, get_criteria_options, CRITERIA
from llm_engine import get_llm_feedback

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "duflo-feedback-dev-key")


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    """Render the main form."""
    criteria = get_criteria_options()
    return render_template("index.html", criteria=criteria)


@app.route("/api/feedback/parametric", methods=["POST"])
def feedback_parametric():
    """Score an experimental design with the parametric model."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    responses = data.get("responses", {})
    result = score_experiment(responses)

    return jsonify({
        "mode": "parametric",
        "total_score": result.total_score,
        "max_score": result.max_score,
        "percentage": result.percentage,
        "grade": result.grade,
        "summary": result.summary,
        "top_strength": result.top_strength,
        "top_weakness": result.top_weakness,
        "criteria": [
            {
                "name": c.name,
                "score": c.score,
                "max_score": c.max_score,
                "feedback": c.feedback,
                "sub_dimensions": [
                    {
                        "label": s.label,
                        "selected": s.selected,
                        "score": s.score,
                        "max_score": s.max_score,
                    }
                    for s in c.sub_dimensions
                ],
            }
            for c in result.criteria
        ],
    })


@app.route("/api/feedback/llm", methods=["POST"])
def feedback_llm():
    """Get LLM-based Duflo feedback."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    form_data = data.get("form_data", {})
    backend = data.get("backend", "auto")

    result = get_llm_feedback(form_data, backend=backend)

    return jsonify({
        "mode": "llm",
        "feedback": result["feedback"],
        "backend_used": result["backend_used"],
        "success": result["success"],
    })


@app.route("/api/criteria", methods=["GET"])
def criteria():
    """Return all criteria definitions for the frontend."""
    return jsonify(get_criteria_options())


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "true").lower() == "true"
    app.run(host="0.0.0.0", port=port, debug=debug)
