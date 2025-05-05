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