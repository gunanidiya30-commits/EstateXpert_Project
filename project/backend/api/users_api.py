from flask import Blueprint, request, jsonify
from db import get_db_connection

users_api = Blueprint("users_api", __name__)

@users_api.route("/users", methods=["GET"])
def get_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, email FROM users")
        users = cursor.fetchall()
        return jsonify({"status": "success", "data": users})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass
