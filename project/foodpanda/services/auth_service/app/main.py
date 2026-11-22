"""Auth service entry point: creates the FastAPI app and mounts the auth routes."""
from fastapi import FastAPI

from app.api.v1 import auth
from app.db.session import engine
from app.models import user

# Creates missing tables at startup. It never changes existing tables (new column, rename, ...),
# so models and DB can drift apart. Proper fix: schema migrations with Alembic (planned).
user.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Food Delivery System Identity Service",
    description="Handles user authentication and authorization.",
    version="1.0.0",
)
app.include_router(auth.router, prefix="/api/v1", tags=["Authentication"])


@app.get("/")
def read_root():
    return {"status": "Identity service is running"}
