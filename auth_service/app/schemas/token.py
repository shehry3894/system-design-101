# app/schemas/token.py
from pydantic import BaseModel


# To return to the client after login (e.g., JWT and type).
class Token(BaseModel):
    access_token: str
    token_type: str


# To extract from the token payload after decoding (e.g., the user’s email).
class TokenData(BaseModel):
    sub: str | None = None  # can hold email, user_id, etc.
