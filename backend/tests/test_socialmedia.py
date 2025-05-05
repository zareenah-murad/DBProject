def test_add_valid_socialmedia(client):
    response = client.post("/add-socialmedia", json={"mediaName": "XPlatform"})
    assert response.status_code == 201
    assert response.json["status"] == "success"

def test_add_duplicate_socialmedia(client):
    client.post("/add-socialmedia", json={"mediaName": "DuplicateMedia"})
    response = client.post("/add-socialmedia", json={"mediaName": "DuplicateMedia"})
    assert response.status_code == 400
    assert "already exists" in response.json["error"]