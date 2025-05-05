def test_posts_by_media_query(client):
    client.post("/add-socialmedia", json={"mediaName": "MediaQ"})
    client.post("/add-user", json={"userID": "uM", "username": "queryuser", "mediaName": "MediaQ", "age": 30})
    client.post("/add-post", json={
        "PostID": "pMedia",
        "UserID": "uM",
        "PostText": "media-related content",
        "PostDateTime": "2025-05-01T10:00:00"
    })

    res = client.get("/query/posts-by-media?mediaName=MediaQ")
    assert res.status_code == 200
    assert len(res.json) == 1
    assert "media-related content" in res.json[0]["content"]

def test_posts_by_time_range_returns_none(client):
    res = client.get("/query/posts-by-time?start=2025-01-01T00:00:00&end=2025-01-02T00:00:00")
    assert res.status_code == 200
    assert isinstance(res.json, list)
    assert len(res.json) == 0