import unittest

from utils.number_to_binary import decimal_to_binary


class TestDecimalToBinary(unittest.TestCase):
    def test_zero(self) -> None:
        self.assertEqual(decimal_to_binary(0), "00000000")

    def test_one(self) -> None:
        self.assertEqual(decimal_to_binary(1), "00000001")

    def test_letter_A_ascii_value(self) -> None:
        self.assertEqual(decimal_to_binary(65), "01000001")

    def test_max_7bit_value(self) -> None:
        self.assertEqual(decimal_to_binary(127), "01111111")

    def test_max_8bit_value(self) -> None:
        self.assertEqual(decimal_to_binary(255), "11111111")

    def test_letter_B_ascii_value(self) -> None:
        self.assertEqual(decimal_to_binary(66), "01000010")

    def test_space_ascii_value(self) -> None:
        self.assertEqual(decimal_to_binary(32), "00100000")

    def test_rejects_negative_number(self) -> None:
        with self.assertRaises(ValueError):
            decimal_to_binary(-1)

    def test_rejects_too_large_number(self) -> None:
        with self.assertRaises(ValueError):
            decimal_to_binary(256)

    def test_rejects_non_integer(self) -> None:
        with self.assertRaises(TypeError):
            decimal_to_binary("65")


if __name__ == "__main__":
    unittest.main()
