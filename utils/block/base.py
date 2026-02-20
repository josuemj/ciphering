"""Base utilities for block cipher labs (academic support).

Context:
- A block cipher operates on fixed-size blocks (e.g., DES: 8 bytes, AES: 16 bytes).
- For variable-length messages, PKCS#7 padding is required before encryption.
- This module provides reusable primitives for:
  1) Manual PKCS#7 padding/unpadding (required in DES-ECB practice).
  2) Secure key generation for DES, 3DES, and AES using OS-backed randomness.

Academic references:
- RFC 5652 (CMS): PKCS#7-compatible padding behavior.
- NIST SP 800-38A: block cipher modes of operation (ECB, CBC).
- NIST FIPS 46-3 / SP 800-67: DES and Triple DES context.
- NIST FIPS 197: AES specification.
"""

import random
import secrets


DES_BLOCK_SIZE = 8
AES_BLOCK_SIZE = 16


def pkcs7_pad(data: bytes, block_size: int) -> bytes:
    """Apply PKCS#7 padding to bytes data."""
    if not isinstance(data, bytes):
        raise TypeError("data must be bytes")
    if not isinstance(block_size, int):
        raise TypeError("block_size must be an integer")
    if block_size < 1 or block_size > 255:
        raise ValueError("block_size must be between 1 and 255")

    pad_len = block_size - (len(data) % block_size)
    if pad_len == 0:
        pad_len = block_size
    return data + bytes([pad_len] * pad_len)


def pkcs7_unpad(padded_data: bytes, block_size: int) -> bytes:
    """Remove PKCS#7 padding from bytes data."""
    if not isinstance(padded_data, bytes):
        raise TypeError("padded_data must be bytes")
    if not isinstance(block_size, int):
        raise TypeError("block_size must be an integer")
    if block_size < 1 or block_size > 255:
        raise ValueError("block_size must be between 1 and 255")
    if len(padded_data) == 0:
        raise ValueError("padded_data cannot be empty")
    if len(padded_data) % block_size != 0:
        raise ValueError("padded_data length must be a multiple of block_size")

    pad_len = padded_data[-1]
    if pad_len < 1 or pad_len > block_size:
        raise ValueError("invalid PKCS#7 padding length")

    expected_padding = bytes([pad_len] * pad_len)
    if padded_data[-pad_len:] != expected_padding:
        raise ValueError("invalid PKCS#7 padding bytes")

    return padded_data[:-pad_len]


def generate_key_bytes(length: int, source: str = "secrets") -> bytes:
    """Generate random key bytes.

    source:
    - "secrets": cryptographically secure with secrets.token_bytes (default)
    - "random": uses random.SystemRandom for secure OS-backed randomness
    """
    if not isinstance(length, int):
        raise TypeError("length must be an integer")
    if length < 1:
        raise ValueError("length must be at least 1")
    if source not in ("secrets", "random"):
        raise ValueError("source must be 'secrets' or 'random'")

    if source == "secrets":
        return secrets.token_bytes(length)

    system_rng = random.SystemRandom()
    return bytes(system_rng.getrandbits(8) for _ in range(length))


def generate_des_key(source: str = "secrets") -> bytes:
    """Generate a DES key (8 bytes)."""
    return generate_key_bytes(DES_BLOCK_SIZE, source=source)


def generate_3des_key(key_length: int = 24, source: str = "secrets") -> bytes:
    """Generate a 3DES key (16 or 24 bytes)."""
    if key_length not in (16, 24):
        raise ValueError("key_length must be 16 or 24 for 3DES")
    return generate_key_bytes(key_length, source=source)


def generate_aes_key(key_length: int = 32, source: str = "secrets") -> bytes:
    """Generate an AES key (16, 24 or 32 bytes)."""
    if key_length not in (16, 24, 32):
        raise ValueError("key_length must be 16, 24, or 32 for AES")
    return generate_key_bytes(key_length, source=source)
