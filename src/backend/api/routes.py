"""API route definitions using direct database access."""

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from src.backend.database import SessionDep
from src.backend.models import DictionaryEntry, WordBase, WordResponse

router = APIRouter(prefix="/api/v1", tags=["dictionary"])


@router.post("/newentry", response_model=WordResponse, status_code=201)
def create_entry(entry: WordBase, db: SessionDep):
    """Add a new word directly to the DB."""
    statement = select(DictionaryEntry).where(DictionaryEntry.word == entry)
    db_entry = db.exec(statement).first()
    if db_entry:
        raise HTTPException(
            status_code=400, detail=f"Entry for '{entry.word}' already exists"
        )

    new_db_entry = DictionaryEntry(word=entry.word, definition=entry.definition)
    db.add(new_db_entry)
    db.commit()
    db.refresh(new_db_entry)
    return new_db_entry


@router.get("/look/{word}", response_model=WordResponse)
def get_entry(word: str, db: SessionDep):
    """Look up a word using a DB index."""
    entry = db.exec(DictionaryEntry).filter(DictionaryEntry.word == word).first()

    if not entry:
        raise HTTPException(status_code=404, detail=f"Can't find entry for {word}")

    return entry


@router.get("/entries", response_model=list[WordResponse])
def list_entries(db: SessionDep, skip: int = 0, limit: int = 100):
    """
    List entries using server-side pagination.
    This prevents the API from hanging by only fetching a small slice of data.
    """
    return db.exec(DictionaryEntry).offset(skip).limit(limit).all()


@router.delete("/entries/{word}")
def delete_entry(word: str, db: SessionDep):
    """Delete a word directly from the database."""
    entry = db.exec(DictionaryEntry).filter(DictionaryEntry.word == word).first()

    if not entry:
        raise HTTPException(status_code=404, detail=f"Can't find entry for {word}")

    db.delete(entry)
    db.commit()

    return {"word": word, "message": f"Entry for '{word}' deleted successfully"}
