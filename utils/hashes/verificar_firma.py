"""
Verificación de la firma digital RSA-PSS sobre el manifiesto SHA256SUMS.txt.

Flujo:
  1. Leer el contenido de SHA256SUMS.txt como bytes
  2. Calcular SHA-256 del contenido
  3. Verificar la firma (.sig) con la clave pública RSA-PSS
"""

from pathlib import Path
from Crypto.PublicKey import RSA
from Crypto.Signature import pss
from Crypto.Hash import SHA256


def verificar_firma_manifiesto(
    ruta_manifiesto: str,
    ruta_clave_publica: str,
    ruta_firma: str,
) -> tuple[bool, str]:
    """Verifica la firma del manifiesto.

    Retorna (valida, mensaje).
    """
    contenido = Path(ruta_manifiesto).read_bytes()
    clave_pub = RSA.import_key(Path(ruta_clave_publica).read_bytes())
    firma     = Path(ruta_firma).read_bytes()

    digest = SHA256.new(contenido)
    try:
        pss.new(clave_pub).verify(digest, firma)
        return True, "Firma valida — el manifiesto no fue alterado y proviene de MediSoft."
    except (ValueError, TypeError) as e:
        return False, f"Firma INVALIDA — {e}"
