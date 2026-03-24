"""Cifrado y descifrado directo con RSA-OAEP (PyCryptodome).

RSA-OAEP solo sirve para mensajes pequeños (con RSA-2048 y SHA-1 ~214 bytes).
Para documentos se recomienda cifrado híbrido (RSA para la clave AES + AES para el documento).
"""

from __future__ import annotations

import argparse
import base64
import getpass
import os
import sys
from pathlib import Path

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA


DEFAULT_ASSETS_DIR = Path(__file__).resolve().parent / "assets"


def cifrar_con_rsa(mensaje: bytes, public_key_pem: bytes) -> bytes:
    public_key = RSA.import_key(public_key_pem)
    cipher = PKCS1_OAEP.new(public_key)

    # Límite OAEP: k - 2*hLen - 2 (SHA-1 por default: hLen=20)
    max_len = public_key.size_in_bytes() - 2 * 20 - 2
    if len(mensaje) > max_len:
        raise ValueError(
            f"Mensaje demasiado grande para RSA-OAEP con esta llave: "
            f"{len(mensaje)} bytes (máximo {max_len})."
        )

    return cipher.encrypt(mensaje)


def _get_passphrase(passphrase: str | None) -> str:
    resolved = passphrase or os.environ.get("RSA_PASSPHRASE")
    if resolved:
        return resolved

    if not sys.stdin.isatty():
        raise SystemExit("Passphrase requerida. Usa --passphrase <valor> o exporta RSA_PASSPHRASE.")

    resolved = getpass.getpass("Passphrase para private_key.pem: ")
    if not resolved:
        raise SystemExit("Passphrase vacía; abortando.")
    return resolved


def descifrar_con_rsa(cifrado: bytes, private_key_pem: bytes) -> bytes:
    passphrase = _get_passphrase(None)
    private_key = RSA.import_key(private_key_pem, passphrase=passphrase)
    cipher = PKCS1_OAEP.new(private_key)
    return cipher.decrypt(cifrado)


def main() -> int:
    parser = argparse.ArgumentParser(description="Cifra y descifra un mensaje usando RSA-OAEP.")
    parser.add_argument(
        "--message",
        default="mensaje",
        help='Mensaje a cifrar (texto UTF-8). Default: "mensaje".',
    )
    parser.add_argument(
        "--public-key",
        type=Path,
        default=DEFAULT_ASSETS_DIR / "public_key.pem",
        help="Ruta al archivo PEM de clave pública.",
    )
    parser.add_argument(
        "--private-key",
        type=Path,
        default=DEFAULT_ASSETS_DIR / "private_key.pem",
        help="Ruta al archivo PEM de clave privada (encriptada).",
    )
    parser.add_argument(
        "--passphrase",
        default=None,
        help="Passphrase para la clave privada (o usa $RSA_PASSPHRASE).",
    )
    args = parser.parse_args()

    public_pem = args.public_key.read_bytes()
    private_pem = args.private_key.read_bytes()

    ciphertext = cifrar_con_rsa(args.message.encode("utf-8"), public_pem)
    print("Cifrado (base64):", base64.b64encode(ciphertext).decode("ascii"))

    passphrase = _get_passphrase(args.passphrase)
    private_key = RSA.import_key(private_pem, passphrase=passphrase)
    plaintext = PKCS1_OAEP.new(private_key).decrypt(ciphertext)
    print("Descifrado:", plaintext.decode("utf-8"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
