import pytest
from flask.testing import FlaskClient
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_add_project_missing_fields(client):
    response = client.post("/add-project", json={
        "projectName": "MyProj"
    })
    assert response.status_code == 400
    assert "one or more fields are missing" in response.json["error"].lower()

def test_add_project_invalid_dates(client: FlaskClient):
    client.post("/add-institute", json={"instituteName": "TestInstitute"})
    response = client.post("/add-project", json={
        "projectName": "InvalidDateProj",
        "managerFirstName": "Jane",
        "managerLastName": "Doe",
        "instituteName": "TestInstitute",
        "startDate": "2025-12-31",
        "endDate": "2025-01-01"
    })
    assert response.status_code == 400
    assert "EndDate must be after or equal to StartDate" in response.json["error"]

def test_add_project_nonexistent_institute(client: FlaskClient):
    response = client.post("/add-project", json={
        "projectName": "OrphanProject",
        "managerFirstName": "John",
        "managerLastName": "Smith",
        "instituteName": "NonexistentInstitute",
        "startDate": "2025-01-01",
        "endDate": "2025-12-31"
    })
    assert response.status_code == 400
    assert "Institute does not exist" in response.json["error"]