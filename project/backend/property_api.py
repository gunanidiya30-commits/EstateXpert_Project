import os
from werkzeug.utils import secure_filename
from flask import Blueprint, request, jsonify
from backend.db import get_db_connection

property_api = Blueprint("property_api", __name__)

UPLOAD_FOLDER = "backend/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def add_property_image(property_id, image_path, is_primary=False):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO property_images (property_id, image_path, is_primary)
        VALUES (%s, %s, %s)
        """,
        (property_id, image_path, is_primary)
    )

    conn.commit()
    cursor.close()
    conn.close()

# ---------------------------
# ADD PROPERTY (JSON BASED)
# ---------------------------
@property_api.route("/add_property", methods=["POST"])
def add_property():
    try:
        data = request.form

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

        # 🔽 THIS MUST BE INSIDE try (INDENTED)
        property_id = cursor.lastrowid

        if "images" in request.files:
            images = request.files.getlist("images")

            for index, image in enumerate(images):
                if image and allowed_file(image.filename):
                    filename = secure_filename(image.filename)
                    image_path = os.path.join(UPLOAD_FOLDER, filename)
                    image.save(image_path)

                    add_property_image(
                        property_id,
                        image_path,
                        is_primary=(index == 0)
                    )

        cursor.close()
        conn.close()

        return jsonify({"message": "Property added successfully!"})

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

