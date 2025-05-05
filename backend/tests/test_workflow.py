def test_full_workflow_end_to_end(client):
    # Step 1: Add Social Media
    res = client.post("/add-socialmedia", json={"mediaName": "FullTestMedia"})
    assert res.status_code == 201

    # Step 2: Add Institute
    res = client.post("/add-institute", json={"instituteName": "TestInstitute"})
    assert res.status_code == 201

    # Step 3: Add User
    res = client.post("/add-user", json={
        "userID": "u123",
        "username": "testuser",
        "mediaName": "FullTestMedia",
        "age": 25
    })
    assert res.status_code == 201

    # Step 4: Add Post
    res = client.post("/add-post", json={
        "PostID": "post123",
        "UserID": "u123",
        "PostText": "Analyzing sentiment in this post.",
        "PostDateTime": "2025-05-05T10:00:00"
    })
    assert res.status_code == 201

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

    # Step 6: Add Field
    res = client.post("/add-field", json={
        "projectName": "AnalysisProj",
        "fieldName": "Sentiment"
    })
    assert res.status_code == 201

    # Step 7: Add Analysis Result
    res = client.post("/add-analysisresult", json={
        "ProjectName": "AnalysisProj",
        "PostID": "post123",
        "FieldName": "Sentiment",
        "FieldValue": "Positive"
    })
    assert res.status_code == 201

    # Step 8: Query Analysis Result
    res = client.get("/query/experiment-results?projectName=AnalysisProj")
    assert res.status_code == 200
    assert len(res.json) == 1
    assert res.json[0]["postID"] == "post123"
    assert res.json[0]["fieldName"].lower() == "sentiment"
    assert res.json[0]["fieldValue"] == "Positive"