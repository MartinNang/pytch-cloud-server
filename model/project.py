import datetime
import uuid

from sqlalchemy import Column, TIMESTAMP
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.sql.sqltypes import BOOLEANTYPE

from db.database import Base


class Project(Base):
    __tablename__ = 'projects'

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(CHAR(50), nullable=False)
    program_kind = Column(CHAR(50), nullable=False)
    status = Column(CHAR(50), nullable=False)
    user_id = Column(CHAR(50), ForeignKey('users.id'), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.datetime.utcnow)
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.datetime.utcnow)
    archived = Column(BOOLEANTYPE, nullable=False, default=False)
    # TODO: patch project code efficiently (high prio)
    # TODO: patch project title (medium prio)
    # TODO: unpack zip file, put in asset store, store link to assets in database (tbd)
    # TODO: add thumbnail? (nice-to-have, v2)
    # TODO: should local storage be cleared during sign out
    # TODO: think about timeout time