import unittest
from utils.hashes.explorar_hashes import hash_md5, hash_sha1, hash_sha256, hash_sha3_256


class TestHashMD5(unittest.TestCase):

    def test_known_value(self):
        self.assertEqual(hash_md5("MediSoft-v2.1.0"), "cac2fe40370e3a68f0a4927c20c75c89")

    def test_empty_string(self):
        self.assertEqual(hash_md5(""), "d41d8cd98f00b204e9800998ecf8427e")

    def test_hex_length(self):
        self.assertEqual(len(hash_md5("MediSoft-v2.1.0")), 32)  # 128 bits / 4

    def test_determinism(self):
        self.assertEqual(hash_md5("MediSoft-v2.1.0"), hash_md5("MediSoft-v2.1.0"))

    def test_case_sensitivity(self):
        self.assertNotEqual(hash_md5("MediSoft-v2.1.0"), hash_md5("medisoft-v2.1.0"))


class TestHashSHA1(unittest.TestCase):

    def test_known_value(self):
        self.assertEqual(hash_sha1("MediSoft-v2.1.0"), "3ab92abc44e23465b154e887f90c3a5e0d642c65")

    def test_empty_string(self):
        self.assertEqual(hash_sha1(""), "da39a3ee5e6b4b0d3255bfef95601890afd80709")

    def test_hex_length(self):
        self.assertEqual(len(hash_sha1("MediSoft-v2.1.0")), 40)  # 160 bits / 4

    def test_determinism(self):
        self.assertEqual(hash_sha1("MediSoft-v2.1.0"), hash_sha1("MediSoft-v2.1.0"))

    def test_case_sensitivity(self):
        self.assertNotEqual(hash_sha1("MediSoft-v2.1.0"), hash_sha1("medisoft-v2.1.0"))


class TestHashSHA256(unittest.TestCase):

    def test_known_value(self):
        self.assertEqual(
            hash_sha256("MediSoft-v2.1.0"),
            "64942401fe64ac1182bd88326ba7ca57a23ea5d0475653dea996ac15e8e74996",
        )

    def test_empty_string(self):
        self.assertEqual(
            hash_sha256(""),
            "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        )

    def test_hex_length(self):
        self.assertEqual(len(hash_sha256("MediSoft-v2.1.0")), 64)  # 256 bits / 4

    def test_determinism(self):
        self.assertEqual(hash_sha256("MediSoft-v2.1.0"), hash_sha256("MediSoft-v2.1.0"))

    def test_case_sensitivity(self):
        self.assertNotEqual(hash_sha256("MediSoft-v2.1.0"), hash_sha256("medisoft-v2.1.0"))


class TestHashSHA3_256(unittest.TestCase):

    def test_known_value(self):
        self.assertEqual(
            hash_sha3_256("MediSoft-v2.1.0"),
            "3b0af4c0a9078e2ddc1606313db9206dcb3a4dbf423d78c0cf16929d303e30d2",
        )

    def test_empty_string(self):
        self.assertEqual(
            hash_sha3_256(""),
            "a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a",
        )

    def test_hex_length(self):
        self.assertEqual(len(hash_sha3_256("MediSoft-v2.1.0")), 64)  # 256 bits / 4

    def test_determinism(self):
        self.assertEqual(hash_sha3_256("MediSoft-v2.1.0"), hash_sha3_256("MediSoft-v2.1.0"))

    def test_case_sensitivity(self):
        self.assertNotEqual(hash_sha3_256("MediSoft-v2.1.0"), hash_sha3_256("medisoft-v2.1.0"))


if __name__ == "__main__":
    unittest.main()
