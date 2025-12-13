from flask import Blueprint, request, jsonify
from backend.db import get_db_connection
import bcrypt

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# -----------------------------
# SIGNUP ROUTE
# -----------------------------
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        cursor.execute(sql, (name, email, hashed_password))
        conn.commit()

        return jsonify({"status": "success", "message": "Signup successful"})

    except Exception as e:
        return jsonify({"status": 'error', "message": str(e)})

    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass


# -----------------------------
# LOGIN ROUTE
# -----------------------------
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email, password FROM users WHERE email=%s", (email,))
        user = cursor.fetchone()
        conn.close()
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    if not user:
        return jsonify({"error": "Invalid email or password"}), 401

    user_id = user[0]
    name = user[1]
    email = user[2]
    stored_hash = user[3]

    if isinstance(stored_hash, str):
        stored_hash = stored_hash.encode("utf-8")

    if not bcrypt.checkpw(password.encode('utf-8'), stored_hash):
        return jsonify({"error": "Invalid email or password"}), 401

    # SUCCESS
    return jsonify({
        "message": "Login successful",
        "user": {
            "id": user_id,
            "name": name,
            "email": email
        }
    }), 200
