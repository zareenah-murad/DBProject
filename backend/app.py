from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
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

from flask import request, jsonify
import re

@app.route("/add-user", methods=["POST", "OPTIONS"])
def add_user():
    if request.method == "OPTIONS":
        response = jsonify({'message': 'CORS preflight successful'})
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response

    data = request.get_json()
    print("DEBUG: Received data =", data)

    def clean_str(value):
        if not isinstance(value, str):
            return None
        return " ".join(value.strip().split())

    username = clean_str(data.get("username"))
    media_name = clean_str(data.get("mediaName"))
    first_name = clean_str(data.get("firstName"))
    last_name = clean_str(data.get("lastName"))
    birth_country = clean_str(data.get("birthCountry"))
    residence_country = clean_str(data.get("residenceCountry"))
    gender = clean_str(data.get("gender"))
    is_verified = 1 if data.get("isVerified") else 0

    print(f"DEBUG: Cleaned values -> userID: {user_id}, username: {username}, media: {media_name}")

    try:
        age = int(data["age"]) if data.get("age") not in ('', None) else None
        if age is not None and (age < 0 or age > 120):
            raise ValueError
    except ValueError:
        print("ERROR: Invalid age format or range.")
        return jsonify({"error": "Age must be a number between 0 and 120"}), 400

    if not all([username, media_name]):
        print("ERROR: One or more required fields are missing.")
        return jsonify({"error": "Missing required fields (username, mediaName)"}), 400

    sql_keywords = [";", "--", "drop", "insert", "delete", "update"]
    html_threats = ["<script", "<img", "<svg", "onerror", "onload", "javascript:"]
    for value in [username, media_name]:
        if any(bad in value.lower() for bad in sql_keywords):
            print(f"ERROR: SQL keyword detected in: {value}")
            return jsonify({"error": "Input contains potentially dangerous content"}), 400
        if any(threat in value.lower() for threat in html_threats):
            print(f"ERROR: HTML/script detected in: {value}")
            return jsonify({"error": "Input contains disallowed HTML or script tags"}), 400
        if not value.isascii():
            print(f"ERROR: Non-ASCII characters found in: {value}")
            return jsonify({"error": "Fields must contain only ASCII characters"}), 400
    
    if not re.match(r"^[A-Za-z0-9_.-]{1,50}$", username):
        return jsonify({"error": "Invalid username format (letters, numbers, underscore, period, dash)"}), 400
    if not re.match(r"^[A-Za-z0-9\s]{1,100}$", media_name):
        return jsonify({"error": "Invalid mediaName format (alphanumeric + space)"}), 400
    
    name_pattern = r"^[A-Za-z\s\-']{1,50}$"  # Allows letters, spaces, hyphens, apostrophes
    for field_name, value in {"firstName": first_name, "lastName": last_name}.items():
        if value:
            if not re.fullmatch(name_pattern, value):
                print(f"ERROR: Invalid {field_name}: {value}")
                return jsonify({
                    "error": f"{field_name} must only contain letters, spaces, hyphens, or apostrophes (1–50 characters)"
                }), 400
            if not value.isascii():
                print(f"ERROR: Non-ASCII in {field_name}: {value}")
                return jsonify({
                    "error": f"{field_name} must contain only ASCII characters"
                }), 400

    cursor = db.cursor()

    try:
        cursor.execute("SELECT 1 FROM SocialMedia WHERE MediaName = %s", (media_name,))
        if cursor.fetchone() is None:
            return jsonify({"error": "MediaName does not exist in SocialMedia table"}), 400
    except Exception as e:
        print("ERROR checking SocialMedia:", str(e))
        return jsonify({"error": "Internal error validating SocialMedia"}), 500

    # Platform-specific username check
    try:
        cursor.execute("SELECT 1 FROM Users WHERE Username = %s AND MediaName = %s", (username, media_name))
        if cursor.fetchone():
            return jsonify({"error": "A user with this username already exists on this media platform."}), 400
    except Exception as e:
        print("ERROR checking for duplicate username:", str(e))
        return jsonify({"error": "Internal error checking username duplication"}), 500

    try:
        cursor.execute("""
            INSERT INTO Users (Username, MediaName, FirstName, LastName,
                       BirthCountry, ResidenceCountry, Age, Gender, IsVerified)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (username, media_name, first_name, last_name,
            birth_country, residence_country, age, gender, is_verified))
        
        db.commit()
        user_id = cursor.lastrowid

    except Exception as e:
        db.rollback()
        error_message = str(e)
        if "Duplicate entry" in error_message and "PRIMARY" in error_message:
            return jsonify({"error": "A user with this User ID already exists. Please use a unique ID."}), 400
        if "foreign key constraint" in error_message.lower():
            return jsonify({"error": "The media platform does not exist. Please check Media Name."}), 400
        return jsonify({"error": "An unexpected database error occurred. Please try again."}), 500

    print("DEBUG: User inserted successfully.")
    return jsonify({"status": "success", "userID": user_id}), 201


@app.route("/add-project", methods=["POST", "OPTIONS"])
def add_project():
    if request.method == "OPTIONS":
        response = jsonify({'message': 'CORS preflight successful'})
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response

    data = request.get_json()
    print("DEBUG: Received data =", data)

    def clean_str(value):
        if not isinstance(value, str):
            return None
        return " ".join(value.strip().split())

    project_name = clean_str(data.get("projectName"))
    manager_first = clean_str(data.get("managerFirstName"))
    manager_last = clean_str(data.get("managerLastName"))
    institute_name = clean_str(data.get("instituteName"))
    start_date = clean_str(data.get("startDate"))
    end_date = clean_str(data.get("endDate"))

    print(f"DEBUG: Cleaned values -> project: {project_name}, manager: {manager_first} {manager_last}, institute: {institute_name}, start: {start_date}, end: {end_date}")

    # Required check
    if not all([project_name, manager_first, manager_last, institute_name, start_date, end_date]):
        print("ERROR: One or more required fields are missing.")
        return jsonify({"error": "One or more fields are missing or of the wrong type"}), 400
    
    project_name = project_name.lower()

    # SQL injection check
    sql_keywords = [";", "--", "drop", "insert", "delete", "update"]
    for value in [project_name, manager_first, manager_last, institute_name]:
        if isinstance(value, str) and any(bad in value.lower() for bad in sql_keywords):
            print(f"ERROR: Input contains SQL-style keyword: {value}")
            return jsonify({"error": "Input contains potentially dangerous content"}), 400

    # HTML threat check
    html_threats = ["<script", "<img", "<svg", "onerror", "onload", "javascript:"]
    for value in [project_name, manager_first, manager_last, institute_name]:
        if any(threat in value.lower() for threat in html_threats):
            print(f"ERROR: Input contains HTML/script threat: {value}")
            return jsonify({"error": "Input contains disallowed HTML or script tags"}), 400

    # ASCII check
    for value in [project_name, manager_first, manager_last, institute_name]:
        if not value.isascii():
            print(f"ERROR: Non-ASCII characters found in: {value}")
            return jsonify({"error": "Fields must contain only ASCII characters"}), 400

    # Type check
    if not all(isinstance(f, str) for f in [project_name, manager_first, manager_last, institute_name, start_date, end_date]):
        print("ERROR: One or more fields are not strings.")
        return jsonify({"error": "All fields must be strings in valid format"}), 400

    # Length checks
    if len(project_name) > 100:
        print("ERROR: ProjectName too long.")
        return jsonify({"error": "ProjectName too long (max 100 characters)"}), 400
    if len(manager_first) > 100 or len(manager_last) > 100:
        print("ERROR: Manager name too long.")
        return jsonify({"error": "Manager name too long (max 100 characters)"}), 400
    if len(institute_name) > 150:
        print("ERROR: InstituteName too long.")
        return jsonify({"error": "InstituteName too long (max 150 characters)"}), 400

    # Date validation
    from datetime import datetime
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        if end < start:
            print("ERROR: End date is before start date.")
            return jsonify({"error": "EndDate must be after or equal to StartDate"}), 400
    except ValueError:
        print("ERROR: Date format is invalid.")
        return jsonify({"error": "Dates must be in YYYY-MM-DD format"}), 400

    cursor = db.cursor()

    try:
        # Check for duplicate project
        cursor.execute("SELECT * FROM Project WHERE ProjectName = %s", (project_name,))
        if cursor.fetchone():
            print(f"ERROR: Project '{project_name}' already exists.")
            return jsonify({"error": "A project with this name already exists"}), 400

        # Check if institute exists
        cursor.execute("SELECT * FROM Institute WHERE InstituteName = %s", (institute_name,))
        if cursor.fetchone() is None:
            print(f"ERROR: Institute '{institute_name}' does not exist.")
            return jsonify({"error": "Institute does not exist"}), 400

        # Insert
        cursor.execute("""
            INSERT INTO Project (ProjectName, ManagerFirstName, ManagerLastName, InstituteName, StartDate, EndDate)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (project_name, manager_first, manager_last, institute_name, start_date, end_date))
        db.commit()
    except Exception as e:
        print("ERROR (DB Exception):", str(e))
        db.rollback()
        return jsonify({"error": str(e)}), 500

    print(f"SUCCESS: Project '{project_name}' added for institute '{institute_name}'.")
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
    print("DEBUG: Received data =", data)

    institute_name = data.get("instituteName")
    if institute_name is None:
        print("ERROR: 'instituteName' key is missing from request body.")
    else:
        print(f"DEBUG: Raw instituteName input = '{institute_name}'")

    # Clean and normalize
    def clean_str(value):
        if not isinstance(value, str):
            return None
        return " ".join(value.strip().split())

    institute_name = clean_str(institute_name)

    # Check required
    if not institute_name:
        print("ERROR: instituteName is empty or invalid after cleaning.")
        return jsonify({"error": "InstituteName is required and must be a valid string"}), 400

    # Check type
    if not isinstance(institute_name, str):
        print("ERROR: instituteName is not a string.")
        return jsonify({"error": "InstituteName must be a string"}), 400

    # Length check
    if len(institute_name) > 150:
        print(f"ERROR: instituteName too long ({len(institute_name)} characters).")
        return jsonify({"error": "InstituteName too long (max 150 characters)"}), 400

    # ASCII-only check
    if not institute_name.isascii():
        print("ERROR: instituteName contains non-ASCII characters.")
        return jsonify({"error": "InstituteName must contain only ASCII characters"}), 400

    # Dangerous keywords (SQL-style)
    if any(bad in institute_name.lower() for bad in [";", "--", "drop", "insert", "delete", "update"]):
        print("ERROR: instituteName contains SQL-like patterns.")
        return jsonify({"error": "InstituteName contains potentially dangerous content"}), 400

    # HTML/script injection
    if any(threat in institute_name.lower() for threat in ["<script", "<img", "<svg", "onerror", "onload", "javascript:"]):
        print("ERROR: instituteName contains disallowed HTML or script tags.")
        return jsonify({"error": "InstituteName contains disallowed HTML or script tags"}), 400

    # Normalize casing (optional)
    institute_name = institute_name.lower()

    cursor = db.cursor()

    try:
        # Check for duplicates
        cursor.execute("SELECT * FROM Institute WHERE InstituteName = %s", (institute_name,))
        if cursor.fetchone():
            print("ERROR: Duplicate institute name already exists in database.")
            return jsonify({"error": "An institute with this name already exists"}), 400

        cursor.execute("INSERT INTO Institute (InstituteName) VALUES (%s)", (institute_name,))
        db.commit()
    except Exception as e:
        print("ERROR (DB Exception):", str(e))
        db.rollback()
        return jsonify({"error": str(e)}), 500

    print("SUCCESS: Institute added =", institute_name)
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
    print("DEBUG: Received data =", data)

    raw_project_name = data.get("projectName")
    raw_field_name = data.get("fieldName")

    if raw_project_name is None:
        print("ERROR: 'projectName' key missing from request.")
    if raw_field_name is None:
        print("ERROR: 'fieldName' key missing from request.")
    else:
        print(f"DEBUG: Raw projectName = '{raw_project_name}', fieldName = '{raw_field_name}'")

    # Type check FIRST
    if not isinstance(raw_project_name, str) or not isinstance(raw_field_name, str):
        print("ERROR: One or both inputs are not strings.")
        return jsonify({"error": "Both fields must be strings"}), 400

    # Now clean
    def clean_str(value):
        return " ".join(value.strip().split())

    project_name = clean_str(raw_project_name)
    field_name = clean_str(raw_field_name)

    # Then required check
    if not project_name or not field_name:
        print("ERROR: Either projectName or fieldName is empty after cleaning.")
        return jsonify({"error": "ProjectName and FieldName are required"}), 400

    # Type check (redundant but consistent with pattern)
    if not isinstance(project_name, str) or not isinstance(field_name, str):
        print("ERROR: Type check failed post-cleaning.")
        return jsonify({"error": "Both fields must be strings"}), 400

    # Length check
    if len(project_name) > 100 or len(field_name) > 100:
        print("ERROR: Length check failed.")
        return jsonify({"error": "FieldName and ProjectName must be <= 100 characters"}), 400

    # ASCII-only check
    if not project_name.isascii() or not field_name.isascii():
        print("ERROR: Non-ASCII characters detected.")
        return jsonify({"error": "Inputs must contain only ASCII characters"}), 400

    # SQL-style junk check
    if any(bad in field_name.lower() for bad in [";", "--", "drop", "insert", "delete", "update"]):
        print("ERROR: SQL-style keyword detected in fieldName.")
        return jsonify({"error": "FieldName contains potentially dangerous content"}), 400

    # Script tag / HTML threat check
    if any(tag in field_name.lower() for tag in ["<script", "<img", "<svg", "onerror", "onload", "javascript:"]):
        print("ERROR: HTML/script content detected in fieldName.")
        return jsonify({"error": "FieldName contains disallowed HTML or script tags"}), 400

    # Normalize case (optional)
    field_name = field_name.lower()

    cursor = db.cursor()

    try:
        # Check that project exists
        cursor.execute("SELECT * FROM Project WHERE ProjectName = %s", (project_name,))
        if cursor.fetchone() is None:
            print(f"ERROR: Project '{project_name}' does not exist.")
            return jsonify({"error": "Project does not exist"}), 400

        # Check for duplicate field in the same project
        cursor.execute("""
            SELECT * FROM Field WHERE ProjectName = %s AND FieldName = %s
        """, (project_name, field_name))
        if cursor.fetchone():
            print("ERROR: Field already exists in this project.")
            return jsonify({"error": "Field already exists in this project"}), 400

        # Insert the field
        cursor.execute("""
            INSERT INTO Field (ProjectName, FieldName)
            VALUES (%s, %s)
        """, (project_name, field_name))
        db.commit()
    except Exception as e:
        print("ERROR (DB Exception):", str(e))
        db.rollback()
        return jsonify({"error": str(e)}), 500

    print("SUCCESS: Field added to project =", project_name, "| Field =", field_name)
    return jsonify({"status": "success", "field": field_name}), 201


from flask import request, jsonify
import re
from datetime import datetime

@app.route("/add-post", methods=["POST", "OPTIONS"])
def add_post():
    if request.method == "OPTIONS":
        response = jsonify({'message': 'CORS preflight successful'})
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response

    data = request.get_json(force=True)
    print("DEBUG: Received data:", data)

    # Required fields
    post_id = data.get("PostID")
    user_id = data.get("UserID")
    post_text = data.get("PostText")
    post_datetime = data.get("PostDateTime")

    if not all([post_id, user_id, post_text, post_datetime]):
        print("ERROR: Missing required fields")
        return jsonify({"error": "Missing required fields (PostID, UserID, PostText, PostDateTime)"}), 400

    if not re.match(r"^[A-Za-z0-9_-]{1,50}$", post_id):
        print("ERROR: Invalid PostID format")
        return jsonify({"error": "Invalid PostID format (letters, numbers, dashes, underscores only)"}), 400

    if not re.match(r"^[A-Za-z0-9_-]{1,50}$", user_id):
        print("ERROR: Invalid UserID format")
        return jsonify({"error": "Invalid UserID format (letters, numbers, dashes, underscores only)"}), 400

    try:
        datetime.fromisoformat(post_datetime)
    except ValueError:
        print("ERROR: Invalid PostDateTime format")
        return jsonify({"error": "Invalid PostDateTime format. Must be ISO format (YYYY-MM-DDTHH:MM:SS)"}), 400

    reposted_by_user_id = data.get("RepostedByUserID") or None
    repost_datetime = data.get("RepostDateTime") or None
    if repost_datetime:
        try:
            datetime.fromisoformat(repost_datetime)
        except ValueError:
            print("ERROR: Invalid RepostTime format")
            return jsonify({"error": "Invalid RepostDateTime format. Must be ISO format"}), 400

    city = data.get("City") or None
    state = data.get("State") or None
    country = data.get("Country") or None

    try:
        likes = int(data["Likes"]) if data.get("Likes") not in ('', None) else None
        if likes is not None and likes < 0:
            raise ValueError
    except ValueError:
        print("ERROR: Likes must be a non-negative integer")
        return jsonify({"error": "Likes must be a non-negative integer"}), 400

    try:
        dislikes = int(data["Dislikes"]) if data.get("Dislikes") not in ('', None) else None
        if dislikes is not None and dislikes < 0:
            raise ValueError
    except ValueError:
        print("ERROR: Dislikes must be a non-negative integer")
        return jsonify({"error": "Dislikes must be a non-negative integer"}), 400

    has_multimedia = 1 if data.get("HasMultimedia") else 0

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
        error_message = str(e)
        print("ERROR (DB Exception):", error_message)

        if "Duplicate entry" in error_message and "PRIMARY" in error_message:
            return jsonify({"error": "A post with this ID already exists. Please use a unique PostID."}), 400

        if "foreign key constraint" in error_message.lower():
            return jsonify({"error": "The UserID or RepostedByUserID does not exist in the Users table."}), 400

        return jsonify({"error": "An unexpected database error occurred. Please try again."}), 500

    print("DEBUG: Post inserted successfully.")
    return jsonify({"status": "success", "post_id": post_id}), 201


@app.route('/update/repost', methods=['POST'])
def mark_post_as_repost():
    data = request.json
    post_id = data.get('postID')
    reposted_by_user_id = data.get('repostedByUserID')
    repost_time = data.get('repostTime')

    if not post_id or not reposted_by_user_id or not repost_time:
        return jsonify({'error': 'postID, repostedByUserID, and repostTime are required.'}), 400

    try:
        cursor = db.cursor()

        # Make sure the post exists
        cursor.execute("SELECT 1 FROM Posts WHERE PostID = %s", (post_id,))
        if cursor.fetchone() is None:
            return jsonify({'error': f'No post found with PostID {post_id}'}), 404

        # Make sure the reposting user exists
        cursor.execute("SELECT 1 FROM Users WHERE UserID = %s", (reposted_by_user_id,))
        if cursor.fetchone() is None:
            return jsonify({'error': f'No user found with UserID {reposted_by_user_id}'}), 404

        # Perform the update
        cursor.execute("""
            UPDATE Posts
            SET RepostedByUserID = %s, RepostTime = %s
            WHERE PostID = %s
        """, (reposted_by_user_id, repost_time, post_id))
        db.commit()

        return jsonify({'message': f'Post {post_id} successfully marked as reposted.'}), 200

    except Exception as e:
        print("ERROR in mark_post_as_repost:", e)
        return jsonify({'error': 'An error occurred while updating the post.'}), 500


@app.route("/add-socialmedia", methods=["POST", "OPTIONS"])
def add_socialmedia():
    if request.method == "OPTIONS":
        response = jsonify({'message': 'CORS preflight successful'})
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response

    data = request.get_json()
    print("DEBUG: Received data =", data)

    media_name = data.get("mediaName")
    if media_name is None:
        print("ERROR: 'MediaName' key is missing from request body.")
    else:
        print(f"DEBUG: Raw MediaName input = '{media_name}'")

    def clean_str(value):
        if not isinstance(value, str):
            return None
        return " ".join(value.strip().split())

    media_name = clean_str(media_name)

    if not media_name:
        print("ERROR: MediaName is empty or invalid after cleaning.")
        return jsonify({"error": "MediaName is required and must be a valid string"}), 400
    if len(media_name) > 100:
        print(f"ERROR: MediaName too long ({len(media_name)} characters).")
        return jsonify({"error": "MediaName too long (max 100 characters)"}), 400
    if not media_name.isascii():
        print("ERROR: MediaName contains non-ASCII characters.")
        return jsonify({"error": "MediaName must contain only ASCII characters"}), 400
    if any(bad in media_name.lower() for bad in [";", "--", "drop", "insert", "delete", "update"]):
        print("ERROR: MediaName contains SQL-like patterns.")
        return jsonify({"error": "MediaName contains potentially dangerous content"}), 400
    if any(threat in media_name.lower() for threat in ["<script", "<img", "<svg", "onerror", "onload", "javascript:"]):
        print("ERROR: MediaName contains HTML/script threats.")
        return jsonify({"error": "MediaName contains disallowed HTML or script tags"}), 400

    media_name = media_name.lower()

    cursor = db.cursor()

    try:
        cursor.execute("SELECT * FROM SocialMedia WHERE MediaName = %s", (media_name,))
        if cursor.fetchone():
            print("ERROR: Duplicate MediaName already exists in database.")
            return jsonify({"error": "This social media platform already exists"}), 400

        cursor.execute("INSERT INTO SocialMedia (MediaName) VALUES (%s)", (media_name,))
        db.commit()
    except Exception as e:
        print("ERROR (DB Exception):", str(e))
        db.rollback()
        return jsonify({"error": str(e)}), 500

    print("SUCCESS: MediaName added =", media_name)
    return jsonify({"status": "success", "media": media_name}), 201


from flask import request, jsonify
import re

@app.route("/add-analysisresult", methods=["POST", "OPTIONS"])
def add_analysisresult():
    if request.method == "OPTIONS":
        response = jsonify({'message': 'CORS preflight successful'})
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response

    data = request.get_json(force=True)
    print("DEBUG: Received data:", data)

    project_name = data.get("ProjectName")
    post_id = data.get("PostID")
    field_name = data.get("FieldName")
    field_value = data.get("FieldValue")

    if not all([project_name, post_id, field_name, field_value]):
        print("ERROR: Missing required fields.")
        return jsonify({"error": "All fields (ProjectName, PostID, FieldName, FieldValue) are required."}), 400

    if not re.match(r"^[A-Za-z0-9_\- ]{1,100}$", project_name):
        print(f"ERROR: Invalid ProjectName format: '{project_name}'")
        return jsonify({"error": "Invalid ProjectName format."}), 400
    if not re.match(r"^[A-Za-z0-9_\-]{1,50}$", post_id):
        print(f"ERROR: Invalid PostID format: '{post_id}'")
        return jsonify({"error": "Invalid PostID format."}), 400
    if not re.match(r"^[A-Za-z0-9_\- ]{1,100}$", field_name):
        print(f"ERROR: Invalid FieldName format: '{field_name}'")
        return jsonify({"error": "Invalid FieldName format."}), 400
    if not isinstance(field_value, str) or len(field_value.strip()) == 0:
        print(f"ERROR: Invalid FieldValue: '{field_value}'")
        return jsonify({"error": "FieldValue must be a non-empty string."}), 400

    cursor = db.cursor()
    try:
        cursor.execute("""
            INSERT INTO AnalysisResult (ProjectName, PostID, FieldName, FieldValue)
            VALUES (%s, %s, %s, %s)
        """, (project_name.strip(), post_id.strip(), field_name.strip(), field_value.strip()))
        db.commit()
    except Exception as e:
        db.rollback()
        error_message = str(e)
        print("ERROR (DB Exception):", error_message)

        if "duplicate entry" in error_message.lower() and "analysisresult.PRIMARY" in error_message:
            return jsonify({"error": "This analysis result already exists for the given project, post, and field."}), 400

        if "foreign key constraint fails" in error_message.lower():
            if "ProjectName" in error_message:
                return jsonify({"error": "Project name does not exist. Please make sure the project is added first."}), 400
            elif "PostID" in error_message:
                return jsonify({"error": "Post ID does not exist. Please add the post before assigning analysis results."}), 400

        return jsonify({"error": f"Database error: {error_message}"}), 500

    print("DEBUG: AnalysisResult inserted successfully.")
    return jsonify({"status": "success"}), 201


@app.route("/add-used-in", methods=["POST", "OPTIONS"])
def add_used_in():
    if request.method == "OPTIONS":
        response = jsonify({'message': 'CORS preflight successful'})
        response.headers.add("Access-Control-Allow-Origin", "http://localhost:3000")
        response.headers.add("Access-Control-Allow-Headers", "Content-Type")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response

    data = request.get_json()
    project = data.get("projectName")
    post = data.get("postID")

    if not project or not post:
        return jsonify({"error": "Both projectName and postID are required."}), 400

    cursor = db.cursor()
    try:
        # Validate project and post existence
        cursor.execute("SELECT 1 FROM Project WHERE ProjectName = %s", (project,))
        if cursor.fetchone() is None:
            return jsonify({"error": "Project does not exist."}), 400

        cursor.execute("SELECT 1 FROM Posts WHERE PostID = %s", (post,))
        if cursor.fetchone() is None:
            return jsonify({"error": "Post does not exist."}), 400

        # Check if already used
        cursor.execute("SELECT 1 FROM Used_In WHERE ProjectName = %s AND PostID = %s", (project, post))
        if cursor.fetchone():
            return jsonify({"error": "This post is already used in this project."}), 400

        # Insert
        cursor.execute("INSERT INTO Used_In (ProjectName, PostID) VALUES (%s, %s)", (project, post))
        db.commit()
    except Exception as e:
        db.rollback()
        return jsonify({"error": f"Database error: {str(e)}"}), 500

    return jsonify({"status": "success"}), 201


@app.route("/query/posts-by-media", methods=["GET"])
def query_posts_by_media():
    media_name = request.args.get("mediaName")

    if not media_name:
        print("ERROR: mediaName parameter is missing.")
        return jsonify({"error": "Please provide a mediaName in the query."}), 400

    cursor = db.cursor()

    try:
        # Check if media exists
        cursor.execute("SELECT 1 FROM SocialMedia WHERE MediaName = %s", (media_name,))
        if cursor.fetchone() is None:
            print(f"ERROR: Media '{media_name}' does not exist in the SocialMedia table.")
            return jsonify({"error": f"The media platform '{media_name}' does not exist."}), 404

        # Query posts
        cursor.execute("""
            SELECT p.PostID, u.Username, p.PostText AS Content, p.PostDateTime,
                GROUP_CONCAT(ui.ProjectName) AS Projects
            FROM Posts p
            JOIN Users u ON p.UserID = u.UserID
            LEFT JOIN Used_In ui ON p.PostID = ui.PostID
            WHERE u.MediaName = %s
            GROUP BY p.PostID
            ORDER BY p.PostDateTime DESC

        """, (media_name,))
        rows = cursor.fetchall()

        results = [
        {
            "postID": row[0],
            "username": row[1],
            "content": row[2],
            "postDateTime": row[3].isoformat() if row[3] else None,
            "projects": row[4].split(',') if row[4] else []
        }
        for row in rows
    ]


        print(f"DEBUG: Found {len(results)} posts for {media_name}")
        return jsonify(results), 200

    except Exception as e:
        print("ERROR during query_posts_by_media:", str(e))
        return jsonify({"error": "Something went wrong while fetching posts."}), 500

@app.route("/query/posts-by-time", methods=["GET"])
def query_posts_by_time():
    try:
        start = request.args.get("start")
        end = request.args.get("end")

        if not start or not end:
            return jsonify({"error": "Start and end datetime are required."}), 400

        try:
            start_dt = datetime.fromisoformat(start)
            end_dt = datetime.fromisoformat(end)
        except ValueError:
            return jsonify({"error": "Invalid datetime format. Use ISO format like 2025-05-03T14:00"}), 400

        if end_dt < start_dt:
            return jsonify({"error": "End time must be after start time."}), 400

        cursor = db.cursor()
        cursor.execute("""
            SELECT p.PostID, u.Username, p.PostText AS content, p.PostDateTime,
                GROUP_CONCAT(ui.ProjectName) AS Projects
            FROM Posts p
            JOIN Users u ON p.UserID = u.UserID
            LEFT JOIN Used_In ui ON p.PostID = ui.PostID
            WHERE p.PostDateTime BETWEEN %s AND %s
            GROUP BY p.PostID
            ORDER BY p.PostDateTime DESC

        """, (start_dt, end_dt))

        results = [
            {
                'postID': r[0],
                'username': r[1],
                'content': r[2],
                'postDateTime': r[3].isoformat() if r[3] else None,
                'projects': r[4].split(',') if r[4] else []
            }
            for r in cursor.fetchall()
        ]

        return jsonify(results)

    except Exception as e:
        print("ERROR during query_posts_by_time:", e)
        return jsonify({"error": "An unexpected error occurred while fetching posts."}), 500


@app.route('/query/posts-by-username', methods=['GET'])
def query_posts_by_username():
    username = request.args.get('username')
    media_name = request.args.get('mediaName')

    if not username or not media_name:
        return jsonify({'error': 'Username and media name are required.'}), 400

    try:
        cursor = db.cursor()

        # Validate user exists first
        cursor.execute("""
            SELECT UserID FROM Users 
            WHERE Username = %s AND MediaName = %s
        """, (username, media_name))
        user_result = cursor.fetchone()
        if not user_result:
            return jsonify({'error': 'No user found with that username on the specified platform.'}), 404

        user_id = user_result[0]

        # Now fetch their posts
        cursor.execute("""
            SELECT p.PostID, p.PostText, p.PostDateTime, GROUP_CONCAT(ui.ProjectName)
            FROM Posts p
            LEFT JOIN Used_In ui ON p.PostID = ui.PostID
            WHERE p.UserID = %s
            GROUP BY p.PostID
            ORDER BY p.PostDateTime DESC
        """, (user_id,))

        posts = cursor.fetchall()
        result = [
            {
                'postID': row[0],
                'username': username,
                'mediaName': media_name,
                'content': row[1],
                'postDateTime': row[2].isoformat() if row[2] else None,
                'projects': row[3].split(',') if row[3] else []
            }
            for row in posts
        ]

        return jsonify(result), 200
    except Exception as e:
        print('ERROR during query_posts_by_username:', e)
        return jsonify({'error': 'Internal server error'}), 500

@app.route("/query/posts-by-name", methods=["GET"])
def query_posts_by_name():
    first = request.args.get("firstName", "").strip()
    last = request.args.get("lastName", "").strip()

    if not first and not last:
        return jsonify({"error": "Please enter at least first name or last name."}), 400

    try:
        cursor = db.cursor()

        # Build query dynamically based on what's provided
        conditions = []
        values = []

        if first:
            conditions.append("LOWER(u.FirstName) = LOWER(%s)")
            values.append(first)
        if last:
            conditions.append("LOWER(u.LastName) = LOWER(%s)")
            values.append(last)

        where_clause = " AND ".join(conditions)

        query = f"""
            SELECT p.PostID, u.Username, u.FirstName, u.LastName, p.PostText, p.PostDateTime,
                GROUP_CONCAT(ui.ProjectName) AS Projects
            FROM Users u
            JOIN Posts p ON u.UserID = p.UserID
            LEFT JOIN Used_In ui ON p.PostID = ui.PostID
            WHERE {where_clause}
            GROUP BY p.PostID
            ORDER BY p.PostDateTime DESC
        """

        cursor.execute(query, values)
        rows = cursor.fetchall()

        results = [
            {
                'postID': row[0],
                'username': row[1],
                'firstName': row[2],
                'lastName': row[3],
                'content': row[4],
                'postDateTime': row[5].isoformat() if row[5] else None,
                'projects': row[6].split(',') if row[6] else []
            }
            for row in rows
        ]

        return jsonify(results), 200
    except Exception as e:
        print("ERROR during query_posts_by_name:", e)
        return jsonify({"error": "An internal error occurred while fetching posts."}), 500


@app.route('/query/experiment-results', methods=['GET'])
def query_experiment_results():
    project_name = request.args.get('projectName')

    if not project_name:
        return jsonify({'error': 'Project name is required.'}), 400

    try:
        cursor = db.cursor()

        # Confirm the project exists
        cursor.execute("SELECT 1 FROM Project WHERE ProjectName = %s", (project_name,))
        if cursor.fetchone() is None:
            return jsonify({'error': 'No project found with that name.'}), 404

        # Fetch associated posts
        cursor.execute("""
            SELECT p.PostID, u.Username, u.FirstName, u.LastName, p.PostText, p.PostDateTime
            FROM Used_In ui
            JOIN Posts p ON ui.PostID = p.PostID
            JOIN Users u ON p.UserID = u.UserID
            WHERE ui.ProjectName = %s
            ORDER BY p.PostDateTime DESC
        """, (project_name,))
        post_rows = cursor.fetchall()

        post_map = {}
        for row in post_rows:
            post_map[row[0]] = {
                'postID': row[0],
                'username': row[1],
                'firstName': row[2],
                'lastName': row[3],
                'content': row[4],
                'postDateTime': row[5].isoformat() if row[5] else None,
                'analysis': []
            }

        # Fetch analysis results
        cursor.execute("""
            SELECT PostID, FieldName, FieldValue
            FROM AnalysisResult
            WHERE ProjectName = %s
        """, (project_name,))
        analysis_rows = cursor.fetchall()

        field_coverage = {}
        post_count = len(post_map)

        for row in analysis_rows:
            post_id, field_name, field_value = row

            if post_id in post_map:
                post_map[post_id]['analysis'].append({
                    'field': field_name,
                    'value': field_value
                })

            # Count field occurrences for coverage
            if field_name not in field_coverage:
                field_coverage[field_name] = set()
            field_coverage[field_name].add(post_id)

        # Convert field_coverage sets to percentages
        field_coverage_percent = {
            field: len(post_ids) / post_count
            for field, post_ids in field_coverage.items()
        }

        return jsonify({
            'posts': list(post_map.values()),
            'fieldCoverage': field_coverage_percent
        }), 200

    except Exception as e:
        print("ERROR during query_experiment_results:", e)
        return jsonify({'error': 'An unexpected error occurred while fetching results.'}), 500


@app.route('/query/posts-by-project', methods=['GET'])
def query_posts_by_project():
    project_name = request.args.get('projectName')

    if not project_name:
        return jsonify({'error': 'Project name is required.'}), 400

    try:
        cursor = db.cursor()

        # Validate project exists
        cursor.execute("SELECT 1 FROM Project WHERE ProjectName = %s", (project_name,))
        if cursor.fetchone() is None:
            return jsonify({'error': 'No project found with that name.'}), 404

        # Fetch associated posts
        cursor.execute("""
            SELECT p.PostID, u.Username, u.MediaName, p.PostText, p.PostDateTime
            FROM Used_In ui
            JOIN Posts p ON ui.PostID = p.PostID
            JOIN Users u ON p.UserID = u.UserID
            WHERE ui.ProjectName = %s
            ORDER BY p.PostDateTime DESC
        """, (project_name,))

        rows = cursor.fetchall()
        results = [
            {
                'postID': r[0],
                'username': r[1],
                'mediaName': r[2],
                'content': r[3],
                'postDateTime': r[4].isoformat() if r[4] else None
            }
            for r in rows
        ]

        return jsonify(results), 200

    except Exception as e:
        print("ERROR during query_posts_by_project:", e)
        return jsonify({'error': 'An error occurred while fetching posts for the project.'}), 500


if __name__ == '__main__':
    print("Starting Flask app...")
    app.run(host="0.0.0.0", port=5050, debug=True)
