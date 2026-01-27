import sys
import os
import random
from utils.text_to_binary import ASCII_DICT


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


# Reverse mapping: decimal value to ASCII character
ASCII_CHARS = {v: k for k, v in ASCII_DICT.items()}


def generate_dynamic_key(k: int) -> str:
    """Generate a random ASCII key of length k.
    
    This function generates a dynamic key where each call produces
    a different random ASCII string.
    
    Args:
        k: Length of the key to generate
        
    Returns:
        A random ASCII string of length k
        
    Raises:
        TypeError: If k is not an integer
        ValueError: If k is less than 1
        
    Examples:
        >>> len(generate_dynamic_key(10))
        10
        >>> generate_dynamic_key(5) != generate_dynamic_key(5)  # Usually True
        True
    """
    if not isinstance(k, int):
        raise TypeError("k must be an integer")
    if k < 1:
        raise ValueError("k must be at least 1")
    
    # Generate k random ASCII characters (0-127)
    key_chars = []
    for _ in range(k):
        random_value = random.randint(0, 127)
        key_chars.append(ASCII_CHARS[random_value])
    
    return "".join(key_chars)