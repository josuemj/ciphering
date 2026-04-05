"""
Simulación Ejercicios 4 y 5 — Autenticidad del manifiesto MediSoft
====================================================================

Escenario:
  Ej4 — MediSoft firma digitalmente SHA256SUMS.txt con su clave privada RSA.
  Ej5 — El hospital valida la firma con la clave pública de MediSoft.
        Se demuestran dos ataques distintos y sus efectos:
          A) Atacante modifica SHA256SUMS.txt → firma inválida (detectado)
          B) Atacante modifica un archivo del paquete pero no el manifiesto
             → firma válida, pero verificar_paquete falla (detectado)

Prerequisito: simulacion_ej3.py debe haberse ejecutado antes
              (crea paquete_medisoft/ con los archivos y SHA256SUMS.txt)
"""

from pathlib import Path
from generar_claves_rsa import generar_par_claves, guardar_claves
from firmar_manifiesto   import firmar_manifiesto
from verificar_firma     import verificar_firma_manifiesto
from verificar_paquete   import verificar_paquete

BASE        = Path(__file__).parent
PAQUETE_DIR = BASE / "paquete_medisoft"
CLAVES_DIR  = BASE / "claves_medisoft"       # clave privada — solo MediSoft
MANIFIESTO  = PAQUETE_DIR / "SHA256SUMS.txt"
FIRMA       = PAQUETE_DIR / "SHA256SUMS.sig"
CLAVE_PRIV  = CLAVES_DIR  / "medisoft_priv.pem"
CLAVE_PUB   = PAQUETE_DIR / "medisoft_pub.pem"  # pública — se distribuye con el paquete


# ─── helpers de presentación ──────────────────────────────────────────────────

def titulo(texto: str) -> None:
    print(f"\n{'='*68}")
    print(f"  {texto}")
    print(f"{'='*68}")

def resultado_firma(valida: bool, mensaje: str) -> None:
    icono = "[OK]  " if valida else "[!!] "
    print(f"\n  {icono} {mensaje}")

def resultado_paquete(resultados: list[dict]) -> None:
    for r in resultados:
        icono = "[OK]" if r["ok"] else "[!!]"
        print(f"  {icono} {r['archivo']}")
        if not r["ok"]:
            print(f"       esperado : {r['hash_esperado']}")
            print(f"       real     : {r['hash_real']}  <-- DISTINTO")
    ok = sum(1 for r in resultados if r["ok"])
    print(f"\n  {ok}/{len(resultados)} archivos integros")


# ─── pasos ────────────────────────────────────────────────────────────────────

def paso_1_generar_claves() -> None:
    titulo("EJ4 — Paso 1: MediSoft genera par de claves RSA-2048")
    pem_priv, pem_pub = generar_par_claves(2048)
    ruta_priv, ruta_pub = guardar_claves(
        pem_priv, pem_pub,
        dir_privado=str(CLAVES_DIR),
        dir_publico=str(PAQUETE_DIR),
    )
    print(f"\n  Clave privada (CONFIDENCIAL): {ruta_priv}")
    print(f"  Clave publica (distribuible): {ruta_pub}")
    print("\n  NOTA: medisoft_priv.pem NUNCA sale del servidor de MediSoft.")
    print("        medisoft_pub.pem se publica junto al paquete de actualizacion.")


def paso_2_firmar_manifiesto() -> None:
    titulo("EJ4 — Paso 2: MediSoft firma SHA256SUMS.txt")
    firma = firmar_manifiesto(str(MANIFIESTO), str(CLAVE_PRIV), str(FIRMA))
    print(f"\n  Manifiesto firmado: {MANIFIESTO.name}")
    print(f"  Firma guardada en : {FIRMA.name}  ({len(firma)} bytes)")
    print(f"  Firma (hex, primeros 32 bytes): {firma[:32].hex()}...")


def paso_3_verificar_original() -> None:
    titulo("EJ5 — Paso 3: Hospital verifica firma (paquete original)")
    valida, mensaje = verificar_firma_manifiesto(
        str(MANIFIESTO), str(CLAVE_PUB), str(FIRMA)
    )
    resultado_firma(valida, mensaje)


def paso_4_atacante_modifica_manifiesto() -> bytes:
    titulo("EJ5 — Paso 4: Atacante altera SHA256SUMS.txt (cambia un char del hash)")
    contenido_original = MANIFIESTO.read_bytes()

    # Cambia el primer carácter del primer hash ('5' → 'f')
    lineas = MANIFIESTO.read_text().splitlines()
    primera_linea_original = lineas[0]
    lineas[0] = 'f' + lineas[0][1:]          # altera el primer nibble
    MANIFIESTO.write_text("\n".join(lineas) + "\n")

    print(f"\n  Linea original : {primera_linea_original[:72]}...")
    print(f"  Linea alterada : {lineas[0][:72]}...")
    return contenido_original


def paso_5_verificar_manifiesto_alterado() -> None:
    titulo("EJ5 — Paso 5: Hospital re-verifica (manifiesto alterado)")
    valida, mensaje = verificar_firma_manifiesto(
        str(MANIFIESTO), str(CLAVE_PUB), str(FIRMA)
    )
    resultado_firma(valida, mensaje)
    print("\n  Cualquier cambio al manifiesto invalida la firma —")
    print("  el atacante no puede recalcularla sin la clave privada de MediSoft.")


def paso_6_restaurar_y_refirmar(contenido_original: bytes) -> None:
    titulo("EJ5 — Paso 6: Restaurar manifiesto y re-firmar para siguiente prueba")
    MANIFIESTO.write_bytes(contenido_original)
    firmar_manifiesto(str(MANIFIESTO), str(CLAVE_PRIV), str(FIRMA))
    print("  Manifiesto restaurado y re-firmado.")


def paso_7_atacante_modifica_archivo() -> None:
    titulo("EJ5 — Paso 7: Atacante modifica un byte en firmware_analizador.bin")
    archivo = PAQUETE_DIR / "firmware_analizador.bin"
    datos = bytearray(archivo.read_bytes())
    pos = 10
    original = datos[pos]
    datos[pos] = (original ^ 0xFF)           # flip de todos los bits del byte
    archivo.write_bytes(bytes(datos))
    print(f"\n  Archivo alterado: {archivo.name}")
    print(f"  Byte en posicion {pos}: 0x{original:02X} -> 0x{datos[pos]:02X}")


def paso_8_verificar_firma_con_archivo_alterado() -> None:
    titulo("EJ5 — Paso 8: Hospital verifica FIRMA (archivo alterado, manifiesto intacto)")
    valida, mensaje = verificar_firma_manifiesto(
        str(MANIFIESTO), str(CLAVE_PUB), str(FIRMA)
    )
    resultado_firma(valida, mensaje)
    print()
    print("  La firma protege el MANIFIESTO, no los archivos directamente.")
    print("  El manifiesto no cambio => la firma sigue siendo valida.")


def paso_9_verificar_paquete_con_archivo_alterado() -> None:
    titulo("EJ5 — Paso 9: Hospital ejecuta verificar_paquete (archivo alterado)")
    resultados = verificar_paquete(str(MANIFIESTO), str(PAQUETE_DIR))
    resultado_paquete(resultados)


def paso_10_respuesta_conceptual() -> None:
    titulo("EJ5 — Respuesta: ¿Por qué la firma es válida pero verificar_paquete falla?")
    print("""
  Las dos capas protegen cosas distintas:

  CAPA 1 — Firma digital (RSA-PSS sobre SHA256SUMS.txt)
    Garantiza: el manifiesto es autentico y no fue alterado.
    Lo que firma: el CONTENIDO de SHA256SUMS.txt.
    Lo que NO firma: los archivos del paquete directamente.

  CAPA 2 — Hashes del manifiesto (SHA-256 por archivo)
    Garantiza: cada archivo coincide exactamente con lo que MediSoft publico.
    Lo que verifica: SHA-256(archivo_descargado) == hash en SHA256SUMS.txt.

  En el paso 7 el atacante modifico firmware_analizador.bin,
  pero NO toco SHA256SUMS.txt.

  => Capa 1: PASA  (el manifiesto no cambio, la firma es valida)
  => Capa 2: FALLA (el hash del archivo ya no coincide con el del manifiesto)

  Para que el ataque sea indetectable el atacante necesitaria:
    1. Modificar el archivo
    2. Recalcular su SHA-256 y actualizar SHA256SUMS.txt
    3. Firmar el nuevo SHA256SUMS.txt con la clave PRIVADA de MediSoft
       (esto es computacionalmente imposible sin la clave privada)
    """)


# ─── main ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    if not MANIFIESTO.exists():
        print("ERROR: Ejecuta primero simulacion_ej3.py para crear el paquete.")
        raise SystemExit(1)

    print("\nSimulacion Ej4+5 — Autenticidad del manifiesto MediSoft")

    paso_1_generar_claves()
    paso_2_firmar_manifiesto()
    paso_3_verificar_original()
    contenido_original = paso_4_atacante_modifica_manifiesto()
    paso_5_verificar_manifiesto_alterado()
    paso_6_restaurar_y_refirmar(contenido_original)
    paso_7_atacante_modifica_archivo()
    paso_8_verificar_firma_con_archivo_alterado()
    paso_9_verificar_paquete_con_archivo_alterado()
    paso_10_respuesta_conceptual()
