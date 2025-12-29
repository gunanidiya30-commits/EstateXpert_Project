from flask import Blueprint, request, jsonify

build_readiness_api = Blueprint("build_readiness_api", __name__)

@build_readiness_api.route("/api/build-readiness", methods=["POST"])
def build_readiness():
    data = request.get_json()

    land_status = data.get("land_status")          # PASS / BORDERLINE / FAIL
    cost_risk = data.get("cost_risk")              # Low / Medium / High
    material_quality = data.get("material_quality")# Good / Average / Poor
    climate_zone = data.get("climate_zone")        # Normal / Coastal / Dry / High Rainfall

    if not all([land_status, cost_risk, material_quality, climate_zone]):
        return jsonify({"error": "All parameters required"}), 400

    score = 0

    # Land contribution (40)
    score += 40 if land_status == "PASS" else 25 if land_status == "BORDERLINE" else 10

    # Cost risk contribution (25)
    score += 25 if cost_risk == "Low" else 15 if cost_risk == "Medium" else 5

    # Material contribution (20)
    score += 20 if material_quality == "Good" else 12 if material_quality == "Average" else 5

    # Climate contribution (15)
    score += 15 if climate_zone == "Normal" else 10

    if score >= 80:
        band = "Excellent"
        advice = "Project is ready for construction with minimal risk."
    elif score >= 60:
        band = "Good"
        advice = "Minor improvements recommended before starting."
    elif score >= 40:
        band = "Moderate"
        advice = "Address key risks before proceeding."
    else:
        band = "High Risk"
        advice = "Construction not advised without major corrections."

    return jsonify({
        "score": score,
        "band": band,
        "advice": advice
    })
