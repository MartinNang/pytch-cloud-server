from datetime import timedelta
from typing import Annotated

import jwt
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import InvalidTokenError
from sqlalchemy.orm import Session
from starlette import status

from config import settings
from db.database import get_db
from model.user import User
from model.user_roles import UserRoles
from schemas.user_schema import UserSchema
from utils.password_utils import verify_password, password_hash
from utils.response_wrapper import api_response

from utils.token_utils import create_access_token, Token, TokenData, get_current_user

router = APIRouter()

# CREATE User
@router.post("/signup")
def create_user(user: UserSchema,
                response: Response, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    if user.username is None:
        raise HTTPException(status_code=400, detail="Username not provided")
    if user.password is None:
        raise HTTPException(status_code=400, detail="Password not provided")
    # if current_user is not None and current_user.role is not UserRoles.ADMIN and user.role is not None and user.role is not UserRoles.USER:
    #     raise HTTPException(status_code=401, detail=f"Current user with id {current_user.id} is not authorisation to create user with role {user.role}")

    # TODO: check if user registering new user is admin (only if role is added and not user)

    new_user = User(**user.model_dump())
    new_user.password = password_hash.hash(user.password)
    if user.role is None:
        new_user.role = UserRoles.ADMIN
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    response.status_code = status.HTTP_201_CREATED

    return api_response(data=new_user, message="User created successfully")

# READ ALL Users
@router.get("/users/")
def get_users(
    response: Response,
    current_user: Annotated[User, Depends(get_current_user)],
    db: Session = Depends(get_db)
):
    check_if_user_exists_and_active(current_user)

    if current_user.role is not UserRoles.ADMIN:
        raise HTTPException(status_code=401,
                            detail=f"Current user with id {current_user.id} is not authorised to read this user")

    users = db.query(User).all()
    return api_response(data=users, message="All users retrieved")

# READ Single User
@router.get("/users/{user_id}")
def get_user(user_id: str, current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    check_if_user_exists_and_active(current_user)

    if current_user.role is not UserRoles.ADMIN and current_user.id != user_id:
        raise HTTPException(status_code=401,
                            detail=f"Current user with id {current_user.id} is not authorised to read this user")

    # TODO: implement educator access rights

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")
    return api_response(data=user, message="User retrieved successfully")

# UPDATE User
@router.put("/users/{user_id}")
def update_user(user_id: str, current_user: Annotated[User, Depends(get_current_user)], user_update: UserSchema, db: Session = Depends(get_db)):
    check_if_user_exists_and_active(current_user)

    if current_user.role is not UserRoles.ADMIN and current_user.id != user_id:
        raise HTTPException(status_code=401, detail=f"Current user with id {current_user.id} is not authorised to update this user")

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
def delete_user(user_id: str, current_user: Annotated[User, Depends(get_current_user)], db: Session = Depends(get_db)):
    check_if_user_exists_and_active(current_user)

    if current_user.role is not UserRoles.ADMIN:
        raise HTTPException(status_code=401, detail=f"Current user with id {current_user.id} is not authorised to delete user")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"User with id {user_id} not found")

    db.delete(user)
    db.commit()
    return api_response(message="User deleted successfully")


DUMMY_HASH = password_hash.hash("dummypassword")

# Sign in User
@router.post("/signin")
async def signin_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user:
        # use dummy hash if user does not exist to keep response time consistent and prevent timing attacks
        # see: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/#hash-and-verify-the-passwords
        verify_password(form_data.password, DUMMY_HASH)
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not password_hash.verify(form_data.password, user.password.strip()):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.jwt_expiry_time)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@router.get("/user-profile")
async def read_current_user(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user

def check_if_user_exists_and_active(current_user: Annotated[User, Depends(get_current_user)]):
    if current_user is None:
        raise HTTPException(status_code=401, detail=f"No user signed in")

    if not current_user.active:
        raise HTTPException(status_code=401, detail=f"Current user with id {current_user.id} is not active")
