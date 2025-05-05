def test_add_valid_socialmedia(client):
    response = client.post("/add-socialmedia", json={"mediaName": "XPlatform"})
    assert response.status_code == 201
    assert response.json["status"] == "success"

def test_add_duplicate_socialmedia(client):
    client.post("/add-socialmedia", json={"mediaName": "DuplicateMedia"})
    response = client.post("/add-socialmedia", json={"mediaName": "DuplicateMedia"})
    assert response.status_code == 400
    assert "already exists" in response.json["error"]

def test_add_socialmedia_missing_field(client):
    response = client.post("/add-socialmedia", json={})
    assert response.status_code == 400
    assert "MediaName is required" in response.json["error"]

def test_add_socialmedia_empty_name(client):
    response = client.post("/add-socialmedia", json={"mediaName": ""})
    assert response.status_code == 400
    assert "MediaName is required" in response.json["error"]

def test_add_socialmedia_long_name(client):
    long_name = "A" * 101  # Exceeds the 100-character limit
    response = client.post("/add-socialmedia", json={"mediaName": long_name})
    assert response.status_code == 400
    assert "MediaName too long" in response.json["error"]

def test_add_socialmedia_non_ascii_name(client):
    response = client.post("/add-socialmedia", json={"mediaName": "MédiaÑame"})
    assert response.status_code == 400
    assert "MediaName must contain only ASCII characters" in response.json["error"]

def test_add_socialmedia_sql_injection_attempt(client):
    response = client.post("/add-socialmedia", json={"mediaName": "DROP TABLE SocialMedia;"})
    assert response.status_code == 400
    assert "MediaName contains potentially dangerous content" in response.json["error"]

def test_add_socialmedia_html_injection_attempt(client):
    response = client.post("/add-socialmedia", json={"mediaName": "<script>alert('hack');</script>"})
    assert response.status_code == 400
    assert "potentially dangerous content" in response.json["error"].lower()

def test_add_socialmedia_case_insensitive_duplicate(client):
    client.post("/add-socialmedia", json={"mediaName": "TestPlatform"})
    response = client.post("/add-socialmedia", json={"mediaName": "testplatform"})  # Same name, different case
    assert response.status_code == 400
    assert "already exists" in response.json["error"]

def test_add_socialmedia_valid_edge_case(client):
    response = client.post("/add-socialmedia", json={"mediaName": "A" * 100})  # Exactly 100 characters
    assert response.status_code == 201
    assert response.json["status"] == "success"