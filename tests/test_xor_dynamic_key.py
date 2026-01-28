import unittest
from utils.ciphers.xor_cipher import xor_cipher
from utils.keys.dynamic_key import generate_dynamic_key


class TestXOR_DynamicKey(unittest.TestCase):

    def test_encrypt_decrypt_with_dynamic_key(self) -> None:
        """Test encryption and decryption with a dynamically generated key."""
        text = "HAIL HYDRA"
        key = generate_dynamic_key(len(text))
        cipher_text = xor_cipher(text, key)
        decrypted = xor_cipher(cipher_text, key)
        self.assertEqual(decrypted, text)

    def test_cipher_text_differs_from_plain(self) -> None:
        """Cipher text should not equal the original plaintext."""
        text = "hollyyyyyy mollyyyyy guacamole"
        key = generate_dynamic_key(len(text))
        cipher_text = xor_cipher(text, key)
        self.assertNotEqual(cipher_text, text)

    def test_key_length_matches_text(self) -> None:
        """Dynamic key length should match the text length."""
        text = "hsdafgfhgjhdtrer24356"
        key = generate_dynamic_key(len(text))
        self.assertEqual(len(key), len(text))

    def test_different_keys_produce_different_ciphers(self) -> None:
        """Two different dynamic keys should produce different cipher texts."""
        text = "LUDWING WAS HERE"
        key1 = generate_dynamic_key(len(text))
        key2 = generate_dynamic_key(len(text))
        cipher1 = xor_cipher(text, key1)
        cipher2 = xor_cipher(text, key2)
        self.assertNotEqual(cipher1, cipher2)

    def test_cipher_text_same_length_as_plain(self) -> None:
        """Cipher text should have the same length as the plaintext."""
        text = "Ibubuue ublemoucle osas"
        key = generate_dynamic_key(len(text))
        cipher_text = xor_cipher(text, key)
        self.assertEqual(len(cipher_text), len(text))


if __name__ == "__main__":
    unittest.main()
