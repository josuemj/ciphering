"""
Firma digital del manifiesto SHA256SUMS.txt usando RSA-PSS + SHA-256.

Flujo:
  1. Leer el contenido completo de SHA256SUMS.txt como bytes
  2. Calcular SHA-256 del contenido
  3. Firmar el hash con la clave privada RSA usando PSS
  4. Guardar la firma binaria en SHA256SUMS.sig
"""

from pathlib import Path
from Crypto.PublicKey import RSA
from Crypto.Signature import pss
from Crypto.Hash import SHA256


def firmar_manifiesto(
    ruta_manifiesto: str,
    ruta_clave_privada: str,
    ruta_firma: str,
) -> bytes:
    """Firma el manifiesto con la clave privada RSA-PSS.

    Retorna los bytes de la firma generada.
    """
    contenido = Path(ruta_manifiesto).read_bytes()
    clave_priv = RSA.import_key(Path(ruta_clave_privada).read_bytes())

    digest = SHA256.new(contenido)
    firma  = pss.new(clave_priv).sign(digest)

    Path(ruta_firma).write_bytes(firma)
    return firma
