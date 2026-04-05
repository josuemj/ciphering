"""
HIBP k-Anonymity Password Checker
----------------------------------
Demuestra por qué almacenar contraseñas como SHA-256 directo es inseguro:
las contraseñas comunes ya tienen sus hashes indexados en bases de datos
públicas de filtraciones (Have I Been Pwned).

Flujo k-Anonymity (nunca envía el hash completo):
  1. SHA-1(password) → hash completo en mayúsculas
  2. Enviar solo los primeros 5 caracteres a la API
  3. La API responde con todos los sufijos que empiezan con esos 5 chars
  4. Buscar localmente si el sufijo aparece en la lista
"""

import urllib.request

from explorar_hashes import hash_sha256, hash_sha1


PASSWORDS = ["admin", "123456", "hospital", "medisoft2024"]
HIBP_URL = "https://api.pwnedpasswords.com/range/"


def sha256_hex(password: str) -> str:
    return hash_sha256(password)


def sha1_hex(password: str) -> str:
    return hash_sha1(password).upper()


def query_hibp(sha1_hash: str) -> int:
    """Consulta HIBP con los primeros 5 chars del hash SHA-1.

    Retorna cuántas veces aparece el hash en filtraciones conocidas (0 si no).
    El hash completo nunca sale de esta máquina.
    """
    prefix = sha1_hash[:5]
    suffix = sha1_hash[5:]

    req = urllib.request.Request(
        HIBP_URL + prefix,
        headers={"User-Agent": "MediSoft-LabHash/1.0"},
    )
    with urllib.request.urlopen(req) as response:
        body = response.read().decode("utf-8")

    for line in body.splitlines():
        returned_suffix, count = line.split(":")
        if returned_suffix == suffix:
            return int(count)
    return 0


def print_results(results: list[dict]) -> None:
    col = {"pwd": 16, "sha256": 64, "sha1": 40, "prefix": 7, "count": 12}
    header = (
        f"{'Password':<{col['pwd']}} "
        f"{'SHA-256 (vulnerable)':<{col['sha256']}} "
        f"{'SHA-1 prefix':<{col['prefix']}} "
        f"{'Filtraciones':>{col['count']}}"
    )
    sep = "-" * len(header)
    print(sep)
    print(header)
    print(sep)
    for r in results:
        filtraciones = str(r["count"]) if r["count"] > 0 else "No encontrado"
        print(
            f"{r['password']:<{col['pwd']}} "
            f"{r['sha256']:<{col['sha256']}} "
            f"{r['sha1'][:5]+'...':<{col['prefix']}} "
            f"{filtraciones:>{col['count']}}"
        )
    print(sep)


if __name__ == "__main__":
    print("\nVerificando contraseñas contra Have I Been Pwned (k-Anonymity)...\n")

    results = []
    for pwd in PASSWORDS:
        sha256 = sha256_hex(pwd)
        sha1   = sha1_hex(pwd)
        prefix = sha1[:5]

        print(f"  [{pwd}] consultando prefijo SHA-1: {prefix}...", end=" ", flush=True)
        count = query_hibp(sha1)
        status = f"{count:,} veces" if count > 0 else "no encontrada"
        print(status)

        results.append({
            "password": pwd,
            "sha256":   sha256,
            "sha1":     sha1,
            "count":    count,
        })

    print()
    print_results(results)

    print("\nDetalle SHA-1 completo (solo visible localmente — nunca se envio):")
    for r in results:
        print(f"  {r['password']:<16} {r['sha1']}")
