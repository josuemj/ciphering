from pathlib import Path
from generar_manifiesto import sha256_archivo


def leer_manifiesto(ruta_manifiesto: str) -> dict[str, str]:
    """Parsea el manifiesto y retorna {nombre_archivo: hash_esperado}."""
    entradas = {}
    for linea in Path(ruta_manifiesto).read_text().splitlines():
        linea = linea.strip()
        if not linea:
            continue
        hash_hex, nombre = linea.split(None, 1)
        entradas[nombre] = hash_hex
    return entradas


def verificar_archivo(ruta: str, hash_esperado: str) -> tuple[bool, str]:
    """Recalcula el SHA-256 del archivo y lo compara contra el hash esperado.

    Retorna (ok, hash_real).
    """
    hash_real = sha256_archivo(ruta)
    return hash_real == hash_esperado, hash_real


def verificar_paquete(ruta_manifiesto: str, directorio: str) -> list[dict]:
    """Verifica todos los archivos listados en el manifiesto.

    Retorna una lista de resultados con claves:
        archivo, ok, hash_esperado, hash_real
    """
    base = Path(directorio)
    entradas = leer_manifiesto(ruta_manifiesto)
    resultados = []
    for nombre, hash_esperado in entradas.items():
        ruta = base / nombre
        if not ruta.exists():
            resultados.append({
                "archivo":       nombre,
                "ok":            False,
                "hash_esperado": hash_esperado,
                "hash_real":     "ARCHIVO NO ENCONTRADO",
            })
            continue
        ok, hash_real = verificar_archivo(str(ruta), hash_esperado)
        resultados.append({
            "archivo":       nombre,
            "ok":            ok,
            "hash_esperado": hash_esperado,
            "hash_real":     hash_real,
        })
    return resultados
