from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from db.database import get_db
# from model import UserRole
from model.user import User
from model.user_roles import UserRoles
from schemas.user_schema import UserSchema
from utils.response_wrapper import api_response
from pwdlib import PasswordHash

from utils.token_utils import create_access_token, Token

router = APIRouter()

password_hash = PasswordHash.recommended()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

ACCESS_TOKEN_EXPIRE_MINUTES = 30

# CREATE User
@router.post("/signup")
def create_user(user: UserSchema, response: Response, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    if user.username is None:
        raise HTTPException(status_code=400, detail="Username not provided")
    if user.password is None:
        raise HTTPException(status_code=400, detail="Password not provided")
    # if user.role is None:
        # raise HTTPException(status_code=400, detail="Authorisation not provided")

    # TODO: check if user registering new user is admin (only if role is added and not user)

    new_user = User(**user.model_dump())
    new_user.password = password_hash.hash(user.password)
    if user.role is None:
        new_user.role = UserRoles.USER
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    response.status_code = status.HTTP_201_CREATED

    return api_response(data=new_user, message="User created successfully")

# READ ALL Users
@router.get("/users/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return api_response(data=users, message="All users retrieved")

# READ Single User
@router.get("/users/{user_id}")
def get_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    return api_response(data=user, message="User retrieved successfully")

# UPDATE User
@router.put("/users/{user_id}")
def update_user(user_id: str, user_update: UserSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")

    for field, value in user_update.model_dump(exclude_unset=True).items():
        if field == "role":
            # TODO: use jwt to check if logged in user is admin before updating a role
            pass
        else:
            setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return api_response(data=user, message="User updated successfully")

# DELETE User
@router.delete("/users/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")

    db.delete(user)
    db.commit()
    return api_response(message="User deleted successfully")

# Sign in User
@router.post("/signin")
async def signin_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not password_hash.verify(form_data.password, user.password.strip()):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")