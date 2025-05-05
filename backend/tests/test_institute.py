import pytest
from flask.testing import FlaskClient
from app import app

def test_add_institute_with_sql_keyword(client: FlaskClient):
    response = client.post("/add-institute", json={"instituteName": "drop table users"})
    assert response.status_code == 400
    assert "potentially dangerous content" in response.json["error"].lower()

def test_add_institute_with_script_tag(client: FlaskClient):
    response = client.post("/add-institute", json={"instituteName": "<script>alert(1)</script>"})
    assert response.status_code == 400
    assert "html or script tags" in response.json["error"].lower()

def test_add_institute_duplicate(client: FlaskClient):
    name = "DuplicateInstitute"
    client.post("/add-institute", json={"instituteName": name})
    res = client.post("/add-institute", json={"instituteName": name})
    assert res.status_code == 400
    assert "already exists" in res.json["error"].lower()