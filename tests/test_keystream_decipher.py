import unittest
from unittest.mock import patch

from utils.keystream.keystream_cipher import encrypt_with_keystream
from utils.keystream.keystream_decipher import decrypt_with_keystream


class TestKeystreamDecipher(unittest.TestCase):

    def test_decrypt_returns_string(self) -> None:
        plaintext = "HELLO"
        ciphertext = encrypt_with_keystream(plaintext, "seed")
        decrypted = decrypt_with_keystream(ciphertext, "seed")
        self.assertIsInstance(decrypted, str)

    def test_decrypt_recovers_exact_original_plaintext(self) -> None:
        plaintext = "Mensaje original 123 !?"
        ciphertext = encrypt_with_keystream(plaintext, "class-key")
        decrypted = decrypt_with_keystream(ciphertext, "class-key")
        self.assertEqual(decrypted, plaintext)

    def test_decrypted_length_matches_original_plaintext(self) -> None:
        plaintext = "STREAM CIPHER"
        ciphertext = encrypt_with_keystream(plaintext, "seed")
        decrypted = decrypt_with_keystream(ciphertext, "seed")
        self.assertEqual(len(decrypted), len(plaintext))

    def test_wrong_seed_does_not_recover_plaintext(self) -> None:
        plaintext = "secure message"
        ciphertext = encrypt_with_keystream(plaintext, "correct-seed")
        decrypted = decrypt_with_keystream(ciphertext, "wrong-seed")
        self.assertNotEqual(decrypted, plaintext)

    def test_empty_ciphertext_returns_empty(self) -> None:
        self.assertEqual(decrypt_with_keystream("", "seed"), "")

    def test_invalid_ciphertext_type_raises_type_error(self) -> None:
        with self.assertRaises(TypeError):
            decrypt_with_keystream(404, "seed")

    def test_invalid_seed_type_raises_type_error(self) -> None:
        with self.assertRaises(TypeError):
            decrypt_with_keystream("cipher", 2.718)

    @patch("utils.keystream.keystream_decipher.generate_prng_keystream")
    def test_generates_keystream_for_ciphertext_length(self, mock_keystream) -> None:
        ciphertext = "ABCDE"
        mock_keystream.return_value = "12345"
        decrypt_with_keystream(ciphertext, "seed")
        mock_keystream.assert_called_once_with("seed", len(ciphertext))


if __name__ == "__main__":
    unittest.main()
