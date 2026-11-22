"""Route dependencies: who is calling, and are they allowed?

FastAPI's Depends() injects these into routes (dependency injection),
so routes don't build sessions or parse tokens themselves, and tests can swap them.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.crud import user as user_crud
from app.db.session import get_db
from app.models.user import User, UserRole

# Reads the token from the "Authorization: Bearer <token>" header.
# tokenUrl only tells the API docs where clients log in.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    """Decode the JWT, then load the user named in its "sub" claim. 401 if anything is wrong."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])  # also checks exp and nbf
    except JWTError:
        raise credentials_exception
    email = payload.get("sub")
    if email is None:
        raise credentials_exception

    user = user_crud.get_user_by_email(db, email=email)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(user: User = Depends(get_current_user)) -> User:
    """Reject users that were deactivated."""
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


def require_role(role: UserRole):
    """Role-based access control (RBAC): returns a dependency that allows only `role`."""

    def role_checker(user: User = Depends(get_current_active_user)) -> User:
        if user.role != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"The user does not have the required role: {role.value}",
            )
        return user

    return role_checker
