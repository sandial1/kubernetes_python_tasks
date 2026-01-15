"""Tests for the Dictionary class."""

import pytest
from src.exercises.dictionary import Dictionary


class TestDictionary:
    """Test suite for Dictionary class."""

    def test_init(self):
        """Test dictionary initialization."""
        dictionary = Dictionary()
        assert dictionary.entries == {}

    def test_newentry_single(self):
        """Test adding a single entry."""
        dictionary = Dictionary()
        dictionary.newentry("python", "A programming language")

        assert "python" in dictionary.entries
        assert dictionary.entries["python"] == "A programming language"

    def test_newentry_multiple(self):
        """Test adding multiple entries."""
        dictionary = Dictionary()
        dictionary.newentry("python", "A programming language")
        dictionary.newentry("java", "Another programming language")

        assert len(dictionary.entries) == 2
        assert dictionary.entries["python"] == "A programming language"
        assert dictionary.entries["java"] == "Another programming language"

    def test_newentry_overwrite(self):
        """Test that newentry overwrites existing entries."""
        dictionary = Dictionary()
        dictionary.newentry("python", "First definition")
        dictionary.newentry("python", "Second definition")

        assert dictionary.entries["python"] == "Second definition"
        assert len(dictionary.entries) == 1

    def test_look_existing_word(self):
        """Test looking up an existing word."""
        dictionary = Dictionary()
        dictionary.newentry("python", "A programming language")

        result = dictionary.look("python")
        assert result == "A programming language"

    def test_look_nonexistent_word(self):
        """Test looking up a non-existent word."""
        dictionary = Dictionary()

        result = dictionary.look("nonexistent")
        assert result == "Can't find entry for nonexistent"

    def test_look_after_multiple_entries(self):
        """Test looking up words after adding multiple entries."""
        dictionary = Dictionary()
        dictionary.newentry("python", "A programming language")
        dictionary.newentry("java", "Another programming language")

        assert dictionary.look("python") == "A programming language"
        assert dictionary.look("java") == "Another programming language"
        assert dictionary.look("ruby") == "Can't find entry for ruby"

    def test_empty_word(self):
        """Test adding and looking up empty string."""
        dictionary = Dictionary()
        dictionary.newentry("", "Empty word definition")

        assert dictionary.look("") == "Empty word definition"

    def test_empty_definition(self):
        """Test adding empty definition."""
        dictionary = Dictionary()
        dictionary.newentry("word", "")

        assert dictionary.look("word") == ""

    def test_case_sensitivity(self):
        """Test that dictionary is case-sensitive."""
        dictionary = Dictionary()
        dictionary.newentry("Python", "Capitalized")
        dictionary.newentry("python", "Lowercase")

        assert dictionary.look("Python") == "Capitalized"
        assert dictionary.look("python") == "Lowercase"
        assert len(dictionary.entries) == 2
