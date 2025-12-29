from flask import Blueprint, request, jsonify
from backend.db import get_db_connection

color_palette_api = Blueprint("color_palette_api", __name__)

@color_palette_api.route("/api/color-palette", methods=["POST"])
def get_color_palette():
    data = request.get_json()
    room_type = data.get("room_type")
    style_tag = data.get("style_tag")

    if not room_type or not style_tag:
        return jsonify({"error": "room_type and style_tag required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT primary_color, secondary_color, accent_color
        FROM interior_color_palettes
        WHERE room_type = %s AND style_tag = %s
        LIMIT 1
    """
    cursor.execute(query, (room_type, style_tag))
    palette = cursor.fetchone()

    cursor.close()
    conn.close()

    if not palette:
        return jsonify({"error": "No palette found"}), 404

    return jsonify(palette)
