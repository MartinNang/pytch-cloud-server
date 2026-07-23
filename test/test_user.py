from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from db.database import init_db
from main import app
from model import User
from schemas.user_schema import UserSchema
from utils.response_wrapper import api_response

client = TestClient(app)

@pytest.fixture(autouse=True)
def run_around_tests():
    init_db()
    yield
    # Code that will run after your test

# READ ALL Users
def test_get_users():
    response = client.get("/api/users/")
    assert response.status_code == 200
    assert response.json() == api_response(data=[], message="All users retrieved")
    
# READ Single User - Not found
def test_get_user_not_found():
    response = client.get("/api/users/0")
    assert response.status_code == 404
    assert response.json() == {"detail": "User with id 0 not found"}

# READ Single User - Found
def test_get_user_found():
    user: UserSchema = UserSchema()
    user.username = "Test User"
    user.email = "test_user@test.com"
    user.password = "test"
    response = client.post("/api/signup/", json=user.model_dump())

    assert response.status_code == 201
    user_id = response.json().get("data").get("id")
    assert user_id is not None

    response = client.get(f"/api/users/{user_id}")
    assert response.status_code == 200
    # assert response.json() == {"detail": "User with id 0 not found"}

# CREATE User
def test_create_user():
    # create user
    user: UserSchema = UserSchema()
    user.username = "Test User"
    user.email = "test_user@test.com"
    user.password = "test"
    response = client.post("/api/signup/", json=user.model_dump())

    assert response.status_code == 201

# UPDATE User
def test_update_user():
    # create user
    user: UserSchema = UserSchema()
    user.username = "Test User"
    user.email = "test_user@test.com"
    user.password = "test"
    response = client.post("/api/signup/", json=user.model_dump())

    assert response.status_code == 201

    # update user
    stored_user = User(**response.json().get("data"))
    assert stored_user is not None
    user.username = "Updated User"
    response = client.put(f"/api/users/{stored_user.id}", json=user.model_dump())

    assert response.status_code == HTTPStatus.OK

# DELETE User
def test_delete_user():
    user: UserSchema = UserSchema()
    user.username = "Test User"
    user.email = "test_user@test.com"
    user.password = "test"
    response = client.post("/api/signup/", json=user.model_dump())

    assert response.status_code == 201

    user_id = response.json().get("data").get("id")
    response = client.delete(f"/api/users/{user_id}")

    assert response.status_code == HTTPStatus.OK

    response = client.get(f"/api/users/{user_id}")

    assert response.status_code == 404