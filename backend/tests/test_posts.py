def test_post_with_negative_dislikes_fails(client):
    client.post("/add-socialmedia", json={"mediaName": "TestMedia"})
    res_user = client.post("/add-user", json={"username": "userX", "mediaName": "TestMedia", "age": 25})
    user_id = res_user.json["userID"]

    res = client.post("/add-post", json={
        "PostID": "pNeg",
        "UserID": user_id,
        "PostText": "test text",
        "PostDateTime": "2025-05-05T10:00:00",
        "Dislikes": -3,
        "Likes": 1
    })
    assert res.status_code == 400
    assert "Dislikes must be a non-negative integer" in res.json["error"]

def test_post_with_negative_likes_fails(client):
    client.post("/add-socialmedia", json={"mediaName": "Net2"})
    res_user = client.post("/add-user", json={"username": "user2", "mediaName": "Net2", "age": 25})
    user_id = res_user.json["userID"]

    res = client.post("/add-post", json={
        "PostID": "p2",
        "UserID": user_id,
        "PostText": "Test post",
        "PostDateTime": "2025-05-05T12:00:00",
        "Likes": -1
    })
    assert res.status_code == 400
    assert "Likes must be a non-negative integer" in res.json["error"]

def test_duplicate_postid_fails(client):
    client.post("/add-socialmedia", json={"mediaName": "PostNet"})
    res_user = client.post("/add-user", json={"username": "poster", "mediaName": "PostNet", "age": 28})
    user_id = res_user.json["userID"]

    post_payload = {
        "PostID": "postX",
        "UserID": user_id,
        "PostText": "Original post",
        "PostDateTime": "2025-05-05T10:00:00",
        "Likes": 5,
        "Dislikes": 0
    }
    res1 = client.post("/add-post", json=post_payload)
    assert res1.status_code == 201

    post_payload["PostText"] = "Duplicate post attempt"
    res2 = client.post("/add-post", json=post_payload)
    assert res2.status_code == 400
    assert "post with this id already exists" in res2.json["error"].lower()

def test_post_with_missing_fields_fails(client):
    client.post("/add-socialmedia", json={"mediaName": "TestMedia"})
    res_user = client.post("/add-user", json={"username": "userY", "mediaName": "TestMedia", "age": 30})
    user_id = res_user.json["userID"]

    res = client.post("/add-post", json={
        "PostID": "pMissing",
        "UserID": user_id,
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
    res_user = client.post("/add-user", json={"username": "userZ", "mediaName": "TestMedia", "age": 22})
    user_id = res_user.json["userID"]

    res = client.post("/add-post", json={
        "PostID": "pInvalidDate",
        "UserID": user_id,
        "PostText": "Invalid datetime test",
        "PostDateTime": "05-05-2025 10:00:00",
        "Likes": 0,
        "Dislikes": 0
    })
    assert res.status_code == 400
    assert "Invalid PostDateTime format" in res.json["error"]

def test_add_post_invalid_postid_format(client):
    client.post("/add-socialmedia", json={"mediaName": "Net"})
    res_user = client.post("/add-user", json={"username": "user1", "mediaName": "Net", "age": 25})
    user_id = res_user.json["userID"]

    res = client.post("/add-post", json={
        "PostID": "invalid id!",
        "UserID": user_id,
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

    res_userA = client.post("/add-user", json={"username": "userA", "mediaName": "TestMedia", "age": 25})
    userA_id = res_userA.json["userID"]

    res_userB = client.post("/add-user", json={"username": "userB", "mediaName": "TestMedia", "age": 30})
    userB_id = res_userB.json["userID"]

    client.post("/add-post", json={
        "PostID": "originalPost",
        "UserID": userA_id,
        "PostText": "Original post content",
        "PostDateTime": "2025-05-05T09:00:00",
        "Likes": 10,
        "Dislikes": 1
    })

    res = client.post("/add-post", json={
        "PostID": "repostPost",
        "UserID": userB_id,
        "PostText": "Reposting original content",
        "PostDateTime": "2025-05-05T10:00:00",
        "RepostedByUserID": userA_id,
        "RepostDateTime": "2025-05-05T10:00:00",
        "Likes": 5,
        "Dislikes": 0
    })
    assert res.status_code == 201
    assert res.json["status"] == "success"

def test_post_with_invalid_repost_datetime_fails(client):
    client.post("/add-socialmedia", json={"mediaName": "TestMedia"})
    res_user = client.post("/add-user", json={"username": "userC", "mediaName": "TestMedia", "age": 27})
    user_id = res_user.json["userID"]

    res = client.post("/add-post", json={
        "PostID": "invalidRepostDate",
        "UserID": user_id,
        "PostText": "Invalid repost datetime",
        "PostDateTime": "2025-05-05T10:00:00",
        "RepostedByUserID": user_id,
        "RepostDateTime": "05-05-2025 10:00:00",  # Invalid format
        "Likes": 0,
        "Dislikes": 0
    })
    assert res.status_code == 400
    assert "Invalid RepostDateTime format" in res.json["error"]

def test_post_with_multimedia_flag(client):
    client.post("/add-socialmedia", json={"mediaName": "MediaWithMultimedia"})
    res_user = client.post("/add-user", json={"username": "userD", "mediaName": "MediaWithMultimedia", "age": 35})
    user_id = res_user.json["userID"]

    res = client.post("/add-post", json={
        "PostID": "postWithMultimedia",
        "UserID": user_id,
        "PostText": "This post has multimedia",
        "PostDateTime": "2025-05-05T10:00:00",
        "HasMultimedia": True,
        "Likes": 15,
        "Dislikes": 3
    })
    assert res.status_code == 201
    assert res.json["status"] == "success"