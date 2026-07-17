import datetime
import uuid

from sqlalchemy import Column, TIMESTAMP
from sqlalchemy.dialects.postgresql import CHAR

from db.database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(CHAR(50), nullable=False)
    email = Column(CHAR(50), nullable=False)
    password = Column(CHAR(100), nullable=False)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.datetime.utcnow)
    authorisations = Column(CHAR(50), nullable=False)
    # TODO: look into amazon identity management to get inspiration for model