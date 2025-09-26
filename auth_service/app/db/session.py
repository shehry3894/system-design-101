# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker  # factory for creating new Session objects.

from app.core.config import settings

# Create the SQLAlchemy engine, (Design Pattern: Singleton, single shared instance, manages the connection pool)
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,  # tells the conn pool to test a connection for liveliness before handing it out to app
    pool_size=10,  # max connections kept in pool
    max_overflow=10,  # extra temporary connections if pool is full
)

# Create a configured "Session" class, (Design Patter: Factory, creates new Session objects on demand)
SessionLocal = sessionmaker(autocommit=False,  # SQLAlchemy won’t commit automatically after each statement.
                            # You must explicitly call db.commit() when you’re ready.
                            autoflush=False,  # Won’t flush pending changes to the DB automatically before a query
                            bind=engine  # Ties this session factory to DB engine (all sessions know which DB to use).
                            )

# Factory Method (wrapping the SessionLocal() creation with lifecycle management).
def get_db():
    """
    Database dependency that provides a session and ensures it's closed.
    """
    db = SessionLocal()  # logical session object, real conn comes from the conn pool (managed by engine)
    try:
        yield db  # for dependency injection
    finally:
        db.close()  # The connection is returned to the pool, not destroyed, other sessions can reuse it
