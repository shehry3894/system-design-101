"""API shapes for users (Pydantic): what clients send and receive. Validation happens here."""
from typing import Self

from pydantic import BaseModel, ConfigDict, EmailStr, model_validator

from app.models.user import UserRole


class UserBase(BaseModel):
    email: EmailStr
    role: UserRole = UserRole.CUSTOMER


class UserCreate(UserBase):
    """Request body for /register."""

    password: str
    password_repeat: str

    @model_validator(mode="after")  # runs after the single fields are validated
    def check_passwords_match(self) -> Self:
        if self.password != self.password_repeat:
            raise ValueError("Passwords do not match")
        return self


class User(UserBase):
    """Response body: no password fields."""

    model_config = ConfigDict(from_attributes=True)  # build directly from a SQLAlchemy User object

    id: int
    is_active: bool
