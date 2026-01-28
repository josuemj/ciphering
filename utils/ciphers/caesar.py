

def caesar_encrypt(text : str, shift: int, alphabet : list) -> str:
    
    """
    Encrypts or decrypts a given text using the Caesar cipher method.
    Parameters:
    - text (str): The input text to be encrypted or decrypted.
    - shift (int): The number of positions to shift each character in the alphabet.
    - alphabet (list): The list of characters representing the alphabet to be used.
    Returns:
    - str: The resulting encrypted or decrypted text.
    
    sample usage:
    >>> caesar_encrypt("hello", 3, list("abcdefghijklmnopqrstuvwxyz"))
    'khoor'
    """
    result = ""
    
    for char in text:
        if char in alphabet:
            index = alphabet.index(char)
            shifted_index = (index + shift) % len(alphabet)
            result += alphabet[shifted_index]
        else:
            result += char
        
    return result