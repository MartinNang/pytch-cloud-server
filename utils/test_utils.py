from http import HTTPStatus

from flask import Response
from starlette.testclient import TestClient

from main import app
from schemas.user_schema import UserSchema

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