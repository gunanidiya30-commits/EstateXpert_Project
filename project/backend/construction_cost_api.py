from flask import Blueprint, request, jsonify
from backend.db import get_db_connection

construction_cost_api = Blueprint("construction_cost_api", __name__)

@construction_cost_api.route("/calculate_construction_cost", methods=["POST"])
def calculate_construction_cost():
    data = request.get_json()

    area_sqft = int(data.get("area_sqft"))
    grade = data.get("construction_grade")

    # cost per sqft based on grade
    rate_map = {
        "basic": 1200,
        "standard": 1800,
        "premium": 2500
    }

    if grade not in rate_map:
        return jsonify({"error": "Invalid construction grade"}), 400

    total_cost = area_sqft * rate_map[grade]
    material_cost = total_cost * 0.6
    labor_cost = total_cost * 0.4

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO construction_cost_estimates
        (area_sqft, construction_grade, material_cost, labor_cost, total_cost)
        VALUES (%s, %s, %s, %s, %s)
    """, (area_sqft, grade, material_cost, labor_cost, total_cost))

    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({
        "area_sqft": area_sqft,
        "construction_grade": grade,
        "material_cost": material_cost,
        "labor_cost": labor_cost,
        "total_cost": total_cost
    })
