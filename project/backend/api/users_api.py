from flask import Blueprint, request, jsonify
from db import get_db_connection

users_api = Blueprint("users_api", __name__)

@users_api.route("/users", methods=["GET"])
def get_users():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id, name, email, password FROM users")
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

@users_api.route('/users/add', methods=['POST'])
def add_user():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)"
    values = (name, email, password)

    cursor.execute(sql, values)
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "User added successfully", "status": "success"})

@users_api.route('/users/delete/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    sql = "DELETE FROM users WHERE id = %s"
    cursor.execute(sql, (user_id,))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "User deleted", "status": "success"})

@users_api.route('/users/update/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()

    sql = """
        UPDATE users 
        SET name = %s, email = %s, password = %s 
        WHERE id = %s
    """
    values = (name, email, password, user_id)

    cursor.execute(sql, values)
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({"message": "User updated successfully", "status": "success"})
