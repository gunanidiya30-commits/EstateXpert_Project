import math
from flask import Blueprint, jsonify, request
from backend.db import get_db_connection

nearby_api = Blueprint("nearby_api", __name__)

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

# ---------------------------
# GET NEARBY FACILITIES
# ---------------------------
@nearby_api.route("/get_nearby_facilities/<int:locality_id>", methods=["GET"])
def get_nearby_facilities(locality_id):
    try:
        facility_type = request.args.get("type")

        conn, cursor = get_db()

        # Fetch locality coordinates
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
            cursor.close()
            conn.close()
            return jsonify({"error": "Locality not found"}), 404

        # Fetch facilities
        if facility_type:
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
                """,
                (facility_type,),
            )
        else:
            cursor.execute(
                """
                SELECT
                    facility_id,
                    facility_name,
                    facility_type,
                    latitude,
                    longitude
                FROM facilities
                """
            )

        facilities = cursor.fetchall()

        # Calculate distances
        results = []
        for f in facilities:
            distance_km = haversine(
                locality["latitude"],
                locality["longitude"],
                f["latitude"],
                f["longitude"],
            )

            f["distance_km"] = distance_km
            results.append(f)

        cursor.close()
        conn.close()

        # Sort by distance
        results.sort(key=lambda x: x["distance_km"])

        return jsonify(results)

    except Exception:
        return jsonify({"error": "Failed to fetch nearby facilities"}), 500
