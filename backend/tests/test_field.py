def test_add_field_missing_keys(client):
    res = client.post("/add-field", json={})
    assert res.status_code == 400
    assert "both fields must be strings" in res.json["error"].lower()

def test_add_field_invalid_type(client):
    res = client.post("/add-field", json={"projectName": 123, "fieldName": ["array"]})
    assert res.status_code == 400
    assert "both fields must be strings" in res.json["error"].lower()

def test_add_field_non_ascii(client):
    client.post("/add-institute", json={"instituteName": "asciiinst"})
    client.post("/add-project", json={
        "projectName": "ascii_proj",
        "managerFirstName": "A",
        "managerLastName": "B",
        "instituteName": "asciiinst",
        "startDate": "2025-01-01",
        "endDate": "2025-12-01"
    })
    res = client.post("/add-field", json={"projectName": "ascii_proj", "fieldName": "非ASCII"})
    assert res.status_code == 400
    assert "ascii characters" in res.json["error"].lower()