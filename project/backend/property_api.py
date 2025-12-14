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

# Add Property API Route
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

@property_api.route("/get_properties/<int:user_id>", methods=["GET"])
def get_properties(user_id):
    try:
        db = get_db()
        cursor = db.cursor(dictionary=True)

        query = "SELECT * FROM properties WHERE user_id = %s ORDER BY created_at DESC"
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()

        return jsonify({"properties": result})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
