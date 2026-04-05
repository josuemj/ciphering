"""
Generación de par de claves RSA-2048 para MediSoft.

La clave privada NUNCA se distribuye — firma el manifiesto internamente.
La clave pública se publica junto al paquete para que el hospital verifique.
"""

from pathlib import Path
from Crypto.PublicKey import RSA


def generar_par_claves(bits: int = 2048) -> tuple[bytes, bytes]:
    """Genera un par RSA. Retorna (pem_privada, pem_publica)."""
    clave = RSA.generate(bits, e=65537)
    return clave.export_key("PEM"), clave.publickey().export_key("PEM")


def guardar_claves(
    pem_priv: bytes,
    pem_pub: bytes,
    dir_privado: str,
    dir_publico: str,
) -> tuple[Path, Path]:
    """Guarda las claves en sus respectivos directorios.

    La clave privada va a dir_privado (solo MediSoft).
    La clave pública va a dir_publico (se distribuye con el paquete).
    """
    ruta_priv = Path(dir_privado) / "medisoft_priv.pem"
    ruta_pub  = Path(dir_publico) / "medisoft_pub.pem"

    Path(dir_privado).mkdir(parents=True, exist_ok=True)
    Path(dir_publico).mkdir(parents=True, exist_ok=True)

    ruta_priv.write_bytes(pem_priv)
    ruta_pub.write_bytes(pem_pub)

    try:
        ruta_priv.chmod(0o600)  # solo lectura para el propietario
    except OSError:
        pass

    return ruta_priv, ruta_pub
