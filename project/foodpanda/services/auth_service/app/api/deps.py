# app/api/deps.py
# Design Pattern: Dependency Injection
# Injects DB sessions, security utilities, and configurations into routes.
# Benefit:
# 1. Reduces tight coupling.
# 2. Makes endpoints easier to test (you can inject mock dependencies).
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import JWTError, jwt

from app.db.session import get_db
from app.core.config import settings
from app.schemas.token import TokenData
from app.crud import user as user_crud
from app.models.user import User, UserRole

# This defines the security scheme. The tokenUrl is the endpoint for getting the token.
# A bridge between FastAPI and the raw JWT in the request header.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")


# Validate user
def get_curr_user(db: Session = Depends(get_db),
                     token: str = Depends(oauth2_scheme)  # automatically extracted JWT from the request.
                     ) -> User:
    """
    Dependency to get the curr user from a JWT token.
    Decodes the token, validates the user, and returns the user object.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # TODO: impl a func to get required key for non-HS256 algorithms as well
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(sub=email)
    except JWTError:
        raise credentials_exception

    curr_user = user_crud.get_user_by_email(db, email=token_data.sub)
    if curr_user is None:
        raise credentials_exception
    return curr_user


def get_curr_active_user(curr_user: User = Depends(get_curr_user)) -> User:
    """Dependency to check if the user is active."""
    if not curr_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return curr_user


# Role-based access control (RBAC)
def require_role(role: UserRole):
    """Dependency factory to require a specific user role."""

    def role_checker(curr_user: User = Depends(get_curr_active_user)) -> User:
        if curr_user.role != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"The user does not have the required role: {role.value}",
            )
        return curr_user

    return role_checker
