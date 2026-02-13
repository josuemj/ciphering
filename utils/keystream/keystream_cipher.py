"""
Prompt:
Implement a function that encrypts plaintext using XOR with a pseudo-random
keystream.

Requirements:
1. Accept plaintext message and key (seed) as parameters.
2. Generate the appropriate keystream for the message length.
3. Apply bitwise XOR between plaintext and keystream.
4. Return the resulting ciphertext.
"""

from utils.keystream.keystream import generate_prng_keystream


def encrypt_with_keystream(plaintext: str, seed: str | int) -> str:
    """Encrypt plaintext using XOR and a deterministic keystream."""
    if not isinstance(plaintext, str):
        raise TypeError("plaintext must be a string")

    if plaintext == "":
        return ""

    keystream = generate_prng_keystream(seed, len(plaintext))
    result = []

    for p_char, k_char in zip(plaintext, keystream):
        result.append(chr(ord(p_char) ^ ord(k_char)))

    return "".join(result)
