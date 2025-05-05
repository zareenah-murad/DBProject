import re
import pytest

def test_duplicate_username_same_platform_fails(client):
    client.post("/add-socialmedia", json={"mediaName": "XNet"})
    client.post("/add-user", json={"userID": "u1", "username": "alex", "mediaName": "XNet", "age": 22})
    res = client.post("/add-user", json={"userID": "u2", "username": "alex", "mediaName": "XNet", "age": 23})
    assert res.status_code == 400
    assert "already exists" in res.json["error"]

def test_same_username_different_platform_succeeds(client):
    client.post("/add-socialmedia", json={"mediaName": "YNet"})
    res = client.post("/add-user", json={"userID": "u3", "username": "alex", "mediaName": "YNet", "age": 24})
    assert res.status_code == 201

def test_add_user_with_is_verified_flag(client):
    client.post("/add-socialmedia", json={"mediaName": "TestVerify"})
    res = client.post("/add-user", json={
        "userID": "verifyUser",
        "username": "veriuser",
        "mediaName": "TestVerify",
        "age": 25,
        "isVerified": True
    })
    assert res.status_code == 201

def test_duplicate_userid_fails(client):
    client.post("/add-socialmedia", json={"mediaName": "DupNet"})
    client.post("/add-user", json={"userID": "dupUser", "username": "first", "mediaName": "DupNet", "age": 30})
    res = client.post("/add-user", json={"userID": "dupUser", "username": "second", "mediaName": "DupNet", "age": 31})
    assert res.status_code == 400
    assert "user id already exists" in res.json["error"].lower()

def test_add_user_with_invalid_age_string(client):
    client.post("/add-socialmedia", json={"mediaName": "AgeBook"})
    res = client.post("/add-user", json={
        "userID": "uAge1",
        "username": "badage",
        "mediaName": "AgeBook",
        "age": "not-a-number"
    })
    assert res.status_code == 400
    assert "age must be a number" in res.json["error"].lower()

def test_add_user_with_out_of_bounds_age(client):
    client.post("/add-socialmedia", json={"mediaName": "AgeBook2"})

    for bad_age in [-1, 121]:
        res = client.post("/add-user", json={
            "userID": f"uBad{bad_age}",
            "username": f"user{bad_age}",
            "mediaName": "AgeBook2",
            "age": bad_age
        })
        assert res.status_code == 400
        assert "age must be a number" in res.json["error"].lower()
    
def test_add_user_missing_userid_fails(client):
    client.post("/add-socialmedia", json={"mediaName": "TestMedia1"})
    res = client.post("/add-user", json={
        # "userID" is missing
        "username": "missingID",
        "mediaName": "TestMedia1",
        "age": 25
    })
    assert res.status_code == 400
    assert "missing required fields" in res.json["error"].lower()

def test_add_user_missing_username_fails(client):
    client.post("/add-socialmedia", json={"mediaName": "TestMedia2"})
    res = client.post("/add-user", json={
        "userID": "uid_missing_username",
        # "username" is missing
        "mediaName": "TestMedia2",
        "age": 25
    })
    assert res.status_code == 400
    assert "missing required fields" in res.json["error"].lower()

def test_add_user_missing_medianame_fails(client):
    res = client.post("/add-user", json={
        "userID": "uid_missing_media",
        "username": "missingMedia",
        # "mediaName" is missing
        "age": 25
    })
    assert res.status_code == 400
    assert "missing required fields" in res.json["error"].lower()

@pytest.mark.parametrize("field, value", [
    ("userID", "u1; DROP TABLE users;"),
    ("username", "admin --"),
    ("mediaName", "XNet DELETE")
])
def test_add_user_rejects_sql_keywords(client, field, value):
    # Set up a valid base request
    payload = {
        "userID": "safeUser",
        "username": "safeName",
        "mediaName": "SafeMedia",
        "age": 25
    }
    # Replace the target field with the malicious value
    payload[field] = value

    # Ensure media platform exists if needed
    if field != "mediaName":
        client.post("/add-socialmedia", json={"mediaName": payload["mediaName"]})

    res = client.post("/add-user", json=payload)
    assert res.status_code == 400
    assert "potentially dangerous content" in res.json["error"].lower()

@pytest.mark.parametrize("field, value", [
    ("userID", "<script>alert('hacked')</script>"),
    ("username", "<img src=x onerror=alert(1)>"),
    ("mediaName", "<svg onload=alert('XSS')>")
])
def test_add_user_rejects_html_injection(client, field, value):
    # Create a valid payload
    payload = {
        "userID": "safeID",
        "username": "safeUser",
        "mediaName": "SafeMedia",
        "age": 25
    }
    # Inject malicious value
    payload[field] = value

    # Ensure the media platform exists (unless it's the test field)
    if field != "mediaName":
        client.post("/add-socialmedia", json={"mediaName": payload["mediaName"]})

    res = client.post("/add-user", json=payload)
    assert res.status_code == 400
    assert "disallowed html or script" in res.json["error"].lower()

@pytest.mark.parametrize("field, value", [
    ("userID", "ユーザー123"),       # Japanese characters
    ("username", "user😊"),          # Emoji
    ("mediaName", "CaféNetwork")     # Accented character
])
def test_add_user_rejects_non_ascii(client, field, value):
    payload = {
        "userID": "asciiID",
        "username": "asciiUser",
        "mediaName": "AsciiMedia",
        "age": 25
    }
    payload[field] = value

    if field != "mediaName":
        client.post("/add-socialmedia", json={"mediaName": payload["mediaName"]})

    res = client.post("/add-user", json=payload)
    assert res.status_code == 400
    assert "ascii" in res.json["error"].lower()

# Test invalid userID format
@pytest.mark.parametrize("invalid_userid", [
    "user!",          # Special character not allowed
    "user id",        # Space not allowed
    "user$",          # Dollar sign
    "a" * 51          # Exceeds 50 characters
])
def test_add_user_invalid_userid_format(client, invalid_userid):
    client.post("/add-socialmedia", json={"mediaName": "ValidMedia1"})
    res = client.post("/add-user", json={
        "userID": invalid_userid,
        "username": "validusername",
        "mediaName": "ValidMedia1",
        "age": 25
    })
    assert res.status_code == 400
    assert "invalid userid format" in res.json["error"].lower()


# Test invalid username format
@pytest.mark.parametrize("invalid_username", [
    "user name",      # Space not allowed
    "user@",          # @ is not allowed
    "user!",          # Exclamation
    "a" * 51          # Exceeds 50 characters
])
def test_add_user_invalid_username_format(client, invalid_username):
    client.post("/add-socialmedia", json={"mediaName": "ValidMedia2"})
    res = client.post("/add-user", json={
        "userID": "validID",
        "username": invalid_username,
        "mediaName": "ValidMedia2",
        "age": 25
    })
    assert res.status_code == 400
    assert "invalid username format" in res.json["error"].lower()


# Test invalid mediaName format
@pytest.mark.parametrize("invalid_medianame", [
    "Media!",         # Special character not allowed
    "Media_123",      # Underscore not allowed
    "Media-Test",     # Dash not allowed
    "a" * 101          # Exceeds 100 characters
])
def test_add_user_invalid_medianame_format(client, invalid_medianame):
    # Only create social media if the test isn't testing its failure
    if re.match(r"^[A-Za-z0-9\s]{1,100}$", invalid_medianame) is None:
        # Skip adding the social media if it's invalid — that's what we're testing
        pass
    else:
        client.post("/add-socialmedia", json={"mediaName": invalid_medianame})

    res = client.post("/add-user", json={
        "userID": "validID2",
        "username": "validusername2",
        "mediaName": invalid_medianame,
        "age": 25
    })
    assert res.status_code == 400
    assert "invalid medianame format" in res.json["error"].lower()