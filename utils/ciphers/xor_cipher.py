def xor_cipher(text: str, key: str) -> str:
    """Perform XOR cipher between text and key.
    
    XOR each character of the text with the corresponding character
    of the key. If the key is shorter than the text, it repeats cyclically.
    
    Args:
        text: The plaintext or ciphertext to process
        key: The key for XOR operation
        
    Returns:
        XOR'd string result
        
    Raises:
        TypeError: If text or key is not a string
        ValueError: If key is empty
    """
    if not isinstance(text, str) or not isinstance(key, str):
        raise TypeError("text and key must be strings")
    if len(key) == 0:
        raise ValueError("key cannot be empty")
    
    result = []
    key_length = len(key)
    
    for i, t_char in enumerate(text):
        k_char = key[i % key_length]  # Cycle through key
        xor_value = ord(t_char) ^ ord(k_char)
        result.append(chr(xor_value))
    
    return "".join(result)