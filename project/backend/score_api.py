from flask import Blueprint, jsonify
from backend.db import get_db_connection
import math

score_api = Blueprint("score_api", __name__)

def calculate_score(locality, facility_count):
    safety_score = (locality["safety_index"] / 10) * 40
    pollution_score = ((10 - locality["pollution_index"]) / 10) * 30

    if facility_count <= 1:
        facility_score = 5
    elif facility_count <= 3:
        facility_score = 15
    else:
        facility_score = 30

    total_score = round(safety_score + pollution_score + facility_score, 1)

    return {
        "total_score": total_score,
        "breakdown": {
            "safety": round(safety_score, 1),
            "pollution": round(pollution_score, 1),
            "facilities": facility_score
        }
    }


def get_score_band(score):
    if score >= 80:
        return "Excellent", "green"
    elif score >= 60:
        return "Good", "light-green"
    elif score >= 40:
        return "Average", "orange"
    else:
        return "Poor", "red"


def generate_explanation(breakdown):
    parts = []

    if breakdown["safety"] >= 30:
        parts.append("High safety levels")
    elif breakdown["safety"] >= 20:
        parts.append("Moderate safety")
    else:
        parts.append("Low safety levels")

    if breakdown["pollution"] >= 20:
        parts.append("Low pollution")
    elif breakdown["pollution"] >= 10:
        parts.append("Moderate pollution")
    else:
        parts.append("High pollution")

    if breakdown["facilities"] >= 30:
        parts.append("Excellent access to nearby facilities")
    elif breakdown["facilities"] >= 15:
        parts.append("Decent access to facilities")
    else:
        parts.append("Limited nearby facilities")

    return ", ".join(parts)

@score_api.route("/get_locality_score/<int:locality_id>", methods=["GET"])
def get_locality_score(locality_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Get locality
    cursor.execute(
        "SELECT * FROM localities WHERE locality_id = %s",
        (locality_id,)
    )
    locality = cursor.fetchone()

    if not locality:
        cursor.close()
        conn.close()
        return jsonify({"error": "Locality not found"}), 404

    # Count nearby facilities using distance (Haversine, 3 km)
    cursor.execute(
        """
        SELECT COUNT(*) AS count
        FROM facilities
        WHERE (
            6371 * acos(
                cos(radians(%s)) *
                cos(radians(latitude)) *
                cos(radians(longitude) - radians(%s)) +
                sin(radians(%s)) *
                sin(radians(latitude))
            )
        ) <= 3
        """,
        (
            locality["latitude"],
            locality["longitude"],
            locality["latitude"],
        ),
    )

    facility_count = cursor.fetchone()["count"]

    score_data = calculate_score(locality, facility_count)

    band, color = get_score_band(score_data["total_score"])
    explanation = generate_explanation(score_data["breakdown"])

    cursor.close()
    conn.close()

    return jsonify({
        "locality_id": locality_id,
        "locality_name": locality["locality_name"],
        "score": score_data["total_score"],
        "band": band,
        "color": color,
        "breakdown": score_data["breakdown"],
        "explanation": explanation
    })

