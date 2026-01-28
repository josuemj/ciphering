import unittest
from utils.ciphers.xor_cipher import xor_cipher

class TestXorCipher(unittest.TestCase):
    

    # Basic functionality tests
    def test_encrypt_decrypt_symmetric(self) -> None:
        """XOR cipher should be symmetric - encrypt then decrypt returns original."""
        plaintext = "Hello"
        key = "Key12"
        encrypted = xor_cipher(plaintext, key)
        decrypted = xor_cipher(encrypted, key)
        self.assertEqual(decrypted, plaintext)

    def test_different_key_different_result(self) -> None:
        """Different keys should produce different ciphertexts."""
        plaintext = "Hello"
        key1 = "Key12"
        key2 = "Other"
        encrypted1 = xor_cipher(plaintext, key1)
        encrypted2 = xor_cipher(plaintext, key2)
        self.assertNotEqual(encrypted1, encrypted2)

    # Key cycling tests
    def test_key_shorter_than_text(self) -> None:
        """Key should cycle when shorter than text."""
        plaintext = "HelloWorld"  # 10 chars
        key = "AB"  # 2 chars - will cycle 5 times
        encrypted = xor_cipher(plaintext, key)
        decrypted = xor_cipher(encrypted, key)
        self.assertEqual(decrypted, plaintext)

    def test_key_longer_than_text(self) -> None:
        """Should work when key is longer than text."""
        plaintext = "Hi"
        key = "VeryLongKey"
        encrypted = xor_cipher(plaintext, key)
        decrypted = xor_cipher(encrypted, key)
        self.assertEqual(decrypted, plaintext)

    def test_key_same_length_as_text(self) -> None:
        """Should work when key and text have same length."""
        plaintext = "Hello"
        key = "World"
        encrypted = xor_cipher(plaintext, key)
        decrypted = xor_cipher(encrypted, key)
        self.assertEqual(decrypted, plaintext)

    # Return type tests
    def test_returns_string(self) -> None:
        """xor_cipher should return a string."""
        result = xor_cipher("Hello", "Key")
        self.assertIsInstance(result, str)

    def test_result_same_length_as_text(self) -> None:
        """Result should have same length as input text."""
        plaintext = "Hello World!"
        key = "Key"
        encrypted = xor_cipher(plaintext, key)
        self.assertEqual(len(encrypted), len(plaintext))

    # Edge cases
    def test_single_character(self) -> None:
        """Should work with single character text and key."""
        plaintext = "A"
        key = "B"
        encrypted = xor_cipher(plaintext, key)
        decrypted = xor_cipher(encrypted, key)
        self.assertEqual(decrypted, plaintext)

    def test_empty_text(self) -> None:
        """Empty text should return empty string."""
        result = xor_cipher("", "key")
        self.assertEqual(result, "")

    def test_same_text_and_key(self) -> None:
        """XOR of same values should produce null characters."""
        text = "AAA"
        key = "AAA"
        result = xor_cipher(text, key)
        # A XOR A = 0 for each character
        self.assertEqual(result, "\x00\x00\x00")

    # Error handling tests
    def test_empty_key_raises_error(self) -> None:
        """Empty key should raise ValueError."""
        with self.assertRaises(ValueError):
            xor_cipher("Hello", "")

    def test_invalid_text_type_raises_error(self) -> None:
        """Non-string text should raise TypeError."""
        with self.assertRaises(TypeError):
            xor_cipher(12345, "key")

    def test_invalid_key_type_raises_error(self) -> None:
        """Non-string key should raise TypeError."""
        with self.assertRaises(TypeError):
            xor_cipher("Hello", 12345)

    def test_none_text_raises_error(self) -> None:
        """None text should raise TypeError."""
        with self.assertRaises(TypeError):
            xor_cipher(None, "key")

    def test_none_key_raises_error(self) -> None:
        """None key should raise TypeError."""
        with self.assertRaises(TypeError):
            xor_cipher("Hello", None)

    # Special characters tests
    def test_with_spaces(self) -> None:
        """Should handle spaces correctly."""
        plaintext = "Hello World"
        key = "Key"
        encrypted = xor_cipher(plaintext, key)
        decrypted = xor_cipher(encrypted, key)
        self.assertEqual(decrypted, plaintext)

    def test_with_special_characters(self) -> None:
        """Should handle special characters correctly."""
        plaintext = "Hello!@#$%^&*()"
        key = "Key123"
        encrypted = xor_cipher(plaintext, key)
        decrypted = xor_cipher(encrypted, key)
        self.assertEqual(decrypted, plaintext)

    def test_with_newlines(self) -> None:
        """Should handle newlines correctly."""
        plaintext = "Hello\nWorld\n"
        key = "Key"
        encrypted = xor_cipher(plaintext, key)
        decrypted = xor_cipher(encrypted, key)
        self.assertEqual(decrypted, plaintext)


if __name__ == "__main__":
    unittest.main()
