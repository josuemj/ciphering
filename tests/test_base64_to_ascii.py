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


if __name__ == "__main__":
    unittest.main()
