"""Auth endpoints: register, log in (get a JWT), read yourself, admin-only check."""
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api import deps
from app.core import security
from app.core.config import settings
from app.crud import user as user_crud
from app.db.session import get_db
from app.models.user import User, UserRole
from app.schemas import token as token_schema
from app.schemas import user as user_schema

router = APIRouter()  # a group of routes; main.py mounts it under /api/v1


@router.post("/register", response_model=user_schema.User)
def register_user(user_in: user_schema.UserCreate, db: Session = Depends(get_db)):
    """Create a user. The caller picks the role (known gap: this includes "admin")."""
    if user_crud.get_user_by_email(db, email=user_in.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return user_crud.create_user(db=db, user=user_in)


@router.post("/token", response_model=token_schema.Token)
def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    """OAuth2 password flow: form fields `username` (our email) and `password` in, access token out."""
    user = user_crud.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",  # same message for both cases: don't reveal which emails exist
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=user_schema.User)
def read_users_me(user: User = Depends(deps.get_current_active_user)):
    """Return the logged-in user."""
    return user


@router.get("/admin/dashboard")
def admin_dashboard(user: User = Depends(deps.require_role(UserRole.ADMIN))):
    """Admins only (403 for everyone else)."""
    return {"message": f"Welcome, {user.email}"}
