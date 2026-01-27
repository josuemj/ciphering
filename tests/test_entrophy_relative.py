import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.entrophy.relative import relative_entropy
from utils.entrophy.probabilites import probabilities


class TestRelativeEntropy(unittest.TestCase):
    """Tests para la función de entropía relativa (divergencia KL)"""

    def test_google(self):
        """Test entropía relativa para 'google'"""
        result = relative_entropy("google", probabilities)
        print(f"Entropía relativa de 'google': {result:.6f} bits")
        self.assertGreaterEqual(result, 0)
        self.assertIsInstance(result, float)

    def test_microsoft(self):
        """Test entropía relativa para 'microsoft'"""
        result = relative_entropy("microsoft", probabilities)
        print(f"Entropía relativa de 'microsoft': {result:.6f} bits")
        self.assertGreaterEqual(result, 0)
        self.assertIsInstance(result, float)

    def test_uvg(self):
        """Test entropía relativa para 'uvg'"""
        result = relative_entropy("uvg", probabilities)
        print(f"Entropía relativa de 'uvg': {result:.6f} bits")
        self.assertGreaterEqual(result, 0)
        self.assertIsInstance(result, float)

    def test_uspsxcjmvb(self):
        """Test entropía relativa para 'uspsxcjmvb'"""
        result = relative_entropy("uspsxcjmvb", probabilities)
        print(f"Entropía relativa de 'uspsxcjmvb': {result:.6f} bits")
        self.assertGreaterEqual(result, 0)
        self.assertIsInstance(result, float)

    def test_uspsn_tn_track(self):
        """Test entropía relativa para 'uspsn-tn-track'"""
        result = relative_entropy("uspsn-tn-track", probabilities)
        print(f"Entropía relativa de 'uspsn-tn-track': {result:.6f} bits")
        self.assertGreaterEqual(result, 0)
        self.assertIsInstance(result, float)

    def test_empty_string(self):
        """Test entropía relativa para string vacío"""
        result = relative_entropy("", probabilities)
        self.assertEqual(result, 0.0)

    def test_all_domains_comparison(self):
        """Comparación de entropía relativa de todos los dominios"""
        domains = ["google", "microsoft", "uvg", "uspsxcjmvb", "uspsn-tn-track"]
        
        print("\n" + "="*60)
        print("COMPARACIÓN DE ENTROPÍA RELATIVA (Divergencia KL)")
        print("="*60)
        
        results = {}
        for domain in domains:
            entropy = relative_entropy(domain, probabilities)
            results[domain] = entropy
            print(f"{domain:20s} -> {entropy:.6f} bits")
        
        print("="*60)
        print("\nNota: Valores más bajos indican distribución más cercana")
        print("a la distribución de referencia (dominios típicos)")
        print("="*60)
        
        # Verificar que todos tienen entropía no negativa (propiedad de KL)
        for domain, entropy in results.items():
            self.assertGreaterEqual(entropy, 0, f"Entropía relativa de {domain} debe ser >= 0")


if __name__ == "__main__":
    unittest.main(verbosity=2)
