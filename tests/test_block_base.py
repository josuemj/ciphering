import unittest

from utils.block.base import (
    generate_3des_key,
    generate_aes_key,
    generate_des_key,
    generate_key_bytes,
    pkcs7_pad,
    pkcs7_unpad,
)


class TestPkcs7Padding(unittest.TestCase):
    def test_pad_adds_padding_for_non_multiple_block_size(self) -> None:
        data = b"HELLO"
        padded = pkcs7_pad(data, 8)
        self.assertEqual(len(padded) % 8, 0)
        self.assertEqual(padded, b"HELLO\x03\x03\x03")

    def test_pad_adds_full_block_when_multiple_of_block_size(self) -> None:
        data = b"12345678"
        padded = pkcs7_pad(data, 8)
        self.assertEqual(padded, b"12345678" + (b"\x08" * 8))

    def test_unpad_recovers_original_data(self) -> None:
        data = b"block-cipher"
        padded = pkcs7_pad(data, 8)
        unpadded = pkcs7_unpad(padded, 8)
        self.assertEqual(unpadded, data)

    def test_unpad_raises_for_invalid_padding_bytes(self) -> None:
        with self.assertRaises(ValueError):
            pkcs7_unpad(b"HELLO\x03\x03\x02", 8)

    def test_unpad_raises_for_non_multiple_length(self) -> None:
        with self.assertRaises(ValueError):
            pkcs7_unpad(b"ABC", 8)

    def test_pad_raises_for_invalid_data_type(self) -> None:
        with self.assertRaises(TypeError):
            pkcs7_pad("HELLO", 8)


class TestKeyGeneration(unittest.TestCase):
    def test_generate_des_key_has_8_bytes(self) -> None:
        key = generate_des_key()
        self.assertEqual(len(key), 8)

    def test_generate_3des_key_16_bytes(self) -> None:
        key = generate_3des_key(16)
        self.assertEqual(len(key), 16)

    def test_generate_3des_key_24_bytes(self) -> None:
        key = generate_3des_key(24)
        self.assertEqual(len(key), 24)

    def test_generate_aes_key_32_bytes(self) -> None:
        key = generate_aes_key(32)
        self.assertEqual(len(key), 32)

    def test_generate_key_with_random_source(self) -> None:
        key = generate_key_bytes(12, source="random")
        self.assertEqual(len(key), 12)

    def test_generate_key_bytes_raises_for_invalid_source(self) -> None:
        with self.assertRaises(ValueError):
            generate_key_bytes(8, source="invalid")

    def test_generate_aes_key_raises_for_invalid_length(self) -> None:
        with self.assertRaises(ValueError):
            generate_aes_key(20)


if __name__ == "__main__":
    unittest.main()
