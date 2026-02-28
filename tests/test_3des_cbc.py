import unittest

from utils.block.triple_des_cbc import (
    generate_iv,
    triple_des_cbc_decrypt,
    triple_des_cbc_encrypt,
)


class TestTripleDESCBC(unittest.TestCase):
    def test_roundtrip_two_key(self) -> None:
        key = b"12345678ABCDEFGH"  # 16 bytes -> K1||K2
        messages = [b"", b"A", b"Short text", b"BlockSized", b"Longer message across blocks!"]
        for msg in messages:
            iv, ct = triple_des_cbc_encrypt(msg, key)
            recovered = triple_des_cbc_decrypt(ct, key, iv)
            self.assertEqual(recovered, msg)

    def test_roundtrip_three_key(self) -> None:
        key = b"SixteenByteKeyFor3DES!!!"  # 24 bytes -> K1||K2||K3
        msg = b"3DES with three distinct keys"
        iv, ct = triple_des_cbc_encrypt(msg, key)
        recovered = triple_des_cbc_decrypt(ct, key, iv)
        self.assertEqual(recovered, msg)

    def test_different_iv_each_encryption(self) -> None:
        key = b"12345678ABCDEFGH"
        msg = b"Same plaintext"
        iv1, ct1 = triple_des_cbc_encrypt(msg, key)
        iv2, ct2 = triple_des_cbc_encrypt(msg, key)
        self.assertNotEqual(iv1, iv2)
        self.assertNotEqual(ct1, ct2)

    def test_invalid_key_length(self) -> None:
        with self.assertRaises(ValueError):
            triple_des_cbc_encrypt(b"hi", b"short")
        with self.assertRaises(ValueError):
            triple_des_cbc_decrypt(b"cipher", b"toolongkeytoolongkeytool", b"12345678")

    def test_invalid_iv_length(self) -> None:
        key = b"12345678ABCDEFGH"
        with self.assertRaises(ValueError):
            triple_des_cbc_decrypt(b"ciphertext", key, b"short")

    def test_generate_iv_length(self) -> None:
        iv = generate_iv()
        self.assertEqual(len(iv), 8)


if __name__ == "__main__":
    unittest.main()
