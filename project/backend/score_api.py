from flask import Blueprint, jsonify
from backend.db import get_db_connection
from math import radians, cos, sin, asin, sqrt

score_api = Blueprint("score_api", __name__)

MAX_FACILITY_SCORE = 60  # normalization cap

# -------------------------
# HELPERS
# -------------------------
def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    return 6371 * (2 * asin(sqrt(a)))

def calculate_score(locality, facilities):
    safety_score = round(locality["safety_index"] * 40, 2)
    pollution_score = round((1 - locality["pollution_index"]) * 20, 2)

    facility_total = sum(f["weighted_score"] for f in facilities)
    facility_score = min(40, round((facility_total / MAX_FACILITY_SCORE) * 40, 2))

    return {
        "total_score": round(safety_score + pollution_score + facility_score, 2),
        "breakdown": {
            "safety": safety_score,
            "pollution": pollution_score,
            "facilities": facility_score,
        },
    }

def get_score_band(score):
    if score >= 80:
        return "Excellent", "green"
    elif score >= 60:
        return "Good", "light-green"
    elif score >= 40:
        return "Average", "orange"
    return "Poor", "red"

def generate_explanation(b):
    return ", ".join([
        "High safety" if b["safety"] >= 30 else "Moderate safety" if b["safety"] >= 20 else "Low safety",
        "Low pollution" if b["pollution"] >= 15 else "Moderate pollution" if b["pollution"] >= 8 else "High pollution",
        "Excellent facilities" if b["facilities"] >= 25 else "Decent facilities" if b["facilities"] >= 12 else "Limited facilities"
    ])

def calculate_facility_component(locality):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT
            (
                6371 * acos(
                    cos(radians(%s)) *
                    cos(radians(latitude)) *
                    cos(radians(longitude) - radians(%s)) +
                    sin(radians(%s)) *
                    sin(radians(latitude))
                )
            ) AS distance,
            type
        FROM facilities
        HAVING distance <= 3
        """,
        (
            locality["latitude"],
            locality["longitude"],
            locality["latitude"],
        )
    )

    facilities = cursor.fetchall()
    cursor.close()
    conn.close()

    if not facilities:
        return 0

    FACILITY_WEIGHTS = {
        "hospital": 1.5,
        "metro": 1.4,
        "school": 1.3,
        "mall": 1.1,
        "park": 1.0
    }

    total_weighted_score = 0

    for f in facilities:
        base_score = 10  # max time_score assumption
        weight = FACILITY_WEIGHTS.get(f["type"], 1.0)
        total_weighted_score += base_score * weight

    max_possible = len(facilities) * 15
    normalized = (total_weighted_score / max_possible) * 30

    return round(min(normalized, 30), 1)


# -------------------------
# API
# -------------------------
@score_api.route("/get_locality_score/<int:locality_id>")
def get_locality_score(locality_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT * FROM localities WHERE locality_id = %s",
        (locality_id,)
    )
    locality = cursor.fetchone()

    if not locality:
        return jsonify({"error": "Locality not found"}), 404

    cursor.execute("SELECT * FROM facilities")
    facilities = cursor.fetchall()

    weights = {
        "hospital": 1.5,
        "metro": 1.4,
        "school": 1.3,
        "mall": 1.1,
        "park": 1.0
    }

    enriched = []
    for f in facilities:
        distance = haversine(
            locality["latitude"],
            locality["longitude"],
            f["latitude"],
            f["longitude"]
        )

        travel_time = (distance / 30) * 60  # minutes

        if travel_time <= 5:
            time_score = 10
        elif travel_time <= 10:
            time_score = 8
        elif travel_time <= 20:
            time_score = 6
        elif travel_time <= 30:
            time_score = 4
        else:
            time_score = 2

        weight = weights.get(f["facility_type"], 1.0)

        enriched.append({
            "weighted_score": round(time_score * weight, 2)
        })

    score_data = calculate_score(locality, enriched)
    band, color = get_score_band(score_data["total_score"])

    return jsonify({
        "locality_id": locality_id,
        "locality_name": locality["locality_name"],
        "score": score_data["total_score"],
        "band": band,
        "color": color,
        "breakdown": score_data["breakdown"],
        "explanation": generate_explanation(score_data["breakdown"])
    })
