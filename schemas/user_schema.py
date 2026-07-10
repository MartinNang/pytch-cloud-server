from typing import Optional
from pydantic import EmailStr
from pydantic_settings import BaseSettings


class UserSchema(BaseSettings):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[str] = None

    class Config:
        from_attributes = True