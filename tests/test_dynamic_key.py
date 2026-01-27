import unittest
from utils.keys.dynamic_key import generate_dynamic_key


class TestDynamicKey(unittest.TestCase):

    # Length correctness tests
    def test_key_length_10(self) -> None:
        key = generate_dynamic_key(10)
        self.assertEqual(len(key), 10)

    def test_key_length_1(self) -> None:
        key = generate_dynamic_key(1)
        self.assertEqual(len(key), 1)

    def test_key_length_100(self) -> None:
        key = generate_dynamic_key(100)
        self.assertEqual(len(key), 100)

    # Return type tests
    def test_returns_string(self) -> None:
        key = generate_dynamic_key(5)
        self.assertIsInstance(key, str)

    # Character validity tests
    def test_valid_ascii_characters(self) -> None:
        key = generate_dynamic_key(100)
        for char in key:
            self.assertGreaterEqual(ord(char), 0)
            self.assertLessEqual(ord(char), 127)

    def test_all_characters_in_ascii_range(self) -> None:
        key = generate_dynamic_key(500)
        for char in key:
            self.assertTrue(0 <= ord(char) <= 127, f"Character '{repr(char)}' is not valid ASCII")

    # Error handling tests - TypeError
    def test_invalid_k_type_string(self) -> None:
        with self.assertRaises(TypeError):
            generate_dynamic_key("10")

    def test_invalid_k_type_float(self) -> None:
        with self.assertRaises(TypeError):
            generate_dynamic_key(10.5)

    def test_invalid_k_type_none(self) -> None:
        with self.assertRaises(TypeError):
            generate_dynamic_key(None)

    def test_invalid_k_type_list(self) -> None:
        with self.assertRaises(TypeError):
            generate_dynamic_key([10])

    # Error handling tests - ValueError
    def test_invalid_k_value_zero(self) -> None:
        with self.assertRaises(ValueError):
            generate_dynamic_key(0)

    def test_invalid_k_value_negative(self) -> None:
        with self.assertRaises(ValueError):
            generate_dynamic_key(-1)

    def test_invalid_k_value_large_negative(self) -> None:
        with self.assertRaises(ValueError):
            generate_dynamic_key(-100)

    # Randomness tests
    def test_randomness_different_calls(self) -> None:
        keys = [generate_dynamic_key(20) for _ in range(10)]
        unique_keys = set(keys)
        self.assertGreater(len(unique_keys), 1, "Keys should be different across calls")

    def test_randomness_character_variation(self) -> None:
        key = generate_dynamic_key(100)
        unique_chars = set(key)
        self.assertGreater(len(unique_chars), 5, "Key should have character variation")


if __name__ == "__main__":
    unittest.main()
