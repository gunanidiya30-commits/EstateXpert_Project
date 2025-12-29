from flask import Blueprint, request, jsonify
from backend.db import get_db_connection

material_comparison_api = Blueprint("material_comparison_api", __name__)

@material_comparison_api.route("/api/material-comparison", methods=["POST"])
def material_comparison():
    data = request.get_json()
    base_material = data.get("base_material")

    if not base_material:
        return jsonify({"error": "Base material is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT alternative_material, cost_index, durability_score, recommendation_tag "
        "FROM material_alternatives WHERE base_material = %s",
        (base_material,)
    )

    results = cursor.fetchall()
    cursor.close()
    conn.close()

    return jsonify({
        "base_material": base_material,
        "alternatives": results
    })
