import pytest

def test_add_used_in_success(client):
    # Setup
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

    res_post = client.post("/add-post", json={
        "UserID": user_id,
        "PostText": "Post to be used",
        "PostDateTime": "2025-05-05T12:00:00"
    })
    post_id = res_post.json["postID"]

    # Act
    res = client.post("/add-used-in", json={"projectName": "ProjUsed", "postID": post_id})

    # Assert
    assert res.status_code == 201
    assert res.json["status"] == "success"

import pytest

@pytest.mark.parametrize("payload", [
    {"postID": "fake_only"},  # Missing projectName
    {"projectName": "ProjOnly"}  # Missing postID
])
def test_add_used_in_missing_fields(client, payload):
    # Setup a project to avoid 404 error unrelated to payload validation
    client.post("/add-institute", json={"instituteName": "TestInst"})
    client.post("/add-project", json={
        "projectName": "ProjOnly",
        "managerFirstName": "F",
        "managerLastName": "L",
        "instituteName": "TestInst",
        "startDate": "2025-01-01",
        "endDate": "2025-12-01"
    })

    # Act
    res = client.post("/add-used-in", json=payload)

    # Assert
    assert res.status_code == 400
    assert "required" in res.json["error"].lower()


def test_add_used_in_duplicate_fails(client):
    # Setup
    client.post("/add-institute", json={"instituteName": "InstDup"})
    client.post("/add-project", json={
        "projectName": "ProjDup",
        "managerFirstName": "Dup",
        "managerLastName": "Case",
        "instituteName": "InstDup",
        "startDate": "2025-01-01",
        "endDate": "2025-12-01"
    })
    client.post("/add-socialmedia", json={"mediaName": "DupNet"})
    res_user = client.post("/add-user", json={"username": "dupuser", "mediaName": "DupNet", "age": 25})
    user_id = res_user.json["userID"]

    res_post = client.post("/add-post", json={
        "UserID": user_id,
        "PostText": "Duplicate post",
        "PostDateTime": "2025-05-06T14:00:00"
    })
    post_id = res_post.json["postID"]

    # First association
    res1 = client.post("/add-used-in", json={"projectName": "ProjDup", "postID": post_id})
    assert res1.status_code == 201

    # Duplicate association
    res2 = client.post("/add-used-in", json={"projectName": "ProjDup", "postID": post_id})
    assert res2.status_code == 400
    assert "already used" in res2.json["error"].lower()


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