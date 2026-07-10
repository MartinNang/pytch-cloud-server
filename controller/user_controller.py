from email import message

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.database import get_db
from model.user import User
from schemas.user_schema import UserSchema
from utils.response_wrapper import api_response

router = APIRouter()

# CREATE User
@router.post("/users/")
def create_user(user: UserSchema, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
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
        raise HTTPException(status_code=404, detail="User not found")
    return api_response(data=user, message="User retrieved successfully")

# UPDATE User
@router.put("/users/{user_id}")
def update_user(user_id: str, user_update: UserSchema, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return api_response(data=user, message="User updated successfully")

# DELETE Customer
@router.delete("/users/{user_id}")
def delete_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return api_response(message="User deleted successfully")
