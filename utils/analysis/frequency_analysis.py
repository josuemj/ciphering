
"""
Module for performing frequency analysis on textual data
Let:
    - English alphabet
"""

from ..ciphers.caesar import caesar_encrypt


def frequency_analysis(text: str) -> dict:
    """
    Analyzes the frequency of each letter in the given text.

    Parameters:
    - text (str): The input text to analyze.

    Returns:
    - dict: A dictionary with letters as keys and their frequencies as values.

    sample usage:
    >>> frequency_analysis("hello world")
    {'h': 1, 'e': 1, 'l': 3, 'o': 2, ' ': 1, 'w': 1, 'r': 1, 'd': 1}
    """
    frequency = {}
    for char in text:
        if char.isalpha():  # Consider only alphabetic characters
            char = char.lower()  # Normalize to lowercase
            if char in frequency:
                frequency[char] += 1
            else:
                frequency[char] = 1
    return frequency

# Example usage

phrase = "The library was silent except for the faint, rhythmic turning of pages. Students sat hunched over weathered books, deep in thought as they prepared for their final exams. A single shaft of light pierced through the tall, dusty windows, illuminating dancing specks of dust that seemed to move in time with the quiet scratching of pencils. Outside, the world continued its frantic pace, but within these walls, time felt suspended in a sea of ink and parchment."

caesar_shifted_phrase = caesar_encrypt(phrase, 3, list("abcdefghijklmnopqrstuvwxyz "))

print("Original Phrase Frequency Analysis:")

print(frequency_analysis(phrase))