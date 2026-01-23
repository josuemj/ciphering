import unittest
from utils.binary_to_base64 import binary_to_base64


class TestBinaryToBase64(unittest.TestCase):
    """Tests for binary_to_base64 function"""

    def test_TQ_example(self) -> None:
        """Test conversion from docstring example: 'TQ'"""
        self.assertEqual(binary_to_base64("010011010000"), "TQ")

    def test_SGk_example(self) -> None:
        """Test conversion from docstring example: 'SGk'"""
        self.assertEqual(binary_to_base64("010010000110100100"), "SGk")

    def test_empty_string(self) -> None:
        """Test empty binary string returns empty Base64"""
        self.assertEqual(binary_to_base64(""), "")

    def test_single_6bit_group(self) -> None:
        """Test single 6-bit group (A=0)"""
        self.assertEqual(binary_to_base64("000000"), "A")

    def test_single_6bit_group_max(self) -> None:
        """Test single 6-bit group max value (/ = 63)"""
        self.assertEqual(binary_to_base64("111111"), "/")

    def test_padding_needed_4bits(self) -> None:
        """Test when binary length is not multiple of 6 (needs 2 zeros padding)"""
        # 0101 -> 010100 -> 20 -> U
        self.assertEqual(binary_to_base64("0101"), "U")

    def test_padding_needed_1bit(self) -> None:
        """Test when binary length needs 5 zeros padding"""
        # 1 -> 100000 -> 32 -> g
        self.assertEqual(binary_to_base64("1"), "g")

    def test_24bit_hello(self) -> None:
        """Test 24-bit binary (3 bytes = 4 Base64 chars)"""
        # "SGVs" represents "Hel"
        # H=72=01001000, e=101=01100101, l=108=01101100
        binary = "010010000110010101101100"
        self.assertEqual(binary_to_base64(binary), "SGVs")

    def test_invalid_characters(self) -> None:
        """Test that invalid characters raise ValueError"""
        with self.assertRaises(ValueError):
            binary_to_base64("01001102")
        with self.assertRaises(ValueError):
            binary_to_base64("0101a010")

    def test_non_string_input(self) -> None:
        """Test that non-string input raises TypeError"""
        with self.assertRaises(TypeError):
            binary_to_base64(101010)
        with self.assertRaises(TypeError):
            binary_to_base64(None)

    def test_all_base64_chars_A_to_Z(self) -> None:
        """Test that values 0-25 map to A-Z"""
        for i in range(26):
            binary = format(i, '06b')
            expected = chr(ord('A') + i)
            self.assertEqual(binary_to_base64(binary), expected)

    def test_all_base64_chars_a_to_z(self) -> None:
        """Test that values 26-51 map to a-z"""
        for i in range(26):
            binary = format(26 + i, '06b')
            expected = chr(ord('a') + i)
            self.assertEqual(binary_to_base64(binary), expected)


if __name__ == "__main__":
    unittest.main()
