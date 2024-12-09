from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_include_router_auth():
    """Should be 401 because of the authentication required"""
    response = client.get("/auth/users/me")
    assert response.status_code == 401


def test_not_existing_router():
    """Should be 404 because of the not existing router"""
    response = client.get("/not_existing_router/")
    assert response.status_code == 404


def test_include_router_wallet():
    """Should be 401 because of the authentication required"""
    response = client.get("/wallet/")
    assert response.status_code == 401


def test_include_router_transactions():
    response = client.get("/transactions/")
    assert response.status_code == 404

