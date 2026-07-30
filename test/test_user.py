from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient
from flask import Response

from db.database import init_db
from main import app
from model import User
from schemas.user_schema import UserSchema
from utils.response_wrapper import api_response

client = TestClient(app)

def sign_up_user(user: UserSchema) -> Response:
    response = client.post("/api/signup/", json=user.model_dump())
    assert response.status_code == HTTPStatus.CREATED
    return response

def sign_in_user(user: UserSchema) -> Response:
    response = client.post(
        "/api/signin/",
        data=user.model_dump(),
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json().get("access_token") is not None
    assert response.json().get("token_type") == "bearer"

    return response

def create_test_user_schema():
    user = UserSchema()
    user.username = "Test User"
    user.email = "test_user@test.com"
    user.password = "test"

    return user

@pytest.fixture(autouse=True)
def run_around_tests():
    init_db()
    yield
    # Code that will run after your test

# READ ALL Users - Unauthenticated
def test_get_users_unauthenticated():
    response = client.get("/api/users/")
    assert response.status_code == HTTPStatus.UNAUTHORIZED

# READ ALL Users - Non-empty
def test_get_users():
    user: UserSchema = create_test_user_schema()

    sign_up_user(user)

    response = sign_in_user(user)

    response = client.get(
        "/api/users/",
        headers={"Authorization": f"Bearer {response.json().get('access_token')}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert len(response.json().get("data")) == 1
    
# READ Single User - Unauthenticated
def test_get_user_unauthenticated():
    user: UserSchema = create_test_user_schema()

    response = sign_up_user(user)
    user_id = response.json().get("data").get("id")
    assert user_id is not None

    sign_in_user(user)

    response = client.get(
        f"/api/users/{user_id}"
    )
    assert response.status_code == HTTPStatus.UNAUTHORIZED

# READ Single User - Not found
def test_get_user_not_found():
    user: UserSchema = create_test_user_schema()

    response = sign_up_user(user)
    user_id = response.json().get("data").get("id")
    assert user_id is not None

    response = sign_in_user(user)

    response = client.get(
        f"/api/users/wrong-id",
        headers={"Authorization": f"Bearer {response.json().get('access_token')}"},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User with id wrong-id not found"}

# READ Single User - Found
def test_get_user_found():
    user: UserSchema = create_test_user_schema()

    response = sign_up_user(user)
    user_id = response.json().get("data").get("id")
    assert user_id is not None

    response = sign_in_user(user)

    response = client.get(
        f"/api/users/{user_id}",
        headers={"Authorization": f"Bearer {response.json().get('access_token')}"},
    )
    assert response.status_code == HTTPStatus.OK

# CREATE User
def test_create_user():
    response = sign_up_user(create_test_user_schema())
    assert response.status_code == HTTPStatus.CREATED

# UPDATE User
def test_update_user():
    user: UserSchema = create_test_user_schema()
    response = sign_up_user(user)
    assert response.status_code == HTTPStatus.CREATED

    access_token = sign_in_user(user).json().get("access_token")

    # update user
    stored_user = User(**response.json().get("data"))
    assert stored_user is not None
    user.username = "Updated User"
    response = client.put(
        f"/api/users/{stored_user.id}",
        headers={"Authorization": f"Bearer {access_token}"},
        json=user.model_dump())

    assert response.status_code == HTTPStatus.OK

# DELETE User
def test_delete_user():
    user: UserSchema = create_test_user_schema()
    response = sign_up_user(user)
    assert response.status_code == HTTPStatus.CREATED

    user_id = response.json().get("data").get("id")
    response = sign_in_user(user)
    assert response.status_code == HTTPStatus.OK
    access_token = response.json().get("access_token")

    response = client.delete(
        f"/api/users/{user_id}",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == HTTPStatus.OK

    response = client.get(
        f"/api/users/{user_id}",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    # by deleting the signed in user, the JWT token is expired and we need to expect a 401 status
    assert response.status_code == HTTPStatus.UNAUTHORIZED