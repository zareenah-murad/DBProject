import pytest
from datetime import datetime

def create_user(client, username="testuser", media_name="XNet", age=25):
    client.post("/add-socialmedia", json={"mediaName": media_name})
    res = client.post("/add-user", json={
        "username": username,
        "mediaName": media_name,
        "age": age
    })
    assert res.status_code == 201
    return res.get_json()["userID"]

def create_post(client, post_id, user_id):
    return client.post("/add-post", json={
        "PostID": post_id,
        "UserID": user_id,
        "PostText": "original content",
        "PostDateTime": datetime.now().isoformat(),
        "Likes": 1,
        "Dislikes": 0
    })

def test_mark_post_as_repost_success(client):
    user_id = create_user(client)
    create_post(client, "p123", user_id)
    res = client.post("/update/repost", json={
        "postID": "p123",
        "repostedByUserID": user_id,
        "repostTime": datetime.now().isoformat()
    })
    assert res.status_code == 200
    assert "successfully marked" in res.get_json()["message"].lower()

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
    assert res.status_code == 404
    assert "no post found" in res.get_json()["error"].lower()

def test_mark_post_as_repost_nonexistent_user(client):
    user_id = create_user(client)
    create_post(client, "p999", user_id)
    res = client.post("/update/repost", json={
        "postID": "p999",
        "repostedByUserID": 999999,  # fake user
        "repostTime": datetime.now().isoformat()
    })
    assert res.status_code == 404
    assert "no user found" in res.get_json()["error"].lower()

def test_mark_post_as_repost_invalid_repost_time(client):
    user_id = create_user(client)
    create_post(client, "pxxx", user_id)
    res = client.post("/update/repost", json={
        "postID": "pxxx",
        "repostedByUserID": user_id,
        "repostTime": "not-a-date"
    })
    assert res.status_code == 400
    assert "valid iso datetime" in res.get_json()["error"].lower()