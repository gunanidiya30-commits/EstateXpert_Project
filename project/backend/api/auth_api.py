from flask import Blueprint, request, jsonify
from backend.db import get_db_connection

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        sql = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
        cursor.execute(sql, (name, email, password))
        conn.commit()

        return jsonify({"status": "success", "message": "Signup successful"})
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        sql = "SELECT id, name, email FROM users WHERE email=%s AND password=%s"
        cursor.execute(sql, (email, password))
        user = cursor.fetchone()

        if user:
            return jsonify({"status": "success", "user": user})
        else:
            return jsonify({"status": "fail", "message": "Invalid email or password"})
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass
