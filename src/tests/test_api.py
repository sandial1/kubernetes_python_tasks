import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine

from src.main import app
from src.backend.database import get_session

# 1. Setup an in-memory database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = Session(autocommit=False, autoflush=False, bind=engine)


# 2. Dependency override to use the test database
def override_get_session():
    with TestingSessionLocal as session:
        yield session


app.dependency_overrides[get_session] = override_get_session
client = TestClient(app)


@pytest.fixture(autouse=True)
def setup_db():
    """Create tables before each test and drop them after."""
    SQLModel.metadata.create_all(bind=engine)
    yield
    SQLModel.metadata.drop_all(bind=engine)


class TestDictionaryAPI:
    """Test suite for Dictionary API endpoints."""

    def test_create_entry(self):
        """Test the POST /api/v1/newentry endpoint."""
        response = client.post(
            "/api/v1/newentry",
            json={"word": "python", "definition": "A programming language"},
        )
        assert response.status_code == 201
        assert response.json()["word"] == "python"

    def test_look_existing_word(self):
        """Test the GET /api/v1/look/{word} endpoint."""
        # First, seed the data
        client.post(
            "/api/v1/newentry",
            json={"word": "fastapi", "definition": "A web framework"},
        )

        response = client.get("/api/v1/look/fastapi")
        assert response.status_code == 200
        assert response.json()["definition"] == "A web framework"

    def test_look_nonexistent_word(self):
        """Test looking up a word that doesn't exist."""
        response = client.get("/api/v1/look/nonexistent")
        assert response.status_code == 404
        assert "Can't find entry" in response.json()["detail"]

    def test_duplicate_entry(self):
        """Test that adding the same word twice returns a 400 error."""
        data = {"word": "unique", "definition": "test"}
        client.post("/api/v1/newentry", json=data)
        response = client.post("/api/v1/newentry", json=data)
        assert response.status_code == 400

    def test_list_entries(self):
        """Test the GET /api/v1/entries pagination."""
        client.post("/api/v1/newentry", json={"word": "a", "definition": "1"})
        client.post("/api/v1/newentry", json={"word": "b", "definition": "2"})

        response = client.get("/api/v1/entries?limit=1")
        assert response.status_code == 200
        assert len(response.json()) == 1

    def test_delete_entry(self):
        """Test the DELETE /api/v1/entries/{word} endpoint."""
        client.post("/api/v1/newentry", json={"word": "gone", "definition": "bye"})
        response = client.delete("/api/v1/entries/gone")
        assert response.status_code == 200

        # Verify it's actually gone
        get_response = client.get("/api/v1/look/gone")
        assert get_response.status_code == 404
    
    def test_delete_entry_not_found(self):
        """Test the DELETE /api/v1/entries/{word} endpoint for not found entries."""        
        response = client.delete("/api/v1/entries/test")
        assert response.status_code == 404
        assert "Can't find entry" in response.json()["detail"]
