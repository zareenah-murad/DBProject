def test_duplicate_analysisresult_fails(client):
    client.post("/add-institute", json={"instituteName": "inst1"})
    client.post("/add-project", json={
        "projectName": "proj1",
        "managerFirstName": "A",
        "managerLastName": "B",
        "instituteName": "inst1",
        "startDate": "2025-01-01",
        "endDate": "2025-12-01"
    })
    client.post("/add-socialmedia", json={"mediaName": "ZZ"})
    client.post("/add-user", json={"username": "zuser", "mediaName": "ZZ", "age": 30})
    client.post("/add-post", json={
        "PostID": "postZ",
        "UserID": "uZ",  # Replace with dynamic lookup if needed
        "PostText": "Z-post",
        "PostDateTime": "2025-05-05T12:00:00"
    })
    client.post("/add-used-in", json={"projectName": "proj1", "postID": "postZ"})
    client.post("/add-field", json={"projectName": "proj1", "fieldName": "sentiment"})

    client.post("/add-analysisresult", json={
        "ProjectName": "proj1",
        "PostID": "postZ",
        "FieldName": "sentiment",
        "FieldValue": "positive"
    })

    res = client.post("/add-analysisresult", json={
        "ProjectName": "proj1",
        "PostID": "postZ",
        "FieldName": "sentiment",
        "FieldValue": "neutral"
    })
    assert res.status_code == 400


def test_post_used_in_multiple_projects(client):
    client.post("/add-institute", json={"instituteName": "InstX"})

    for pname in ["P1", "P2"]:
        client.post("/add-project", json={
            "projectName": pname,
            "managerFirstName": "A",
            "managerLastName": "B",
            "instituteName": "InstX",
            "startDate": "2025-01-01",
            "endDate": "2025-12-01"
        })
        client.post("/add-field", json={"projectName": pname, "fieldName": "engagement"})

    client.post("/add-socialmedia", json={"mediaName": "SNet"})
    res_user = client.post("/add-user", json={"username": "puser", "mediaName": "SNet", "age": 30})
    user_id = res_user.json["userID"]

    client.post("/add-post", json={
        "PostID": "sharedPost",
        "UserID": user_id,
        "PostText": "Cross-project post",
        "PostDateTime": "2025-05-05T15:00:00"
    })

    for pname in ["P1", "P2"]:
        client.post("/add-used-in", json={"projectName": pname, "postID": "sharedPost"})
        res = client.post("/add-analysisresult", json={
            "ProjectName": pname,
            "PostID": "sharedPost",
            "FieldName": "engagement",
            "FieldValue": "high"
        })
        assert res.status_code == 201


def test_query_experiment_results_nonexistent_project(client):
    res = client.get("/query/experiment-results?projectName=nonexistent_proj")
    assert res.status_code == 404
    assert "no project found" in res.json["error"].lower()


def test_query_experiment_results_with_no_analysis(client):
    client.post("/add-institute", json={"instituteName": "InstA"})
    client.post("/add-project", json={
        "projectName": "ProjA",
        "managerFirstName": "Z",
        "managerLastName": "Y",
        "instituteName": "InstA",
        "startDate": "2025-01-01",
        "endDate": "2025-12-31"
    })
    client.post("/add-socialmedia", json={"mediaName": "MTest"})
    res_user = client.post("/add-user", json={"username": "testuser", "mediaName": "MTest", "age": 22})
    user_id = res_user.json["userID"]
    client.post("/add-post", json={
        "PostID": "noAnalysisPost",
        "UserID": user_id,
        "PostText": "No analysis for this post",
        "PostDateTime": "2025-05-05T10:00:00"
    })
    client.post("/add-used-in", json={"projectName": "ProjA", "postID": "noAnalysisPost"})

    res = client.get("/query/experiment-results?projectName=ProjA")
    assert res.status_code == 200
    assert len(res.json["posts"]) == 1
    assert res.json["posts"][0]["analysis"] == []
    assert res.json["fieldCoverage"] == {}


def test_query_experiment_results_partial_coverage(client):
    client.post("/add-institute", json={"instituteName": "InstB"})
    client.post("/add-project", json={
        "projectName": "ProjB",
        "managerFirstName": "A",
        "managerLastName": "B",
        "instituteName": "InstB",
        "startDate": "2025-01-01",
        "endDate": "2025-12-31"
    })
    client.post("/add-field", json={"projectName": "ProjB", "fieldName": "sentiment"})
    client.post("/add-field", json={"projectName": "ProjB", "fieldName": "emotion"})
    client.post("/add-socialmedia", json={"mediaName": "MTest2"})
    res_user = client.post("/add-user", json={"username": "user1", "mediaName": "MTest2", "age": 28})
    user_id = res_user.json["userID"]

    for i in range(2):
        pid = f"partialPost{i}"
        client.post("/add-post", json={
            "PostID": pid,
            "UserID": user_id,
            "PostText": f"Post {i}",
            "PostDateTime": f"2025-05-0{i+1}T12:00:00"
        })
        client.post("/add-used-in", json={"projectName": "ProjB", "postID": pid})

    client.post("/add-analysisresult", json={
        "ProjectName": "ProjB",
        "PostID": "partialPost0",
        "FieldName": "sentiment",
        "FieldValue": "neutral"
    })

    res = client.get("/query/experiment-results?projectName=ProjB")
    assert res.status_code == 200
    assert res.json["fieldCoverage"]["sentiment"] == 0.5
    assert "emotion" not in res.json["fieldCoverage"]


def test_add_analysisresult_missing_field_value(client):
    client.post("/add-institute", json={"instituteName": "inst1"})
    client.post("/add-project", json={
        "projectName": "proj1",
        "managerFirstName": "A",
        "managerLastName": "B",
        "instituteName": "inst1",
        "startDate": "2025-01-01",
        "endDate": "2025-12-01"
    })
    client.post("/add-socialmedia", json={"mediaName": "ZZ"})
    client.post("/add-user", json={"username": "zuser", "mediaName": "ZZ", "age": 30})
    client.post("/add-post", json={
        "PostID": "postZ",
        "UserID": "uZ",  # Replace with dynamic lookup if needed
        "PostText": "Z-post",
        "PostDateTime": "2025-05-05T12:00:00"
    })
    client.post("/add-used-in", json={"projectName": "proj1", "postID": "postZ"})
    client.post("/add-field", json={"projectName": "proj1", "fieldName": "sentiment"})

    client.post("/add-analysisresult", json={
        "ProjectName": "proj1",
        "PostID": "postZ",
        "FieldName": "sentiment",
        "FieldValue": "positive"
    })

    res = client.post("/add-analysisresult", json={
        "ProjectName": "proj1",
        "PostID": "postZ",
        "FieldName": "sentiment"
        # FieldValue is missing
    })
    assert res.status_code == 400
    assert "all fields" in res.json["error"].lower()


def test_analysisresult_field_not_in_project(client):
    client.post("/add-institute", json={"instituteName": "inst1"})
    client.post("/add-project", json={
        "projectName": "proj1",
        "managerFirstName": "A",
        "managerLastName": "B",
        "instituteName": "inst1",
        "startDate": "2025-01-01",
        "endDate": "2025-12-01"
    })
    client.post("/add-socialmedia", json={"mediaName": "ZZ"})
    res_user = client.post("/add-user", json={"username": "zuser", "mediaName": "ZZ", "age": 30})
    user_id = res_user.json["userID"]

    client.post("/add-post", json={
        "PostID": "postZ",
        "UserID": user_id,
        "PostText": "Z-post",
        "PostDateTime": "2025-05-05T12:00:00"
    })

    client.post("/add-used-in", json={"projectName": "proj1", "postID": "postZ"})

    # Don't add the field
    res = client.post("/add-analysisresult", json={
        "ProjectName": "proj1",
        "PostID": "postZ",
        "FieldName": "not_existing",
        "FieldValue": "value"
    })

    assert res.status_code in [400, 500]
    assert (
        "field" in res.json["error"].lower()
        or "foreign key" in res.json["error"].lower()
        or "project name" in res.json["error"].lower()
        or "constraint" in res.json["error"].lower()
    )


def test_analysisresult_invalid_fieldname_format(client):
    res = client.post("/add-analysisresult", json={
        "ProjectName": "proj1",
        "PostID": "postZ",
        "FieldName": "bad@field!",
        "FieldValue": "neutral"
    })
    assert res.status_code == 400
    assert "invalid fieldname format" in res.json["error"].lower()
