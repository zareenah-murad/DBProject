import pytest

def test_add_used_in_success(client):
    client.post("/add-institute", json={"instituteName": "InstUsed"})
    client.post("/add-project", json={
        "projectName": "ProjUsed",
        "managerFirstName": "First",
        "managerLastName": "Last",
        "instituteName": "InstUsed",
        "startDate": "2025-01-01",
        "endDate": "2025-12-01"
    })
    client.post("/add-socialmedia", json={"mediaName": "UsedNet"})
    res_user = client.post("/add-user", json={"username": "useduser", "mediaName": "UsedNet", "age": 30})
    user_id = res_user.json["userID"]
    client.post("/add-post", json={
        "PostID": "postUsed",
        "UserID": user_id,
        "PostText": "Post to be used",
        "PostDateTime": "2025-05-05T12:00:00"
    })

    res = client.post("/add-used-in", json={"projectName": "ProjUsed", "postID": "postUsed"})
    assert res.status_code == 201
    assert res.json["status"] == "success"

def test_add_used_in_duplicate_fails(client):
    test_add_used_in_success(client)
    res = client.post("/add-used-in", json={"projectName": "ProjUsed", "postID": "postUsed"})
    assert res.status_code == 400
    assert "already used" in res.json["error"].lower()

@pytest.mark.parametrize("payload", [
    {"postID": "postUsed"},
    {"projectName": "ProjUsed"}
])
def test_add_used_in_missing_fields(client, payload):
    res = client.post("/add-used-in", json=payload)
    assert res.status_code == 400
    assert "required" in res.json["error"].lower()

def test_add_used_in_invalid_project(client):
    client.post("/add-socialmedia", json={"mediaName": "NPNet"})
    res_user = client.post("/add-user", json={"username": "userNP", "mediaName": "NPNet", "age": 25})
    user_id = res_user.json["userID"]
    client.post("/add-post", json={
        "PostID": "postNP",
        "UserID": user_id,
        "PostText": "Orphan post",
        "PostDateTime": "2025-05-05T12:00:00"
    })

    res = client.post("/add-used-in", json={"projectName": "NonProj", "postID": "postNP"})
    assert res.status_code == 400
    assert "project does not exist" in res.json["error"].lower()

def test_add_used_in_invalid_post(client):
    client.post("/add-institute", json={"instituteName": "PPInst"})
    client.post("/add-project", json={
        "projectName": "PPProj",
        "managerFirstName": "F",
        "managerLastName": "L",
        "instituteName": "PPInst",
        "startDate": "2025-01-01",
        "endDate": "2025-12-01"
    })

    res = client.post("/add-used-in", json={"projectName": "PPProj", "postID": "nonexistentPost"})
    assert res.status_code == 400
    assert "post does not exist" in res.json["error"].lower()