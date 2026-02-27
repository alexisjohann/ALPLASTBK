"""
GPS Homepage — Flask Application
=================================
Interactive dashboard for the Global Preference Survey (GPS) data,
integrated with the Evidence-Based Framework (EBF).

Based on: Falk, Becker, Dohmen, Enke, Huffman & Sunde (2018)
"Global Evidence on Economic Preferences", QJE 133(4), 1645-1692.

Usage:
    python app.py
    # Open http://localhost:5001
"""

import json
import os
from pathlib import Path

from flask import Flask, jsonify, render_template, send_from_directory

app = Flask(__name__)

DATA_DIR = Path(__file__).parent / "static"
GPS_DATA_PATH = DATA_DIR / "gps_data.json"


def load_gps_data():
    """Load GPS country-level preference data."""
    with open(GPS_DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


@app.route("/")
def index():
    """Render the GPS homepage."""
    return render_template("index.html")


@app.route("/static/<path:filename>")
def static_files(filename):
    """Serve static files."""
    return send_from_directory("static", filename)


@app.route("/api/data")
def api_data():
    """Return full GPS dataset as JSON."""
    data = load_gps_data()
    return jsonify(data)


@app.route("/api/countries")
def api_countries():
    """Return list of countries with their preference scores."""
    data = load_gps_data()
    return jsonify(data["countries"])


@app.route("/api/country/<iso>")
def api_country(iso):
    """Return preference data for a specific country by ISO code."""
    data = load_gps_data()
    country = next((c for c in data["countries"] if c["iso"] == iso.upper()), None)
    if country is None:
        return jsonify({"error": f"Country not found: {iso}"}), 404
    return jsonify(country)


@app.route("/api/rankings/<preference>")
def api_rankings(preference):
    """Return countries ranked by a specific preference dimension."""
    valid_prefs = ["patience", "risktaking", "posrecip", "negrecip", "altruism", "trust"]
    if preference not in valid_prefs:
        return jsonify({"error": f"Invalid preference: {preference}", "valid": valid_prefs}), 400

    data = load_gps_data()
    ranked = sorted(data["countries"], key=lambda c: c[preference], reverse=True)
    for i, c in enumerate(ranked):
        c["rank"] = i + 1
    return jsonify(ranked)


@app.route("/api/compare/<iso_a>/<iso_b>")
def api_compare(iso_a, iso_b):
    """Compare two countries across all preference dimensions."""
    data = load_gps_data()
    country_a = next((c for c in data["countries"] if c["iso"] == iso_a.upper()), None)
    country_b = next((c for c in data["countries"] if c["iso"] == iso_b.upper()), None)

    if country_a is None:
        return jsonify({"error": f"Country not found: {iso_a}"}), 404
    if country_b is None:
        return jsonify({"error": f"Country not found: {iso_b}"}), 404

    prefs = ["patience", "risktaking", "posrecip", "negrecip", "altruism", "trust"]
    comparison = {
        "country_a": country_a,
        "country_b": country_b,
        "differences": {p: round(country_a[p] - country_b[p], 3) for p in prefs},
        "euclidean_distance": round(
            sum((country_a[p] - country_b[p]) ** 2 for p in prefs) ** 0.5, 3
        ),
    }
    return jsonify(comparison)


@app.route("/api/regions")
def api_regions():
    """Return preference averages by region."""
    data = load_gps_data()
    prefs = ["patience", "risktaking", "posrecip", "negrecip", "altruism", "trust"]
    regions = {}

    for c in data["countries"]:
        r = c["region"]
        if r not in regions:
            regions[r] = {"countries": [], "averages": {p: 0 for p in prefs}}
        regions[r]["countries"].append(c["country"])
        for p in prefs:
            regions[r]["averages"][p] += c[p]

    for r in regions:
        n = len(regions[r]["countries"])
        for p in prefs:
            regions[r]["averages"][p] = round(regions[r]["averages"][p] / n, 3)
        regions[r]["n_countries"] = n

    return jsonify(regions)


@app.route("/api/metadata")
def api_metadata():
    """Return GPS dataset metadata and EBF integration info."""
    data = load_gps_data()
    return jsonify(data["metadata"])


@app.route("/api/findings")
def api_findings():
    """Return key findings (variance decomposition, GDP correlations, etc.)."""
    data = load_gps_data()
    return jsonify(data["key_findings"])


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    print(f"\n  GPS Homepage running at http://localhost:{port}")
    print(f"  Data: {len(load_gps_data()['countries'])} countries loaded\n")
    app.run(host="0.0.0.0", port=port, debug=debug)
