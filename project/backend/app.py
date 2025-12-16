import os
from werkzeug.utils import secure_filename
from flask import Flask, jsonify
from backend.db import get_db_connection
from backend.api.users_api import users_api
from backend.api.auth_api import auth_bp
from backend.property_api import property_api
from flask import send_from_directory

from flask_cors import CORS


app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
CORS(
    app,
    resources={r"/api/*": {"origins": "*"}},
    supports_credentials=True
)


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


@app.route('/upload_image/<int:property_id>', methods=['POST'])
def upload_image(property_id):
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image = request.files['image']          # get uploaded file
    filename = secure_filename(image.filename)  # clean file name
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    image.save(filepath)    # save file to uploads/

    # Save filename to database (not full path)
    cursor = mysql.connection.cursor()
    cursor.execute(
        "UPDATE properties SET image=%s WHERE id=%s",
        (filename, property_id)
    )
    mysql.connection.commit()
    cursor.close()

    return jsonify({"message": "Image uploaded successfully", "filename": filename})

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

app.register_blueprint(users_api, url_prefix="/api")
app.register_blueprint(auth_bp)              # correct
app.register_blueprint(property_api)         # keep this



if __name__ == "__main__":
    app.run(debug=True)
