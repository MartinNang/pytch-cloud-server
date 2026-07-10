import datetime
import enum
import uuid

from db.database import Base
from sqlalchemy import Column, TIMESTAMP, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import CHAR

class UserRoles(enum.Enum):
    USER = 1
    EDUCATOR = 2
    ADMIN = 3

class User(Base):
    __tablename__ = 'users'

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(CHAR(50), nullable=False)
    email = Column(CHAR(50), nullable=False)
    password = Column(CHAR(100), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.datetime.utcnow)
    role_id = Column(Enum(UserRoles))
    # TODO: look into amazon identity management to get inspiration for model