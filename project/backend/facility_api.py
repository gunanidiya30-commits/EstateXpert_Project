from flask import Blueprint, jsonify
from backend.db import get_db_connection

facility_api = Blueprint("facility_api", __name__)

# ---------------------------
# HELPERS (MATCH OTHER APIS)
# ---------------------------
def get_db():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    return conn, cursor

# ---------------------------
# GET ALL FACILITIES
# ---------------------------
@facility_api.route("/get_facilities", methods=["GET"])
def get_facilities():
    try:
        conn, cursor = get_db()

        cursor.execute(
            """
            SELECT
                facility_id,
                facility_name,
                facility_type,
                latitude,
                longitude
            FROM facilities
            ORDER BY facility_type, facility_name
            """
        )

        data = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify(data)

    except Exception:
        return jsonify({"error": "Failed to fetch facilities"}), 500

# ---------------------------
# GET FACILITIES BY TYPE
# ---------------------------
@facility_api.route("/get_facilities/<string:facility_type>", methods=["GET"])
def get_facilities_by_type(facility_type):
    try:
        if facility_type not in ["school", "hospital", "transport"]:
            return jsonify({"error": "Invalid facility type"}), 400

        conn, cursor = get_db()

        cursor.execute(
            """
            SELECT
                facility_id,
                facility_name,
                facility_type,
                latitude,
                longitude
            FROM facilities
            WHERE facility_type = %s
            ORDER BY facility_name
            """,
            (facility_type,),
        )

        data = cursor.fetchall()
        cursor.close()
        conn.close()

        return jsonify(data)

    except Exception:
        return jsonify({"error": "Failed to fetch facilities"}), 500
