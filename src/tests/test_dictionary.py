import pytest
from exercises.dictionary import Dictionary


class TestDictionaryInit:
    """Test dictionary initialization."""

    def test_creates_empty_dictionary(self):
        """A new Dictionary should start empty."""
        d = Dictionary()
        assert d.entries == {}

    def test_multiple_instances_are_independent(self):
        """Each Dictionary instance should be independent."""
        d1 = Dictionary()
        d2 = Dictionary()
        d1.newentry("test", "definition")
        d2.newentry("test2", "definition2")
        assert "test" not in d2.entries
        assert "test2" not in d1.entries
        assert d1 is not d2


class TestNewEntry:
    """Test adding entries to the dictionary."""

    def test_add_single_entry(self):
        """Should be able to add a single word and definition."""
        d = Dictionary()
        d.newentry("Apple", "A fruit that grows on trees")
        assert "Apple" in d.entries
        assert d.entries["Apple"] == "A fruit that grows on trees"
        assert isinstance(d.entries, dict)
        assert len(d.entries) == 1
        assert list(d.entries.keys()) == ["Apple"]
        assert list(d.entries.values()) == ["A fruit that grows on trees"]

    def test_add_multiple_entries(self):
        """Should be able to add multiple different words."""
        d = Dictionary()
        d.newentry("Apple", "A fruit that grows on trees")
        d.newentry("Banana", "A yellow tropical fruit")
        assert len(d.entries) == 2
        assert d.entries["Apple"] == "A fruit that grows on trees"
        assert d.entries["Banana"] == "A yellow tropical fruit"
        assert set(d.entries.keys()) == {"Apple", "Banana"}
        assert set(d.entries.values()) == {"A fruit that grows on trees", "A yellow tropical fruit"}

    def test_overwrite_existing_entry(self):
        """Adding the same word again should overwrite the old definition."""
        d = Dictionary()
        d.newentry("Apple", "First definition")
        assert d.entries["Apple"] == "First definition"
        d.newentry("Apple", "Second definition")
        assert d.entries["Apple"] == "Second definition"
        assert len(d.entries) == 1

    def test_case_sensitive_keys(self):
        """Words should be case-sensitive (Apple vs apple are different)."""
        d = Dictionary()
        d.newentry("Apple", "Capitalized fruit")
        d.newentry("apple", "Lowercase fruit")
        assert len(d.entries) == 2
        assert d.entries["Apple"] == "Capitalized fruit"
        assert d.entries["apple"] == "Lowercase fruit"

    def test_empty_definition(self):
        """Should be able to add entries with empty definitions."""
        d = Dictionary()
        d.newentry("Word", "")
        assert d.entries["Word"] == ""

    def test_special_characters_in_word(self):
        """Should handle words with special characters."""
        d = Dictionary()
        d.newentry("hi-tech", "Advanced technology")
        assert d.entries["hi-tech"] == "Advanced technology"


class TestLook:
    """Test looking up entries in the dictionary."""

    def test_look_existing_word(self):
        """Should return the definition for existing words."""
        d = Dictionary()
        d.newentry("Apple", "A fruit that grows on trees")
        result = d.look("Apple")
        assert result == "A fruit that grows on trees"

    def test_look_nonexistent_word(self):
        """Should return error message for words not in dictionary."""
        d = Dictionary()
        result = d.look("Banana")
        assert result == "Can't find entry for Banana"

    def test_look_after_adding_multiple(self):
        """Should correctly find words among multiple entries."""
        d = Dictionary()
        d.newentry("Apple", "A fruit")
        d.newentry("Banana", "A yellow fruit")
        d.newentry("Cherry", "A red fruit")
        assert d.look("Apple") == "A fruit"
        assert d.look("Banana") == "A yellow fruit"
        assert d.look("Cherry") == "A red fruit"

    def test_look_case_sensitive(self):
        """Looking up words should be case-sensitive."""
        d = Dictionary()
        d.newentry("Apple", "Capitalized")
        assert d.look("apple") == "Can't find entry for apple"
        assert d.look("Apple") == "Capitalized"

    def test_look_empty_dictionary(self):
        """Should return error message when dictionary is empty."""
        d = Dictionary()
        result = d.look("Anything")
        assert result == "Can't find entry for Anything"

    def test_error_message_includes_word(self):
        """Error message should include the word that wasn't found."""
        d = Dictionary()
        result = d.look("UniqueWord123")
        assert "UniqueWord123" in result


class TestIntegration:
    """Test realistic usage scenarios."""

    def test_example_from_kata(self):
        """Test the exact example from the kata description."""
        d = Dictionary()
        d.newentry("Apple", "A fruit that grows on trees")
        assert d.look("Apple") == "A fruit that grows on trees"
        assert d.look("Banana") == "Can't find entry for Banana"

    def test_building_actual_dictionary(self):
        """Test building a small working dictionary."""
        d = Dictionary()
        d.newentry("Python", "A programming language")
        d.newentry("Test", "A procedure to check correctness")
        d.newentry("Dictionary", "A collection of words and definitions")

        assert d.look("Python") == "A programming language"
        assert d.look("Test") == "A procedure to check correctness"
        assert d.look("Dictionary") == "A collection of words and definitions"
        assert d.look("Java") == "Can't find entry for Java"
