# app/crud/user.py
# Design Pattern: Repository / Data Access Layer Pattern (CRUD Layer)
# abstracting raw SQLAlchemy queries behind functions like get_user_by_email, create_user.
# Decouples business logic (API) from data persistence.
# Benefit:
# 1. Decouples business logic (API) from data persistence.
# 2. Makes it easy to switch DBs (Postgres → MySQL) without touching API code.
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


def get_user_by_email(db: Session, email: str) -> User | None:
    """Fetches a user by their email address."""
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, user: UserCreate) -> User:
    """Creates a new user in the database."""
    hashed_password = get_password_hash(user.password)
    db_user = User(
        email=user.email,
        hashed_password=hashed_password,
        role=user.role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
