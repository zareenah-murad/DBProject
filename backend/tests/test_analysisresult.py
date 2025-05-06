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