"""
DES encryption/decryption helpers for academic practice (ECB mode).

Features:
- Manual PKCS#7 padding (uses utilities from ``utils.block.base``)
- Secure key validation (expects 8-byte DES keys)
- Single-block helpers (no padding) plus full-message ECB with padding

Implementation notes:
- Pure Python DES core (key schedule, Feistel rounds, S-boxes, permutations)
- Designed for clarity over speed; suitable for didactic use and tests.
"""

from __future__ import annotations

from typing import Iterable, List

from utils.block.base import DES_BLOCK_SIZE, pkcs7_pad, pkcs7_unpad

# --- DES tables (FIPS 46-3) -------------------------------------------------

IP = [
    58,
    50,
    42,
    34,
    26,
    18,
    10,
    2,
    60,
    52,
    44,
    36,
    28,
    20,
    12,
    4,
    62,
    54,
    46,
    38,
    30,
    22,
    14,
    6,
    64,
    56,
    48,
    40,
    32,
    24,
    16,
    8,
    57,
    49,
    41,
    33,
    25,
    17,
    9,
    1,
    59,
    51,
    43,
    35,
    27,
    19,
    11,
    3,
    61,
    53,
    45,
    37,
    29,
    21,
    13,
    5,
    63,
    55,
    47,
    39,
    31,
    23,
    15,
    7,
]

FP = [
    40,
    8,
    48,
    16,
    56,
    24,
    64,
    32,
    39,
    7,
    47,
    15,
    55,
    23,
    63,
    31,
    38,
    6,
    46,
    14,
    54,
    22,
    62,
    30,
    37,
    5,
    45,
    13,
    53,
    21,
    61,
    29,
    36,
    4,
    44,
    12,
    52,
    20,
    60,
    28,
    35,
    3,
    43,
    11,
    51,
    19,
    59,
    27,
    34,
    2,
    42,
    10,
    50,
    18,
    58,
    26,
    33,
    1,
    41,
    9,
    49,
    17,
    57,
    25,
]

EXPANSION = [
    32,
    1,
    2,
    3,
    4,
    5,
    4,
    5,
    6,
    7,
    8,
    9,
    8,
    9,
    10,
    11,
    12,
    13,
    12,
    13,
    14,
    15,
    16,
    17,
    16,
    17,
    18,
    19,
    20,
    21,
    20,
    21,
    22,
    23,
    24,
    25,
    24,
    25,
    26,
    27,
    28,
    29,
    28,
    29,
    30,
    31,
    32,
    1,
]

P = [
    16,
    7,
    20,
    21,
    29,
    12,
    28,
    17,
    1,
    15,
    23,
    26,
    5,
    18,
    31,
    10,
    2,
    8,
    24,
    14,
    32,
    27,
    3,
    9,
    19,
    13,
    30,
    6,
    22,
    11,
    4,
    25,
]

S_BOXES = [
    [
        [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
    ],
    [
        [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
    ],
    [
        [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
    ],
    [
        [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
    ],
    [
        [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
    ],
    [
        [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
    ],
    [
        [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
    ],
    [
        [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
    ],
]

PC1 = [
    57,
    49,
    41,
    33,
    25,
    17,
    9,
    1,
    58,
    50,
    42,
    34,
    26,
    18,
    10,
    2,
    59,
    51,
    43,
    35,
    27,
    19,
    11,
    3,
    60,
    52,
    44,
    36,
    63,
    55,
    47,
    39,
    31,
    23,
    15,
    7,
    62,
    54,
    46,
    38,
    30,
    22,
    14,
    6,
    61,
    53,
    45,
    37,
    29,
    21,
    13,
    5,
    28,
    20,
    12,
    4,
]

PC2 = [
    14,
    17,
    11,
    24,
    1,
    5,
    3,
    28,
    15,
    6,
    21,
    10,
    23,
    19,
    12,
    4,
    26,
    8,
    16,
    7,
    27,
    20,
    13,
    2,
    41,
    52,
    31,
    37,
    47,
    55,
    30,
    40,
    51,
    45,
    33,
    48,
    44,
    49,
    39,
    56,
    34,
    53,
    46,
    42,
    50,
    36,
    29,
    32,
]

SHIFT_SCHEDULE = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]


# --- internal helpers -------------------------------------------------------

def _ensure_bytes(value: bytes | bytearray, name: str) -> bytes:
    if not isinstance(value, (bytes, bytearray)):
        raise TypeError(f"{name} must be bytes")
    return bytes(value)


def _permute(block: int, table: Iterable[int], input_bits: int) -> int:
    """Generic bit permutation helper."""
    result = 0
    for pos in table:
        # Positions are 1-indexed from MSB to LSB
        bit = (block >> (input_bits - pos)) & 1
        result = (result << 1) | bit
    return result


def _left_rotate_28(value: int, shift: int) -> int:
    """Rotate a 28-bit value left by shift bits."""
    mask = (1 << 28) - 1
    return ((value << shift) & mask) | (value >> (28 - shift))


def _create_subkeys(key: bytes) -> List[int]:
    key_bytes = _ensure_bytes(key, "key")
    if len(key_bytes) != DES_BLOCK_SIZE:
        raise ValueError("DES key must be exactly 8 bytes")

    key_int = int.from_bytes(key_bytes, "big")
    permuted = _permute(key_int, PC1, 64)  # 56 bits
    c = (permuted >> 28) & ((1 << 28) - 1)
    d = permuted & ((1 << 28) - 1)

    subkeys: List[int] = []
    for shift in SHIFT_SCHEDULE:
        c = _left_rotate_28(c, shift)
        d = _left_rotate_28(d, shift)
        combined = (c << 28) | d
        subkey = _permute(combined, PC2, 56)  # 48 bits
        subkeys.append(subkey)
    return subkeys


def _feistel(right: int, subkey: int) -> int:
    expanded = _permute(right, EXPANSION, 32)  # 48 bits
    mixed = expanded ^ subkey

    s_output = 0
    for i in range(8):
        chunk = (mixed >> (42 - 6 * i)) & 0x3F
        row = ((chunk & 0b100000) >> 4) | (chunk & 0b000001)
        col = (chunk >> 1) & 0x0F
        s_val = S_BOXES[i][row][col]
        s_output = (s_output << 4) | s_val

    return _permute(s_output, P, 32)


def _process_block(block: bytes, subkeys: List[int]) -> bytes:
    block_bytes = _ensure_bytes(block, "block")
    if len(block_bytes) != DES_BLOCK_SIZE:
        raise ValueError("block must be exactly 8 bytes")

    block_int = int.from_bytes(block_bytes, "big")
    permuted = _permute(block_int, IP, 64)
    left = (permuted >> 32) & 0xFFFFFFFF
    right = permuted & 0xFFFFFFFF

    for subkey in subkeys:
        left, right = right, left ^ _feistel(right, subkey)

    pre_output = (right << 32) | left  # final swap before FP
    final_int = _permute(pre_output, FP, 64)
    return final_int.to_bytes(DES_BLOCK_SIZE, "big")

__all__ = [
    "des_ecb_encrypt",
    "des_ecb_decrypt",
    "des_encrypt_block",
    "des_decrypt_block",
]


def des_encrypt_block(block: bytes, key: bytes) -> bytes:
    """Encrypt a single 8-byte block with DES (no padding)."""
    subkeys = _create_subkeys(key)
    return _process_block(block, subkeys)


def des_decrypt_block(block: bytes, key: bytes) -> bytes:
    """Decrypt a single 8-byte block with DES (no padding)."""
    subkeys = list(reversed(_create_subkeys(key)))
    return _process_block(block, subkeys)


def des_ecb_encrypt(plaintext: bytes, key: bytes) -> bytes:
    """Encrypt arbitrary-length plaintext with DES-ECB using PKCS#7 padding."""
    plain_bytes = _ensure_bytes(plaintext, "plaintext")
    padded = pkcs7_pad(plain_bytes, DES_BLOCK_SIZE)
    subkeys = _create_subkeys(key)

    blocks = []
    for i in range(0, len(padded), DES_BLOCK_SIZE):
        block = padded[i : i + DES_BLOCK_SIZE]
        blocks.append(_process_block(block, subkeys))
    return b"".join(blocks)


def des_ecb_decrypt(ciphertext: bytes, key: bytes) -> bytes:
    """Decrypt DES-ECB ciphertext and remove PKCS#7 padding."""
    cipher_bytes = _ensure_bytes(ciphertext, "ciphertext")
    if len(cipher_bytes) % DES_BLOCK_SIZE != 0 or len(cipher_bytes) == 0:
        raise ValueError("ciphertext length must be a non-empty multiple of 8 bytes")

    subkeys = list(reversed(_create_subkeys(key)))
    blocks = []
    for i in range(0, len(cipher_bytes), DES_BLOCK_SIZE):
        block = cipher_bytes[i : i + DES_BLOCK_SIZE]
        blocks.append(_process_block(block, subkeys))

    padded_plain = b"".join(blocks)
    return pkcs7_unpad(padded_plain, DES_BLOCK_SIZE)
