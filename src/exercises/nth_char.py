def nth_char(words: list[str]) -> str:
    """
    Concatenate the nth letter from each word to construct a new word.

    Takes an array of words and returns a string where each character is
    taken from the nth position of each word, where n is the position of
    the word in the list (0-indexed).

    Args:
        words: List of words to process

    Returns:
        A new string constructed from the nth character of each word

    Example:
        >>> nth_char(["yoda", "best", "has"])
        "yes"

    Explanation:
        - n=0: take character at index 0 from "yoda" → "y"
        - n=1: take character at index 1 from "best" → "e"
        - n=2: take character at index 2 from "has" → "s"
        - Result: "yes"

    Note:
        Test cases contain valid input only (non-empty array,
        and each word has enough letters).
    """
    result = ""

    for n, word in enumerate(words):
        result += word[n]

    return result
