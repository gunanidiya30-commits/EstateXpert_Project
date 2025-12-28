import os
from werkzeug.utils import secure_filename
from flask import Flask, jsonify, request
from backend.db import get_db_connection
from backend.api.users_api import users_api
from backend.api.auth_api import auth_bp
from backend.property_api import property_api
from backend.locality_api import locality_api
from backend.facility_api import facility_api
from backend.nearby_api import nearby_api
from backend.score_api import score_api
from backend.emi_api import emi_api
from backend.rent_vs_buy_api import rent_vs_buy_api
from backend.roi_loan_api import roi_loan_api
from backend.construction_cost_api import construction_cost_api
from flask import send_from_directory

from flask_cors import CORS


app = Flask(__name__)
CORS(app)
UPLOAD_FOLDER = os.path.join(os.getcwd(), "backend/uploads")

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)




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



@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(
        os.path.join(app.root_path, "uploads"),
        filename
    )

app.register_blueprint(users_api, url_prefix="/api")
app.register_blueprint(auth_bp)              # correct
app.register_blueprint(property_api)         # keep this
app.register_blueprint(locality_api)
app.register_blueprint(facility_api)
app.register_blueprint(nearby_api)
app.register_blueprint(score_api)
app.register_blueprint(emi_api)
app.register_blueprint(rent_vs_buy_api)
app.register_blueprint(roi_loan_api)
app.register_blueprint(construction_cost_api)




if __name__ == "__main__":
    app.run(debug=True)
