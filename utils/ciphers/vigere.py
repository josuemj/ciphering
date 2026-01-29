def vigere_encrypt(text: str, key: str, alphabet: list) -> str:
    """
    Encrypts the given text using the Vigenère cipher with the provided key and alphabet.
    Parameters:
    - text (str): The input text to be encrypted.
    - key (str): The encryption key.
    - alphabet (list): The list of characters representing the alphabet to be used.
    """
    n = len(text)
    N = len(alphabet)
    key_length = len(key)
    result = ""
    if key_length == n:
        pass # One time pad
    elif key_length < n:
        # Repeat the key to match the length of the alphabet
        key = (key * (n // key_length)) + key[:n % key_length]
    elif key_length > n:
        # Truncate the key to match the length of the alphabet
        key = key[:n]
            
    for i in range(len(text)):
        
        p_i = alphabet.index(text[i])
        
        k_i_mid_k = alphabet.index(key[i])
        
        ciphered_char = (p_i + k_i_mid_k) % N
        
        result += alphabet[ciphered_char]
    return result

def vigere_decrypt(text: str, key: str, alphabet: list) -> str:
    """
    Decrypts the given text using the Vigenère cipher with the provided key and alphabet.
    Parameters:
    - text (str): The input text to be encrypted.
    - key (str): The encryption key.
    - alphabet (list): The list of characters representing the alphabet to be used.
    """
    n = len(text)
    N = len(alphabet)
    key_length = len(key)
    result = ""
    if key_length == n:
        pass # One time pad
    elif key_length < n:
        # Repeat the key to match the length of the alphabet
        key = (key * (n // key_length)) + key[:n % key_length]
    elif key_length > n:
        # Truncate the key to match the length of the alphabet
        key = key[:n]
            
    for i in range(len(text)):
        
        p_i = alphabet.index(text[i])
        
        k_i_mid_k = alphabet.index(key[i])
        
        decrypted_char = (p_i - k_i_mid_k) % N
        
        result += alphabet[decrypted_char]
    return result


