from typing import Optional

from sqlmodel import Field, SQLModel


class WordBase(SQLModel):
    word: str = Field(unique=True, index=True)
    definition: str


class DictionaryEntry(WordBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class WordResponse(WordBase):
    pass
