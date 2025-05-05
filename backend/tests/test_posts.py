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