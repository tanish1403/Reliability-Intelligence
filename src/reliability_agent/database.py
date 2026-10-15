"""SQLAlchemy database session and engine setup."""

import os
from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session

# Use SQLite for local testing/default if DATABASE_URL not set, supporting PostgreSQL in production/docker
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./reliability.db")

# For SQLite, connect_args is needed for threading; for PostgreSQL, it is omitted
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """Dependency that provides a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

