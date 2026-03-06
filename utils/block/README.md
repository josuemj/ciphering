# Análisis de Seguridad - Block Ciphers

## Análisis de Tamaños de Clave

**Pregunta:** ¿Qué tamaño de clave está usando para DES, 3DES y AES? Para cada uno:

- Indique el tamaño en bits y bytes
- Explique por qué DES se considera inseguro hoy en día
- Calcule cuánto tiempo tomaría un ataque de fuerza bruta con hardware moderno

### Tamaños de clave usados en cada algoritmo

- **DES:** 8 bytes = 64 bits

```powershell
python -c "from utils.block.base import generate_des_key; k=generate_des_key(); print(f'DES: {len(k)} bytes = {len(k)*8} bits')"
```

```text
DES: 8 bytes = 64 bits
```

- **3DES (por defecto):** 24 bytes = 192 bits

```powershell
python -c "from utils.block.base import generate_3des_key; k=generate_3des_key(); print(f'3DES: {len(k)} bytes = {len(k)*8} bits')"
```

```text
3DES: 24 bytes = 192 bits
```

- **AES (por defecto, AES-256):** 32 bytes = 256 bits

```powershell
python -c "from utils.block.base import generate_aes_key; k=generate_aes_key(); print(f'AES: {len(k)} bytes = {len(k)*8} bits')"
```

```text
AES: 32 bytes = 256 bits
```
Riesgo de DES:
- **Clave efectiva pequeña:** aunque se manejen **8 bytes (64 bits)**, DES tiene **56 bits efectivos** de clave (hay bits de paridad). Eso reduce el espacio de busqueda a `2^56`, que hoy es alcanzable por fuerza bruta.
- **Bloque de 64 bits:** al cifrar muchos datos con la misma clave, el bloque pequeno facilita colisiones (cumpleanos) y patrones estadisticos.
- **Legado:** en la practica moderna se usa **AES**; **3DES** es principalmente compatibilidad/legado, no recomendado para disenos nuevos.

**Calcule cuanto tiempo tomaria un ataque de fuerza bruta con hardware moderno (estimacion)**

Si una maquina prueba `R` claves/segundo, el tiempo promedio de busqueda exhaustiva es:

`tiempo_promedio ≈ 2^(k-1) / R`  (peor caso: `2^k / R`)

- **DES (k = 56 bits efectivos):**
  - Si `R = 10^12` claves/s: peor caso `2^56 / 10^12` ≈ **20 horas** (promedio ≈ **10 horas**)
  - Si `R = 10^15` claves/s: peor caso `2^56 / 10^15` ≈ **72 segundos** (promedio ≈ **36 segundos**)
- **3DES (24 bytes en este repo)** y **AES-256 (32 bytes en este repo):** por fuerza bruta directa son muchisimo mas costosos que DES; en la practica, los riesgos reales suelen venir de modo de operacion, IV, padding, implementacion o mal manejo de llaves, no de enumerar todas las claves.

---

## Comparación de Modos de Operación

**Pregunta:** Compare ECB vs CBC mostrando:

- ¿Qué modo de operación implementó en cada algoritmo?
- ¿Cuáles son las diferencias fundamentales entre ECB y CBC?
- ¿Se puede notar la diferencia directamente en una imagen?

**Requisitos:**
- Incluya las tres imágenes lado a lado: original, cifrada con ECB, cifrada con CBC
- Señale específicamente qué patrones son visibles en ECB pero no en CBC
- Proporcione el código exacto que usó para generar estas imágenes

---

## Vulnerabilidad de ECB

**Pregunta:** ¿Por qué no debemos usar ECB en datos sensibles?

**Requisitos:**
- Cree un ejemplo que muestre cómo bloques idénticos producen cifrados idénticos
- Cifre un mensaje que contenga texto repetido (ej: "ATAQUE ATAQUE ATAQUE") con ECB y CBC
- Muestre en hexadecimal cómo los bloques cifrados son iguales en ECB pero diferentes en CBC
- Explique qué información podría filtrar esto en un escenario real

---

## Vector de Inicialización (IV)

**Pregunta:** ¿Qué es el IV y por qué es necesario en CBC pero no en ECB?

**Requisitos:**
- Implemente un experimento: cifre el mismo mensaje dos veces con CBC usando:
  - El mismo IV
  - IVs diferentes
- Muestre cómo los cifrados resultantes son diferentes en el caso 2
- Explique qué pasaría si un atacante intercepta mensajes cifrados con el mismo IV

---

## Padding

**Pregunta:** ¿Qué es el padding y por qué es necesario?

**Requisitos:**
- Muestre el resultado de su función `pkcs7_pad` con diferentes mensajes:
  - Mensaje de 5 bytes
  - Mensaje de 8 bytes (exactamente un bloque de DES)
  - Mensaje de 10 bytes
- Explique byte por byte qué se agregó en cada caso
- Demuestre que su función `pkcs7_unpad` recupera el mensaje original
