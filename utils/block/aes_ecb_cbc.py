"""AES encryption in ECB and CBC modes for image visual analysis.

Demonstrates why ECB mode is insecure by encrypting BMP image pixel data
while preserving the header, allowing visual comparison of modes.

Uses AES-256 (32-byte key) with PyCryptodome.
"""

from __future__ import annotations

import secrets

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from utils.block.base import AES_BLOCK_SIZE

__all__ = [
    "aes_ecb_encrypt_image",
    "aes_cbc_encrypt_image",
    "generate_aes_iv",
]


def generate_aes_iv() -> bytes:
    """Generate a fresh 16-byte IV for AES CBC."""
    return secrets.token_bytes(AES_BLOCK_SIZE)


def aes_ecb_encrypt_image(image_data: bytes, key: bytes, header_size: int = 54) -> bytes:
    """Encrypt BMP pixel data with AES-256 ECB, keeping the header intact.

    Args:
        image_data: Raw BMP file bytes.
        key: 32-byte AES key.
        header_size: Number of header bytes to preserve (default 54 for BMP).

    Returns:
        BMP bytes with original header and ECB-encrypted pixel data.
    """
    _validate_inputs(image_data, key, header_size)
    header = image_data[:header_size]
    pixels = image_data[header_size:]

    cipher = AES.new(key, AES.MODE_ECB)
    encrypted_pixels = cipher.encrypt(pad(pixels, AES_BLOCK_SIZE))

    # Truncate to original pixel length so the BMP stays valid
    return header + encrypted_pixels[: len(pixels)]


def aes_cbc_encrypt_image(
    image_data: bytes, key: bytes, header_size: int = 54, *, iv: bytes | None = None
) -> bytes:
    """Encrypt BMP pixel data with AES-256 CBC, keeping the header intact.

    Args:
        image_data: Raw BMP file bytes.
        key: 32-byte AES key.
        header_size: Number of header bytes to preserve (default 54 for BMP).
        iv: Optional 16-byte IV. If omitted, a fresh random IV is generated.

    Returns:
        BMP bytes with original header and CBC-encrypted pixel data.
    """
    _validate_inputs(image_data, key, header_size)
    header = image_data[:header_size]
    pixels = image_data[header_size:]

    if iv is None:
        iv = generate_aes_iv()
    else:
        if not isinstance(iv, (bytes, bytearray)):
            raise TypeError("iv must be bytes")
        if len(iv) != AES_BLOCK_SIZE:
            raise ValueError("iv must be 16 bytes for AES")

    cipher = AES.new(key, AES.MODE_CBC, iv=bytes(iv))
    encrypted_pixels = cipher.encrypt(pad(pixels, AES_BLOCK_SIZE))

    return header + encrypted_pixels[: len(pixels)]


def _validate_inputs(image_data: bytes, key: bytes, header_size: int) -> None:
    if not isinstance(image_data, (bytes, bytearray)):
        raise TypeError("image_data must be bytes")
    if not isinstance(key, (bytes, bytearray)):
        raise TypeError("key must be bytes")
    if len(key) != 32:
        raise ValueError("key must be 32 bytes for AES-256")
    if len(image_data) <= header_size:
        raise ValueError("image_data must be larger than header_size")
