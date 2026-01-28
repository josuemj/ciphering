from utils.ciphers.caesar import caesar_encrypt


def rot13(message: str, alphabet: list) -> str:
    """
    Applies ROT13 to the given message.
    ROT13 is a special case of Caesar cipher with a fixed shift of 13.
    Applying rot13 twice returns the original message.

    Parameters:
    - message (str): The input text.
    - alphabet (list): The list of characters representing the alphabet to be used.
    Returns:
    - str: The ROT13-transformed text.

    sample usage:
    >>> rot13("hello", list("abcdefghijklmnopqrstuvwxyz"))
    'uryyb'
    """
    return caesar_encrypt(message, 13, alphabet)
