# app/main.py
from fastapi import FastAPI
from app.api.v1 import auth
from app.db.session import engine
from app.models import user

user.Base.metadata.create_all(bind=engine)
# tells SQLAlchemy to look at all models inheriting from Base (like User in user.py)
# and create the tables in the database if they don’t already exist.
# cons:
# Does not handle changes to existing tables (e.g., adding a column, renaming a column, changing constraints).
# If you change your models, create_all() won’t automatically migrate your DB schema — it just skips existing tables
# That means you’d end up with models and DB schema out of sync.
# TODO: Use Alembic for database migrations, a git for DB schema. why?


app = FastAPI(
    title="Food Delivery System Identity Service",
    description="Handles user authentication and authorization.",
    version="1.0.0"
)

# Include the API router
app.include_router(auth.router, prefix="/api/v1", tags=["Authentication"])


@app.get("/")
def read_root():
    return {"status": "Identity service is running"}
