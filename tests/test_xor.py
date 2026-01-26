import unittest
from utils.xor import xor

class TestXOR(unittest.TestCase):
    
    # XOR truth table tests
    def test_table_11(self) -> None:
        self.assertEqual(xor("1", "1"), "0")
    
    def test_table_10(self) -> None:
        self.assertEqual(xor("1", "0"), "1")
    
    def test_table_00(self) -> None:
        self.assertEqual(xor("0", "0"), "0")
    
    def test_table_01(self) -> None:
        self.assertEqual(xor("0", "1"), "1")

    # Multi-bit XOR tests
    def test_multi_bit_same(self) -> None:
        self.assertEqual(xor("1010", "1010"), "0000")
    
    def test_multi_bit_opposite(self) -> None:
        self.assertEqual(xor("1010", "0101"), "1111")
    
    def test_multi_bit_mixed(self) -> None:
        self.assertEqual(xor("11001100", "10101010"), "01100110")

    # Edge cases - Empty strings
    def test_empty_strings(self) -> None:
        self.assertEqual(xor("", ""), "")

    # Edge cases - All zeros
    def test_all_zeros(self) -> None:
        self.assertEqual(xor("00000000", "00000000"), "00000000")

    # Edge cases - All ones
    def test_all_ones(self) -> None:
        self.assertEqual(xor("11111111", "11111111"), "00000000")

    # Edge cases - Mixed all ones and zeros
    def test_ones_xor_zeros(self) -> None:
        self.assertEqual(xor("11111111", "00000000"), "11111111")

    # Complex XOR - Long binary strings
    def test_long_binary_strings(self) -> None:
        bin1 = "1100110011001100110011001100110011001100"
        bin2 = "1010101010101010101010101010101010101010"
        expected = "0110011001100110011001100110011001100110"
        self.assertEqual(xor(bin1, bin2), expected)

    # XOR properties - Self-inverse (A XOR A = 0)
    def test_self_inverse_property(self) -> None:
        test_value = "10110011"
        result = xor(test_value, test_value)
        self.assertEqual(result, "0" * len(test_value))

    # XOR properties - Identity (A XOR 0 = A)
    def test_identity_property(self) -> None:
        test_value = "10110011"
        zeros = "0" * len(test_value)
        self.assertEqual(xor(test_value, zeros), test_value)

    # XOR properties - Commutativity (A XOR B = B XOR A)
    def test_commutativity_property(self) -> None:
        bin1 = "11001010"
        bin2 = "10101100"
        self.assertEqual(xor(bin1, bin2), xor(bin2, bin1))

    # XOR properties - Associativity ((A XOR B) XOR C = A XOR (B XOR C))
    def test_associativity_property(self) -> None:
        a = "11001010"
        b = "10101100"
        c = "01010101"
        left_side = xor(xor(a, b), c)
        right_side = xor(a, xor(b, c))
        self.assertEqual(left_side, right_side)

    # XOR properties - Double XOR returns original (A XOR B XOR B = A)
    def test_double_xor_returns_original(self) -> None:
        original = "10110011"
        key = "11001100"
        encrypted = xor(original, key)
        decrypted = xor(encrypted, key)
        self.assertEqual(decrypted, original)

    # Error handling - Different lengths should raise ValueError
    def test_different_lengths_raises_error(self) -> None:
        with self.assertRaises(ValueError):
            xor("1010", "101")
    
    def test_different_lengths_longer_second(self) -> None:
        with self.assertRaises(ValueError):
            xor("101", "1010")

    # 8-bit byte XOR tests (simulating ASCII characters)
    def test_byte_xor_encryption(self) -> None:
        # 'A' = 01000001, 'B' = 01000010
        char_a = "01000001"
        char_b = "01000010"
        self.assertEqual(xor(char_a, char_b), "00000011")

    # 16-bit XOR test
    def test_16_bit_xor(self) -> None:
        bin1 = "1111000011110000"
        bin2 = "0000111100001111"
        expected = "1111111111111111"
        self.assertEqual(xor(bin1, bin2), expected)

    # 32-bit XOR test
    def test_32_bit_xor(self) -> None:
        bin1 = "11110000111100001111000011110000"
        bin2 = "10101010101010101010101010101010"
        expected = "01011010010110100101101001011010"
        self.assertEqual(xor(bin1, bin2), expected)

    # Pattern recognition tests
    def test_alternating_pattern(self) -> None:
        pattern1 = "01010101"
        pattern2 = "10101010"
        self.assertEqual(xor(pattern1, pattern2), "11111111")

    def test_nibble_pattern(self) -> None:
        # Testing 4-bit patterns
        self.assertEqual(xor("1111", "0000"), "1111")
        self.assertEqual(xor("1111", "1111"), "0000")
        self.assertEqual(xor("1100", "0011"), "1111")

if __name__ == "__main__":
    unittest.main()
