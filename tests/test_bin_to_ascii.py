import unittest

from utils.bin_to_ascii import bin_to_ascii, DECIMAL_TO_ASCII


class TestBinToAscii(unittest.TestCase):
    """Tests for bin_to_ascii function (binary to ASCII text conversion)"""

    # Basic conversion tests
    def test_single_char_uppercase_h(self) -> None:
        """Test conversion of 'H' (01001000)"""
        self.assertEqual(bin_to_ascii("01001000"), "H")

    def test_single_char_lowercase_i(self) -> None:
        """Test conversion of 'i' (01101001)"""
        self.assertEqual(bin_to_ascii("01101001"), "i")

    def test_hello_continuous(self) -> None:
        """Test conversion of 'Hello' as continuous binary"""
        # H=72, e=101, l=108, l=108, o=111
        binary = "0100100001100101011011000110110001101111"
        self.assertEqual(bin_to_ascii(binary), "Hello")

    def test_hello_space_separated(self) -> None:
        """Test conversion of 'Hello' with space-separated bytes"""
        binary = "01001000 01100101 01101100 01101100 01101111"
        self.assertEqual(bin_to_ascii(binary), "Hello")

    def test_hi_continuous(self) -> None:
        """Test conversion of 'Hi' as continuous binary"""
        self.assertEqual(bin_to_ascii("0100100001101001"), "Hi")

    def test_hi_space_separated(self) -> None:
        """Test conversion of 'Hi' with space-separated bytes"""
        self.assertEqual(bin_to_ascii("01001000 01101001"), "Hi")

    # Special character tests
    def test_space_char(self) -> None:
        """Test conversion of space character (32 = 00100000)"""
        self.assertEqual(bin_to_ascii("00100000"), " ")

    def test_exclamation(self) -> None:
        """Test conversion of '!' (33 = 00100001)"""
        self.assertEqual(bin_to_ascii("00100001"), "!")

    def test_newline(self) -> None:
        """Test conversion of newline character (10 = 00001010)"""
        self.assertEqual(bin_to_ascii("00001010"), "\n")

    def test_null_char(self) -> None:
        """Test conversion of null character (0 = 00000000)"""
        self.assertEqual(bin_to_ascii("00000000"), "\x00")

    # Digit tests
    def test_digit_zero(self) -> None:
        """Test conversion of '0' (48 = 00110000)"""
        self.assertEqual(bin_to_ascii("00110000"), "0")

    def test_digit_nine(self) -> None:
        """Test conversion of '9' (57 = 00111001)"""
        self.assertEqual(bin_to_ascii("00111001"), "9")

    # Mixed content tests
    def test_hello_world_with_space(self) -> None:
        """Test conversion of 'Hi!' with space-separated bytes"""
        # H=72, i=105, !=33
        binary = "01001000 01101001 00100001"
        self.assertEqual(bin_to_ascii(binary), "Hi!")

    def test_numbers_123(self) -> None:
        """Test conversion of '123'"""
        # 1=49, 2=50, 3=51
        binary = "00110001 00110010 00110011"
        self.assertEqual(bin_to_ascii(binary), "123")

    # Edge cases
    def test_empty_string(self) -> None:
        """Test conversion of empty string"""
        self.assertEqual(bin_to_ascii(""), "")

    def test_del_char(self) -> None:
        """Test conversion of DEL character (127 = 01111111)"""
        self.assertEqual(bin_to_ascii("01111111"), "\x7f")

    # Error handling tests
    def test_rejects_non_string(self) -> None:
        """Test that non-string input raises TypeError"""
        with self.assertRaises(TypeError):
            bin_to_ascii(12345678)

    def test_rejects_none(self) -> None:
        """Test that None input raises TypeError"""
        with self.assertRaises(TypeError):
            bin_to_ascii(None)

    def test_rejects_list(self) -> None:
        """Test that list input raises TypeError"""
        with self.assertRaises(TypeError):
            bin_to_ascii(["01001000"])

    def test_rejects_not_divisible_by_8(self) -> None:
        """Test that binary string not divisible by 8 raises ValueError"""
        with self.assertRaises(ValueError):
            bin_to_ascii("0100100")  # 7 bits

    def test_rejects_invalid_characters(self) -> None:
        """Test that string with non-binary characters raises ValueError"""
        with self.assertRaises(ValueError):
            bin_to_ascii("0100100a")

    def test_rejects_9_bits(self) -> None:
        """Test that 9-bit string raises ValueError"""
        with self.assertRaises(ValueError):
            bin_to_ascii("010010001")


class TestDecimalToAsciiDict(unittest.TestCase):
    """Tests for the DECIMAL_TO_ASCII dictionary"""

    def test_dict_has_128_entries(self) -> None:
        """Test that dictionary has all 128 ASCII values"""
        self.assertEqual(len(DECIMAL_TO_ASCII), 128)

    def test_dict_maps_65_to_A(self) -> None:
        """Test that 65 maps to 'A'"""
        self.assertEqual(DECIMAL_TO_ASCII[65], "A")

    def test_dict_maps_97_to_a(self) -> None:
        """Test that 97 maps to 'a'"""
        self.assertEqual(DECIMAL_TO_ASCII[97], "a")

    def test_dict_maps_48_to_0(self) -> None:
        """Test that 48 maps to '0'"""
        self.assertEqual(DECIMAL_TO_ASCII[48], "0")

    def test_dict_maps_32_to_space(self) -> None:
        """Test that 32 maps to space"""
        self.assertEqual(DECIMAL_TO_ASCII[32], " ")


if __name__ == "__main__":
    unittest.main()
