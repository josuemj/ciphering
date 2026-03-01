import unittest

from utils.block.base import DES_BLOCK_SIZE
from utils.block.des_ecb import (
    des_decrypt_block,
    des_ecb_decrypt,
    des_ecb_encrypt,
    des_encrypt_block,
)


class TestDesEcbBlock(unittest.TestCase):
    def setUp(self) -> None:
        self.key = bytes.fromhex("133457799BBCDFF1")
        self.plain_block = bytes.fromhex("0123456789ABCDEF")
        self.expected_cipher_block = bytes.fromhex("85E813540F0AB405")

    def test_encrypt_block_matches_known_vector(self) -> None:
        cipher = des_encrypt_block(self.plain_block, self.key)
        self.assertEqual(cipher, self.expected_cipher_block)

    def test_decrypt_block_roundtrip(self) -> None:
        plain = des_decrypt_block(self.expected_cipher_block, self.key)
        self.assertEqual(plain, self.plain_block)


class TestDesEcbPadding(unittest.TestCase):
    def test_roundtrip_various_lengths(self) -> None:
        key = b"SecrKey!"
        messages = [
            b"",
            b"A",
            b"HELLO DES",
            b"12345678",  # exact block size
            b"Longer message that spans multiple DES blocks.",
        ]
        for msg in messages:
            cipher = des_ecb_encrypt(msg, key)
            recovered = des_ecb_decrypt(cipher, key)
            self.assertEqual(recovered, msg)

    def test_padding_adds_full_block_when_exact_multiple(self) -> None:
        key = b"EightKey"
        plaintext = b"ABCDEFGH"  # 8 bytes
        cipher = des_ecb_encrypt(plaintext, key)
        self.assertEqual(len(cipher), 2 * DES_BLOCK_SIZE)
        recovered = des_ecb_decrypt(cipher, key)
        self.assertEqual(recovered, plaintext)

    def test_invalid_key_length_raises(self) -> None:
        with self.assertRaises(ValueError):
            des_ecb_encrypt(b"hi", b"short")
        with self.assertRaises(ValueError):
            des_decrypt_block(b"ABCDEFGH", b"toolongkey")

    def test_invalid_ciphertext_length_raises(self) -> None:
        key = b"8bytekey"
        with self.assertRaises(ValueError):
            des_ecb_decrypt(b"12345", key)


if __name__ == "__main__":
    unittest.main()
