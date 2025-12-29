from flask import Blueprint, request, jsonify
from backend.db import get_db_connection

interior_budget_api = Blueprint("interior_budget_api", __name__)

@interior_budget_api.route("/api/interior-budget-plan", methods=["POST"])
def generate_budget_plan():
    data = request.get_json()
    room_type = data.get("room_type")
    style_tag = data.get("style_tag")

    if not room_type or not style_tag:
        return jsonify({"error": "room_type and style_tag required"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT item_name, item_cost
        FROM interior_budget_items
        WHERE room_type = %s AND style_tag = %s
    """
    cursor.execute(query, (room_type, style_tag))
    items = cursor.fetchall()

    total_cost = sum(item["item_cost"] for item in items)

    cursor.close()
    conn.close()

    return jsonify({
        "room_type": room_type,
        "style_tag": style_tag,
        "items": items,
        "total_cost": total_cost
    })
