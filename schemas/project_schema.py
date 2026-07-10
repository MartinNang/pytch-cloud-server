from typing import Optional

from pydantic_settings import BaseSettings
from sqlmodel import Field


class ProjectSchema(BaseSettings):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: Optional[str] = None
    program_kind: Optional[str] = None
    # status: Optional[str] = None
    user_id: Optional[str] = None
    archived: Optional[bool] = None

    class Config:
        from_attributes = True