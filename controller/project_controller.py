from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, UploadFile, Response, File
from sqlalchemy.orm import Session
from starlette import status
from starlette.responses import FileResponse

from db.database import get_db
from model import User
from model.project import Project
from schemas.project_schema import ProjectSchema
from utils import files_manager
from utils.response_wrapper import api_response
from utils.token_utils import get_current_user

router = APIRouter()

# READ ALL Projects
@router.get("/projects/")
def get_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    return api_response(data=projects, message="All projects retrieved")

# READ Single Project
@router.get("/projects/{project_id}")
def get_project(project_id: str,
                current_user: Annotated[User, Depends(get_current_user)],
                db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail=f"Project with id {project_id} not found")
    return api_response(data=project, message="Project retrieved successfully")

# CREATE Project
@router.post("/projects/")
async def create_project(project: ProjectSchema,
                         response: Response,
                         current_user: Annotated[User, Depends(get_current_user)],
                         db: Session = Depends(get_db)):
    if db.query(Project).filter(Project.id == project.id).first():
        raise HTTPException(status_code=400, detail="Project already created")

    new_project = Project(**project.model_dump())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    project_path = files_manager.get_files_root().joinpath(str(new_project.id).strip())
    project_path.mkdir(parents=True, exist_ok=True)

    response.status_code = status.HTTP_201_CREATED

    return api_response(data=new_project, message="Project created successfully")

# Download a listed Project
@router.get("/projects/{project_id}/download")
async def load_project(project_id: str,
                       db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail=f"Project with id {project_id} not found")
    # TODO: check if project is publically listed

    project_path = files_manager.get_files_root().joinpath(str(project.id).strip())
    file_location = f"{project_path}/project.pytch"

    res = FileResponse(file_location, media_type='application/octet-stream', filename="project.pytch")

    return res

# TODO: Download an unlisted project (check if user has access to this project)

# Upload Project
@router.post("/projects/{project_id}/upload")
async def create_project(project_id: str,
                         response: Response,
                         current_user: Annotated[User, Depends(get_current_user)],
                         uploaded: UploadFile = File(...), db: Session = Depends(get_db)):

    # TODO: fix json body in file upload request not working
    project = db.query(Project).filter(Project.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail=f"Project with id {project_id} not found")

    project_path = files_manager.get_files_root().joinpath(str(project.id).strip())
    file_location = project_path.joinpath("project.pytch")
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded.file.read())

    response.status_code = status.HTTP_201_CREATED

    return api_response(data=file_location, message="Project uploaded successfully")

# UPDATE Project
@router.put("/projects/{project_id}")
def update_project(project_id: str, response: Response,
                   current_user: Annotated[User, Depends(get_current_user)],
                   project_update: ProjectSchema, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail=f"Project with id {project_id} not found")

    for field, value in project_update.model_dump(exclude_unset=True).items():
        setattr(project, field, value)

    db.commit()
    db.refresh(project)

    return api_response(data=project, message="Project updated successfully")

# DELETE Project
@router.delete("/projects/{project_id}")
def delete_project(project_id: str,
                   current_user: Annotated[User, Depends(get_current_user)],
                   db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail=f"Project with id {project_id} not found")

    db.delete(project)
    db.commit()
    return api_response(message="Project deleted successfully")
