from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session
from starlette.responses import FileResponse

from db.database import get_db
from model.project import Project
from schemas.project_schema import ProjectSchema
from utils import files_manager
from utils.response_wrapper import api_response
from pathlib import Path

router = APIRouter()

# CREATE Project
@router.post("/projects/")
async def create_project(project: ProjectSchema, db: Session = Depends(get_db)):
    if db.query(Project).filter(Project.id == project.id).first():
        raise HTTPException(status_code=400, detail="Project already created")

    new_project = Project(**project.dict())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    return api_response(data=new_project, message="Project created successfully")

# Download Project
@router.get("/projects/{project_id}/")
async def load_project(project_id: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    project_path = files_manager.get_files_root().joinpath(str(project.id))
    project_path.mkdir(parents=True, exist_ok=True)
    file_location = f"{project_path}/project.pytch"

    res = FileResponse(file_location, media_type='application/octet-stream', filename="project.pytch")

    return res

# Upload Project
@router.post("/projects/{project_id}/")
async def create_project(project_id: str, uploaded: UploadFile, db: Session = Depends(get_db)):

    # TODO: fix json body in file upload request not working
    # TODO: use project id as folder or file name
    project = db.query(Project).filter(Project.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")

    project_path = files_manager.get_files_root().joinpath(str(project.id))
    project_path.mkdir(parents=True, exist_ok=True)
    file_location = f"{project_path}/project.pytch"
    with open(file_location, "wb+") as file_object:
        file_object.write(uploaded.file.read())

    return api_response(data=file_location, message="Project uploaded successfully")

# READ ALL Projects
@router.get("/projects/")
def get_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    return api_response(data=projects, message="All projects retrieved")

# READ Single Project
@router.get("/projects/{project_id}")
def get_user(project_id: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return api_response(data=project, message="Project retrieved successfully")

# UPDATE Project
@router.put("/projects/{project_id}")
def update_user(project_id: str, project_update: ProjectSchema, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    for field, value in project_update.dict(exclude_unset=True).items():
        setattr(project, field, value)

    db.commit()
    db.refresh(project)
    return api_response(data=project, message="Project updated successfully")

# DELETE Project
@router.delete("/projects/{project_id}")
def delete_user(project_id: str, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    db.delete(project)
    db.commit()
    return api_response(message="Project deleted successfully")
