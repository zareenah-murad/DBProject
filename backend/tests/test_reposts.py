import pytest
from unittest.mock import patch

def test_mark_post_as_repost_success(client):
    # Setup: Add social media, users, and post
    client.post("/add-socialmedia", json={"mediaName": "TestMedia"})
    res_user1 = client.post("/add-user", json={"username": "user1", "mediaName": "TestMedia", "age": 25})
    user1_id = res_user1.json["userID"]  # Get the actual UserID for user1

    res_user2 = client.post("/add-user", json={"username": "user2", "mediaName": "TestMedia", "age": 30})
    user2_id = res_user2.json["userID"]  # Get the actual UserID for user2

    client.post("/add-post", json={
        "PostID": "post1",
        "UserID": user1_id,  # Use the correct UserID
        "PostText": "Original post",
        "PostDateTime": "2025-05-05T10:00:00"
    })

    # Test: Mark the post as reposted
    res = client.post("/update/repost", json={
        "postID": "post1",
        "repostedByUserID": user2_id,  # Use the correct UserID
        "repostTime": "2025-05-06T12:00:00"
    })
    assert res.status_code == 200
    assert res.json["message"] == "Post post1 successfully marked as reposted."

def test_mark_post_as_repost_missing_fields(client):
    res = client.post("/update/repost", json={
        "postID": "post1",
        # Missing repostedByUserID and repostTime
    })
    assert res.status_code == 400
    assert "postID, repostedByUserID, and repostTime are required." in res.json["error"]

def test_mark_post_as_repost_invalid_timestamp(client):
    res = client.post("/update/repost", json={
        "postID": "post1",
        "repostedByUserID": 2,
        "repostTime": "invalid-timestamp"
    })
    assert res.status_code == 400
    assert "repostTime must be a valid ISO datetime string." in res.json["error"]

def test_mark_post_as_repost_nonexistent_post(client):
    res = client.post("/update/repost", json={
        "postID": "nonexistentPost",
        "repostedByUserID": 2,
        "repostTime": "2025-05-06T12:00:00"
    })
    assert res.status_code == 404
    assert "No post found with PostID nonexistentPost" in res.json["error"]

def test_mark_post_as_repost_nonexistent_user(client):
    # Setup: Add social media and a valid user
    client.post("/add-socialmedia", json={"mediaName": "TestMedia"})
    res_user1 = client.post("/add-user", json={"username": "user1", "mediaName": "TestMedia", "age": 25})
    user1_id = res_user1.json["userID"]  # Get the actual UserID for user1

    # Add a post with the correct UserID
    client.post("/add-post", json={
        "PostID": "post1",
        "UserID": user1_id,  # Use the correct UserID
        "PostText": "Original post",
        "PostDateTime": "2025-05-05T10:00:00"
    })

    # Test: Use a non-existent user ID
    res = client.post("/update/repost", json={
        "postID": "post1",
        "repostedByUserID": 999,  # Non-existent user ID
        "repostTime": "2025-05-06T12:00:00"
    })
    assert res.status_code == 404
    assert "No user found with UserID 999" in res.json["error"]

def test_mark_post_as_repost_internal_server_error(client):
    # Setup minimal valid data
    client.post("/add-socialmedia", json={"mediaName": "ErrorTestNet"})
    res_user1 = client.post("/add-user", json={"username": "original", "mediaName": "ErrorTestNet", "age": 25})
    res_user2 = client.post("/add-user", json={"username": "reposter", "mediaName": "ErrorTestNet", "age": 30})

    user1_id = res_user1.json["userID"]
    user2_id = res_user2.json["userID"]

    client.post("/add-post", json={
        "PostID": "errPost",
        "UserID": user1_id,
        "PostText": "Will trigger error",
        "PostDateTime": "2025-05-05T10:00:00"
    })

    # Patch the `cursor.execute` method to throw a RuntimeError
    with patch("MySQLdb.cursors.BaseCursor.execute", side_effect=RuntimeError("Forced failure")):
        res = client.post("/update/repost", json={
            "postID": "errPost",
            "repostedByUserID": user2_id,
            "repostTime": "2025-05-05T12:00:00"
        })

    assert res.status_code == 500
    assert "an error occurred while updating the post" in res.json["error"].lower()

def test_repost_overwrites_previous_repost(client):
    # Add social media platform
    client.post("/add-socialmedia", json={"mediaName": "RepostMedia"})

    # Add the owner user
    owner = client.post("/add-user", json={"username": "poster", "mediaName": "RepostMedia", "age": 28})
    assert owner.status_code == 201
    assert "userID" in owner.json, f"Response missing 'userID': {owner.json}"
    owner_id = owner.json["userID"]

    # Add the first reposter
    reposter1 = client.post("/add-user", json={"username": "rep1", "mediaName": "RepostMedia", "age": 25})
    assert reposter1.status_code == 201
    assert "userID" in reposter1.json, f"Response missing 'userID': {reposter1.json}"
    reposter1_id = reposter1.json["userID"]

    # Add the second reposter
    reposter2 = client.post("/add-user", json={"username": "rep2", "mediaName": "RepostMedia", "age": 26})
    assert reposter2.status_code == 201
    assert "userID" in reposter2.json, f"Response missing 'userID': {reposter2.json}"
    reposter2_id = reposter2.json["userID"]

    # Add the post
    post = client.post("/add-post", json={
        "PostID": "dupRepost",
        "UserID": owner_id,  # Use the correct UserID
        "PostText": "Content to be reposted",
        "PostDateTime": "2025-05-01T10:00:00"
    })
    assert post.status_code == 201

    # First repost
    res1 = client.post("/update/repost", json={
        "postID": "dupRepost",
        "repostedByUserID": reposter1_id,
        "repostTime": "2025-05-02T12:00:00"
    })
    assert res1.status_code == 200

    # Second repost (overwrite)
    res2 = client.post("/update/repost", json={
        "postID": "dupRepost",
        "repostedByUserID": reposter2_id,
        "repostTime": "2025-05-03T14:00:00"
    })
    assert res2.status_code == 200
    assert f"Post dupRepost successfully marked as reposted." in res2.json["message"]