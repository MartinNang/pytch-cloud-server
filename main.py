# main.py
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from controller.user_controller import router as user_router
from controller.project_controller import router as project_router
from db.database import init_db
from utils import files_manager

files_manager.init_files_root()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(user_router, prefix="/api", tags=["Users"])
app.include_router(project_router, prefix="/api", tags=["Users"])

@app.get("/")
def root():
    return {"message": "Welcome to the Pytch Cloud Storage API"}
