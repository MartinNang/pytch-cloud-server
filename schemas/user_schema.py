import datetime
from typing import Optional
from xmlrpc.client import DateTime

from fastapi.openapi.models import Schema
from pydantic import EmailStr, BaseModel


class UserSchema(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    authorisations: Optional[str] = None

    class Config:
        from_attributes = True