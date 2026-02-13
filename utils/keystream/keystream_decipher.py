"""
Prompt:
Implement a function that decrypts ciphertext generated with XOR and a
pseudo-random keystream.

Requirements:
1. Accept ciphertext and key (seed) as parameters.
2. Generate the same keystream used during encryption.
3. Apply bitwise XOR to recover the original plaintext.
4. Verify that decryption reproduces the exact original plaintext.
"""

from utils.keystream.keystream import generate_prng_keystream


def decrypt_with_keystream(ciphertext: str, seed: str | int) -> str:
    """Decrypt ciphertext using XOR and a deterministic keystream."""
    if not isinstance(ciphertext, str):
        raise TypeError("ciphertext must be a string")

    if ciphertext == "":
        return ""

    keystream = generate_prng_keystream(seed, len(ciphertext))
    result = []

    for c_char, k_char in zip(ciphertext, keystream):
        result.append(chr(ord(c_char) ^ ord(k_char)))

    return "".join(result)
