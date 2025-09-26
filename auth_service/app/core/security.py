# app/core/security.py
from datetime import datetime, timedelta, timezone

from passlib.context import CryptContext  # password hashing/verification with different algorithms.
from jose import JWTError, jwt

from app.core.config import settings

# Setup password hashing context for whole app.
pwd_context = CryptContext(
    schemes=["bcrypt"],  # bcrypt as the hashing algorithm (industry standard for password storage)
    deprecated="auto"
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plain password against a hashed one."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hashes a plain password."""
    # diff each time even in case of same password, because bcrypt generates a new salt each time
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """Creates a JWT access token."""
    to_encode = data.copy()  # e.g {"sub": user.email}

    utc_now = datetime.now(timezone.utc)
    if expires_delta:
        expire = utc_now + expires_delta
    else:
        expire = utc_now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({
        "exp": expire,
        "iat": utc_now,  # Issued at
        "nbf": utc_now  # Not valid before, ensures token can’t be used prematurely
    })

    secret_key = settings.SECRET_KEY
    if not settings.ALGORITHM.startswith("HS"):  # starts with # RS256, ES256, etc.
        with open(settings.PRIVATE_KEY_PATH) as f:
            secret_key = f.read()

    encoded_jwt = jwt.encode(to_encode,
                             secret_key,
                             algorithm=settings.ALGORITHM)

    return encoded_jwt
