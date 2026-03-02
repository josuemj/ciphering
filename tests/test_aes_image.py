"""AES ECB vs CBC visual analysis on a BMP image.

Generates a patterned BMP image, encrypts it with AES-256 in ECB and CBC
modes (header preserved), and saves the results to img/ for visual comparison.

Run:
    python -m pytest tests/test_aes_image.py -v -s
"""

import os
import struct
import unittest

from utils.block.base import generate_aes_key
from utils.block.aes_ecb_cbc import aes_ecb_encrypt_image, aes_cbc_encrypt_image


IMG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "img")


def _create_patterned_bmp(width: int = 200, height: int = 200) -> bytes:
    """Create a 24-bit BMP with a repeating colour pattern.

    The pattern has large uniform blocks so that ECB's weakness
    (identical plaintext blocks → identical ciphertext blocks) is clearly
    visible after encryption.
    """
    row_bytes = width * 3
    padding_per_row = (4 - row_bytes % 4) % 4
    pixel_data_size = (row_bytes + padding_per_row) * height
    file_size = 54 + pixel_data_size

    # -- BMP file header (14 bytes) --
    header = b"BM"
    header += struct.pack("<I", file_size)
    header += b"\x00\x00\x00\x00"          # reserved
    header += struct.pack("<I", 54)         # pixel data offset

    # -- DIB header (BITMAPINFOHEADER, 40 bytes) --
    header += struct.pack("<I", 40)         # header size
    header += struct.pack("<i", width)
    header += struct.pack("<i", height)
    header += struct.pack("<HH", 1, 24)    # planes, bits per pixel
    header += struct.pack("<I", 0)          # no compression
    header += struct.pack("<I", pixel_data_size)
    header += struct.pack("<ii", 2835, 2835)  # pixels per metre
    header += struct.pack("<II", 0, 0)      # colours

    # -- Pixel data: coloured block pattern --
    colours = [
        (255, 0, 0),    # red
        (0, 255, 0),    # green
        (0, 0, 255),    # blue
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


class TestAesImageEncryption(unittest.TestCase):
    """Encrypt a patterned BMP with AES-256 ECB and CBC and save results."""

    @classmethod
    def setUpClass(cls) -> None:
        os.makedirs(IMG_DIR, exist_ok=True)
        cls.key = generate_aes_key(32)
        cls.bmp = _create_patterned_bmp()

    def test_save_original(self) -> None:
        path = os.path.join(IMG_DIR, "original.bmp")
        with open(path, "wb") as f:
            f.write(self.bmp)
        self.assertTrue(os.path.exists(path))
        print(f"  Saved: {path}")

    def test_ecb_encryption_saves_image(self) -> None:
        encrypted = aes_ecb_encrypt_image(self.bmp, self.key)
        # Header must be preserved
        self.assertEqual(encrypted[:2], b"BM")
        self.assertEqual(encrypted[:54], self.bmp[:54])

        path = os.path.join(IMG_DIR, "ecb_encrypted.bmp")
        with open(path, "wb") as f:
            f.write(encrypted)
        self.assertTrue(os.path.exists(path))
        print(f"  Saved: {path}")

    def test_cbc_encryption_saves_image(self) -> None:
        encrypted = aes_cbc_encrypt_image(self.bmp, self.key)
        self.assertEqual(encrypted[:2], b"BM")
        self.assertEqual(encrypted[:54], self.bmp[:54])

        path = os.path.join(IMG_DIR, "cbc_encrypted.bmp")
        with open(path, "wb") as f:
            f.write(encrypted)
        self.assertTrue(os.path.exists(path))
        print(f"  Saved: {path}")

    def test_ecb_shows_patterns(self) -> None:
        """ECB should produce repeating ciphertext blocks for identical input blocks."""
        encrypted = aes_ecb_encrypt_image(self.bmp, self.key)
        pixel_data = encrypted[54:]

        # Count unique 16-byte blocks in the ciphertext
        blocks = [pixel_data[i : i + 16] for i in range(0, len(pixel_data) - 15, 16)]
        unique = len(set(blocks))
        total = len(blocks)

        # ECB on a patterned image: many duplicate blocks
        print(f"  ECB: {unique} unique / {total} total blocks "
              f"({unique / total * 100:.1f}% unique)")
        self.assertLess(unique, total, "ECB should have duplicate ciphertext blocks")

    def test_cbc_hides_patterns(self) -> None:
        """CBC should produce near-unique ciphertext blocks."""
        encrypted = aes_cbc_encrypt_image(self.bmp, self.key)
        pixel_data = encrypted[54:]

        blocks = [pixel_data[i : i + 16] for i in range(0, len(pixel_data) - 15, 16)]
        unique = len(set(blocks))
        total = len(blocks)

        ratio = unique / total
        print(f"  CBC: {unique} unique / {total} total blocks "
              f"({ratio * 100:.1f}% unique)")
        self.assertGreater(ratio, 0.99, "CBC should have nearly all unique blocks")


if __name__ == "__main__":
    unittest.main()
