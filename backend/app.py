from flask import Flask, request, jsonify
from flask_cors import CORS
import MySQLdb
import config

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000", "http://127.0.0.1:3000"])

db = MySQLdb.connect(
    host=config.MYSQL_HOST,
    user=config.MYSQL_USER,
    passwd=config.MYSQL_PASSWORD,
    db=config.MYSQL_DB
)

@app.after_request
def apply_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "http://localhost:3000"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response

@app.route("/test-cors", methods=["GET", "OPTIONS"])
def test_cors():
    if request.method == "OPTIONS":
        response = jsonify({'message': 'CORS preflight successful'})
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        return response
    return jsonify({"message": "CORS test route is working"})

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Backend is running!"})

@app.route("/add-user", methods=["POST", "OPTIONS"])
def add_user():
    if request.method == "OPTIONS":
        response = jsonify({'message': 'CORS preflight successful'})
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response

    data = request.get_json()

    # Extract fields
    user_id = data.get("userID")
    username = data.get("username")
    media_name = data.get("mediaName")
    first_name = data.get("firstName") or None
    last_name = data.get("lastName") or None
    birth_country = data.get("birthCountry") or None
    residence_country = data.get("residenceCountry") or None
    age = data.get("age") if data.get("age") not in ('', None) else None
    gender = data.get("gender") or None
    is_verified = 1 if data.get("isVerified") else 0

    if not user_id or not username or not media_name:
        return jsonify({"error": "Missing required fields (UserID, Username, MediaName)"}), 400

    cursor = db.cursor()

    try:
        cursor.execute("""
            INSERT INTO Users (UserID, Username, MediaName, FirstName, LastName, 
                               BirthCountry, ResidenceCountry, Age, Gender, IsVerified)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (user_id, username, media_name, first_name, last_name, 
              birth_country, residence_country, age, gender, is_verified))
        db.commit()
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify({"status": "success", "username": username}), 201

if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(host="0.0.0.0", port=5050, debug=True)
