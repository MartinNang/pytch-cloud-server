from typing import Optional

from pydantic import EmailStr, BaseModel
from sqlmodel import Field


class ProjectSchema(BaseModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: Optional[str] = None
    program_kind: Optional[str] = None
    # status: Optional[str] = None
    user_id: Optional[str] = None
    archived: Optional[bool] = None

    class Config:
        from_attributes = True