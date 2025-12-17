from flask import Blueprint, request, jsonify
from backend.db import get_db_connection

property_api = Blueprint("property_api", __name__)

# ---------------------------
# ADD PROPERTY (JSON BASED)
# ---------------------------
@property_api.route("/add_property", methods=["POST"])
def add_property():
    try:
        data = request.get_json()

        title = data.get("title")
        price = data.get("price")
        location = data.get("location")
        description = data.get("description")
        user_id = data.get("user_id")

        conn = get_db_connection()
        cursor = conn.cursor()

        sql = """
            INSERT INTO properties (title, price, location, description, user_id)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (title, price, location, description, user_id))
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "Property added successfully!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------------------
# GET PROPERTIES BY USER
# ---------------------------
@property_api.route("/get_properties/<int:user_id>", methods=["GET"])
def get_properties(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM properties WHERE user_id = %s ORDER BY id DESC",
            (user_id,)
        )

        properties = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(properties)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------------------
# GET SINGLE PROPERTY
# ---------------------------
@property_api.route("/get_property/<int:property_id>", methods=["GET"])
def get_property(property_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            "SELECT * FROM properties WHERE id = %s",
            (property_id,)
        )

        prop = cursor.fetchone()

        cursor.close()
        conn.close()

        return jsonify(prop)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------------------
# UPDATE PROPERTY
# ---------------------------
@property_api.route("/update_property/<int:property_id>", methods=["PUT"])
def update_property(property_id):
    try:
        data = request.get_json()

        title = data.get("title")
        price = data.get("price")
        location = data.get("location")
        description = data.get("description")

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE properties
            SET title=%s, price=%s, location=%s, description=%s
            WHERE id=%s
        """, (title, price, location, description, property_id))

        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "Property updated successfully!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@property_api.route("/property/<int:property_id>", methods=["GET"])
def get_single_property(property_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute(
        "SELECT * FROM properties WHERE id = %s",
        (property_id,)
    )

    property_data = cursor.fetchone()
    cursor.close()

    if not property_data:
        return jsonify({"error": "Property not found"}), 404

    return jsonify(property_data), 200

