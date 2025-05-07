def test_full_workflow_end_to_end(client):
    # Step 1: Add Social Media
    res = client.post("/add-socialmedia", json={"mediaName": "FullTestMedia"})
    assert res.status_code == 201

    # Step 2: Add Institute
    res = client.post("/add-institute", json={"instituteName": "TestInstitute"})
    assert res.status_code == 201

    # Step 3: Add User
    res_user = client.post("/add-user", json={
        "username": "testuser",
        "mediaName": "FullTestMedia",
        "age": 25
    })
    user_id = res_user.json["userID"]

    # Step 4: Add Post
    res_post = client.post("/add-post", json={
        "UserID": user_id,
        "PostText": "Analyzing sentiment in this post.",
        "PostDateTime": "2025-05-05T10:00:00"
    })
    assert res_post.status_code == 201
    post_id = res_post.json["postID"]

    # Step 5: Add Project
    res = client.post("/add-project", json={
        "projectName": "AnalysisProj",
        "managerFirstName": "Alice",
        "managerLastName": "Smith",
        "instituteName": "TestInstitute",
        "startDate": "2025-01-01",
        "endDate": "2025-12-31"
    })
    assert res.status_code == 201

    # Step 6: Add Fields
    for field in ["Sentiment", "Emotion"]:
        res = client.post("/add-field", json={
            "projectName": "AnalysisProj",
            "fieldName": field
        })
        assert res.status_code == 201

    # Step 7: Add Used_In entry
    res = client.post("/add-used-in", json={
        "projectName": "AnalysisProj",
        "postID": post_id
    })
    assert res.status_code == 201

    # Step 8: Add Partial Analysis Result
    res = client.post("/add-analysisresult", json={
        "ProjectName": "AnalysisProj",
        "PostID": post_id,
        "FieldName": "Sentiment",
        "FieldValue": "Positive"
    })
    assert res.status_code == 201

    # Step 9: Query Analysis Result
    res = client.get("/query/experiment-results?projectName=AnalysisProj")
    assert res.status_code == 200

    posts = res.json["posts"]
    assert len(posts) == 1
    post = posts[0]
    assert post["postID"] == post_id
    assert post["username"] == "testuser"
    assert any(a["field"] == "Sentiment" and a["value"] == "Positive" for a in post["analysis"])
    assert res.json["fieldCoverage"]["Sentiment"] == 1.0
    assert "Emotion" not in res.json["fieldCoverage"]

    # Step 10: Query Posts by Project
    res = client.get("/query/posts-by-project?projectName=AnalysisProj")
    assert res.status_code == 200
    assert any(p["postID"] == post_id for p in res.json)


def test_full_workflow_complete_analysis(client):
    # Add Social Media & Institute
    client.post("/add-socialmedia", json={"mediaName": "FullTestMedia2"})
    client.post("/add-institute", json={"instituteName": "TestInstitute2"})

    # Add User
    res_user = client.post("/add-user", json={
        "username": "userX",
        "mediaName": "FullTestMedia2",
        "age": 40
    })
    user_id = res_user.json["userID"]

    # Add Post
    res_post = client.post("/add-post", json={
        "UserID": user_id,
        "PostText": "Comprehensive analysis post.",
        "PostDateTime": "2025-06-01T14:00:00"
    })
    post_id = res_post.json["postID"]

    # Add Project
    client.post("/add-project", json={
        "projectName": "CompleteAnalysisProj",
        "managerFirstName": "Jamie",
        "managerLastName": "Lee",
        "instituteName": "TestInstitute2",
        "startDate": "2025-01-01",
        "endDate": "2025-12-31"
    })

    # Add Fields
    fields = ["Sentiment", "Emotion"]
    for f in fields:
        client.post("/add-field", json={
            "projectName": "CompleteAnalysisProj",
            "fieldName": f
        })

    # Associate post with project
    client.post("/add-used-in", json={
        "projectName": "CompleteAnalysisProj",
        "postID": post_id
    })

    # Add analysis results for all fields
    for f, val in zip(fields, ["Positive", "Joyful"]):
        client.post("/add-analysisresult", json={
            "ProjectName": "CompleteAnalysisProj",
            "PostID": post_id,
            "FieldName": f,
            "FieldValue": val
        })

    # Query results
    res = client.get("/query/experiment-results?projectName=CompleteAnalysisProj")
    assert res.status_code == 200

    posts = res.json["posts"]
    assert len(posts) == 1
    analysis = posts[0]["analysis"]
    field_coverage = res.json["fieldCoverage"]

    assert any(a["field"] == "Sentiment" and a["value"] == "Positive" for a in analysis)
    assert any(a["field"] == "Emotion" and a["value"] == "Joyful" for a in analysis)

    for f in fields:
        assert field_coverage[f] == 1.0
