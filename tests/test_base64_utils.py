import unittest

from utils.base64_utils import DECIMAL_TO_BASE64, get_base64_char, BASE64_PADDING


class TestDecimalToBase64Dict(unittest.TestCase):
    """Tests for the DECIMAL_TO_BASE64 dictionary"""
    
    def test_dictionary_has_64_entries(self) -> None:
        """Test that dictionary has exactly 64 entries (0-63)"""
        self.assertEqual(len(DECIMAL_TO_BASE64), 64)
    
    def test_uppercase_A_to_Z(self) -> None:
        """Test A-Z mapping to 0-25"""
        for i in range(26):
            self.assertEqual(DECIMAL_TO_BASE64[i], chr(ord('A') + i))
    
    def test_lowercase_a_to_z(self) -> None:
        """Test a-z mapping to 26-51"""
        for i in range(26):
            self.assertEqual(DECIMAL_TO_BASE64[26 + i], chr(ord('a') + i))
    
    def test_digits_0_to_9(self) -> None:
        """Test 0-9 mapping to 52-61"""
        for i in range(10):
            self.assertEqual(DECIMAL_TO_BASE64[52 + i], chr(ord('0') + i))
    
    def test_plus_sign(self) -> None:
        """Test + mapping to 62"""
        self.assertEqual(DECIMAL_TO_BASE64[62], '+')
    
    def test_forward_slash(self) -> None:
        """Test / mapping to 63"""
        self.assertEqual(DECIMAL_TO_BASE64[63], '/')
    
    def test_padding_character(self) -> None:
        """Test padding character is '='"""
        self.assertEqual(BASE64_PADDING, '=')


class TestGetBase64Char(unittest.TestCase):
    """Tests for the get_base64_char function"""
    
    def test_zero_returns_A(self) -> None:
        """Test that 0 returns 'A'"""
        self.assertEqual(get_base64_char(0), 'A')
    
    def test_25_returns_Z(self) -> None:
        """Test that 25 returns 'Z'"""
        self.assertEqual(get_base64_char(25), 'Z')
    
    def test_26_returns_lowercase_a(self) -> None:
        """Test that 26 returns 'a'"""
        self.assertEqual(get_base64_char(26), 'a')
    
    def test_51_returns_lowercase_z(self) -> None:
        """Test that 51 returns 'z'"""
        self.assertEqual(get_base64_char(51), 'z')
    
    def test_52_returns_digit_0(self) -> None:
        """Test that 52 returns '0'"""
        self.assertEqual(get_base64_char(52), '0')
    
    def test_61_returns_digit_9(self) -> None:
        """Test that 61 returns '9'"""
        self.assertEqual(get_base64_char(61), '9')
    
    def test_62_returns_plus(self) -> None:
        """Test that 62 returns '+'"""
        self.assertEqual(get_base64_char(62), '+')
    
    def test_63_returns_slash(self) -> None:
        """Test that 63 returns '/'"""
        self.assertEqual(get_base64_char(63), '/')
    
    def test_rejects_negative_number(self) -> None:
        """Test that negative numbers raise ValueError"""
        with self.assertRaises(ValueError):
            get_base64_char(-1)
    
    def test_rejects_too_large_number(self) -> None:
        """Test that numbers > 63 raise ValueError"""
        with self.assertRaises(ValueError):
            get_base64_char(64)
    
    def test_rejects_non_integer(self) -> None:
        """Test that non-integers raise TypeError"""
        with self.assertRaises(TypeError):
            get_base64_char("0")
        with self.assertRaises(TypeError):
            get_base64_char(3.14)


if __name__ == "__main__":
    unittest.main()
