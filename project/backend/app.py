from flask import Flask, jsonify
from backend.db import get_db_connection
from backend.api.users_api import users_api
from backend.api.auth_api import auth_bp
from backend.property_api import property_api
from flask_cors import CORS


app = Flask(__name__)
CORS(app)



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
app.register_blueprint(auth_bp)              # correct
app.register_blueprint(property_api)         # keep this



if __name__ == "__main__":
    app.run(debug=True)
