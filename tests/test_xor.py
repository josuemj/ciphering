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

if __name__ == "__main__":
    unittest.main()
