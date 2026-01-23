import unittest

from utils.binary_to_decimal import binary6_to_decimal, binary_to_decimal


class TestBinary6ToDecimal(unittest.TestCase): 
    """Tests for binary6_to_decimal function (6-bit binary to decimal 0-63)"""
    
    def test_all_zeros(self) -> None:
        """Test conversion of 000000 to 0"""
        self.assertEqual(binary6_to_decimal("000000"), 0)
    
    def test_all_ones(self) -> None:
        """Test conversion of 111111 to 63"""
        self.assertEqual(binary6_to_decimal("111111"), 63)
    
    def test_one(self) -> None:
        """Test conversion of 000001 to 1"""
        self.assertEqual(binary6_to_decimal("000001"), 1)
    
    def test_two(self) -> None:
        """Test conversion of 000010 to 2"""
        self.assertEqual(binary6_to_decimal("000010"), 2)
    
    def test_nineteen(self) -> None:
        """Test conversion of 010011 to 19 (T in Base64)"""
        self.assertEqual(binary6_to_decimal("010011"), 19)
    
    def test_sixteen(self) -> None:
        """Test conversion of 010000 to 16 (Q in Base64)"""
        self.assertEqual(binary6_to_decimal("010000"), 16)
    
    def test_thirty_two(self) -> None:
        """Test conversion of 100000 to 32"""
        self.assertEqual(binary6_to_decimal("100000"), 32)
    
    def test_rejects_non_string(self) -> None:
        """Test that non-string input raises TypeError"""
        with self.assertRaises(TypeError):
            binary6_to_decimal(123456)
    
    def test_rejects_too_short(self) -> None:
        """Test that strings shorter than 6 chars raise ValueError"""
        with self.assertRaises(ValueError):
            binary6_to_decimal("01011")
    
    def test_rejects_too_long(self) -> None:
        """Test that strings longer than 6 chars raise ValueError"""
        with self.assertRaises(ValueError):
            binary6_to_decimal("0101110")
    
    def test_rejects_invalid_characters(self) -> None:
        """Test that invalid characters raise ValueError"""
        with self.assertRaises(ValueError):
            binary6_to_decimal("01012a")


class TestBinaryToDecimal(unittest.TestCase):
    """Tests for binary_to_decimal function (any length binary to decimal)"""
    
    def test_8bit_zero(self) -> None:
        """Test conversion of 00000000 to 0"""
        self.assertEqual(binary_to_decimal("00000000"), 0)
    
    def test_8bit_max(self) -> None:
        """Test conversion of 11111111 to 255"""
        self.assertEqual(binary_to_decimal("11111111"), 255)
    
    def test_ascii_A(self) -> None:
        """Test conversion of 01000001 to 65 (ASCII 'A')"""
        self.assertEqual(binary_to_decimal("01000001"), 65)
    
    def test_single_bit_one(self) -> None:
        """Test conversion of '1' to 1"""
        self.assertEqual(binary_to_decimal("1"), 1)
    
    def test_single_bit_zero(self) -> None:
        """Test conversion of '0' to 0"""
        self.assertEqual(binary_to_decimal("0"), 0)
    
    def test_16bit_value(self) -> None:
        """Test conversion of 16-bit binary"""
        self.assertEqual(binary_to_decimal("0000000100000000"), 256)
    
    def test_rejects_non_string(self) -> None:
        """Test that non-string input raises TypeError"""
        with self.assertRaises(TypeError):
            binary_to_decimal(12345678)
    
    def test_rejects_empty_string(self) -> None:
        """Test that empty string raises ValueError"""
        with self.assertRaises(ValueError):
            binary_to_decimal("")
    
    def test_rejects_invalid_characters(self) -> None:
        """Test that invalid characters raise ValueError"""
        with self.assertRaises(ValueError):
            binary_to_decimal("0101012a")


if __name__ == "__main__":
    unittest.main()
