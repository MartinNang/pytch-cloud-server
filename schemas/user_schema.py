from typing import Optional
from pydantic import EmailStr, ConfigDict
from pydantic_settings import BaseSettings

from model.user_roles import UserRoles


class UserSchema(BaseSettings):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[UserRoles] = None

    model_config = ConfigDict(from_attributes=True)