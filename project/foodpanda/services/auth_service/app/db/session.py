"""Database connection: one engine (with a connection pool) and a session per request."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# One engine per process. It owns the connection pool.
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # test a connection before using it, so dropped connections are replaced
    pool_size=10,  # connections kept open in the pool
    max_overflow=10,  # extra temporary connections when all 10 are busy
)

# A factory for sessions. autocommit/autoflush off: nothing is written until db.commit().
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    """FastAPI dependency: one session per request, always closed afterwards."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # gives the connection back to the pool
