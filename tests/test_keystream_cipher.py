import unittest
from unittest.mock import patch

from utils.keystream.keystream_cipher import encrypt_with_keystream


class TestKeystreamCipher(unittest.TestCase):

    def test_encrypt_returns_string(self) -> None:
        ciphertext = encrypt_with_keystream("HELLO", "seed")
        self.assertIsInstance(ciphertext, str)

    def test_ciphertext_has_same_length_as_plaintext(self) -> None:
        plaintext = "HELLO STREAM"
        ciphertext = encrypt_with_keystream(plaintext, "seed")
        self.assertEqual(len(ciphertext), len(plaintext))

    def test_same_plaintext_and_seed_are_deterministic(self) -> None:
        plaintext = "deterministic"
        cipher_1 = encrypt_with_keystream(plaintext, "same-seed")
        cipher_2 = encrypt_with_keystream(plaintext, "same-seed")
        self.assertEqual(cipher_1, cipher_2)

    def test_different_seed_produces_different_ciphertext(self) -> None:
        plaintext = "HELLO WORLD"
        cipher_1 = encrypt_with_keystream(plaintext, "seed-a")
        cipher_2 = encrypt_with_keystream(plaintext, "seed-b")
        self.assertNotEqual(cipher_1, cipher_2)

    def test_encrypt_decrypt_round_trip_with_same_seed(self) -> None:
        plaintext = "XOR stream cipher"
        ciphertext = encrypt_with_keystream(plaintext, "course-key")
        recovered = encrypt_with_keystream(ciphertext, "course-key")
        self.assertEqual(recovered, plaintext)

    def test_empty_plaintext_returns_empty(self) -> None:
        self.assertEqual(encrypt_with_keystream("", "seed"), "")

    def test_invalid_plaintext_type_raises_type_error(self) -> None:
        with self.assertRaises(TypeError):
            encrypt_with_keystream(123, "seed")

    def test_invalid_seed_type_raises_type_error(self) -> None:
        with self.assertRaises(TypeError):
            encrypt_with_keystream("hello", 3.1416)

    @patch("utils.keystream.keystream_cipher.generate_prng_keystream")
    def test_generates_keystream_for_plaintext_length(self, mock_keystream) -> None:
        plaintext = "ABCDE"
        mock_keystream.return_value = "12345"
        encrypt_with_keystream(plaintext, "seed")
        mock_keystream.assert_called_once_with("seed", len(plaintext))


if __name__ == "__main__":
    unittest.main()
