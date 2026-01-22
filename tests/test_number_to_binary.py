import unittest

from utils.number_to_binary import decimal_to_binary, decimal_to_binary_6


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


class TestDecimalToBinary6(unittest.TestCase):
    """Tests for decimal_to_binary_6 function (Base64 conversion)"""
    
    def test_zero(self) -> None:
        """Test conversion of 0 to 6-bit binary"""
        self.assertEqual(decimal_to_binary_6(0), "000000")
    
    def test_one(self) -> None:
        """Test conversion of 1 to 6-bit binary"""
        self.assertEqual(decimal_to_binary_6(1), "000001")
    
    def test_six(self) -> None:
        """Test conversion of 6 to 6-bit binary"""
        self.assertEqual(decimal_to_binary_6(6), "000110")
    
    def test_eighteen(self) -> None:
        """Test conversion of 18 to 6-bit binary"""
        self.assertEqual(decimal_to_binary_6(18), "010010")
    
    def test_max_value_63(self) -> None:
        """Test conversion of 63 (max Base64 value) to 6-bit binary"""
        self.assertEqual(decimal_to_binary_6(63), "111111")
    
    def test_letter_T_base64_value(self) -> None:
        """Test conversion of 19 (Base64 'T') to 6-bit binary"""
        self.assertEqual(decimal_to_binary_6(19), "010011")
    
    def test_letter_Q_base64_value(self) -> None:
        """Test conversion of 16 (Base64 'Q') to 6-bit binary"""
        self.assertEqual(decimal_to_binary_6(16), "010000")
    
    def test_all_6_bits_length(self) -> None:
        """Test that all conversions produce exactly 6 bits"""
        for value in range(64):
            result = decimal_to_binary_6(value)
            self.assertEqual(len(result), 6, f"Value {value} should produce 6 bits")
    
    def test_only_binary_digits(self) -> None:
        """Test that result contains only 0 and 1"""
        for value in range(64):
            result = decimal_to_binary_6(value)
            self.assertTrue(all(c in '01' for c in result), 
                          f"Result for {value} should only contain 0 and 1")
    
    def test_rejects_negative_number(self) -> None:
        """Test that negative numbers are rejected"""
        with self.assertRaises(ValueError):
            decimal_to_binary_6(-1)
    
    def test_rejects_too_large_number(self) -> None:
        """Test that numbers > 63 are rejected"""
        with self.assertRaises(ValueError):
            decimal_to_binary_6(64)
    
    def test_rejects_non_integer(self) -> None:
        """Test that non-integers are rejected"""
        with self.assertRaises(TypeError):
            decimal_to_binary_6("19")


if __name__ == "__main__":
    unittest.main()
