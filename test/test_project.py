from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from db.database import init_db
from main import app
from schemas.project_schema import ProjectSchema
from schemas.user_schema import UserSchema
from utils.files_manager import get_test_resources_root
from utils.response_wrapper import api_response

client = TestClient(app)

@pytest.fixture(autouse=True)
def run_around_tests():
    init_db()
    yield
    # Code that will run after your test

# READ ALL Projects - empty
def test_get_projects():
    response = client.get("/api/projects/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == api_response(data=[], message="All projects retrieved")

# READ Single Project - Not found
def test_get_project_not_found():
    response = client.get("/api/projects/0")
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "Project with id 0 not found"}

# CREATE Project
def test_create_project():
    # create user
    user: UserSchema = UserSchema()
    user.username = "Test User"
    user.email = "test_user@test.com"
    user.password = "test"
    response = client.post("/api/signup/", json=user.model_dump())

    assert response.status_code == HTTPStatus.CREATED

    user_id = response.json().get("data").get("id")
    assert user_id is not None

    # create project
    project: ProjectSchema = ProjectSchema()
    project.id = "test_project_id"
    project.title = "Test Project"
    project.program_kind = "flat"
    project.archived = False
    project.user_id = user_id
    project.status = "listed"
    response = client.post("/api/projects/", json=project.model_dump())

    assert response.status_code == HTTPStatus.CREATED

# UPLOAD Project
def test_upload_project():
    # create user
    user: UserSchema = UserSchema()
    user.username = "Test User"
    user.email = "test_user@test.com"
    user.password = "test"
    response = client.post("/api/signup/", json=user.model_dump())

    assert response.status_code == HTTPStatus.CREATED

    user_id = response.json().get("data").get("id")
    assert user_id is not None

    # create project
    project: ProjectSchema = ProjectSchema()
    project.id = "test_project_id"
    project.title = "Test Project"
    project.program_kind = "flat"
    project.archived = False
    project.user_id = user_id
    project.status = "listed"
    response = client.post("/api/projects/", json=project.model_dump())

    assert response.status_code == HTTPStatus.CREATED

    # upload project zip file
    _test_project = get_test_resources_root().joinpath('test-project.pytch')
    _files = {'uploaded': _test_project.open('rb')}
    response = client.post(f"/api/projects/{project.id}/upload", files=_files)

    assert response.status_code == HTTPStatus.CREATED

# DOWNLOAD Project
def test_download_project():
    # create user
    user: UserSchema = UserSchema()
    user.username = "Test User"
    user.email = "test_user@test.com"
    user.password = "test"
    response = client.post("/api/signup/", json=user.model_dump())

    assert response.status_code == HTTPStatus.CREATED

    user_id = response.json().get("data").get("id")
    assert user_id is not None

    # create project
    project: ProjectSchema = ProjectSchema()
    project.id = "test_project_id"
    project.title = "Test Project"
    project.program_kind = "flat"
    project.archived = False
    project.user_id = user_id
    project.status = "listed"
    response = client.post("/api/projects/", json=project.model_dump())

    assert response.status_code == HTTPStatus.CREATED

    # upload project zip file
    _test_project = get_test_resources_root().joinpath('test-project.pytch')
    _files = {'uploaded': _test_project.open('rb')}
    response = client.post(f"/api/projects/{project.id}/upload", files=_files)

    assert response.status_code == HTTPStatus.CREATED

    # download project zip file
    response = client.get(f"/api/projects/{project.id}/download")

    assert response.status_code == HTTPStatus.OK

# UPDATE Project - title
def test_update_project_title():
    # create user
    user: UserSchema = UserSchema()
    user.username = "Test User"

    user: UserSchema = UserSchema()
    user.username = "Test User"
    user.email = "test_user@test.com"
    user.password = "test"
    response = client.post("/api/signup/", json=user.model_dump())

    assert response.status_code == HTTPStatus.CREATED

    user_id = response.json().get("data").get("id")
    assert user_id is not None

    # create project
    project: ProjectSchema = ProjectSchema()
    project.id = "test_project_id"
    project.title = "Test Project"
    project.program_kind = "flat"
    project.archived = False
    project.user_id = user_id
    project.status = "listed"
    response = client.post("/api/projects/", json=project.model_dump())

    assert response.status_code == HTTPStatus.CREATED

    # update project title
    project.title = "Test Project v2"
    response = client.put(f"/api/projects/{project.id.strip()}", json=project.model_dump())

    assert response.status_code == HTTPStatus.OK
    assert response.json().get("data").get("title").strip() == project.title

# DELETE Project
def test_delete_project():
    # create user
    user: UserSchema = UserSchema()
    user.username = "Test User"

    user: UserSchema = UserSchema()
    user.username = "Test User"
    user.email = "test_user@test.com"
    user.password = "test"
    response = client.post("/api/signup/", json=user.model_dump())

    assert response.status_code == HTTPStatus.CREATED

    user_id = response.json().get("data").get("id")
    assert user_id is not None

    # create project
    project: ProjectSchema = ProjectSchema()
    project.id = "test_project_id"
    project.title = "Test Project"
    project.program_kind = "flat"
    project.archived = False
    project.user_id = user_id
    project.status = "listed"
    response = client.post("/api/projects/", json=project.model_dump())

    assert response.status_code == HTTPStatus.CREATED

    # delete project
    response = client.delete(f"/api/projects/{project.id}")

    assert response.status_code == HTTPStatus.OK

    # find single project
    response = client.get(f"/api/projects/{project.id}")

    assert response.status_code == HTTPStatus.NOT_FOUND

# TODO: UPDATE Project - project code

# TODO: UPDATE Project - non-default asset