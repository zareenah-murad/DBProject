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