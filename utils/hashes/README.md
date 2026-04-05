# Lab — Funciones Hash (MediSoft S.A.)

## Ejercicio 1 — Exploración de algoritmos hash

**Archivos:** `explorar_hashes.py`, `comparacion_1.py`, `hash_utils.py`
**Tests:** `tests/test_explorar_hashes.py`

### Ejecución

```bash
# Desde utils/hashes/
python comparacion_1.py
```

### Tabla comparativa

| Input | Algoritmo | Bits | Hex len | Bits cambiados | Hash |
|---|---|---:|---:|---:|---|
| MediSoft-v2.1.0 | MD5 | 128 | 32 | 61 | `cac2fe40370e3a68f0a4927c20c75c89` |
| medisoft-v2.1.0 | MD5 | 128 | 32 | 61 | `fa386a0d796e388b24cb3302c185a445` |
| MediSoft-v2.1.0 | SHA-1 | 160 | 40 | 77 | `3ab92abc44e23465b154e887f90c3a5e0d642c65` |
| medisoft-v2.1.0 | SHA-1 | 160 | 40 | 77 | `4fe9fa8c97db362ecce61ee6302a92f0505217cd` |
| MediSoft-v2.1.0 | SHA-256 | 256 | 64 | **120** | `64942401fe64ac1182bd88326ba7ca57a23ea5d0475653dea996ac15e8e74996` |
| medisoft-v2.1.0 | SHA-256 | 256 | 64 | **120** | `ec8d163da33b9832c33fbb2d7cba98f5a7087aa6cbdecc04eb32810b1f1f895e` |
| MediSoft-v2.1.0 | SHA-3/256 | 256 | 64 | **139** | `3b0af4c0a9078e2ddc1606313db9206dcb3a4dbf423d78c0cf16929d303e30d2` |
| medisoft-v2.1.0 | SHA-3/256 | 256 | 64 | **139** | `569daf2d0645c0ab6c0a7960cb552f28ac1a222284fa5605ab11cfe0a2dce82c` |

> **Bits cambiados** = distancia de Hamming calculada con XOR entre los dos digests del mismo algoritmo.

---

### Preguntas de análisis

#### ¿Cuántos bits cambiaron en SHA-256? ¿Qué propiedad demuestra?

Entre `"MediSoft-v2.1.0"` y `"medisoft-v2.1.0"` — un cambio de capitalización — SHA-256 produjo digests que difieren en **120 de 256 bits (46.9 %)**.

Esto demuestra el **efecto avalancha**: una modificación mínima en el input se propaga de forma impredecible por todo el digest, alterando aproximadamente la mitad de los bits de salida.

#### ¿Por qué MD5 es inseguro para integridad de archivos?

MD5 produce un digest de solo **128 bits**. Por el principio del cumpleaños, la resistencia a colisiones de una función hash de n bits es ~2^(n/2). Para MD5:

```
2^(128/2) = 2^64 ≈ 1.8 × 10^19 operaciones
```

En teoría esto parece grande, pero en la práctica se han encontrado colisiones estructurales — dos entradas distintas con el mismo MD5 — en segundos usando hardware moderno. Las colisiones permiten que un atacante genere un paquete malicioso con el mismo hash que el legítimo: el hospital descargaría malware pensando que el hash coincide.

---

## Ejercicio 2 — Verificación contra filtraciones (HIBP k-Anonymity)

**Archivo:** `hibp_check.py`

### Descripción

Se toma una lista de contraseñas comunes, se calcula su SHA-256 (para ilustrar la vulnerabilidad) y su SHA-1 (requerido por la API de HIBP), y se consulta [Have I Been Pwned](https://haveibeenpwned.com/) para saber cuántas veces aparecen en filtraciones públicas, sin revelar el hash completo.

### Ejecución

```bash
# Desde utils/hashes/
python hibp_check.py
```

### Resultados

| Password | SHA-256 | SHA-1 prefix | Filtraciones |
|---|---|---|---:|
| admin | `8c6976e5...` | `D033E...` | 42,085,691 |
| 123456 | `8d969eef...` | `7C4A8...` | 209,972,844 |
| hospital | `8afe3c83...` | `2B2D0...` | 118,791 |
| medisoft2024 | `78c12e8e...` | `F80CF...` | **No encontrado** |

### ¿Por qué SHA-256 directo es inseguro para contraseñas?

SHA-256 es **rápido por diseño** — puede calcular miles de millones de hashes por segundo en una GPU moderna. Para contraseñas comunes como `admin` o `123456`, los atacantes precalculan tablas rainbow con SHA-256 de millones de contraseñas. Al robar la base de datos, basta buscar el hash y obtener la contraseña en milisegundos.

### Nota técnica: SHA-1 vs SHA-256 en HIBP

La API de HIBP usa **SHA-1**, no SHA-256. El lab muestra SHA-256 como ilustración del hash directo vulnerable, pero el lookup real requiere SHA-1 siguiendo el protocolo de HIBP. Ambos hashes se calculan localmente; solo el prefijo SHA-1 de 5 caracteres sale de la máquina.

---

## Ejercicio 3 — Verificación de integridad de distribución

**Archivos:** `generar_manifiesto.py`, `verificar_paquete.py`, `simulacion_ej3.py`

```
generar_manifiesto.py   ← módulo MediSoft (publicador)
  sha256_archivo()          calcula SHA-256 de un archivo en bloques
  agregar_al_manifiesto()   escribe una línea al SHA256SUMS.txt
  generar_manifiesto()      orquesta ambas para N archivos

verificar_paquete.py    ← módulo Hospital (verificador)
  leer_manifiesto()         parsea SHA256SUMS.txt → {nombre: hash}
  verificar_archivo()       recalcula SHA-256 y compara
  verificar_paquete()       verifica todos los archivos del manifiesto

simulacion_ej3.py       ← script de simulación (invoca ambos módulos)
  paso_1: crea paquete_medisoft/ con 5 archivos simulados
  paso_2: genera SHA256SUMS.txt
  paso_3: verifica (todo OK)
  paso_4: atacante modifica un byte en update_script.sh
  paso_5: re-verifica (detecta la manipulación)
```

### Ejecución

```bash
# Desde utils/hashes/
python simulacion_ej3.py
```

### Salida — Verificación 1 (paquete íntegro)

| Archivo | Estado |
|---|---|
| config.ini | OK |
| firmware_analizador.bin | OK |
| driver_lab.dll | OK |
| update_script.sh | OK |
| release_notes.txt | OK |

### Salida — Verificación 2 (byte modificado en `update_script.sh`)

| Archivo | Estado | Detalle |
|---|---|---|
| config.ini | OK | — |
| firmware_analizador.bin | OK | — |
| driver_lab.dll | OK | — |
| **update_script.sh** | **FALLO** | byte pos 32: `0x6F` → `0x70` |
| release_notes.txt | OK | — |

```
esperado : cb47ea5585d1f560b42d5b476ba26546e77dabd7de1a5ef0697aff08d3af97fc
real     : ff8ae3ec36a3f73b8e50688bc05af6ac5ad2fa40ca5df83e42f36ea5cf255960
```

Un solo byte cambiado produce un hash completamente distinto (efecto avalancha).

---

## Ejercicios 4 y 5 — Autenticidad del manifiesto (Firma Digital RSA-PSS)

**Archivos:** `generar_claves_rsa.py`, `firmar_manifiesto.py`, `verificar_firma.py`, `simulacion_ej4_5.py`

### Arquitectura

```
generar_claves_rsa.py        generar_par_claves()   → (pem_priv, pem_pub)
                             guardar_claves()        → medisoft_priv.pem / medisoft_pub.pem

firmar_manifiesto.py         firmar_manifiesto()     → SHA256SUMS.sig (256 bytes, RSA-PSS)

verificar_firma.py           verificar_firma_manifiesto() → (bool, mensaje)

simulacion_ej4_5.py          orquesta los 3 módulos + verificar_paquete en 10 pasos
```

```
claves_medisoft/
  medisoft_priv.pem       ← PRIVADA — nunca se distribuye (solo MediSoft)
paquete_medisoft/
  SHA256SUMS.txt          ← manifiesto (del ej3)
  SHA256SUMS.sig          ← firma RSA-PSS del manifiesto
  medisoft_pub.pem        ← PUBLICA — se distribuye con el paquete
```

### Ejecución

```bash
# Desde utils/hashes/ (requiere haber corrido simulacion_ej3.py antes)
python simulacion_ej4_5.py
```

### Resultados

| Paso | Escenario | Firma | verificar_paquete |
|---|---|---|---|
| 3 | Paquete original | **VALIDA** | 5/5 OK |
| 5 | SHA256SUMS.txt alterado (1 char) | **INVALIDA** | — |
| 8 | `firmware_analizador.bin` alterado, manifiesto intacto | **VALIDA** | 3/5 OK (falla) |

### Respuesta: ¿Por qué la firma es válida pero `verificar_paquete` falla?

Las dos capas protegen cosas distintas:

| Capa | Qué protege | Cómo |
|---|---|---|
| **Firma RSA-PSS** | La autenticidad del manifiesto | SHA-256(SHA256SUMS.txt) cifrado con clave privada |
| **Hashes del manifiesto** | La integridad de cada archivo | SHA-256(archivo) comparado contra SHA256SUMS.txt |

Cuando el atacante modifica `firmware_analizador.bin` sin tocar `SHA256SUMS.txt`:
- **Capa 1 pasa**: el manifiesto no cambió, la firma sigue siendo válida
- **Capa 2 falla**: el hash recalculado del archivo no coincide con el del manifiesto

Para que el ataque sea indetectable el atacante necesitaría:
1. Modificar el archivo
2. Recalcular el SHA-256 y actualizar `SHA256SUMS.txt`
3. Firmar el nuevo `SHA256SUMS.txt` con la **clave privada de MediSoft** — computacionalmente imposible sin ella