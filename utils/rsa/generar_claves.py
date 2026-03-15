"""Genera un par de claves RSA y las exporta a PEM.
"""

from __future__ import annotations

import argparse
import getpass
import os
import sys
from pathlib import Path
from Crypto.PublicKey import RSA



DEFAULT_BITS = 2048


def _positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("El valor debe ser un entero positivo.")
    return parsed


def generate_keypair(bits: int) -> RSA.RsaKey:
    if bits < 1024:
        raise ValueError("RSA bits debe ser >= 1024.")
    return RSA.generate(bits, e=65537)


def export_keys_to_assets_dir(
    private_key: RSA.RsaKey,
    *,
    out_dir: Path,
    passphrase: str,
) -> tuple[Path, Path]:
    out_dir.mkdir(parents=True, exist_ok=True)

    private_key_pem = private_key.export_key(
        format="PEM",
        passphrase=passphrase,
        pkcs=8,
        protection="scryptAndAES128-CBC",
    )
    public_key_pem = private_key.publickey().export_key(format="PEM")

    private_path = out_dir / "private_key.pem"
    public_path = out_dir / "public_key.pem"

    private_path.write_bytes(private_key_pem)
    public_path.write_bytes(public_key_pem)

    try:
        private_path.chmod(0o600)
    except OSError:
        pass

    return private_path, public_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Genera claves RSA y las exporta en PEM.")
    parser.add_argument("--bits", type=_positive_int, default=DEFAULT_BITS, help="Tamaño de la clave RSA.")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path(__file__).resolve().parent / "assets",
        help="Directorio donde se guardarán los archivos PEM.",
    )
    parser.add_argument(
        "--passphrase",
        default=None,
        help="Passphrase para proteger la clave privada (o usa $RSA_PASSPHRASE).",
    )
    args = parser.parse_args()

    passphrase = args.passphrase or os.environ.get("RSA_PASSPHRASE")
    if not passphrase:
        if not sys.stdin.isatty():
            raise SystemExit(
                "Passphrase requerida. Usa --passphrase <valor> o exporta RSA_PASSPHRASE."
            )
        passphrase = getpass.getpass("Passphrase para private_key.pem: ")
        if not passphrase:
            raise SystemExit("Passphrase vacía; abortando.")

    keypair = generate_keypair(args.bits)
    private_path, public_path = export_keys_to_assets_dir(
        keypair,
        out_dir=args.out_dir,
        passphrase=passphrase,
    )

    print(f"OK: {private_path}")
    print(f"OK: {public_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
