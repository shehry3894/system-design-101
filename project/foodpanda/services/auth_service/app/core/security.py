"""Password hashing and JWT creation."""
from datetime import datetime, timedelta, timezone

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

# bcrypt: a slow, salted hash, so stolen hashes are hard to crack.
# (OWASP's first choice today is Argon2id; bcrypt is still acceptable.)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    # A new random salt each time: the same password gives a different hash.
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Sign a JWT with `data` (e.g. {"sub": email}) plus exp, iat and nbf times."""
    now = datetime.now(timezone.utc)
    claims = {
        **data,
        "exp": now + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)),  # expires at
        "iat": now,  # issued at
        "nbf": now,  # not valid before
    }
    return jwt.encode(claims, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
