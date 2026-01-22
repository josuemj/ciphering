import unittest

from utils.text_to_binary import text_to_binary, base64_to_binary


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
        
    def test_word(self) -> None:
        self.assertEqual(text_to_binary("Josue"), "01001010 01101111 01110011 01110101 01100101")   

    def test_rejects_non_ascii(self) -> None:
        with self.assertRaisesRegex(ValueError, r"Invalid character 'ñ'"):
            text_to_binary("ñ")

    def test_rejects_non_string(self) -> None:
        with self.assertRaises(TypeError):
            text_to_binary(123)


class TestBase64ToBinary(unittest.TestCase):
    """Tests for base64_to_binary function"""
    
    def test_TQ_with_padding(self) -> None:
        """Test conversion of 'TQ==' (T=19→010011, Q=16→010000)"""
        result = base64_to_binary("TQ==")
        self.assertEqual(result, "010011010000")
    
    def test_SGk_with_padding(self) -> None:
        """Test conversion of 'SGk=' (S=18, G=6, k=36)"""
        # S=18→010010, G=6→000110, k=36→100100
        result = base64_to_binary("SGk=")
        self.assertEqual(result, "010010000110100100")
    
    def test_SG9sYQ_with_padding(self) -> None:
        """Test conversion of 'SG9sYQ==' (Hola in Base64)"""
        # S=18→010010, G=6→000110, 9=61→111101, s=44→101100, Y=24→011000, Q=16→010000
        result = base64_to_binary("SG9sYQ==")
        self.assertEqual(result, "010010000110111101101100011000010000")
    
    def test_no_padding(self) -> None:
        """Test conversion without padding"""
        # A=0→000000, B=1→000001, C=2→000010
        result = base64_to_binary("ABC")
        self.assertEqual(result, "000000000001000010")
    
    def test_single_character(self) -> None:
        """Test single Base64 character (A=0)"""
        result = base64_to_binary("A")
        self.assertEqual(result, "000000")
    
    def test_lowercase_letters(self) -> None:
        """Test lowercase Base64 characters (a=26, b=27)"""
        result = base64_to_binary("ab")
        self.assertEqual(result, "011010011011")
    
    def test_digits(self) -> None:
        """Test Base64 digits (0=52, 1=53)"""
        result = base64_to_binary("01")
        self.assertEqual(result, "110100110101")
    
    def test_special_characters(self) -> None:
        """Test Base64 special characters (+=62, /=63)"""
        result = base64_to_binary("+/")
        self.assertEqual(result, "111110111111")
    
    def test_max_value(self) -> None:
        """Test maximum Base64 value (/ = 63 → 111111)"""
        result = base64_to_binary("/")
        self.assertEqual(result, "111111")
    
    def test_min_value(self) -> None:
        """Test minimum Base64 value (A = 0 → 000000)"""
        result = base64_to_binary("A")
        self.assertEqual(result, "000000")
    
    def test_only_binary_digits(self) -> None:
        """Test that result contains only 0 and 1"""
        result = base64_to_binary("SGVsbG8=")
        self.assertTrue(all(c in '01' for c in result), 
                       "Result should only contain 0 and 1")
    
    def test_six_bits_per_character(self) -> None:
        """Test that each character produces exactly 6 bits"""
        text = "ABCD"  # 4 characters without padding
        result = base64_to_binary(text)
        self.assertEqual(len(result), 24, "4 characters should produce 24 bits (4 × 6)")
    
    def test_padding_not_converted(self) -> None:
        """Test that padding characters are not converted to bits"""
        # TQ== has 2 chars after removing padding, should be 12 bits (2 × 6)
        result = base64_to_binary("TQ==")
        self.assertEqual(len(result), 12, "Padding should not be converted")
    
    def test_rejects_invalid_character(self) -> None:
        """Test that invalid Base64 characters are rejected"""
        with self.assertRaises(ValueError):
            base64_to_binary("AB@C")  # @ is not a valid Base64 character
    
    def test_rejects_non_string(self) -> None:
        """Test that non-strings are rejected"""
        with self.assertRaises(TypeError):
            base64_to_binary(1234)
    
    def test_empty_string(self) -> None:
        """Test empty string"""
        result = base64_to_binary("")
        self.assertEqual(result, "")
    
    def test_only_padding(self) -> None:
        """Test string with only padding characters"""
        result = base64_to_binary("==")
        self.assertEqual(result, "")


if __name__ == "__main__":
    unittest.main()
