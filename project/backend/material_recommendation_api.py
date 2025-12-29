from flask import Blueprint, request, jsonify
from backend.db import get_db_connection

material_recommendation_api = Blueprint("material_recommendation_api", __name__)

@material_recommendation_api.route("/api/material-recommendation", methods=["POST"])
def recommend_materials():
    data = request.get_json()
    grade = data.get("grade")

    if not grade:
        return jsonify({"error": "Construction grade is required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT material_name, category, quality_grade, recommended_for
        FROM construction_materials
        WHERE quality_grade = %s
        """,
        (grade,)
    )

    materials = cursor.fetchall()
    cursor.close()
    conn.close()

    if not materials:
        return jsonify({"error": "No materials found for this grade"}), 404

    return jsonify({
        "selected_grade": grade,
        "reason":
            f"Materials are selected because they match the {grade} construction quality requirements.",
        "materials": materials
    })
