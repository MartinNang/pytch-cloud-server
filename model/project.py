import datetime
import enum
import uuid

from sqlalchemy import Column, TIMESTAMP
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import BOOLEANTYPE, Enum

from db.database import Base

class ProgramKind(enum.Enum):
    FLAT = "flat"
    PER_METHOD = "per-method"

class ProjectStatus(enum.Enum):
    LISTED = "listed"
    UNLISTED = "unlisted"

class Project(Base):
    __tablename__ = 'projects'

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(CHAR(50), nullable=False)
    program_kind = Column(Enum(ProgramKind), nullable=False)
    status = Column(Enum(ProjectStatus), nullable=False)
    user_id = Column(CHAR(50), ForeignKey('users.id'), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.datetime.now(datetime.UTC))
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.datetime.now(datetime.UTC))
    archived = Column(BOOLEANTYPE, nullable=False, default=False)