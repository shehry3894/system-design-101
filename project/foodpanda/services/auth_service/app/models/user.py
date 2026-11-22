# app/models/user.py
# DB representation (SQLAlchemy)
# Represents the database table structure
# Defines columns, constraints, and relationships
# CRUD operations with DB
import enum
from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()  # returns a base class that ORM models will inherit from


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    CUSTOMER = "customer"
    RESTAURANT = "restaurant"
    DRIVER = "driver"


class User(Base):  # now SQLAlchemy knows it’s a table
    __tablename__ = "users"  # table name in DB

    id = Column(Integer,
                primary_key=True,
                index=True  # BP: For primary keys, this is redundant because DBs automatically index primary keys
                # same as `CREATE UNIQUE INDEX users_pkey ON users(id);`
                )
    email = Column(String,
                   unique=True,
                   index=True,  # BP: unique=True already creates a unique index behind the scenes.
                   # same as `CREATE UNIQUE INDEX users_email_key ON users(email);`
                   nullable=False)
    # 2 indexes total (one for id, one for email).

    hashed_password = Column(String, nullable=False)
    role = Column(
        Enum(UserRole),  # Tells SQLAlchemy to store values from a Python Enum class, DB col will only accept those val
        nullable=False,
        default=UserRole.CUSTOMER)
    is_active = Column(Boolean(), default=True)
