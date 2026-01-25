"""Database connection and session management."""

import logging
import time
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import exc
from sqlmodel import Session, SQLModel, create_engine

from src.backend.config import settings

# Setup logging to see retry attempts in 'kubectl logs'
logger = logging.getLogger(__name__)

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=10,
    max_overflow=5,
    pool_timeout=30,
    echo=False,
)


def get_session():
    with Session(autocommit=False, autoflush=False, bind=engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]


def init_db():
    """Initialize database with retries for Kubernetes resilience."""
    max_retries = 5
    retry_delay = 5

    for i in range(max_retries):
        try:
            logger.info(f"Connecting to database (attempt {i + 1}/{max_retries})...")
            SQLModel.metadata.create_all(engine)
            logger.info("Database initialized successfully.")
            break
        except exc.OperationalError as e:
            if i == max_retries - 1:
                logger.error("Could not connect to database after max retries.")
                raise e
            logger.warning(f"Database not ready, retrying in {retry_delay}s...")
            time.sleep(retry_delay)
