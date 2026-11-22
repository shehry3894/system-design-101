# app/schemas/user.py
# API data representation (Pydantic).
# Represents the shape of data you send/receive via API (request & response).
# Does validation and serialization.
from typing_extensions import Self
from pydantic import BaseModel, EmailStr, model_validator

from app.models.user import UserRole


# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    role: UserRole = UserRole.CUSTOMER


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str
    password_repeat: str

    @model_validator(mode='after')  # run "after" the whole model has been validated
    def check_passwords_match(self) -> Self:
        if self.password != self.password_repeat:
            raise ValueError('Passwords do not match')
        return self


# Properties to return to client
class User(UserBase):
    id: int
    is_active: bool

    class Config:
        from_attributes = True  # allows creating this schema directly from SQLAlchemy ORM objects without manually converting them.
        # db_user = db.query(UserModel).first()
        # return User.model_validate(db_user)   # works because of from_attributes=True


# for PATCH/PUT endpoints.
class UserUpdate(BaseModel):
    email: EmailStr | None = None
    role: UserRole | None = None
    password: str | None = None

    @model_validator(mode="after")
    # no @classmethod decorator? @model_validator turns it into a class-level validator.
    def at_least_one_field(cls, values):
        if not any(values.dict().values()):  # safer
            raise ValueError("At least one field must be provided for update")
        return values
