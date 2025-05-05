def test_post_with_negative_dislikes_fails(client):
    client.post("/add-socialmedia", json={"mediaName": "TestMedia"})
    client.post("/add-user", json={"userID": "uidX", "username": "userX", "mediaName": "TestMedia", "age": 25})

    res = client.post("/add-post", json={
        "PostID": "pNeg",
        "UserID": "uidX",
        "PostText": "test text",
        "PostDateTime": "2025-05-05T10:00:00",
        "Dislikes": -3,
        "Likes": 1
    })
    assert res.status_code == 400
    assert "Dislikes must be a non-negative integer" in res.json["error"]

def test_post_with_negative_likes_fails(client):
    client.post("/add-socialmedia", json={"mediaName": "Net2"})
    client.post("/add-user", json={"userID": "u2", "username": "user2", "mediaName": "Net2", "age": 25})
    res = client.post("/add-post", json={
        "PostID": "p2",
        "UserID": "u2",
        "PostText": "Test post",
        "PostDateTime": "2025-05-05T12:00:00",
        "Likes": -1
    })
    assert res.status_code == 400
    assert "Likes must be a non-negative integer" in res.json["error"]

def test_duplicate_postid_fails(client):
    client.post("/add-socialmedia", json={"mediaName": "PostNet"})
    client.post("/add-user", json={"userID": "userP", "username": "poster", "mediaName": "PostNet", "age": 28})

    post_payload = {
        "PostID": "postX",
        "UserID": "userP",
        "PostText": "Original post",
        "PostDateTime": "2025-05-05T10:00:00",
        "Likes": 5,
        "Dislikes": 0
    }
    res1 = client.post("/add-post", json=post_payload)
    assert res1.status_code == 201

    # Try to add the same PostID again
    post_payload["PostText"] = "Duplicate post attempt"
    res2 = client.post("/add-post", json=post_payload)
    assert res2.status_code == 400
    assert "post with this id already exists" in res2.json["error"].lower()

def test_post_with_missing_fields_fails(client):
    client.post("/add-socialmedia", json={"mediaName": "TestMedia"})
    client.post("/add-user", json={"userID": "uidY", "username": "userY", "mediaName": "TestMedia", "age": 30})

    res = client.post("/add-post", json={
        "PostID": "pMissing",
        "UserID": "uidY",
        # Missing PostText and PostDateTime
        "Likes": 10,
        "Dislikes": 2
    })
    assert res.status_code == 400
    assert "Missing required fields" in res.json["error"]

def test_add_post_empty_fields(client):
    res = client.post("/add-post", json={})
    assert res.status_code == 400
    assert "Missing required fields" in res.json["error"]

def test_post_with_invalid_datetime_format_fails(client):
    client.post("/add-socialmedia", json={"mediaName": "TestMedia"})
    client.post("/add-user", json={"userID": "uidZ", "username": "userZ", "mediaName": "TestMedia", "age": 22})

    res = client.post("/add-post", json={
        "PostID": "pInvalidDate",
        "UserID": "uidZ",
        "PostText": "Invalid datetime test",
        "PostDateTime": "05-05-2025 10:00:00",  # Invalid format
        "Likes": 0,
        "Dislikes": 0
    })
    assert res.status_code == 400
    assert "Invalid PostDateTime format" in res.json["error"]

def test_add_post_invalid_postid_format(client):
    client.post("/add-socialmedia", json={"mediaName": "Net"})
    client.post("/add-user", json={"userID": "u1", "username": "user1", "mediaName": "Net", "age": 25})
    res = client.post("/add-post", json={
        "PostID": "invalid id!",
        "UserID": "u1",
        "PostText": "Test",
        "PostDateTime": "2025-05-05T12:00:00"
    })
    assert res.status_code == 400
    assert "Invalid PostID format" in res.json["error"]

def test_post_with_nonexistent_userid_fails(client):
    client.post("/add-socialmedia", json={"mediaName": "TestMedia"})

    res = client.post("/add-post", json={
        "PostID": "pNonexistentUser",
        "UserID": "nonexistentUser",
        "PostText": "This user does not exist",
        "PostDateTime": "2025-05-05T10:00:00",
        "Likes": 0,
        "Dislikes": 0
    })
    assert res.status_code == 400
    assert "UserID does not exist" in res.json["error"]

def test_post_with_repost_data(client):
    client.post("/add-socialmedia", json={"mediaName": "TestMedia"})
    client.post("/add-user", json={"userID": "uidA", "username": "userA", "mediaName": "TestMedia", "age": 25})
    client.post("/add-user", json={"userID": "uidB", "username": "userB", "mediaName": "TestMedia", "age": 30})

    # Original post
    client.post("/add-post", json={
        "PostID": "originalPost",
        "UserID": "uidA",
        "PostText": "Original post content",
        "PostDateTime": "2025-05-05T09:00:00",
        "Likes": 10,
        "Dislikes": 1
    })

    # Repost
    res = client.post("/add-post", json={
        "PostID": "repostPost",
        "UserID": "uidB",
        "PostText": "Reposting original content",
        "PostDateTime": "2025-05-05T10:00:00",
        "RepostedByUserID": "uidA",
        "RepostDateTime": "2025-05-05T10:00:00",
        "Likes": 5,
        "Dislikes": 0
    })
    assert res.status_code == 201
    assert res.json["status"] == "success"

def test_post_with_invalid_repost_datetime_fails(client):
    client.post("/add-socialmedia", json={"mediaName": "TestMedia"})
    client.post("/add-user", json={"userID": "uidC", "username": "userC", "mediaName": "TestMedia", "age": 27})

    res = client.post("/add-post", json={
        "PostID": "invalidRepostDate",
        "UserID": "uidC",
        "PostText": "Invalid repost datetime",
        "PostDateTime": "2025-05-05T10:00:00",
        "RepostedByUserID": "uidC",
        "RepostDateTime": "05-05-2025 10:00:00",  # Invalid format
        "Likes": 0,
        "Dislikes": 0
    })
    assert res.status_code == 400
    assert "Invalid RepostDateTime format" in res.json["error"]

def test_post_with_multimedia_flag(client):
    client.post("/add-socialmedia", json={"mediaName": "MediaWithMultimedia"})
    client.post("/add-user", json={"userID": "uidD", "username": "userD", "mediaName": "MediaWithMultimedia", "age": 35})

    res = client.post("/add-post", json={
        "PostID": "postWithMultimedia",
        "UserID": "uidD",
        "PostText": "This post has multimedia",
        "PostDateTime": "2025-05-05T10:00:00",
        "HasMultimedia": True,
        "Likes": 15,
        "Dislikes": 3
    })
    assert res.status_code == 201
    assert res.json["status"] == "success"