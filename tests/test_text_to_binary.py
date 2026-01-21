import unittest

from utils.text_to_binary import text_to_binary


class TestTextToBinary(unittest.TestCase):
    def test_empty_string(self) -> None:
        self.assertEqual(text_to_binary(""), "")

    def test_single_character(self) -> None:
        self.assertEqual(text_to_binary("A"), "01000001")

    def test_multiple_characters(self) -> None:
        self.assertEqual(text_to_binary("AB"), "01000001 01000010")

    def test_includes_space(self) -> None:
        self.assertEqual(text_to_binary("Hi "), "01001000 01101001 00100000")

    def test_control_character_newline(self) -> None:
        self.assertEqual(text_to_binary("A\n"), "01000001 00001010")

    def test_del_character(self) -> None:
        self.assertEqual(text_to_binary("\x7f"), "01111111")

    def test_rejects_non_ascii(self) -> None:
        with self.assertRaises(ValueError):
            text_to_binary("ñ")

    def test_rejects_non_string(self) -> None:
        with self.assertRaises(TypeError):
            text_to_binary(123)


if __name__ == "__main__":
    unittest.main()
