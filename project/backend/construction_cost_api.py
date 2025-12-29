from flask import Blueprint, request, jsonify
from backend.db import get_db_connection

construction_cost_api = Blueprint("construction_cost_api", __name__)

@construction_cost_api.route("/api/construction-cost", methods=["POST"])
def calculate_construction_cost():
    data = request.get_json()

    area = data.get("area")
    grade = data.get("grade")

    if not area or not grade:
        return jsonify({"error": "Area and grade are required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT material_cost_per_sqft, labor_cost_per_sqft
        FROM construction_cost_rates
        WHERE grade = %s
        """,
        (grade,)
    )

    rate = cursor.fetchone()
    cursor.close()
    conn.close()

    if not rate:
        return jsonify({"error": "Invalid construction grade"}), 400

    material_cost = rate["material_cost_per_sqft"] * area
    labor_cost = rate["labor_cost_per_sqft"] * area
    total_cost = material_cost + labor_cost

    return jsonify({
        "area_sqft": area,
        "grade": grade,
        "material_cost": material_cost,
        "labor_cost": labor_cost,
        "total_cost": total_cost
    })
