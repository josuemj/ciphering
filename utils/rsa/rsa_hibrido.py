"""Cifrado híbrido: RSA-OAEP + AES-256-GCM (PyCryptodome).

Flujo:
1) Generar una clave AES aleatoria de 256 bits.
2) Cifrar el documento con AES-GCM -> nonce + tag + ciphertext.
3) Cifrar (envolver) la clave AES con RSA-OAEP usando la clave pública del destinatario.
"""

from __future__ import annotations

import argparse
import base64
import getpass
import os
import sys
from pathlib import Path

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes


DEFAULT_ASSETS_DIR = Path(__file__).resolve().parent / "assets"
PKG_MAGIC = b"HYB1"
GCM_NONCE_LEN = 12
GCM_TAG_LEN = 16
AES_KEY_LEN = 32  # 256 bits


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


def encrypt_document(document: bytes, recipient_public_key_pem: bytes) -> bytes:
    # a) clave AES-256 aleatoria
    aes_key = get_random_bytes(AES_KEY_LEN)

    # b) AES-GCM: nonce + tag + ciphertext
    nonce = get_random_bytes(GCM_NONCE_LEN)
    aes = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = aes.encrypt_and_digest(document)

    # c) Envolver la clave AES con RSA-OAEP (clave pública)
    public_key = RSA.import_key(recipient_public_key_pem)
    wrapped_key = PKCS1_OAEP.new(public_key).encrypt(aes_key)

    # Empaque binario simple:
    # magic(4) | wrapped_len(2) | wrapped_key | nonce_len(1) | nonce | tag(16) | ciphertext
    wrapped_len = len(wrapped_key).to_bytes(2, "big")
    nonce_len = len(nonce).to_bytes(1, "big")
    return PKG_MAGIC + wrapped_len + wrapped_key + nonce_len + nonce + tag + ciphertext


def _import_private_key(private_key_pem: bytes, passphrase: str | None) -> RSA.RsaKey:
    try:
        return RSA.import_key(private_key_pem)
    except (ValueError, TypeError):
        resolved = _get_passphrase(passphrase)
        return RSA.import_key(private_key_pem, passphrase=resolved)


def decrypt_document(pkg: bytes, recipient_private_key_pem: bytes) -> bytes:
    if len(pkg) < 4 + 2 + 1 + GCM_TAG_LEN:
        raise ValueError("Paquete inválido: muy corto.")
    if pkg[:4] != PKG_MAGIC:
        raise ValueError("Paquete inválido: encabezado incorrecto.")

    idx = 4
    wrapped_len = int.from_bytes(pkg[idx : idx + 2], "big")
    idx += 2
    if wrapped_len <= 0 or idx + wrapped_len + 1 > len(pkg):
        raise ValueError("Paquete inválido: longitud de clave envuelta.")

    wrapped_key = pkg[idx : idx + wrapped_len]
    idx += wrapped_len

    nonce_len = pkg[idx]
    idx += 1
    if nonce_len <= 0 or idx + nonce_len + GCM_TAG_LEN > len(pkg):
        raise ValueError("Paquete inválido: longitud de nonce.")

    nonce = pkg[idx : idx + nonce_len]
    idx += nonce_len

    tag = pkg[idx : idx + GCM_TAG_LEN]
    idx += GCM_TAG_LEN

    ciphertext = pkg[idx:]

    private_key = _import_private_key(recipient_private_key_pem, passphrase=None)
    aes_key = PKCS1_OAEP.new(private_key).decrypt(wrapped_key)

    aes = AES.new(aes_key, AES.MODE_GCM, nonce=nonce)
    return aes.decrypt_and_verify(ciphertext, tag)


def main() -> int:
    parser = argparse.ArgumentParser(description="Demo: cifrado híbrido RSA-OAEP + AES-256-GCM.")
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

    pub_pem = args.public_key.read_bytes()
    priv_pem = args.private_key.read_bytes()

    # Resolver passphrase una sola vez para evitar prompts repetidos.
    os.environ["RSA_PASSPHRASE"] = _get_passphrase(args.passphrase)

    # Documento pequeño (ejemplo)
    doc = "Contrato de confidencialidad No. 2025-GT-001".encode("utf-8")
    pkg = encrypt_document(doc, pub_pem)
    descifrado = decrypt_document(pkg, priv_pem)
    assert descifrado == doc

    print("Paquete (base64):", base64.b64encode(pkg).decode("ascii"))
    print("Descifrado:", descifrado.decode("utf-8"))

    doc_grande = os.urandom(1024 * 1024)
    pkg2 = encrypt_document(doc_grande, pub_pem)

    assert decrypt_document(pkg2, priv_pem) == doc_grande
    print("Archivo 1 MB: OK")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
