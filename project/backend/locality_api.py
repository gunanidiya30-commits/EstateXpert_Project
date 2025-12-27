from flask import Blueprint, jsonify
from backend.db import get_db_connection
import requests

locality_api = Blueprint("locality_api", __name__)

# ---------------------------
# DB HELPER
# ---------------------------
def get_db():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    return conn, cursor

# ---------------------------
# LOCALITY SCORE CALCULATION
# ---------------------------
def calculate_locality_score(locality, facility_score=0):
    # Base score (CORE logic – unchanged)
    safety_score = locality["safety_index"] * 0.6
    pollution_score = (100 - locality["pollution_index"]) * 0.4

    base_score = round((safety_score + pollution_score) / 10, 2)

    # ✅ Micro‑step E integration (70% base, 30% facility)
    final_score = round(
        (base_score * 0.7) + (facility_score * 0.3),
        2
    )

    return base_score, min(10, final_score)

# ---------------------------
# GET LOCALITY SCORE
# ---------------------------
@locality_api.route("/get_locality_score/<int:locality_id>", methods=["GET"])
def get_locality_score(locality_id):
    try:
        conn, cursor = get_db()

        cursor.execute(
            """
            SELECT
                locality_id,
                locality_name,
                city,
                safety_index,
                pollution_index
            FROM localities
            WHERE locality_id = %s
            """,
            (locality_id,),
        )

        locality = cursor.fetchone()
        cursor.close()
        conn.close()

        if not locality:
            return jsonify({"error": "Locality not found"}), 404

        # 🔗 Fetch facility score from nearby_api
        facility_score = 0
        response = requests.get(
            f"http://127.0.0.1:5000/get_nearby_facilities/{locality_id}"
        )

        if response.status_code == 200:
            facility_score = response.json().get("facility_score", 0)

        base_score, final_score = calculate_locality_score(
            locality, facility_score
        )

        return jsonify({
            "locality_id": locality_id,
            "locality_name": locality["locality_name"],
            "base_locality_score": base_score,
            "facility_score": facility_score,
            "final_locality_score": final_score
        })

    except Exception:
        return jsonify({"error": "Failed to calculate locality score"}), 500
