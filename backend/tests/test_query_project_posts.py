def test_query_posts_by_project_success(client):
    client.post("/add-institute", json={"instituteName": "InstY"})
    client.post("/add-project", json={
        "projectName": "ProjY",
        "managerFirstName": "M",
        "managerLastName": "N",
        "instituteName": "InstY",
        "startDate": "2025-01-01",
        "endDate": "2025-12-31"
    })
    client.post("/add-socialmedia", json={"mediaName": "MediaY"})
    res_user = client.post("/add-user", json={"username": "userY", "mediaName": "MediaY", "age": 30})
    user_id = res_user.json["userID"]

    res_post = client.post("/add-post", json={
        "UserID": user_id,
        "PostText": "Project related post",
        "PostDateTime": "2025-05-05T10:00:00"
    })
    post_id = res_post.json["postID"]

    client.post("/add-used-in", json={"projectName": "ProjY", "postID": post_id})

    res = client.get("/query/posts-by-project?projectName=ProjY")
    assert res.status_code == 200
    assert len(res.json) == 1
    assert res.json[0]["postID"] == post_id
    assert res.json[0]["username"] == "userY"
    assert res.json[0]["mediaName"] == "MediaY"


def test_query_posts_by_project_missing_param(client):
    res = client.get("/query/posts-by-project")
    assert res.status_code == 400
    assert "project name is required" in res.json["error"].lower()

def test_query_posts_by_project_nonexistent(client):
    res = client.get("/query/posts-by-project?projectName=NoSuchProject")
    assert res.status_code == 404
    assert "no project found" in res.json["error"].lower()


def test_query_project_with_no_posts(client):
    client.post("/add-institute", json={"instituteName": "InstNoPosts"})
    client.post("/add-project", json={
        "projectName": "ProjNoPosts",
        "managerFirstName": "None",
        "managerLastName": "Here",
        "instituteName": "InstNoPosts",
        "startDate": "2025-01-01",
        "endDate": "2025-12-31"
    })

    res = client.get("/query/posts-by-project?projectName=ProjNoPosts")
    assert res.status_code == 200
    assert isinstance(res.json, list)
    assert len(res.json) == 0


def test_query_project_multiple_posts_sorted(client):
    client.post("/add-institute", json={"instituteName": "InstSort"})
    client.post("/add-project", json={
        "projectName": "ProjSort",
        "managerFirstName": "Sort",
        "managerLastName": "Check",
        "instituteName": "InstSort",
        "startDate": "2025-01-01",
        "endDate": "2025-12-31"
    })
    client.post("/add-socialmedia", json={"mediaName": "SortMedia"})
    res_user = client.post("/add-user", json={"username": "sorter", "mediaName": "SortMedia", "age": 29})
    user_id = res_user.json["userID"]

    posts = [
        ("2025-05-01T10:00:00"),
        ("2025-05-03T10:00:00"),
        ("2025-05-02T10:00:00")
    ]

    inserted_ids = []
    for dt in posts:
        res_post = client.post("/add-post", json={
            "UserID": user_id,
            "PostText": "Check sorting",
            "PostDateTime": dt
        })
        post_id = res_post.json["postID"]
        inserted_ids.append((post_id, dt))
        client.post("/add-used-in", json={"projectName": "ProjSort", "postID": post_id})

    # Sort descending by PostDateTime for expected order
    expected_order = [pid for pid, _ in sorted(inserted_ids, key=lambda x: x[1], reverse=True)]

    res = client.get("/query/posts-by-project?projectName=ProjSort")
    assert res.status_code == 200
    returned_ids = [post["postID"] for post in res.json]
    assert returned_ids == expected_order
