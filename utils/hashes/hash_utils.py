def bits_diferentes(hex1: str, hex2: str) -> int:
    """Cuenta los bits que difieren entre dos hex digests (distancia de Hamming a nivel de bits).

    Convierte cada digest a entero, aplica XOR y cuenta los bits en 1
    del resultado (popcount). Cada bit en 1 representa un bit que cambió.
    """
    if len(hex1) != len(hex2):
        raise ValueError("Los digests deben tener la misma longitud.")
    xor_val = int(hex1, 16) ^ int(hex2, 16)
    return bin(xor_val).count("1")
