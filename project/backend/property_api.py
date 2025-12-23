import os
from werkzeug.utils import secure_filename
from flask import Blueprint, request, jsonify
from backend.db import get_db_connection

property_api = Blueprint("property_api", __name__)

UPLOAD_FOLDER = "backend/uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

# ---------------------------
# HELPERS
# ---------------------------
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
# ADD PROPERTY
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

        cursor.execute(
            """
            INSERT INTO properties (title, price, location, description, user_id)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (title, price, location, description, user_id)
        )
        conn.commit()

        property_id = cursor.lastrowid

        # ✅ Track saved images
        saved_images = []

        if "images" in request.files:
            images = request.files.getlist("images")

            for image in images:
                if image and allowed_file(image.filename):
                    filename = secure_filename(image.filename)
                    save_path = os.path.join(UPLOAD_FOLDER, filename)
                    image.save(save_path)

                    image_path = f"/uploads/{filename}"

                    add_property_image(
                        property_id,
                        image_path,
                        is_primary=False
                    )

                    saved_images.append(image_path)

        # ✅ Day‑16 Micro‑step A: enforce at least one image
        if len(saved_images) == 0:
            cursor.close()
            conn.close()
            return jsonify({"error": "At least one property image is required"}), 400

        # ✅ Day‑16 Micro‑step B: auto‑assign primary image
        cursor.execute(
            """
            UPDATE property_images
            SET is_primary = 1
            WHERE property_id = %s
            ORDER BY display_order ASC, id ASC
            LIMIT 1
            """,
            (property_id,)
        )
        conn.commit()

        cursor.close()
        conn.close()

        return jsonify({"message": "Property added successfully!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------------------
# GET PROPERTIES BY USER (WITH THUMBNAIL)
# ---------------------------
@property_api.route("/get_properties/<int:user_id>", methods=["GET"])
def get_properties(user_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute(
            """
            SELECT
                p.*,
                pi.image_path AS thumbnail
            FROM properties p
            LEFT JOIN property_images pi
                ON p.id = pi.property_id AND pi.is_primary = TRUE
            WHERE p.user_id = %s
            ORDER BY p.id DESC
            """,
            (user_id,)
        )

        properties = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify(properties)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# ---------------------------
# GET SINGLE PROPERTY (WITH IMAGE GALLERY)
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
        property_data = cursor.fetchone()

        if not property_data:
            return jsonify({"error": "Property not found"}), 404

        cursor.execute(
            """
            SELECT image_path
            FROM property_images
            WHERE property_id = %s
            ORDER BY display_order ASC, id ASC
            """,
            (property_id,)
        )
        images = cursor.fetchall()

        property_data["images"] = [img["image_path"] for img in images]

        cursor.close()
        conn.close()

        return jsonify(property_data)

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

        cursor.execute(
            """
            UPDATE properties
            SET title=%s, price=%s, location=%s, description=%s
            WHERE id=%s
            """,
            (title, price, location, description, property_id)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"message": "Property updated successfully!"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@property_api.route("/delete_property_image/<int:image_id>", methods=["DELETE"])
def delete_property_image(image_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # Get property_id of the image
        cursor.execute(
            "SELECT property_id FROM property_images WHERE id = %s",
            (image_id,)
        )
        image = cursor.fetchone()
        if not image:
            return jsonify({"error": "Image not found"}), 404

        property_id = image["property_id"]

        # Count images for this property
        cursor.execute(
            "SELECT COUNT(*) AS count FROM property_images WHERE property_id = %s",
            (property_id,)
        )
        image_count = cursor.fetchone()["count"]

        if image_count <= 1:
            return jsonify({"error": "A property must have at least one image"}), 400

        # Safe to delete
        cursor.execute(
            "DELETE FROM property_images WHERE id = %s",
            (image_id,)
        )
        conn.commit()

        cursor.close()
        conn.close()
        return jsonify({"message": "Image deleted successfully"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500
