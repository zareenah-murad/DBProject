def test_cors_get_request(client):
    res = client.get("/test-cors")
    assert res.status_code == 200
    assert res.json["message"] == "CORS test route is working"

def test_cors_options_request(client):
    res = client.options("/test-cors")
    assert res.status_code == 200
    assert res.json["message"] == "CORS preflight successful"

    # Check CORS headers
    assert res.headers["Access-Control-Allow-Origin"] == "http://localhost:3000"
    assert "GET" in res.headers["Access-Control-Allow-Methods"]
    assert "POST" in res.headers["Access-Control-Allow-Methods"]
    assert "OPTIONS" in res.headers["Access-Control-Allow-Methods"]
    assert "Content-Type" in res.headers["Access-Control-Allow-Headers"]

def test_home_route(client):
    res = client.get("/")
    assert res.status_code == 200
    assert res.json["message"] == "Backend is running!"

def test_add_user_options_preflight(client):
    res = client.options("/add-user")
    assert res.status_code == 200
    assert res.json["message"] == "CORS preflight successful"

    # Validate headers
    assert res.headers["Access-Control-Allow-Origin"] == "http://localhost:3000"
    assert "POST" in res.headers["Access-Control-Allow-Methods"]
    assert "OPTIONS" in res.headers["Access-Control-Allow-Methods"]
    assert "Content-Type" in res.headers["Access-Control-Allow-Headers"]