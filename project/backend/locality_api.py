from flask import Blueprint, jsonify
from backend.db import get_db_connection

locality_api = Blueprint("locality_api", __name__)

# ---------------------------
# HELPERS (MATCH PROPERTY API)
# ---------------------------
def get_db():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    return conn, cursor

# ---------------------------
# GET ALL LOCALITIES
# ---------------------------
@locality_api.route("/get_localities", methods=["GET"])
def get_localities():
    try:
        conn, cursor = get_db()

        cursor.execute(
            """
            SELECT
                locality_id,
                locality_name,
                city,
                latitude,
                longitude,
                safety_index,
                pollution_index
            FROM localities
            ORDER BY city, locality_name
            """
        )

        data = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify(data)

    except Exception:
        return jsonify({"error": "Failed to fetch localities"}), 500

# ---------------------------
# GET SINGLE LOCALITY
# ---------------------------
@locality_api.route("/get_locality/<int:locality_id>", methods=["GET"])
def get_locality(locality_id):
    try:
        conn, cursor = get_db()

        cursor.execute(
            """
            SELECT
                locality_id,
                locality_name,
                city,
                latitude,
                longitude,
                safety_index,
                pollution_index
            FROM localities
            WHERE locality_id = %s
            """,
            (locality_id,),
        )

        data = cursor.fetchone()
        cursor.close()
        conn.close()

        if not data:
            return jsonify({"error": "Locality not found"}), 404

        return jsonify(data)

    except Exception:
        return jsonify({"error": "Failed to fetch locality"}), 500
