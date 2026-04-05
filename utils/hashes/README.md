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