import unittest

from utils.ciphers.vigere import vigere_decrypt, vigere_encrypt

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


class TestVigereDecrypt(unittest.TestCase):

    def test_basic_decryption_with_repeating_key(self) -> None:
        """Known ciphertext/plaintext pair verifies key repetition logic."""
        ciphertext = "lxfopvefrnhr"
        key = "lemon"
        expected_plaintext = "attackatdawn"
        self.assertEqual(
            vigere_decrypt(ciphertext, key, ALPHABET),
            expected_plaintext,
        )

    def test_key_longer_than_text_truncates(self) -> None:
        """When the key is longer than the text, only the needed prefix is used."""
        ciphertext = "ssyrg"
        key = "longsecret"
        expected_plaintext = "hello"
        self.assertEqual(
            vigere_decrypt(ciphertext, key, ALPHABET),
            expected_plaintext,
        )

    def test_key_same_length_uses_one_time_pad_behavior(self) -> None:
        """Key that matches the text length should not repeat or truncate."""
        ciphertext = "ticksd"
        key = "random"
        expected_plaintext = "cipher"
        self.assertEqual(
            vigere_decrypt(ciphertext, key, ALPHABET),
            expected_plaintext,
        )

    def test_encrypt_then_decrypt_roundtrip(self) -> None:
        """Encrypting and then decrypting should return the original text."""
        plaintext = "thequickbrownfox"
        key = "secret"
        intermediate = vigere_encrypt(plaintext, key, ALPHABET)
        self.assertEqual(
            vigere_decrypt(intermediate, key, ALPHABET),
            plaintext,
        )

    def test_text_char_not_in_alphabet_raises(self) -> None:
        """Characters outside the alphabet should raise ValueError."""
        with self.assertRaises(ValueError):
            vigere_decrypt("ABC", "key", ALPHABET)


if __name__ == "__main__":
    unittest.main()
