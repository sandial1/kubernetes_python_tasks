import pytest
from exercises.nth_char import nth_char


class TestBasicFunctionality:
    """Test basic nth character extraction."""

    def test_example_from_kata(self):
        """Test the exact example from the kata description."""
        result = nth_char(["yoda", "best", "has"])
        assert result == "yes"

    def test_single_word(self):
        """Should work with a single word (take first character)."""
        result = nth_char(["hello"])
        assert result == "h"

    def test_two_words(self):
        """Should work with two words."""
        result = nth_char(["ab", "cd"])
        # n=0: "ab"[0] = "a"
        # n=1: "cd"[1] = "d"
        assert result == "ad"

    def test_four_words(self):
        """Should work with multiple words."""
        result = nth_char(["abcd", "efgh", "ijkl", "mnop"])
        # n=0: "abcd"[0] = "a"
        # n=1: "efgh"[1] = "f"
        # n=2: "ijkl"[2] = "k"
        # n=3: "mnop"[3] = "p"
        assert result == "afkp"


class TestDifferentWordLengths:
    """Test with words of various lengths."""

    def test_words_with_exact_length(self):
        """Words where each word length equals its position + 1."""
        result = nth_char(["a", "bc", "def"])
        # n=0: "a"[0] = "a"
        # n=1: "bc"[1] = "c"
        # n=2: "def"[2] = "f"
        assert result == "acf"

    def test_long_words(self):
        """Should work with longer words."""
        result = nth_char(["programming", "development", "testing"])
        # n=0: "programming"[0] = "p"
        # n=1: "development"[1] = "e"
        # n=2: "testing"[2] = "s"
        assert result == "pes"

    def test_words_much_longer_than_needed(self):
        """Should work when words are much longer than required index."""
        result = nth_char(["alphabet", "beautiful", "catastrophe"])
        # n=0: "alphabet"[0] = "a"
        # n=1: "beautiful"[1] = "e"
        # n=2: "catastrophe"[2] = "t"
        assert result == "aet"


class TestCaseSensitivity:
    """Test that case is preserved correctly."""

    def test_uppercase_letters(self):
        """Should preserve uppercase letters."""
        result = nth_char(["YODA", "BEST", "HAS"])
        assert result == "YES"

    def test_mixed_case(self):
        """Should preserve mixed case correctly."""
        result = nth_char(["Apple", "bAnana", "chErry"])
        # n=0: "Apple"[0] = "A"
        # n=1: "bAnana"[1] = "A"
        # n=2: "chErry"[2] = "E"
        assert result == "AAE"

    def test_lowercase(self):
        """Should handle lowercase correctly."""
        result = nth_char(["cat", "dog", "rat"])
        # n=0: "cat"[0] = "c"
        # n=1: "dog"[1] = "o"
        # n=2: "rat"[2] = "t"
        assert result == "cot"


class TestSpecialCharacters:
    """Test words containing numbers and special characters."""

    def test_words_with_numbers(self):
        """Should handle words containing numbers."""
        result = nth_char(["a1b", "c2d", "e3f"])
        # n=0: "a1b"[0] = "a"
        # n=1: "c2d"[1] = "2"
        # n=2: "e3f"[2] = "f"
        assert result == "a2f"

    def test_words_with_special_chars(self):
        """Should handle special characters."""
        result = nth_char(["h@llo", "w#rld", "t$st"])
        # n=0: "h@llo"[0] = "h"
        # n=1: "w#rld"[1] = "#"
        # n=2: "t$st"[2] = "s"
        assert result == "h#s"

    def test_words_with_spaces_and_punctuation(self):
        """Should handle spaces and punctuation if they exist."""
        result = nth_char(["a-b", "c.d", "e!f"])
        # n=0: "a-b"[0] = "a"
        # n=1: "c.d"[1] = "."
        # n=2: "e!f"[2] = "f"
        assert result == "a.f"


class TestRealWorldScenarios:
    """Test with realistic word combinations."""

    def test_sentence_words(self):
        """Test with common English words."""
        result = nth_char(["twice", "award", "olive", "catch", "nerve"])
        # n=0: "twice"[0] = "t"
        # n=1: "award"[1] = "w"
        # n=2: "olive"[2] = "i"
        # n=3: "catch"[3] = "c"
        # n=4: "nerve"[4] = "e"
        assert result == "twice"

    def test_programming_terms(self):
        """Test with programming-related words."""
        result = nth_char(["function", "variable", "constant"])
        # n=0: "function"[0] = "f"
        # n=1: "variable"[1] = "a"
        # n=2: "constant"[2] = "n"
        assert result == "fan"

    def test_five_word_sentence(self):
        """Test with five words."""
        result = nth_char(["apple", "banana", "cherry", "dragon", "elephant"])
        # n=0: "apple"[0] = "a"
        # n=1: "banana"[1] = "a"
        # n=2: "cherry"[2] = "e"
        # n=3: "dragon"[3] = "g"
        # n=4: "elephant"[4] = "h"
        assert result == "aaegh"


class TestEmptyInput:
    """Test edge case with empty input."""

    def test_empty_list(self):
        """Should return empty string for empty list."""
        result = nth_char([])
        assert result == ""


class TestVerifyIndexing:
    """Verify the indexing logic is correct."""

    def test_position_zero(self):
        """First word uses index 0."""
        result = nth_char(["abc"])
        assert result == "a"

    def test_position_one(self):
        """Second word uses index 1."""
        result = nth_char(["x", "abc"])
        # n=0: "x"[0] = "x"
        # n=1: "abc"[1] = "b"
        assert result == "xb"

    def test_position_two(self):
        """Third word uses index 2."""
        result = nth_char(["x", "xy", "abc"])
        # n=0: "x"[0] = "x"
        # n=1: "xy"[1] = "y"
        # n=2: "abc"[2] = "c"
        assert result == "xyc"

    def test_sequential_positions(self):
        """Verify each position increments correctly."""
        result = nth_char(["0123456", "0123456", "0123456", "0123456"])
        # n=0: [0] = "0"
        # n=1: [1] = "1"
        # n=2: [2] = "2"
        # n=3: [3] = "3"
        assert result == "0123"
