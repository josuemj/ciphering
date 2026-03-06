"""
Triple DES (3DES) helpers for CBC mode encryption/decryption.

Requirements:
- Secure key generation/validation for 16-byte (2-key) and 24-byte (3-key) 3DES.
- Random IV per encryption (8 bytes, DES block size) using `secrets.token_bytes`.
- PKCS#7 padding via Crypto.Util.Padding (spec says use library pad/unpad, not manual).

Notes on key sizes:
- 16 bytes -> two-key 3DES (K1 || K2); third stage reuses K1 (effective ~112-bit security).
- 24 bytes -> three-key 3DES (K1 || K2 || K3); effective ~168-bit security (theoretical).
"""

from __future__ import annotations

import secrets
from typing import Tuple

from Crypto.Cipher import DES3
from Crypto.Util.Padding import pad, unpad

from utils.block.base import DES_BLOCK_SIZE

__all__ = ["triple_des_cbc_encrypt", "triple_des_cbc_decrypt", "generate_iv"]


def _validate_and_adjust_key(key: bytes) -> bytes:
    if not isinstance(key, (bytes, bytearray)):
        raise TypeError("key must be bytes")
    if len(key) not in (16, 24):
        raise ValueError("3DES key must be 16 or 24 bytes")
    adjusted = DES3.adjust_key_parity(bytes(key))
    # DES3.new will raise if the key is still weak/invalid; surface that error.
    DES3.new(adjusted, DES3.MODE_ECB)
    return adjusted


def generate_iv() -> bytes:
    """Generate a fresh 8-byte IV suitable for DES/3DES CBC."""
    return secrets.token_bytes(DES_BLOCK_SIZE)


def triple_des_cbc_encrypt(plaintext: bytes, key: bytes, *, iv: bytes | None = None) -> Tuple[bytes, bytes]:
    """
    Encrypt arbitrary plaintext with 3DES-CBC.

    Returns:
        (iv, ciphertext)
    """
    if not isinstance(plaintext, (bytes, bytearray)):
        raise TypeError("plaintext must be bytes")

    if iv is None:
        iv = generate_iv()
    else:
        if not isinstance(iv, (bytes, bytearray)):
            raise TypeError("iv must be bytes")
        if len(iv) != DES_BLOCK_SIZE:
            raise ValueError("IV must be 8 bytes for 3DES")
        iv = bytes(iv)

    adjusted_key = _validate_and_adjust_key(key)
    cipher = DES3.new(adjusted_key, DES3.MODE_CBC, iv=iv)
    padded = pad(bytes(plaintext), DES_BLOCK_SIZE)
    ciphertext = cipher.encrypt(padded)
    return iv, ciphertext


def triple_des_cbc_decrypt(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    """Decrypt 3DES-CBC ciphertext using the provided IV."""
    if not isinstance(ciphertext, (bytes, bytearray)):
        raise TypeError("ciphertext must be bytes")
    if not isinstance(iv, (bytes, bytearray)):
        raise TypeError("iv must be bytes")
    if len(iv) != DES_BLOCK_SIZE:
        raise ValueError("IV must be 8 bytes for 3DES")

    adjusted_key = _validate_and_adjust_key(key)
    cipher = DES3.new(adjusted_key, DES3.MODE_CBC, iv=bytes(iv))
    padded_plain = cipher.decrypt(bytes(ciphertext))
    return unpad(padded_plain, DES_BLOCK_SIZE)
