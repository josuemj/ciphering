import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.entrophy.shanon import shannon_entropy


class TestShannonEntropy(unittest.TestCase):
    """Tests para la función de entropía de Shannon"""

    def test_google(self):
        """Test entropía de Shannon para 'google'"""
        result = shannon_entropy("google")
        print(f"Shannon entropy de 'google': {result:.6f} bits")
        self.assertGreater(result, 0)
        self.assertIsInstance(result, float)

    def test_microsoft(self):
        """Test entropía de Shannon para 'microsoft'"""
        result = shannon_entropy("microsoft")
        print(f"Shannon entropy de 'microsoft': {result:.6f} bits")
        self.assertGreater(result, 0)
        self.assertIsInstance(result, float)

    def test_uvg(self):
        """Test entropía de Shannon para 'uvg'"""
        result = shannon_entropy("uvg")
        print(f"Shannon entropy de 'uvg': {result:.6f} bits")
        self.assertGreater(result, 0)
        self.assertIsInstance(result, float)

    def test_uspsxcjmvb(self):
        """Test entropía de Shannon para 'uspsxcjmvb'"""
        result = shannon_entropy("uspsxcjmvb")
        print(f"Shannon entropy de 'uspsxcjmvb': {result:.6f} bits")
        self.assertGreater(result, 0)
        self.assertIsInstance(result, float)

    def test_uspsn_tn_track(self):
        """Test entropía de Shannon para 'uspsn-tn-track'"""
        result = shannon_entropy("uspsn-tn-track")
        print(f"Shannon entropy de 'uspsn-tn-track': {result:.6f} bits")
        self.assertGreater(result, 0)
        self.assertIsInstance(result, float)

    def test_empty_string(self):
        """Test entropía de Shannon para string vacío"""
        result = shannon_entropy("")
        self.assertEqual(result, 0.0)

    def test_single_char(self):
        """Test entropía de Shannon para un solo carácter"""
        result = shannon_entropy("a")
        self.assertEqual(result, 0.0)

    def test_all_domains_comparison(self):
        """Comparación de entropía de todos los dominios"""
        domains = ["google", "microsoft", "uvg", "uspsxcjmvb", "uspsn-tn-track"]
        
        print("\n" + "="*60)
        print("COMPARACIÓN DE ENTROPÍA DE SHANNON")
        print("="*60)
        
        results = {}
        for domain in domains:
            entropy = shannon_entropy(domain)
            results[domain] = entropy
            print(f"{domain:20s} -> {entropy:.6f} bits")
        
        print("="*60)
        
        # Verificar que todos tienen entropía positiva
        for domain, entropy in results.items():
            self.assertGreater(entropy, 0, f"Entropía de {domain} debe ser positiva")


if __name__ == "__main__":
    unittest.main(verbosity=2)
