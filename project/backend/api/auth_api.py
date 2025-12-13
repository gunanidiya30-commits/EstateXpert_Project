from flask import Blueprint, request, jsonify
from backend.db import get_db_connection
import bcrypt

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# -----------------------------
# SIGNUP ROUTE  (SAFE + FIXED)
# -----------------------------
@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    # Hash password (important security fix)
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
# LOGIN ROUTE (SAFE + FIXED)
# -----------------------------
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    # Input validation
    if not email or not password:
        return jsonify({"status": "fail", "message": "Email and password required"}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT id, name, email, password FROM users WHERE email=%s"
        cursor.execute(sql, (email,))
        user = cursor.fetchone()

        # If email not found
        if not user:
            return jsonify({"status": "fail", "message": "Invalid email or password"}), 401

        stored_hash = user["password"]

        # bcrypt password match
        import bcrypt
        if bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
            return jsonify({
                "status": "success",
                "message": "Login successful",
                "user": {
                    "id": user["id"],
                    "name": user["name"],
                    "email": user["email"]
                }
            }), 200

        # Password incorrect
        return jsonify({"status": "fail", "message": "Invalid email or password"}), 401

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass
