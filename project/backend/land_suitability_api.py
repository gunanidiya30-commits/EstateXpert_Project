from flask import Blueprint, request, jsonify
from backend.db import get_db_connection

land_suitability_api = Blueprint("land_suitability_api", __name__)

@land_suitability_api.route("/api/land-suitability", methods=["POST"])
def check_land_suitability():
    data = request.get_json()

    slope = data.get("slope_percent")
    road_width = data.get("road_width_feet")
    soil_capacity = data.get("soil_bearing_capacity")

    if slope is None or road_width is None or soil_capacity is None:
        return jsonify({"error": "All land parameters are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM land_suitability_rules")
    rules = cursor.fetchall()

    results = []
    overall_pass = True

    for rule in rules:
        value = None

        if rule["parameter"] == "slope_percent":
            value = slope
        elif rule["parameter"] == "road_width_feet":
            value = road_width
        elif rule["parameter"] == "soil_bearing_capacity":
            value = soil_capacity

        passed = True

        if rule["min_value"] is not None and value < rule["min_value"]:
            passed = False
        if rule["max_value"] is not None and value > rule["max_value"]:
            passed = False

        if not passed:
            overall_pass = False

        results.append({
            "rule": rule["rule_name"],
            "status": "PASS" if passed else "FAIL",
            "message": rule["pass_message"] if passed else rule["fail_message"]
        })

    cursor.close()
    conn.close()

    return jsonify({
        "overall_result": "PASS" if overall_pass else "FAIL",
        "details": results
    })
