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
    client.post("/add-user", json={"userID": "uZ", "username": "zuser", "mediaName": "ZZ", "age": 30})
    client.post("/add-post", json={
        "PostID": "postZ",
        "UserID": "uZ",
        "PostText": "Z-post",
        "PostDateTime": "2025-05-05T12:00:00"
    })
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

def test_analysis_of_nonexistent_post_fails(client):
    client.post("/add-institute", json={"instituteName": "TestInst"})
    client.post("/add-project", json={
        "projectName": "TestProj",
        "managerFirstName": "A",
        "managerLastName": "B",
        "instituteName": "TestInst",
        "startDate": "2025-01-01",
        "endDate": "2025-12-01"
    })
    client.post("/add-field", json={"projectName": "TestProj", "fieldName": "relevance"})

    res = client.post("/add-analysisresult", json={
        "ProjectName": "TestProj",
        "PostID": "nonexistent_post",
        "FieldName": "relevance",
        "FieldValue": "high"
    })
    assert res.status_code == 400
    assert "post" in res.json["error"].lower()

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
    client.post("/add-user", json={"userID": "userP", "username": "puser", "mediaName": "SNet", "age": 30})
    client.post("/add-post", json={
        "PostID": "sharedPost",
        "UserID": "userP",
        "PostText": "Cross-project post",
        "PostDateTime": "2025-05-05T15:00:00"
    })

    for pname in ["P1", "P2"]:
        res = client.post("/add-analysisresult", json={
            "ProjectName": pname,
            "PostID": "sharedPost",
            "FieldName": "engagement",
            "FieldValue": "high"
        })
        assert res.status_code == 201

def test_analysis_with_nonexistent_field_fails(client):
    client.post("/add-institute", json={"instituteName": "CheckField"})
    client.post("/add-project", json={
        "projectName": "FieldProj",
        "managerFirstName": "F",
        "managerLastName": "M",
        "instituteName": "CheckField",
        "startDate": "2025-01-01",
        "endDate": "2025-12-01"
    })
    client.post("/add-socialmedia", json={"mediaName": "FieldMedia"})
    client.post("/add-user", json={"userID": "userF", "username": "userf", "mediaName": "FieldMedia", "age": 30})
    client.post("/add-post", json={
        "PostID": "postF",
        "UserID": "userF",
        "PostText": "Content",
        "PostDateTime": "2025-05-05T12:00:00"
    })

    res = client.post("/add-analysisresult", json={
        "ProjectName": "FieldProj",
        "PostID": "postF",
        "FieldName": "nonexistentField",
        "FieldValue": "someValue"
    })
    assert res.status_code == 400

def test_duplicate_composite_key_analysisresult_fails(client):
    client.post("/add-institute", json={"instituteName": "UniX"})
    client.post("/add-project", json={
        "projectName": "projX",
        "managerFirstName": "Jane",
        "managerLastName": "Doe",
        "instituteName": "UniX",
        "startDate": "2025-01-01",
        "endDate": "2025-12-31"
    })
    client.post("/add-socialmedia", json={"mediaName": "XMedia"})
    client.post("/add-user", json={"userID": "uX", "username": "analyst", "mediaName": "XMedia", "age": 30})
    client.post("/add-post", json={
        "PostID": "postX",
        "UserID": "uX",
        "PostText": "Test for PK",
        "PostDateTime": "2025-05-05T15:00:00"
    })
    client.post("/add-field", json={"projectName": "projX", "fieldName": "topic"})

    res1 = client.post("/add-analysisresult", json={
        "ProjectName": "projX",
        "PostID": "postX",
        "FieldName": "topic",
        "FieldValue": "AI"
    })
    assert res1.status_code == 201

    res2 = client.post("/add-analysisresult", json={
        "ProjectName": "projX",
        "PostID": "postX",
        "FieldName": "topic",
        "FieldValue": "ML"
    })
    assert res2.status_code == 400
    assert "already exists" in res2.json["error"].lower()

def test_add_analysisresult_missing_fields(client):
    res = client.post("/add-analysisresult", json={})
    assert res.status_code == 400
    assert "required" in res.json["error"].lower()

def test_add_analysisresult_invalid_projectname_format(client):
    client.post("/add-institute", json={"instituteName": "TechU"})
    client.post("/add-project", json={
        "projectName": "AnalysisTestProj",
        "managerFirstName": "John",
        "managerLastName": "Doe",
        "instituteName": "TechU",
        "startDate": "2025-01-01",
        "endDate": "2025-12-31"
    })
    client.post("/add-field", json={"projectName": "AnalysisTestProj", "fieldName": "fieldA"})
    client.post("/add-socialmedia", json={"mediaName": "MediaA"})
    client.post("/add-user", json={"userID": "uA", "username": "userA", "mediaName": "MediaA", "age": 20})
    client.post("/add-post", json={"PostID": "pA", "UserID": "uA", "PostText": "Text", "PostDateTime": "2025-01-01T12:00:00"})
    
    res = client.post("/add-analysisresult", json={
        "ProjectName": "!!!Invalid",
        "PostID": "pA",
        "FieldName": "fieldA",
        "FieldValue": "value"
    })
    assert res.status_code == 400
    assert "invalid projectname format" in res.json["error"].lower()

def test_add_analysisresult_empty_field_value(client):
    res = client.post("/add-analysisresult", json={
        "ProjectName": "projX",
        "PostID": "postX",
        "FieldName": "sentiment",
        "FieldValue": ""
    })
    assert res.status_code == 400
    assert "all fields" in res.json["error"].lower()