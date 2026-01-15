"""API route definitions using the Dictionary class."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.backend.database import get_db, DictionaryEntry
from src.backend.models import WordEntry, WordResponse, MessageResponse
from src.exercises.dictionary import Dictionary

router = APIRouter(prefix="/api/v1", tags=["dictionary"])


def db_to_dictionary(db: Session) -> Dictionary:
    """
    Load all entries from database into a Dictionary instance.

    Args:
        db: Database session

    Returns:
        Dictionary instance populated with all entries
    """
    dictionary = Dictionary()
    entries = db.query(DictionaryEntry).all()
    for entry in entries:
        dictionary.entries[entry.word] = entry.definition
    return dictionary


def sync_dictionary_to_db(dictionary: Dictionary, db: Session):
    """
    Sync Dictionary entries back to the database.

    Args:
        dictionary: Dictionary instance
        db: Database session
    """
    # Get existing words in DB
    existing_words = {e.word for e in db.query(DictionaryEntry).all()}

    # Add or update entries
    for word, definition in dictionary.entries.items():
        if word in existing_words:
            # Update existing
            entry = (
                db.query(DictionaryEntry).filter(DictionaryEntry.word == word).first()
            )
            entry.definition = definition
        else:
            # Create new
            db_entry = DictionaryEntry(word=word, definition=definition)
            db.add(db_entry)

    db.commit()


@router.post("/newentry", response_model=WordResponse, status_code=201)
def create_entry(entry: WordEntry, db: Session = Depends(get_db)):
    """
    Add a new word and its definition to the dictionary.

    Args:
        entry: WordEntry containing word and definition

    Returns:
        The created entry

    Raises:
        HTTPException: If word already exists
    """
    # Load dictionary from DB
    dictionary = db_to_dictionary(db)

    # Check if word already exists
    if entry.word in dictionary.entries:
        raise HTTPException(
            status_code=400, detail=f"Entry for '{entry.word}' already exists"
        )

    # Use Dictionary class to add entry
    dictionary.newentry(entry.word, entry.definition)

    # Sync back to database
    sync_dictionary_to_db(dictionary, db)

    return WordResponse(word=entry.word, definition=entry.definition)


@router.get("/look/{word}", response_model=WordResponse)
def get_entry(word: str, db: Session = Depends(get_db)):
    """
    Look up a word in the dictionary.

    Args:
        word: The word to look up

    Returns:
        The word and its definition

    Raises:
        HTTPException: If word not found
    """
    # Load dictionary from DB
    dictionary = db_to_dictionary(db)

    # Use Dictionary class to look up word
    result = dictionary.look(word)

    # Check if it's an error message
    if result.startswith("Can't find entry for"):
        raise HTTPException(status_code=404, detail=result)

    return WordResponse(word=word, definition=result)


@router.get("/entries", response_model=list[WordResponse])
def list_entries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    List all dictionary entries.

    Args:
        skip: Number of entries to skip
        limit: Maximum number of entries to return

    Returns:
        List of all entries
    """
    # Load dictionary from DB
    dictionary = db_to_dictionary(db)

    # Convert to list and apply pagination
    entries_list = [
        WordResponse(word=word, definition=definition)
        for word, definition in dictionary.entries.items()
    ]

    return entries_list[skip : skip + limit]


@router.delete("/entries/{word}", response_model=MessageResponse)
def delete_entry(word: str, db: Session = Depends(get_db)):
    """
    Delete a word from the dictionary.

    Args:
        word: The word to delete

    Returns:
        Success message

    Raises:
        HTTPException: If word not found
    """
    # Check if entry exists
    entry = db.query(DictionaryEntry).filter(DictionaryEntry.word == word).first()
    if not entry:
        raise HTTPException(status_code=404, detail=f"Can't find entry for {word}")

    # Delete from database
    db.delete(entry)
    db.commit()

    return MessageResponse(message=f"Entry for '{word}' deleted successfully")
