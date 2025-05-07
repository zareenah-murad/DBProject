import pytest
from datetime import datetime

def create_user(client, username="testuser"):
    client.post("/add-socialmedia", json={"mediaName": "XNet"})
    res = client.post("/add-user", json={
        "username": username,
        "mediaName": "XNet",
        "age": 25
    })
    return res.json["userID"]

def create_post(client, user_id):
    res = client.post("/add-post", json={
        "UserID": user_id,
        "PostText": "Test post content",
        "PostDateTime": datetime.now().isoformat()
    })
    return res.json["postID"]


def test_mark_post_as_repost_missing_fields(client):
    res = client.post("/update/repost", json={})
    assert res.status_code == 400
    assert "required" in res.get_json()["error"].lower()

def test_mark_post_as_repost_nonexistent_post(client):
    user_id = create_user(client)
    res = client.post("/update/repost", json={
        "postID": "nonexistent",
        "repostedByUserID": user_id,
        "repostTime": datetime.now().isoformat()
    })
    assert res.status_code == 404  # ✅ fixed
    assert "no post found" in res.get_json()["error"].lower()


def test_mark_post_as_repost_success(client):
    original_user_id = create_user(client)
    post_id = create_post(client, original_user_id)

    reposter_id = create_user(client, username="reposter")  # use different user

    res = client.post("/update/repost", json={
        "postID": post_id,
        "repostedByUserID": reposter_id,
        "repostTime": datetime.now().isoformat()
    })

    assert res.status_code == 200 
    assert "successfully marked" in res.get_json()["message"].lower()


def test_mark_post_as_repost_nonexistent_user(client):
    original_user_id = create_user(client)
    post_id = create_post(client, original_user_id)

    res = client.post("/update/repost", json={
        "postID": post_id,
        "repostedByUserID": 999999,
        "repostTime": datetime.now().isoformat()
    })
    assert res.status_code == 404  
    assert "no user found" in res.get_json()["error"].lower()


def test_mark_post_as_repost_invalid_repost_time(client):
    user_id = create_user(client)
    post_id = create_post(client, user_id)

    res = client.post("/update/repost", json={
        "postID": post_id,
        "repostedByUserID": user_id,
        "repostTime": "invalid-time-format"
    })
    assert res.status_code == 400
    assert "reposttime must be a valid iso datetime" in res.get_json()["error"].lower()  # ✅ fixed string check
