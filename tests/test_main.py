import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def get_auth_token(username="admin", password="secret"):
    response = client.post("/token", data={"username": username, "password": password})
    assert response.status_code == 200, "Token retrieval failed"
    token = response.json().get("access_token")
    assert token, "No token found in response"
    return token


def test_token_invalid_credentials():
    response = client.post("/token", data={"username": "wrong", "password": "wrong"})
    assert response.status_code == 401
    assert response.json().get("detail") == "Incorrect username or password"


def test_token_valid_credentials():
    token = get_auth_token()
    assert isinstance(token, str) and len(token) > 0


def test_protected_endpoint_without_token():
    response = client.get("/contacts")
    assert response.status_code == 401


@pytest.mark.usefixtures("populate_data")
def test_get_contacts_authorized():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/contacts", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2, "Expected 2 contacts in mock data"
    assert data[0]["name"] == "Test Contact 1"


@pytest.mark.usefixtures("populate_data")
def test_get_invoices_authorized():
    token = get_auth_token()
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/invoices", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2, "Expected 2 invoices in mock data"
    assert data[0]["number"] == "INV101"
