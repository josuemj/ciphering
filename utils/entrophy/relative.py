import math
from collections import Counter
from typing import Dict


def relative_entropy(text: str, probabilities: Dict[str, float], *, epsilon: float = 1e-12) -> float:
    """
    Entropía relativa como divergencia KL D(P||Q) en bits:
        D(P||Q) = sum_x P(x) * log2(P(x) / Q(x))

    - P(x): distribución empírica de caracteres en `text`
    - Q(x): distribución de referencia en `probabilities`

    Si un carácter no existe en `probabilities` o tiene Q(x)=0, se usa `epsilon`.
    """
    if not text:
        return 0.0

    counts = Counter(text)
    n = len(text)

    d_kl = 0.0
    for ch, k in counts.items():
        p = k / n
        q = probabilities.get(ch, 0.0)
        q = q if q > 0.0 else epsilon
        d_kl += p * math.log2(p / q)

    return d_kl