import math
from flask import Blueprint, jsonify, request
from backend.db import get_db_connection

nearby_api = Blueprint("nearby_api", __name__)

# ---------------------------
# CONSTANTS
# ---------------------------
FACILITY_WEIGHTS = {
    "hospital": 1.5,
    "metro": 1.4,
    "school": 1.3,
    "mall": 1.1,
    "park": 1.0
}

# ---------------------------
# HELPERS
# ---------------------------
def get_db():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    return conn, cursor


def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Earth radius in KM
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)

    a = (
        math.sin(d_lat / 2) ** 2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(d_lon / 2) ** 2
    )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)


def distance_bucket(distance):
    if distance <= 1:
        return "Excellent"
    elif distance <= 3:
        return "Good"
    elif distance <= 5:
        return "Average"
    return "Poor"


def time_score(distance_km):
    if distance_km <= 1:
        return 10
    elif distance_km <= 3:
        return 7
    elif distance_km <= 5:
        return 4
    return 1


def calculate_facility_score(facilities):
    if not facilities:
        return 0

    scores = [f["weighted_score"] for f in facilities if "weighted_score" in f]

    if not scores:
        return 0

    avg_score = sum(scores) / len(scores)
    normalized = round(avg_score / 1.5, 2)

    return min(normalized, 10)

# ---------------------------
# GET NEARBY FACILITIES
# ---------------------------
@nearby_api.route("/get_nearby_facilities/<int:locality_id>", methods=["GET"])
def get_nearby_facilities(locality_id):
    try:
        facility_type = request.args.get("type")

        conn, cursor = get_db()

        cursor.execute(
            """
            SELECT latitude, longitude
            FROM localities
            WHERE locality_id = %s
            """,
            (locality_id,),
        )
        locality = cursor.fetchone()

        if not locality:
            return jsonify({"error": "Locality not found"}), 404

        if facility_type:
            cursor.execute(
                """
                SELECT facility_id, facility_name, facility_type, latitude, longitude
                FROM facilities
                WHERE facility_type = %s
                """,
                (facility_type,),
            )
        else:
            cursor.execute(
                """
                SELECT facility_id, facility_name, facility_type, latitude, longitude
                FROM facilities
                """
            )

        facilities = cursor.fetchall()

        results = []
        for f in facilities:
            distance_km = haversine(
                locality["latitude"],
                locality["longitude"],
                f["latitude"],
                f["longitude"],
            )

            base_score = time_score(distance_km)
            weight = FACILITY_WEIGHTS.get(f["facility_type"], 1.0)
            weighted_score = round(base_score * weight, 2)

            results.append({
                "facility_id": f["facility_id"],
                "name": f["facility_name"],
                "type": f["facility_type"],
                "latitude": f["latitude"],
                "longitude": f["longitude"],
                "distance_km": distance_km,
                "travel_band": distance_bucket(distance_km),
                "time_score": base_score,
                "weight": weight,
                "weighted_score": weighted_score
            })

        results.sort(key=lambda x: x["distance_km"])

        facility_score = calculate_facility_score(results)

        return jsonify({
            "facilities": results,
            "facility_score": facility_score
        })

    except Exception as e:
        print(e)
        return jsonify({"error": "Failed to fetch nearby facilities"}), 500
