
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