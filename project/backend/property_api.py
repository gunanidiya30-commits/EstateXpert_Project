from flask import Blueprint, request, jsonify
import mysql.connector

property_api = Blueprint("property_api", __name__)

# Database connection function
def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # your password
        database="estatexpert_db"
    )

# ---------------------------
# ADD PROPERTY
# ---------------------------
@property_api.route("/add_property", methods=["POST"])
def add_property():
    data = request.get_json()

    user_id = data.get("user_id")
    title = data.get("title")
    price = data.get("price")
    location = data.get("location")
    description = data.get("description")

    try:
        db = get_db()
        cursor = db.cursor()

        sql = """
            INSERT INTO properties (user_id, title, price, location, description)
            VALUES (%s, %s, %s, %s, %s)
        """

        cursor.execute(sql, (user_id, title, price, location, description))
        db.commit()

        return jsonify({"message": "Property added successfully!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------------------
# GET ALL PROPERTIES OF ONE USER
# ---------------------------
@property_api.route("/get_properties/<int:user_id>", methods=["GET"])
def get_properties(user_id):
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        sql = "SELECT * FROM properties WHERE user_id = %s ORDER BY id DESC"
        cursor.execute(sql, (user_id,))

        properties = cursor.fetchall()
        return jsonify(properties)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------------------
# GET SINGLE PROPERTY FOR EDIT
# ---------------------------
@property_api.route("/get_properties_single/<int:property_id>", methods=["GET"])
def get_single_property(property_id):
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        sql = "SELECT * FROM properties WHERE id = %s"
        cursor.execute(sql, (property_id,))

        property_data = cursor.fetchone()
        return jsonify(property_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------------------
# UPDATE PROPERTY
# ---------------------------
@property_api.route('/update_property/<int:property_id>', methods=['PUT'])
def update_property(property_id):
    data = request.get_json()

    title = data.get("title")
    price = data.get("price")
    location = data.get("location")
    description = data.get("description")

    try:
        db = get_db()
        cursor = db.cursor()

        query = """
            UPDATE properties
            SET title=%s, price=%s, location=%s, description=%s
            WHERE id=%s
        """

        cursor.execute(query, (title, price, location, description, property_id))
        db.commit()

        return jsonify({"message": "Property updated successfully!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
