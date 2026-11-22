"""API shape of the login response."""
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str  # always "bearer"
