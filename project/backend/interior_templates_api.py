from flask import Blueprint, jsonify
from backend.db import get_db_connection

interior_templates_api = Blueprint("interior_templates_api", __name__)

@interior_templates_api.route("/api/interior-templates", methods=["GET"])
def get_interior_templates():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM interior_templates")
    templates = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(templates)
