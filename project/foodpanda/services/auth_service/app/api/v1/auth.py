# app/api/v1/auth.py
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas import user as user_schema, token as token_schema
from app.crud import user as user_crud
from app.core import security
from app.core.config import settings
from app.api import deps
from app.db.session import get_db
from app.models.user import User, UserRole

# Creates a mini-router object where we can register endpoints (@router.get, @router.post, etc.)
router = APIRouter()  # FastAPI’s way of modularizing routes and later plug in main app


@router.post("/register", response_model=user_schema.User)
def register_user(user_in: user_schema.UserCreate,
                  db: Session = Depends(get_db)
                  ):
    """
    Register a new user.
    Roles can be specified during creation (e.g., customer, restaurant).
    """
    user = user_crud.get_user_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    return user_crud.create_user(db=db, user=user_in)


@router.post("/token", response_model=token_schema.Token)
def login_for_access_token(db: Session = Depends(get_db),
                           form_data: OAuth2PasswordRequestForm = Depends()
                           # OAuth2PasswordRequestForm makes form data
                           # (username, password, scope (optional, "read write admin"),
                           # client_id (optional),
                           # client_secret (optional), Only for confidential clients like backend servers)
                           # compatible with OAuth2 flows.
                           ):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = user_crud.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=user_schema.User)
def read_users_me(user: User = Depends(deps.get_curr_active_user)):
    """
    Fetch the curr logged-in user.
    """
    return user


@router.get("/admin/dashboard")
def admin_dashboard(current_user: User = Depends(deps.require_role(UserRole.ADMIN))):
    return {
        "message": f"Welcome, {current_user.email}"
    }
