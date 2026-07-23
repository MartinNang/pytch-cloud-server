import enum
from sqlalchemy import Integer, Enum, Column

from db.database import Base


class UserRoles(enum.Enum):
    USER = "user"
    EDUCATOR = "educator"
    ADMIN = "admin"

# class UserRole(Base):
#     __tablename__ = 'user_roles'
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     value = Column(Enum(UserRoles), unique=True, nullable=False)
