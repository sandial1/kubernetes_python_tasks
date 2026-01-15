"""Pydantic models for API request/response validation."""

from pydantic import BaseModel


class WordEntry(BaseModel):
    word: str
    definition: str


class WordResponse(BaseModel):
    word: str
    definition: str


class MessageResponse(BaseModel):
    message: str
