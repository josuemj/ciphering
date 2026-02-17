## Analisis  de Seguridad

> Todos los ejemplos se pueden ejecutar con: `python -X utf8 utils/keystream/demo.py`

### 2.1 Variación de la Clave
- ¿Qué sucede cuando cambia la clave utilizada para generar el keystream? Demuestre con un ejemplo concreto.

Se cifra el mismo mensaje `"HELLO WORLD"` con dos claves distintas (`secretA` y `secretB`). Cada clave inicializa el LCG con un estado diferente, produciendo keystreams completamente distintos y, por lo tanto, ciphertexts diferentes.

```python
mensaje = "HELLO WORLD"
clave_a = "secretA"
clave_b = "secretB"

keystream_a = generate_prng_keystream(clave_a, len(mensaje))
keystream_b = generate_prng_keystream(clave_b, len(mensaje))

cifrado_a = encrypt_with_keystream(mensaje, clave_a)
cifrado_b = encrypt_with_keystream(mensaje, clave_b)

descifrado_a = decrypt_with_keystream(cifrado_a, clave_a)
descifrado_b = decrypt_with_keystream(cifrado_b, clave_b)
```

**Salida:**
```
Mensaje original:      'HELLO WORLD'
Clave A:               'secretA'
Clave B:               'secretB'

Keystream A (hex):     05 5a 0b 68 01 26 67 14 3d 32 03
Keystream B (hex):     72 43 40 79 3e 1f 6c 35 4a 3b 58

Cifrado con clave A (hex): 4d 1f 47 24 4e 06 30 5b 6f 7e 47
Cifrado con clave B (hex): 3a 06 0c 35 71 3f 3b 7a 18 77 1c

Descifrado A:          'HELLO WORLD'
Descifrado B:          'HELLO WORLD'
```

**Conclusión:** Al cambiar la clave, el keystream generado es diferente, produciendo ciphertexts distintos. Cada clave genera una secuencia pseudo-aleatoria única.

---

### 2.2 Reutilización del Keystream
- ¿Qué riesgos de seguridad existen si reutiliza el mismo keystream para cifrar dos mensajes diferentes? Implemente un ejemplo que demuestre esta vulnerabilidad

Se cifran dos mensajes distintos (`"ATAQUE HOY"` y `"NADA PASAA"`) con la misma clave. Un atacante que intercepte ambos ciphertexts puede hacer XOR entre ellos y la clave se cancela: `C1 XOR C2 = (M1 XOR K) XOR (M2 XOR K) = M1 XOR M2`.

```python
mensaje_1 = "ATAQUE HOY"
mensaje_2 = "NADA PASAA"
clave = "misma_clave"

cifrado_1 = encrypt_with_keystream(mensaje_1, clave)
cifrado_2 = encrypt_with_keystream(mensaje_2, clave)

# El atacante hace XOR entre los dos ciphertexts
xor_cifrados = "".join(
    chr(ord(a) ^ ord(b)) for a, b in zip(cifrado_1, cifrado_2)
)

# Verificación: XOR directo de los mensajes originales
xor_mensajes = "".join(
    chr(ord(a) ^ ord(b)) for a, b in zip(mensaje_1, mensaje_2)
)
```

**Salida:**
```
Mensaje 1:             'ATAQUE HOY'
Mensaje 2:             'NADA PASAA'
Clave (misma):         'misma_clave'

Cifrado 1 (hex):       70 42 56 55 38 67 13 38 26 37
Cifrado 2 (hex):       7f 57 53 45 4d 72 72 23 28 2f

C1 XOR C2 (hex):       0f 15 05 10 75 15 61 1b 0e 18
M1 XOR M2 (hex):       0f 15 05 10 75 15 61 1b 0e 18

C1 XOR C2 == M1 XOR M2?  True
```

**Conclusión:** Si se reutiliza el mismo keystream, un atacante puede hacer XOR entre los dos ciphertexts y obtener `M1 XOR M2`, eliminando la clave por completo.

---

### 2.3 Longitud del Keystream

- ¿Cómo afecta la longitud del keystream a la seguridad del cifrado? Considere tanto keystreams más cortos como más largos que el mensaje.

Se comparan tres escenarios: keystream más corto (7 chars), exacto (15 chars) y más largo (30 chars) que el mensaje `"MENSAJE SECRETO"`.

```python
mensaje = "MENSAJE SECRETO"
clave = "clave123"

# Keystream más corto que el mensaje
ks_corto = generate_prng_keystream(clave, 7)
cifrado_parcial = "".join(
    chr(ord(p) ^ ord(k)) for p, k in zip(mensaje[:7], ks_corto)
)
parte_expuesta = mensaje[7:]

# Keystream de longitud exacta
cifrado_exacto = encrypt_with_keystream(mensaje, clave)

# Keystream más largo que el mensaje
ks_largo = generate_prng_keystream(clave, 30)
cifrado_largo = "".join(
    chr(ord(p) ^ ord(k)) for p, k in zip(mensaje, ks_largo)
)
```

**Salida:**
```
Mensaje:                'MENSAJE SECRETO' (longitud: 15)
Clave:                  'clave123'

--- Keystream CORTO (7 caracteres) ---
Solo cifra 7 chars (hex): 0d 3c 70 4c 2d 7f 0f
Parte expuesta:         ' SECRETO'
Resultado:              los últimos 8 caracteres quedan en TEXTO PLANO

--- Keystream EXACTO (15 caracteres) ---
Cifrado completo (hex): 0d 3c 70 4c 2d 7f 0f 1b 0b 74 55 45 41 39 6d
Descifrado:             'MENSAJE SECRETO'

--- Keystream LARGO (30 caracteres) ---
Cifrado (hex):          0d 3c 70 4c 2d 7f 0f 1b 0b 74 55 45 41 39 6d
¿Igual al exacto?      True
(Solo se usan los primeros len(mensaje) bytes del keystream)
```

**Conclusión:** Un keystream más corto que el mensaje deja parte del texto **sin cifrar**. Un keystream más largo no mejora la seguridad ya que los bytes extra se descartan. Lo ideal es que el keystream tenga **exactamente la misma longitud** que el mensaje.

---

### 2.4 Consideraciones Prácticas
- ¿Qué consideraciones debe tener al generar un keystream en un entorno de producción real?
Mencione al menos 3 aspectos críticos

**1. Usar un CSPRNG (Generador Criptográficamente Seguro)**
- El LCG usado en esta demo es **predecible**: un atacante que observe suficiente keystream puede deducir el estado interno y predecir valores futuros.
- En producción usar: `os.urandom()`, `secrets`..

**2. Nunca reutilizar clave**
- Cada mensaje debe usar un par (clave, nonce) **único**.
- Como se demostro en 2.2, reutilizar el keystream es fatal.

**3. Gestion segura de claves**
- Almacenar claves en HSM o key vaults, **nunca en codigo fuente**.
- Rotar claves periodicamente.

**4. Integridad del mensaje (Autenticacion)**
- XOR solo provee confidencialidad, **NO integridad**.
- Un atacante puede modificar bits del ciphertext y alterar el plaintext de forma predecible (**bit-flipping attack**).

```python
mensaje = "PAGAR: 100$"
clave = "clave_demo"
cifrado = encrypt_with_keystream(mensaje, clave)

# Atacante modifica el byte en posicion 7 para cambiar '1' por '9'
cifrado_mod = list(cifrado)
cifrado_mod[7] = chr(ord(cifrado_mod[7]) ^ ord('1') ^ ord('9'))
cifrado_mod = "".join(cifrado_mod)

descifrado_mod = decrypt_with_keystream(cifrado_mod, clave)
```

**Salida:**
```
Mensaje original:       'PAGAR: 100$'
Cifrado (hex):          31 47 00 35 4f 28 43 51 29 6e 1b
Cifrado modificado:     31 47 00 35 4f 28 43 59 29 6e 1b
Descifrado modificado:  'PAGAR: 900$'
El atacante cambio '100' por '900' sin conocer la clave.
```

Sin mecanismo de autenticacion, el receptor no puede detectar que el mensaje fue alterado.

---
