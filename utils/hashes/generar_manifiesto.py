import hashlib
from pathlib import Path


def sha256_archivo(ruta: str) -> str:
    """Calcula el SHA-256 de un archivo leyéndolo en bloques de 64 KB."""
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for bloque in iter(lambda: f.read(65536), b""):
            h.update(bloque)
    return h.hexdigest()


def agregar_al_manifiesto(hash_hex: str, nombre_archivo: str, ruta_manifiesto: str) -> None:
    """Agrega una línea '<HASH>  <nombre>' al manifiesto (formato sha256sum estándar)."""
    with open(ruta_manifiesto, "a") as f:
        f.write(f"{hash_hex}  {nombre_archivo}\n")


def generar_manifiesto(archivos: list[str], ruta_manifiesto: str) -> dict[str, str]:
    """Calcula el SHA-256 de cada archivo y construye el manifiesto.

    Retorna un dict {nombre_archivo: hash_hex}.
    """
    Path(ruta_manifiesto).write_text("")  # limpiar/crear el archivo

    resultados = {}
    for ruta in archivos:
        nombre = Path(ruta).name
        hash_hex = sha256_archivo(ruta)
        agregar_al_manifiesto(hash_hex, nombre, ruta_manifiesto)
        resultados[nombre] = hash_hex
    return resultados
