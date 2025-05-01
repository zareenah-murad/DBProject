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

@app.route("/add-project", methods=["POST", "OPTIONS"])
def add_project():
    if request.method == "OPTIONS":
        response = jsonify({'message': 'CORS preflight successful'})
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response

    data = request.get_json()

    # Extract Fields and Trim White Space
    def clean_str(value):
        if not isinstance(value, str):
            return None
        return " ".join(value.strip().split())

    # Use the helper to clean each input
    project_name = clean_str(data.get("ProjectName"))
    manager_first = clean_str(data.get("ManagerFirstName"))
    manager_last = clean_str(data.get("ManagerLastName"))
    institute_name = clean_str(data.get("InstituteName"))
    start_date = clean_str(data.get("StartDate"))
    end_date = clean_str(data.get("EndDate"))

    project_name = project_name.lower()

    # CHECK 1: SQL injection-style check (after clean_str & type check)
    dangerous_inputs = [project_name, manager_first, manager_last, institute_name]
    sql_keywords = [";", "--", "drop", "insert", "delete", "update"]

    for value in dangerous_inputs:
        if isinstance(value, str) and any(bad in value.lower() for bad in sql_keywords):
            return jsonify({"error": "Input contains potentially dangerous content"}), 400

    # CHECK 2: HTML Threats
    html_threats = ["<script", "<img", "<svg", "onerror", "onload", "javascript:"]
    for value in [project_name, manager_first, manager_last, institute_name]:
        if any(threat in value.lower() for threat in html_threats):
            return jsonify({"error": "Input contains disallowed HTML or script tags"}), 400

    # CHECK 3: Reject non-ASCII characters
    for value in [project_name, manager_first, manager_last, institute_name]:
        if not value.isascii():
            return jsonify({"error": "Fields must contain only ASCII characters"}), 400

    # CHECK 4: Check for required fields (already in place)
    if not all([project_name, manager_first, manager_last, institute_name, start_date, end_date]):
        return jsonify({"error": "One or more fields are missing or of the wrong type"}), 400

    # CHECK 5: Type checks (everything must be a string)
    if not all(isinstance(f, str) for f in [project_name, manager_first, manager_last, institute_name, start_date, end_date]):
        return jsonify({"error": "All fields must be strings in valid format"}), 400

    # CHECK 6: Length limits (based on schema)
    if len(project_name) > 100:
        return jsonify({"error": "ProjectName too long (max 100 characters)"}), 400
    if len(manager_first) > 100 or len(manager_last) > 100:
        return jsonify({"error": "Manager name too long (max 100 characters)"}), 400
    if len(institute_name) > 150:
        return jsonify({"error": "InstituteName too long (max 150 characters)"}), 400

    # CHECK 7: Validate date format and order
    from datetime import datetime
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        if end < start:
            return jsonify({"error": "EndDate must be after or equal to StartDate"}), 400
    except ValueError:
        return jsonify({"error": "Dates must be in YYYY-MM-DD format"}), 400

    cursor = db.cursor()

    try:
        # CHECK 8: Check for duplicate project name (after trimming)
        cursor.execute("SELECT * FROM Project WHERE ProjectName = %s", (project_name,))
        if cursor.fetchone():
            return jsonify({"error": "A project with this name already exists"}), 400

        # CHECK 9: Check if the institute exists
        cursor.execute("SELECT * FROM Institute WHERE InstituteName = %s", (institute_name,))
        if cursor.fetchone() is None:
            return jsonify({"error": "Institute does not exist"}), 400

        cursor.execute("""
            INSERT INTO Project (ProjectName, ManagerFirstName, ManagerLastName, InstituteName, StartDate, EndDate)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (project_name, manager_first, manager_last, institute_name, start_date, end_date))
        db.commit()
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify({"status": "success", "project": project_name}), 201

@app.route("/add-institute", methods=["POST", "OPTIONS"])
def add_institute():
    if request.method == "OPTIONS":
        response = jsonify({'message': 'CORS preflight successful'})
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response

    data = request.get_json()
    institute_name = data.get("InstituteName")

    # Clean and normalize
    def clean_str(value):
        if not isinstance(value, str):
            return None
        return " ".join(value.strip().split())

    institute_name = clean_str(institute_name)

    # Check required
    if not institute_name:
        return jsonify({"error": "InstituteName is required and must be a valid string"}), 400

    # Check type
    if not isinstance(institute_name, str):
        return jsonify({"error": "InstituteName must be a string"}), 400

    # Length check
    if len(institute_name) > 150:
        return jsonify({"error": "InstituteName too long (max 150 characters)"}), 400

    # ASCII-only check
    if not institute_name.isascii():
        return jsonify({"error": "InstituteName must contain only ASCII characters"}), 400

    # Dangerous keywords (SQL-style)
    if any(bad in institute_name.lower() for bad in [";", "--", "drop", "insert", "delete", "update"]):
        return jsonify({"error": "InstituteName contains potentially dangerous content"}), 400

    # HTML/script injection
    if any(threat in institute_name.lower() for threat in ["<script", "<img", "<svg", "onerror", "onload", "javascript:"]):
        return jsonify({"error": "InstituteName contains disallowed HTML or script tags"}), 400

    # Normalize casing (optional)
    institute_name = institute_name.lower()

    cursor = db.cursor()

    try:
        # Check for duplicates
        cursor.execute("SELECT * FROM Institute WHERE InstituteName = %s", (institute_name,))
        if cursor.fetchone():
            return jsonify({"error": "An institute with this name already exists"}), 400

        cursor.execute("INSERT INTO Institute (InstituteName) VALUES (%s)", (institute_name,))
        db.commit()
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify({"status": "success", "institute": institute_name}), 201


@app.route("/add-field", methods=["POST", "OPTIONS"])
def add_field():
    if request.method == "OPTIONS":
        response = jsonify({'message': 'CORS preflight successful'})
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response

    data = request.get_json()

    raw_project_name = data.get("ProjectName")
    raw_field_name = data.get("FieldName")

    # Type check FIRST
    if not isinstance(raw_project_name, str) or not isinstance(raw_field_name, str):
        return jsonify({"error": "Both fields must be strings"}), 400

    # Now clean
    def clean_str(value):
        return " ".join(value.strip().split())

    project_name = clean_str(raw_project_name)
    field_name = clean_str(raw_field_name)

    # Then required check
    if not project_name or not field_name:
        return jsonify({"error": "ProjectName and FieldName are required"}), 400

    # Type check
    if not isinstance(project_name, str) or not isinstance(field_name, str):
        return jsonify({"error": "Both fields must be strings"}), 400

    # Length check
    if len(project_name) > 100 or len(field_name) > 100:
        return jsonify({"error": "FieldName and ProjectName must be <= 100 characters"}), 400

    # ASCII-only check
    if not project_name.isascii() or not field_name.isascii():
        return jsonify({"error": "Inputs must contain only ASCII characters"}), 400

    # SQL-style junk check
    if any(bad in field_name.lower() for bad in [";", "--", "drop", "insert", "delete", "update"]):
        return jsonify({"error": "FieldName contains potentially dangerous content"}), 400

    # Script tag / HTML threat check
    if any(tag in field_name.lower() for tag in ["<script", "<img", "<svg", "onerror", "onload", "javascript:"]):
        return jsonify({"error": "FieldName contains disallowed HTML or script tags"}), 400

    # Normalize case (optional)
    field_name = field_name.lower()

    cursor = db.cursor()

    try:
        # Check that project exists
        cursor.execute("SELECT * FROM Project WHERE ProjectName = %s", (project_name,))
        if cursor.fetchone() is None:
            return jsonify({"error": "Project does not exist"}), 400

        # Check for duplicate field in the same project
        cursor.execute("""
            SELECT * FROM Field WHERE ProjectName = %s AND FieldName = %s
        """, (project_name, field_name))
        if cursor.fetchone():
            return jsonify({"error": "Field already exists in this project"}), 400

        # Insert the field
        cursor.execute("""
            INSERT INTO Field (ProjectName, FieldName)
            VALUES (%s, %s)
        """, (project_name, field_name))
        db.commit()
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify({"status": "success", "field": field_name}), 201

@app.route("/add-post", methods=["POST", "OPTIONS"])
def add_post():
    if request.method == "OPTIONS":
        response = jsonify({'message': 'CORS preflight successful'})
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response

    data = request.get_json()

    post_id = data.get("PostID")
    user_id = data.get("UserID")
    post_text = data.get("PostText")
    post_datetime = data.get("PostDateTime")

    # Optional fields
    reposted_by_user_id = data.get("RepostedByUserID") or None
    repost_datetime = data.get("RepostDateTime") or None
    city = data.get("City") or None
    state = data.get("State") or None
    country = data.get("Country") or None
    likes = data.get("Likes") if data.get("Likes") not in ('', None) else None
    dislikes = data.get("Dislikes") if data.get("Dislikes") not in ('', None) else None
    has_multimedia = 1 if data.get("HasMultimedia") else 0

    if not post_id or not user_id or not post_text or not post_datetime:
        return jsonify({"error": "Missing required fields (PostID, UserID, PostText, PostDateTime)"}), 400

    cursor = db.cursor()

    try:
        cursor.execute("""
            INSERT INTO Posts (PostID, UserID, PostText, PostDateTime, RepostedByUserID, RepostDateTime,
                               City, State, Country, Likes, Dislikes, HasMultimedia)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            post_id, user_id, post_text, post_datetime,
            reposted_by_user_id, repost_datetime,
            city, state, country, likes, dislikes, has_multimedia
        ))
        db.commit()
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify({"status": "success", "post_id": post_id}), 201

@app.route("/add-socialmedia", methods=["POST", "OPTIONS"])
def add_socialmedia():
    if request.method == "OPTIONS":
        response = jsonify({'message': 'CORS preflight successful'})
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response

    data = request.get_json()
    media_name = data.get("MediaName")

    # Helper to clean and normalize
    def clean_str(value):
        if not isinstance(value, str):
            return None
        return " ".join(value.strip().split())

    media_name = clean_str(media_name)

    # Required + type check
    if not media_name:
        return jsonify({"error": "MediaName is required and must be a valid string"}), 400
    if not isinstance(media_name, str):
        return jsonify({"error": "MediaName must be a string"}), 400

    # Length limit
    if len(media_name) > 100:
        return jsonify({"error": "MediaName too long (max 100 characters)"}), 400

    # ASCII only
    if not media_name.isascii():
        return jsonify({"error": "MediaName must contain only ASCII characters"}), 400

    # SQL keyword block
    if any(bad in media_name.lower() for bad in [";", "--", "drop", "insert", "delete", "update"]):
        return jsonify({"error": "MediaName contains potentially dangerous content"}), 400

    # HTML/script block
    if any(threat in media_name.lower() for threat in ["<script", "<img", "<svg", "onerror", "onload", "javascript:"]):
        return jsonify({"error": "MediaName contains disallowed HTML or script tags"}), 400

    # Normalize casing
    media_name = media_name.lower()

    cursor = db.cursor()

    try:
        # Duplicate check
        cursor.execute("SELECT * FROM SocialMedia WHERE MediaName = %s", (media_name,))
        if cursor.fetchone():
            return jsonify({"error": "This social media platform already exists"}), 400

        cursor.execute("INSERT INTO SocialMedia (MediaName) VALUES (%s)", (media_name,))
        db.commit()
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify({"status": "success", "media": media_name}), 201


@app.route("/add-analysisresult", methods=["POST", "OPTIONS"])
def add_analysisresult():
    if request.method == "OPTIONS":
        response = jsonify({'message': 'CORS preflight successful'})
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response

    data = request.get_json()

    project_name = data.get("ProjectName")
    post_id = data.get("PostID")
    field_name = data.get("FieldName")
    field_value = data.get("FieldValue")

    if not all([project_name, post_id, field_name, field_value]):
        return jsonify({"error": "All fields (ProjectName, PostID, FieldName, FieldValue) are required."}), 400

    cursor = db.cursor()

    try:
        cursor.execute("""
            INSERT INTO AnalysisResult (ProjectName, PostID, FieldName, FieldValue)
            VALUES (%s, %s, %s, %s)
        """, (project_name, post_id, field_name, field_value))
        db.commit()
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500

    return jsonify({"status": "success"}), 201


if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(host="0.0.0.0", port=5050, debug=True)
