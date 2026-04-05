"""
Simulación Ejercicio 3 — Integridad de distribución MediSoft
=============================================================
Escenario:
  - MediSoft publica un release y genera el manifiesto SHA256SUMS.txt
  - El hospital descarga el paquete y verifica la integridad
  - Un atacante modifica un byte en un archivo del mirror comprometido
  - El verificador detecta la manipulación
"""

import os
from pathlib import Path
from generar_manifiesto import generar_manifiesto
from verificar_paquete import verificar_paquete

PAQUETE_DIR = Path(__file__).parent / "paquete_medisoft"
MANIFIESTO  = PAQUETE_DIR / "SHA256SUMS.txt"

ARCHIVOS_SIMULADOS = {
    "config.ini": (
        "[medisoft]\n"
        "version = 2.1.0\n"
        "hospital_id = GT-001\n"
        "server = lab.medisoft.com\n"
        "timeout = 30\n"
    ),
    "firmware_analizador.bin": (
        "MEDISOFT_FW\x00\x01\x02\x00"
        "INIT_SEQ:0xDEADBEEF\n"
        "CALIB_TABLE:256,512,1024\n"
        "CRC_BLOCK:0xFF00AA55\n"
    ),
    "driver_lab.dll": (
        "MZ_HEADER_SIMULATED\n"
        "EXPORT:connect_device\n"
        "EXPORT:read_sample\n"
        "EXPORT:calibrate\n"
        "EXPORT:disconnect\n"
    ),
    "update_script.sh": (
        "#!/bin/bash\n"
        "set -e\n"
        "echo 'MediSoft v2.1.0 update'\n"
        "cp firmware_analizador.bin /opt/medisoft/fw/\n"
        "cp driver_lab.dll /opt/medisoft/drivers/\n"
        "systemctl restart medisoft-lab\n"
    ),
    "release_notes.txt": (
        "MediSoft v2.1.0 — Release Notes\n"
        "================================\n"
        "- Correccion: timeout en lecturas de alta frecuencia\n"
        "- Mejora: calibracion automatica al iniciar\n"
        "- Seguridad: TLS 1.3 para comunicacion con servidor\n"
    ),
}


# ─── utilidades de presentación ───────────────────────────────────────────────

def imprimir_reporte(resultados: list[dict], titulo: str) -> None:
    print(f"\n{'='*70}")
    print(f"  {titulo}")
    print(f"{'='*70}")
    col_archivo = 28
    for r in resultados:
        estado = "OK" if r["ok"] else "FALLO"
        icono  = "[OK]" if r["ok"] else "[!!]"
        print(f"\n  {icono} {r['archivo']}")
        print(f"       esperado : {r['hash_esperado']}")
        if r["ok"]:
            print(f"       real     : {r['hash_real']}")
        else:
            print(f"       real     : {r['hash_real']}  <-- DISTINTO")
        print(f"       estado   : {estado}")
    ok_count   = sum(1 for r in resultados if r["ok"])
    fail_count = len(resultados) - ok_count
    print(f"\n  Resultado: {ok_count}/{len(resultados)} archivos OK"
          + (f"  |  {fail_count} MANIPULADO(S)" if fail_count else ""))
    print(f"{'='*70}")


# ─── pasos de la simulación ───────────────────────────────────────────────────

def paso_1_crear_paquete() -> None:
    print("\n[MEDISOFT] Creando paquete de distribución...")
    PAQUETE_DIR.mkdir(exist_ok=True)
    for nombre, contenido in ARCHIVOS_SIMULADOS.items():
        (PAQUETE_DIR / nombre).write_text(contenido, encoding="utf-8")
    print(f"  {len(ARCHIVOS_SIMULADOS)} archivos creados en: {PAQUETE_DIR}")


def paso_2_generar_manifiesto() -> None:
    print("\n[MEDISOFT] Generando manifiesto SHA256SUMS.txt...")
    archivos = [str(PAQUETE_DIR / nombre) for nombre in ARCHIVOS_SIMULADOS]
    hashes = generar_manifiesto(archivos, str(MANIFIESTO))
    for nombre, h in hashes.items():
        print(f"  {h}  {nombre}")
    print(f"\n  Manifiesto guardado en: {MANIFIESTO}")


def paso_3_verificar_integro() -> None:
    print("\n[HOSPITAL] Verificando paquete recibido (sin manipulacion)...")
    resultados = verificar_paquete(str(MANIFIESTO), str(PAQUETE_DIR))
    imprimir_reporte(resultados, "Verificacion 1 — Paquete original")


def paso_4_atacante_modifica() -> str:
    archivo_objetivo = PAQUETE_DIR / "update_script.sh"
    print(f"\n[ATACANTE] Modificando un byte en: {archivo_objetivo.name}")
    contenido = bytearray(archivo_objetivo.read_bytes())
    pos = 32
    original = contenido[pos]
    contenido[pos] = (original + 1) % 256
    archivo_objetivo.write_bytes(bytes(contenido))
    print(f"  Byte en posicion {pos}: 0x{original:02X} -> 0x{contenido[pos]:02X}")
    return archivo_objetivo.name


def paso_5_verificar_comprometido() -> None:
    print("\n[HOSPITAL] Re-verificando paquete (post-manipulacion)...")
    resultados = verificar_paquete(str(MANIFIESTO), str(PAQUETE_DIR))
    imprimir_reporte(resultados, "Verificacion 2 — Paquete comprometido")


# ─── main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\nSimulacion: Integridad de distribucion MediSoft v2.1.0")
    print("Escenario: mirror comprometido inyecta codigo en update_script.sh\n")

    paso_1_crear_paquete()
    paso_2_generar_manifiesto()
    paso_3_verificar_integro()
    paso_4_atacante_modifica()
    paso_5_verificar_comprometido()
