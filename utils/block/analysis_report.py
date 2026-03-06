"""Generate reproducible outputs for the Block Ciphers security analysis README.

This script is meant to be run from the project root to produce:
- Console output (copy/paste into utils/block/README.md)
- Image artifacts for ECB vs CBC visual comparison

Examples:
    python -m utils.block.analysis_report
    python -m utils.block.analysis_report --out-dir utils/block/img
"""

from __future__ import annotations

import argparse
import os
import struct
from dataclasses import dataclass

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

from utils.block.aes_ecb_cbc import aes_cbc_encrypt_image, aes_ecb_encrypt_image
from utils.block.base import (
    AES_BLOCK_SIZE,
    DES_BLOCK_SIZE,
    generate_aes_key,
    generate_3des_key,
    generate_des_key,
    pkcs7_pad,
    pkcs7_unpad,
)


def _create_patterned_bmp(width: int = 200, height: int = 200) -> bytes:
    """Create a 24-bit BMP with a repeating colour pattern (large uniform blocks)."""
    row_bytes = width * 3
    padding_per_row = (4 - row_bytes % 4) % 4
    pixel_data_size = (row_bytes + padding_per_row) * height
    file_size = 54 + pixel_data_size

    # -- BMP file header (14 bytes) --
    header = b"BM"
    header += struct.pack("<I", file_size)
    header += b"\x00\x00\x00\x00"  # reserved
    header += struct.pack("<I", 54)  # pixel data offset

    # -- DIB header (BITMAPINFOHEADER, 40 bytes) --
    header += struct.pack("<I", 40)  # header size
    header += struct.pack("<i", width)
    header += struct.pack("<i", height)
    header += struct.pack("<HH", 1, 24)  # planes, bits per pixel
    header += struct.pack("<I", 0)  # no compression
    header += struct.pack("<I", pixel_data_size)
    header += struct.pack("<ii", 2835, 2835)  # pixels per metre
    header += struct.pack("<II", 0, 0)  # colours

    # -- Pixel data: coloured horizontal blocks --
    colours = [
        (255, 0, 0),  # red
        (0, 255, 0),  # green
        (0, 0, 255),  # blue
        (255, 255, 0),  # yellow
    ]
    rows = bytearray()
    block_h = height // len(colours)
    for y in range(height):
        colour_idx = y // block_h if y // block_h < len(colours) else len(colours) - 1
        r, g, b = colours[colour_idx]
        row = bytes([b, g, r]) * width  # BMP stores BGR
        rows.extend(row)
        rows.extend(b"\x00" * padding_per_row)

    return header + bytes(rows)


def _chunk(data: bytes, size: int) -> list[bytes]:
    return [data[i : i + size] for i in range(0, len(data), size)]


def _hex_blocks(data: bytes, block_size: int, limit: int = 6) -> list[str]:
    blocks = _chunk(data, block_size)
    return [blocks[i].hex() for i in range(min(limit, len(blocks)))]


@dataclass(frozen=True)
class BruteForceEstimate:
    rate_keys_per_sec: float
    worst_seconds: float
    avg_seconds: float


def _estimate_bruteforce(k_bits: int, rate_keys_per_sec: float) -> BruteForceEstimate:
    keyspace = 2**k_bits
    worst = keyspace / rate_keys_per_sec
    avg = (keyspace / 2) / rate_keys_per_sec
    return BruteForceEstimate(rate_keys_per_sec=rate_keys_per_sec, worst_seconds=worst, avg_seconds=avg)


def _format_seconds(seconds: float) -> str:
    if seconds < 1:
        return f"{seconds:.3f} s"
    if seconds < 120:
        return f"{seconds:.1f} s"
    minutes = seconds / 60
    if minutes < 120:
        return f"{minutes:.1f} min"
    hours = minutes / 60
    if hours < 72:
        return f"{hours:.1f} h"
    days = hours / 24
    return f"{days:.1f} days"


def _aes_text_ecb_cbc_demo() -> None:
    print("== Vulnerabilidad de ECB (demo con AES) ==")
    key = bytes.fromhex(
        "000102030405060708090a0b0c0d0e0f"
        "101112131415161718191a1b1c1d1e1f"
    )  # 32 bytes (AES-256)
    iv = bytes.fromhex("0f0e0d0c0b0a09080706050403020100")

    # 16-byte block; repeated to force identical plaintext blocks.
    repeated_block = b"ATAQUE ATAQUE 12"  # 16 bytes exactly
    plaintext = repeated_block * 4

    ecb = AES.new(key, AES.MODE_ECB).encrypt(pad(plaintext, AES_BLOCK_SIZE))
    cbc = AES.new(key, AES.MODE_CBC, iv=iv).encrypt(pad(plaintext, AES_BLOCK_SIZE))

    ecb_blocks = _chunk(ecb, AES_BLOCK_SIZE)
    cbc_blocks = _chunk(cbc, AES_BLOCK_SIZE)

    print(f"plaintext (repr): {plaintext!r}")
    print(f"plaintext length: {len(plaintext)} bytes")
    print("ECB first blocks (hex):")
    for i, hx in enumerate(_hex_blocks(ecb, AES_BLOCK_SIZE, limit=4)):
        print(f"  C[{i}]: {hx}")
    print(f"ECB: C[0] == C[1]? {ecb_blocks[0] == ecb_blocks[1]}")

    print("CBC first blocks (hex):")
    for i, hx in enumerate(_hex_blocks(cbc, AES_BLOCK_SIZE, limit=4)):
        print(f"  C[{i}]: {hx}")
    print(f"CBC: C[0] == C[1]? {cbc_blocks[0] == cbc_blocks[1]}")
    print()


def _iv_experiment() -> None:
    print("== Vector de Inicialización (IV) (AES-CBC) ==")
    key = bytes.fromhex(
        "603deb1015ca71be2b73aef0857d7781"
        "1f352c073b6108d72d9810a30914dff4"
    )  # 32 bytes (AES-256)
    msg = b"MISMO MENSAJE, MISMA CLAVE"

    fixed_iv = b"\x00" * AES_BLOCK_SIZE
    ct1 = AES.new(key, AES.MODE_CBC, iv=fixed_iv).encrypt(pad(msg, AES_BLOCK_SIZE))
    ct2 = AES.new(key, AES.MODE_CBC, iv=fixed_iv).encrypt(pad(msg, AES_BLOCK_SIZE))

    iv_a = bytes.fromhex("00112233445566778899aabbccddeeff")
    iv_b = bytes.fromhex("ffeeddccbbaa99887766554433221100")
    ct3 = AES.new(key, AES.MODE_CBC, iv=iv_a).encrypt(pad(msg, AES_BLOCK_SIZE))
    ct4 = AES.new(key, AES.MODE_CBC, iv=iv_b).encrypt(pad(msg, AES_BLOCK_SIZE))

    print(f"msg (repr): {msg!r}")
    print(f"same IV twice -> ct1 == ct2 ? {ct1 == ct2}")
    print(f"ct1 (hex): {ct1.hex()}")
    print(f"ct2 (hex): {ct2.hex()}")
    print(f"two different IVs -> ct3 == ct4 ? {ct3 == ct4}")
    print(f"iv_a (hex): {iv_a.hex()}")
    print(f"ct3 (hex): {ct3.hex()}")
    print(f"iv_b (hex): {iv_b.hex()}")
    print(f"ct4 (hex): {ct4.hex()}")
    print()


def _padding_demo() -> None:
    print("== Padding (PKCS#7, bloque DES=8) ==")
    examples = [
        (b"ABCDE", "5 bytes"),
        (b"ABCDEFGH", "8 bytes (exactamente un bloque)"),
        (b"ABCDEFGHIJ", "10 bytes"),
    ]
    for msg, label in examples:
        padded = pkcs7_pad(msg, DES_BLOCK_SIZE)
        pad_len = padded[-1]
        recovered = pkcs7_unpad(padded, DES_BLOCK_SIZE)
        print(f"- {label}")
        print(f"  msg (repr): {msg!r}")
        print(f"  padded (hex): {padded.hex()}")
        print(f"  pad_len: {pad_len} (0x{pad_len:02x})")
        print(f"  unpad ok? {recovered == msg}")
    print()


def _key_sizes_and_estimates() -> None:
    print("== Tamaños de clave (este repo) ==")
    des_key = generate_des_key()
    des3_key = generate_3des_key()
    aes_key = generate_aes_key()
    print(f"DES:  {len(des_key)} bytes = {len(des_key) * 8} bits")
    print(f"3DES: {len(des3_key)} bytes = {len(des3_key) * 8} bits (por defecto)")
    print(f"AES:  {len(aes_key)} bytes = {len(aes_key) * 8} bits (por defecto, AES-256)")
    print()

    print("== Fuerza bruta (estimación para DES) ==")
    print("Nota: DES usa 56 bits efectivos de clave (los otros bits son de paridad).")
    for r in (1e12, 1e15):
        est = _estimate_bruteforce(56, r)
        print(
            f"R={est.rate_keys_per_sec:.0e} claves/s -> "
            f"peor={_format_seconds(est.worst_seconds)}, "
            f"promedio={_format_seconds(est.avg_seconds)}"
        )
    print()


def _image_demo(out_dir: str) -> None:
    print("== ECB vs CBC en imagen (AES-256) ==")
    os.makedirs(out_dir, exist_ok=True)

    key = bytes.fromhex(
        "2b7e151628aed2a6abf7158809cf4f3c"
        "3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f3f"
    )  # 32 bytes
    fixed_iv = b"\x11" * AES_BLOCK_SIZE

    bmp = _create_patterned_bmp()
    original_path = os.path.join(out_dir, "original.bmp")
    ecb_path = os.path.join(out_dir, "ecb_encrypted.bmp")
    cbc_path = os.path.join(out_dir, "cbc_encrypted.bmp")

    with open(original_path, "wb") as f:
        f.write(bmp)

    ecb = aes_ecb_encrypt_image(bmp, key)
    with open(ecb_path, "wb") as f:
        f.write(ecb)

    cbc = aes_cbc_encrypt_image(bmp, key, iv=fixed_iv)
    with open(cbc_path, "wb") as f:
        f.write(cbc)

    ecb_pixels = ecb[54:]
    cbc_pixels = cbc[54:]
    ecb_blocks = [ecb_pixels[i : i + 16] for i in range(0, len(ecb_pixels) - 15, 16)]
    cbc_blocks = [cbc_pixels[i : i + 16] for i in range(0, len(cbc_pixels) - 15, 16)]
    ecb_unique = len(set(ecb_blocks))
    cbc_unique = len(set(cbc_blocks))

    print(f"Saved: {original_path}")
    print(f"Saved: {ecb_path}")
    print(f"Saved: {cbc_path}")
    print(f"ECB unique blocks: {ecb_unique} / {len(ecb_blocks)} ({ecb_unique / len(ecb_blocks) * 100:.1f}% unique)")
    print(f"CBC unique blocks: {cbc_unique} / {len(cbc_blocks)} ({cbc_unique / len(cbc_blocks) * 100:.1f}% unique)")
    print()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--out-dir",
        default=os.path.join("utils", "block", "img"),
        help="Directorio donde guardar las imagenes BMP",
    )
    parser.add_argument(
        "--only",
        nargs="+",
        choices=["keys", "image", "ecb", "iv", "padding"],
        help="Ejecuta solo secciones especificas (default: todas)",
    )
    args = parser.parse_args()

    sections = args.only or ["keys", "image", "ecb", "iv", "padding"]
    if "keys" in sections:
        _key_sizes_and_estimates()
    if "image" in sections:
        _image_demo(args.out_dir)
    if "ecb" in sections:
        _aes_text_ecb_cbc_demo()
    if "iv" in sections:
        _iv_experiment()
    if "padding" in sections:
        _padding_demo()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
