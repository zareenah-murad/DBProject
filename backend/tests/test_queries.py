def test_posts_by_media_query(client):
    client.post("/add-socialmedia", json={"mediaName": "MediaQ"})
    res_user = client.post("/add-user", json={"username": "queryuser", "mediaName": "MediaQ", "age": 30})
    user_id = res_user.json["userID"]

    client.post("/add-post", json={
        "PostID": "pMedia",
        "UserID": user_id,  # ✅ Use actual int
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

def test_posts_by_username_query(client):
    client.post("/add-socialmedia", json={"mediaName": "MediaQ"})
    res_user = client.post("/add-user", json={"username": "queryuser", "mediaName": "MediaQ", "age": 30})
    user_id = res_user.json["userID"]

    client.post("/add-post", json={
        "PostID": "pUser",
        "UserID": user_id,
        "PostText": "user-specific content",
        "PostDateTime": "2025-05-01T10:00:00"
    })

    res = client.get("/query/posts-by-username?username=queryuser&mediaName=MediaQ")
    assert res.status_code == 200
    assert len(res.json) == 1
    assert "user-specific content" in res.json[0]["content"]

def test_posts_by_name_query(client):
    client.post("/add-socialmedia", json={"mediaName": "MediaQ"})
    res_user = client.post("/add-user", json={
        "username": "queryuser",
        "mediaName": "MediaQ",
        "firstName": "John",
        "lastName": "Doe",
        "age": 30
    })
    user_id = res_user.json["userID"]

    client.post("/add-post", json={
        "PostID": "pName",
        "UserID": user_id,
        "PostText": "name-specific content",
        "PostDateTime": "2025-05-01T10:00:00"
    })

    res = client.get("/query/posts-by-name?firstName=John&lastName=Doe&mediaName=MediaQ")
    assert res.status_code == 200
    assert len(res.json) == 1
    assert "name-specific content" in res.json[0]["content"]

def test_experiment_results_query(client):
    client.post("/add-socialmedia", json={"mediaName": "MediaQ"})

    res_user = client.post("/add-user", json={
        "username": "queryuser",
        "mediaName": "MediaQ",
        "age": 30
    })
    user_id = res_user.json["userID"]

    res_post = client.post("/add-post", json={
        "UserID": user_id,
        "PostText": "experiment-related content",
        "PostDateTime": "2025-05-01T10:00:00"
    })
    post_id = res_post.json["postID"]

    client.post("/add-institute", json={"instituteName": "Tech Institute"})
    client.post("/add-project", json={
        "projectName": "Experiment1",
        "managerFirstName": "Alice",
        "managerLastName": "Smith",
        "instituteName": "Tech Institute",
        "startDate": "2025-01-01",
        "endDate": "2025-12-31"
    })

    client.post("/add-used-in", json={"projectName": "Experiment1", "postID": post_id})
    client.post("/add-field", json={"fieldName": "Field1", "projectName": "Experiment1"})

    client.post("/add-analysisresult", json={
        "ProjectName": "Experiment1",
        "PostID": post_id,
        "FieldName": "Field1",
        "FieldValue": "Value1"
    })

    res = client.get("/query/experiment-results?projectName=Experiment1")
    assert res.status_code == 200

    # Validate structure
    assert "posts" in res.json
    assert isinstance(res.json["posts"], list)
    assert "fieldCoverage" in res.json
    assert isinstance(res.json["fieldCoverage"], dict)

    # Validate post with expected ID and analysis result exists
    posts = res.json["posts"]
    matched_post = next((p for p in posts if p["postID"] == post_id), None)
    assert matched_post is not None

    analysis_fields = matched_post.get("analysis", [])
    assert any(field["field"] == "Field1" and field["value"] == "Value1" for field in analysis_fields)

def test_query_posts_by_time_missing_params(client):
    res = client.get("/query/posts-by-time")
    assert res.status_code == 400
    assert "start and end datetime are required" in res.json["error"].lower()

def test_query_posts_by_time_invalid_format(client):
    res = client.get("/query/posts-by-time?start=invalid&end=alsoinvalid")
    assert res.status_code == 400
    assert "invalid datetime format" in res.json["error"].lower()

def test_query_posts_by_time_end_before_start(client):
    res = client.get("/query/posts-by-time?start=2025-05-05T12:00:00&end=2025-05-01T12:00:00")
    assert res.status_code == 400
    assert "end time must be after start time" in res.json["error"].lower()