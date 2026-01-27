
import math
from collections import Counter

def shannon_entropy(text: str) -> float:
    """
    Entropía de Shannon en bits por carácter, usando la distribución
    """
    if not text:
        return 0.0

    counts = Counter(text)
    n = len(text)

    h = 0.0
    for k in counts.values():
        p = k / n
        h -= p * math.log2(p)

    return h