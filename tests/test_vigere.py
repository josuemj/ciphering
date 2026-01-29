import unittest

from utils.ciphers.vigere import vigere_encrypt

ALPHABET = list("abcdefghijklmnopqrstuvwxyz")


class TestVigereEncrypt(unittest.TestCase):

    def test_basic_encryption_with_repeating_key(self) -> None:
        """Known plaintext/ciphertext pair verifies key repetition logic."""
        plaintext = "attackatdawn"
        key = "lemon"
        expected_ciphertext = "lxfopvefrnhr"
        self.assertEqual(
            vigere_encrypt(plaintext, key, ALPHABET),
            expected_ciphertext,
        )

    def test_key_longer_than_text_truncates(self) -> None:
        """When the key is longer than the text, only the needed prefix is used."""
        plaintext = "hello"
        key = "longsecret"
        expected_ciphertext = "ssyrg"
        self.assertEqual(
            vigere_encrypt(plaintext, key, ALPHABET),
            expected_ciphertext,
        )

    def test_key_same_length_uses_one_time_pad_behavior(self) -> None:
        """Key that matches the text length should not repeat or truncate."""
        plaintext = "cipher"
        key = "random"
        expected_ciphertext = "ticksd"
        self.assertEqual(
            vigere_encrypt(plaintext, key, ALPHABET),
            expected_ciphertext,
        )

    def test_text_char_not_in_alphabet_raises(self) -> None:
        """Characters outside the alphabet should raise ValueError."""
        with self.assertRaises(ValueError):
            vigere_encrypt("Hello", "key", ALPHABET)


if __name__ == "__main__":
    unittest.main()
