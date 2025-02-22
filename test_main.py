import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

client = TestClient(app)


def test_register():
    response = client.post("/register", json={"username": "test_user", "password": "test@12345"})
    print("response:: ", response.json())
    assert response.status_code == 200
    assert response.json() == {"message": "success", "username": "test_user"}


def test_login_failure():
    response = client.post("/login", json={"username": "test_user", "password": "test@12345"})
    print("response:: ", response.json())
    assert response.status_code == 200


def test_create_organization():
    response = client.post("/create_organization", json={"name": "test_org"})
    print("response:: ", response.json())
    assert response.status_code == 200


def test_create_cluster():
    login_response = client.post("/login", json={"username": "test_user", "password": "test@12345"})
    print("login_response:: ", login_response.json())
    token = login_response['token']
    response = client.post(
        "/create_cluster",
        json={"cluster_name": "TestingCluster"},
        headers={"Authorization": f"Bearer {token}"}
    )
    print("response:: ", response.json())
    assert response.status_code == 200


def test_create_deployment_failure():
    login_response = client.post("/login", json={"username": "test_user", "password": "test@12345"})
    print("login_response:: ", login_response.json())

    token = login_response['token']
    response = client.post(
        "/create_deployment",
        json={"deployment_name": "TestDeployment"},
        headers={"Authorization": f"Bearer {token}"}
    )
    print("response:: ", response.json())
    assert response.status_code == 200
