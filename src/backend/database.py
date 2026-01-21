"""Database connection and session management."""

import logging
import time

from sqlalchemy import Column, Integer, String, Text, create_engine, exc
from sqlalchemy.orm import Session, declarative_base, sessionmaker
from src.backend.config import settings

from src.backend.config import settings

# Setup logging to see retry attempts in 'kubectl logs'
logger = logging.getLogger(__name__)

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

# Use pool_pre_ping to liveness check connections
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    pool_size=10,
    max_overflow=5,
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    """Initialize database with retries for Kubernetes resilience."""
    max_retries = 5
    retry_delay = 5
    
    for i in range(max_retries):
        try:
            logger.info(f"Connecting to database (attempt {i+1}/{max_retries})...")
            # This creates the tables if they don't exist
            Base.metadata.create_all(bind=engine)
            logger.info("Database initialized successfully.")
            break
        except exc.OperationalError as e:
            if i == max_retries - 1:
                logger.error("Could not connect to database after max retries.")
                raise e
            logger.warning(f"Database not ready, retrying in {retry_delay}s...")
            time.sleep(retry_delay)

class DictionaryEntry(Base):
    """SQLAlchemy model for dictionary entries."""

    __tablename__ = "dictionary_entries"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(255), unique=True, index=True, nullable=False)
    definition = Column(Text, nullable=False)


def get_db():
    """Dependency to get database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
