# main.py
import os
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Depends
from controller.user_controller import router as user_router
from controller.project_controller import router as project_router
from db.database import init_db
from utils import files_manager
from utils.token_utils import oauth2_scheme

files_manager.init_files_root()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(user_router, prefix="/api", tags=["Users"])
app.include_router(project_router, prefix="/api", tags=["Users"])

@app.get("/api/token/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}

@app.get("/api/")
def root():
    return {"message": "Welcome to the Pytch Cloud Storage API"}
