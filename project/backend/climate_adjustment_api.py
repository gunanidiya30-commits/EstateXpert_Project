from flask import Blueprint, request, jsonify
from backend.db import get_db_connection

climate_adjustment_api = Blueprint("climate_adjustment_api", __name__)

@climate_adjustment_api.route("/api/climate-adjustment", methods=["POST"])
def climate_adjustment():
    data = request.get_json()
    climate_zone = data.get("climate_zone")

    if not climate_zone:
        return jsonify({"error": "Climate zone is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT cost_multiplier, material_note "
        "FROM climate_adjustment_factors WHERE climate_zone = %s",
        (climate_zone,)
    )

    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if not result:
        return jsonify({"error": "Climate zone not found"}), 404

    return jsonify({
        "climate_zone": climate_zone,
        "cost_multiplier": float(result["cost_multiplier"]),
        "material_note": result["material_note"]
    })
