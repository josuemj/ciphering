import unittest
from utils.ciphers.caesar import caesar_encrypt, caesar_decrypt

ALPHABET = list("abcdefghijklmnopqrstuvwxyz")

class TestCaesarEncrypt(unittest.TestCase):

    # Basic encryption tests
    def test_encrypt_hello(self) -> None:
        self.assertEqual(caesar_encrypt("hello", 3, ALPHABET), "khoor")

    def test_encrypt_abc(self) -> None:
        self.assertEqual(caesar_encrypt("abc", 1, ALPHABET), "bcd")

    def test_encrypt_xyz_wraps(self) -> None:
        self.assertEqual(caesar_encrypt("xyz", 3, ALPHABET), "abc")

    def test_encrypt_shift_zero(self) -> None:
        self.assertEqual(caesar_encrypt("hello", 0, ALPHABET), "hello")

    def test_encrypt_full_rotation(self) -> None:
        self.assertEqual(caesar_encrypt("hello", 26, ALPHABET), "hello")

    # Non-alphabet characters preserved
    def test_encrypt_preserves_spaces(self) -> None:
        self.assertEqual(caesar_encrypt("hello world", 3, ALPHABET), "khoor zruog")

    def test_encrypt_preserves_numbers(self) -> None:
        self.assertEqual(caesar_encrypt("abc123", 1, ALPHABET), "bcd123")

    def test_encrypt_preserves_punctuation(self) -> None:
        self.assertEqual(caesar_encrypt("hi!", 2, ALPHABET), "jk!")

    # Edge cases
    def test_encrypt_empty_string(self) -> None:
        self.assertEqual(caesar_encrypt("", 3, ALPHABET), "")

    def test_encrypt_single_char(self) -> None:
        self.assertEqual(caesar_encrypt("a", 1, ALPHABET), "b")

    def test_encrypt_large_shift(self) -> None:
        self.assertEqual(caesar_encrypt("a", 53, ALPHABET), "b")

    # Custom alphabet
    def test_encrypt_custom_alphabet(self) -> None:
        custom = list("abc")
        self.assertEqual(caesar_encrypt("abc", 1, custom), "bca")

if __name__ == "__main__":
    unittest.main()
