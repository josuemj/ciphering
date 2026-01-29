import unittest
from utils.ciphers.rot13 import rot13
from test_caesar import ALPHABET

class TestROT13(unittest.TestCase):

    # Basic tests
    def test_hello(self) -> None:
        self.assertEqual(rot13("hello", ALPHABET), "uryyb")

    def test_uryyb(self) -> None:
        self.assertEqual(rot13("uryyb", ALPHABET), "hello")

    def test_abc(self) -> None:
        self.assertEqual(rot13("abc", ALPHABET), "nop")

    # ROT13 property: applying twice returns original
    def test_double_rot13(self) -> None:
        self.assertEqual(rot13(rot13("hello", ALPHABET), ALPHABET), "hello")
    def test_double_rot13_full_alphabet(self) -> None:
        original = "abcdefghijklmnopqrstuvwxyz"
        self.assertEqual(rot13(rot13(original, ALPHABET), ALPHABET), original)

    # Non-alphabet characters preserved
    def test_preserves_spaces(self) -> None:
        self.assertEqual(rot13("hello world", ALPHABET), "uryyb jbeyq")

    def test_preserves_numbers(self) -> None:
        self.assertEqual(rot13("abc123", ALPHABET), "nop123")

    def test_preserves_punctuation(self) -> None:
        self.assertEqual(rot13("hi!", ALPHABET), "uv!")

    # Edge cases
    def test_empty_string(self) -> None:
        self.assertEqual(rot13("", ALPHABET), "")

    def test_single_char(self) -> None:
        self.assertEqual(rot13("a", ALPHABET), "n")

    def test_single_char_n(self) -> None:
        self.assertEqual(rot13("n", ALPHABET), "a")

    # Full alphabet shift
    def test_full_alphabet(self) -> None:
        self.assertEqual(
            rot13("abcdefghijklmnopqrstuvwxyz", ALPHABET),
            "nopqrstuvwxyzabcdefghijklm",
        )


if __name__ == "__main__":
    unittest.main()
