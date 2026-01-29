def vigere(text: str, key: str, alphabet: list) -> str:
    n = len(text)
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
        ciphered_char = (alphabet.index(text[i]) + alphabet.index(key[i % len(key)])) % len(alphabet)
        result += alphabet[ciphered_char]
    return result

