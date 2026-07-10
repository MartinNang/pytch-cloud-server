import datetime
import uuid

from sqlalchemy import Column, TIMESTAMP
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.sql.sqltypes import BOOLEANTYPE


class Project:
    __tablename__ = 'projects'

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(CHAR(50), nullable=False)
    program_kind = Column(CHAR(50), nullable=False)
    user_id = Column(CHAR(50), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.datetime.utcnow)
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.datetime.utcnow)
    archived = Column(BOOLEANTYPE(50), nullable=False, default=False)
    # TODO: patch project code efficiently (high prio)
    # TODO: patch project title (medium prio)
    # TODO: unpack zip file, put in asset store, store link to assets in database (tbd)
    # TODO: add thumbnail? (nice-to-have, v2)
    # TODO: should local storage be cleared during sign out
    # TODO: think about timeout time