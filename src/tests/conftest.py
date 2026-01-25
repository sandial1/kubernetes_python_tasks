"""Pytest configuration and fixtures."""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool

from src.backend.database import get_session
from src.main import app

# Create in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = Session(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db_session():
    """Create a fresh database session for each test."""
    SQLModel.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        SQLModel.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session):
    """Create a test client with overridden database dependency."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_session] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def sample_entries():
    """Sample dictionary entries for testing."""
    return [
        {"word": "python", "definition": "A high-level programming language"},
        {"word": "fastapi", "definition": "A modern web framework for building APIs"},
        {"word": "pytest", "definition": "A testing framework for Python"},
    ]
