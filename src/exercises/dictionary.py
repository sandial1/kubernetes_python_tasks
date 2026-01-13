"""A simple dictionary class that stores word definitions."""


class Dictionary:
    def __init__(self):
        self.entries = {}

    def newentry(self, word: str, definition: str) -> None:
        """
        Add a new word and its definition to the dictionary.

        Args:
            word: The word to add
            definition: The definition of the word
        """
        self.entries[word] = definition

    def look(self, word: str) -> str:
        """
        Look up a word in the dictionary.

        Args:
            word: The word to look up

        Returns:
            The definition if found, or an error message:
            Can't find entry for {word} if not found.
        """
        if word in self.entries:
            return self.entries[word]
        return f"Can't find entry for {word}"
