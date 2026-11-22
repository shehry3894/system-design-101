"""Database tables (SQLAlchemy models). Schemas in app/schemas define the API shape instead."""
import enum

from sqlalchemy import Boolean, Column, Enum, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()  # every model inherits from this; create_all() makes their tables


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"
    RESTAURANT = "restaurant"
    DRIVER = "driver"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)  # a primary key is indexed automatically
    email = Column(String, unique=True, nullable=False)  # unique also creates an index: fast lookup by email
    hashed_password = Column(String, nullable=False)  # never the plain password
    role = Column(Enum(UserRole), nullable=False, default=UserRole.CUSTOMER)  # DB accepts only these values
    is_active = Column(Boolean, default=True)
