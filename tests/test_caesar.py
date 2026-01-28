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

class TestCaesarDecrypt(unittest.TestCase):

    # Basic decryption tests
    def test_decrypt_khoor(self) -> None:
        self.assertEqual(caesar_decrypt("khoor", 3, ALPHABET), "hello")

    def test_decrypt_bcd(self) -> None:
        self.assertEqual(caesar_decrypt("bcd", 1, ALPHABET), "abc")

    def test_decrypt_abc_wraps(self) -> None:
        self.assertEqual(caesar_decrypt("abc", 3, ALPHABET), "xyz")

    def test_decrypt_shift_zero(self) -> None:
        self.assertEqual(caesar_decrypt("hello", 0, ALPHABET), "hello")

    def test_decrypt_full_rotation(self) -> None:
        self.assertEqual(caesar_decrypt("hello", 26, ALPHABET), "hello")

    # Non-alphabet characters preserved
    def test_decrypt_preserves_spaces(self) -> None:
        self.assertEqual(caesar_decrypt("khoor zruog", 3, ALPHABET), "hello world")

    def test_decrypt_preserves_numbers(self) -> None:
        self.assertEqual(caesar_decrypt("bcd123", 1, ALPHABET), "abc123")

    def test_decrypt_preserves_punctuation(self) -> None:
        self.assertEqual(caesar_decrypt("jk!", 2, ALPHABET), "hi!")

    # Edge cases
    def test_decrypt_empty_string(self) -> None:
        self.assertEqual(caesar_decrypt("", 3, ALPHABET), "")

    def test_decrypt_single_char(self) -> None:
        self.assertEqual(caesar_decrypt("b", 1, ALPHABET), "a")

    def test_decrypt_large_shift(self) -> None:
        self.assertEqual(caesar_decrypt("b", 53, ALPHABET), "a")

    # Roundtrip: encrypt then decrypt returns original
    def test_roundtrip(self) -> None:
        original = "the quick brown fox"
        shift = 7
        encrypted = caesar_encrypt(original, shift, ALPHABET)
        decrypted = caesar_decrypt(encrypted, shift, ALPHABET)
        self.assertEqual(decrypted, original)

    def test_roundtrip_all_letters(self) -> None:
        original = "abcdefghijklmnopqrstuvwxyz"
        shift = 13
        encrypted = caesar_encrypt(original, shift, ALPHABET)
        decrypted = caesar_decrypt(encrypted, shift, ALPHABET)
        self.assertEqual(decrypted, original)

if __name__ == "__main__":
    unittest.main()
