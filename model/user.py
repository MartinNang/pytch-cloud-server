import datetime
import enum
import uuid

from db.database import Base
from sqlalchemy import Column, TIMESTAMP, ForeignKey, Enum, Boolean
from sqlalchemy.dialects.postgresql import CHAR

from model.user_roles import UserRoles


class User(Base):
    __tablename__ = 'users'

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(CHAR(50), nullable=False)
    email = Column(CHAR(50), nullable=False)
    password = Column(CHAR(100), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.datetime.now(datetime.UTC))
    role = Column(Enum(UserRoles), nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    # TODO: look into amazon identity management to get inspiration for model