import unittest

from utils.base64_to_ascii import base64_to_ascii


class TestBase64ToAscii(unittest.TestCase):
    def test_decodes_hello(self) -> None:
        self.assertEqual(base64_to_ascii("SGVsbG8="), "Hello")

    def test_decodes_sentence_without_padding(self) -> None:
        self.assertEqual(base64_to_ascii("SGVsbG8gV29ybGQh"), "Hello World!")

    def test_handles_padding(self) -> None:
        self.assertEqual(base64_to_ascii("TWE="), "Ma")

    def test_empty_string(self) -> None:
        self.assertEqual(base64_to_ascii(""), "")

    def test_only_padding(self) -> None:
        self.assertEqual(base64_to_ascii("=="), "")

    def test_non_string_input(self) -> None:
        with self.assertRaises(TypeError):
            base64_to_ascii(123)  # type: ignore[arg-type]

    def test_invalid_character(self) -> None:
        with self.assertRaises(ValueError):
            base64_to_ascii("SGVsbG8@")

    def test_invalid_bit_length(self) -> None:
        with self.assertRaises(ValueError):
            base64_to_ascii("A")

    def test_decodes_long_phrase(self) -> None:
        self.assertEqual(
            base64_to_ascii("VGhlIHF1aWNrIGJyb3duIGZveCBqdW1wcyBvdmVyIHRoZSBsYXp5IGRvZw=="),
            "The quick brown fox jumps over the lazy dog"
        )

    def test_decodes_spanish_phrase(self) -> None:
        # "Hola mundo"
        self.assertEqual(base64_to_ascii("SG9sYSBtdW5kbw=="), "Hola mundo")

    def test_decodes_phrase_with_punctuation(self) -> None:
        # "Hello, World! How are you?"
        self.assertEqual(
            base64_to_ascii("SGVsbG8sIFdvcmxkISBIb3cgYXJlIHlvdT8="),
            "Hello, World! How are you?"
        )

    def test_decodes_numbers(self) -> None:
        # "12345"
        self.assertEqual(base64_to_ascii("MTIzNDU="), "12345")

    def test_decodes_mixed_alphanumeric(self) -> None:
        # "abc123XYZ"
        self.assertEqual(base64_to_ascii("YWJjMTIzWFla"), "abc123XYZ")

    # Edge cases
    def test_single_character(self) -> None:
        # "A"
        self.assertEqual(base64_to_ascii("QQ=="), "A")

    def test_two_characters(self) -> None:
        # "AB"
        self.assertEqual(base64_to_ascii("QUI="), "AB")

    def test_three_characters(self) -> None:
        # "ABC" - no padding needed
        self.assertEqual(base64_to_ascii("QUJD"), "ABC")

    def test_special_characters(self) -> None:
        # "!@#$%^&*()"
        self.assertEqual(base64_to_ascii("IUAjJCVeJiooKQ=="), "!@#$%^&*()")

    def test_whitespace_only(self) -> None:
        # "   " (three spaces)
        self.assertEqual(base64_to_ascii("ICAg"), "   ")

    def test_tabs_and_newlines(self) -> None:
        # "a\tb\nc"
        self.assertEqual(base64_to_ascii("YQliCm4="), "a\tb\nn")

    def test_multiline_text(self) -> None:
        # "Line1\nLine2\nLine3"
        self.assertEqual(
            base64_to_ascii("TGluZTEKTGluZTIKTGluZTM="),
            "Line1\nLine2\nLine3"
        )

    def test_all_lowercase(self) -> None:
        # "abcdefghijklmnopqrstuvwxyz"
        self.assertEqual(
            base64_to_ascii("YWJjZGVmZ2hpamtsbW5vcHFyc3R1dnd4eXo="),
            "abcdefghijklmnopqrstuvwxyz"
        )

    def test_all_uppercase(self) -> None:
        # "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        self.assertEqual(
            base64_to_ascii("QUJDREVGR0hJSktMTU5PUFFSU1RVVldYWVo="),
            "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        )

    def test_all_digits(self) -> None:
        # "0123456789"
        self.assertEqual(base64_to_ascii("MDEyMzQ1Njc4OQ=="), "0123456789")

    def test_cryptography_phrase(self) -> None:
        # "Cryptography is fun!"
        self.assertEqual(
            base64_to_ascii("Q3J5cHRvZ3JhcGh5IGlzIGZ1biE="),
            "Cryptography is fun!"
        )

    def test_invalid_length_two_chars(self) -> None:
        with self.assertRaises(ValueError):
            base64_to_ascii("AB")  # Invalid length

    def test_whitespace_in_base64(self) -> None:
        with self.assertRaises(ValueError):
            base64_to_ascii("SGVs bG8=")  # Space is invalid in base64

    def test_newline_in_base64(self) -> None:
        with self.assertRaises(ValueError):
            base64_to_ascii("SGVs\nbG8=")  # Newline is invalid


if __name__ == "__main__":
    unittest.main()
