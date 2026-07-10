# main.py
from contextlib import asynccontextmanager

from fastapi import FastAPI
from controller.user_controller import router as user_router
from db.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
app = FastAPI(lifespan=lifespan)

app.include_router(user_router, prefix="/api", tags=["Users"])

@app.get("/")
def root():
    return {"message": "Welcome to the FastAPI CRUD API"}