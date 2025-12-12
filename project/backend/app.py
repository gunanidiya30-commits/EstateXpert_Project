from flask import Flask, jsonify
from db import get_db_connection
from api.users_api import users_api


app = Flask(__name__)

@app.route("/test-db")
def test_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        return jsonify({"status": "success", "message": "Database connected"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
    finally:
        try:
            cursor.close()
            conn.close()
        except:
            pass

@app.route("/")
def home():
    return "Backend running successfully"

app.register_blueprint(users_api, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True)
