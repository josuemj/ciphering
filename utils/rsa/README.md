# Escenario

Plataforma de Transferencia de Documentos Legales Una firma de abogados necesita transferir documentos confidenciales entre sus oficinas de Guatemala
City, Miami y Madrid. Los documentos contienen contratos, acuerdos de confidencialidad y datos personales.

El sistema debe garantizar:
- Solo el destinatario pueda leer el documento

### 1. El sistema usa RSA como mecanismo de intercambio de clave, protegiendo una clave AES que cifra el documento real.
- RSA no soporta archivos grandes de forma directa: con una clave típica (p. ej., RSA‑2048) solo puedes cifrar unos cientos de bytes por operación; un contrato/PDF requiere partirlo en muchos bloques, lo que complica el diseño.
- Sería muy lento y caro computacionalmente: cifrar megabytes con RSA es muchísimo más lento que con AES, especialmente si hay muchos documentos y usuarios.

### 2. Generación de claves RSA en `generar_claves.py`

Instalar dependencias:
```bash
pip3 install -r requirements.txt
```

Generar claves y guardar los PEM en `utils/rsa/assets/` (ejemplo con la passphrase requerida `lab04uvg`):
```bash
python3 utils/rsa/generar_claves.py --passphrase lab04uvg
```

Alternativa (sin exponer la passphrase en el comando):
```bash
export RSA_PASSPHRASE='lab04uvg'
python3 utils/rsa/generar_claves.py
```

Archivos generados:
- `utils/rsa/assets/private_key.pem` (protegida con passphrase)
- `utils/rsa/assets/public_key.pem`

Opcional (cambiar bits):
```bash
python3 utils/rsa/generar_claves.py --bits 3072 --passphrase lab04uvg
```

### 3. Cifrado y Descifrado Directo con RSA-OAEP

Este ejemplo cifra el texto `"mensaje"` con la **clave pública** usando RSA-OAEP, y luego lo descifra con la **clave privada**.

Puntos clave:
- El cifrado con OAEP es **aleatorio** (aunque el mensaje sea el mismo, el ciphertext cambia en cada corrida).
- RSA-OAEP se usa para **mensajes cortos**; para documentos completos se usa cifrado híbrido (RSA + AES).

```bash
export RSA_PASSPHRASE='lab04uvg'
python3 utils/rsa/rsa_oeap.py --message "mensaje"
```

Salida:
```text
Cifrado (base64): F2wGKmsB5mTFMqwpU1LdGrzyFRdzyruUBxETxMT7wGLRcN5K3Zj+SgqgbEPq5Zg1MLWEfCk2a4zd31FF1OHhdchfY87JAqAgVk6pldroP6FlWOtcLHFejy58hqnHnIE8NnK9P37O0m4W/dhhbkplhPOjFwinzndtr+M550eZ+VE2q5PcHWcfnpvygJozYak/a0JMWTDKlGBX+0tz6oYrlHr3N0X7JSPw2nygHLMSKWW70dKuK6YYq51DlOBwmHH5pTCAthT/G2Ats0v9Ka1QrUbqD2j99m+9Fawnynzu7M2DIicEqq/XwDEBA9m5N4zOWHuRF23Vl/FRfKaosXJCyA==
Descifrado: mensaje
```

```bash
python3 utils/rsa/rsa_oeap.py --message "mensaje" --passphrase lab04uvg
```

Salida:
```text
Cifrado (base64): IJKUc7XSsAJMgio3sNAxr1Lk/cIXKS1vsJ25x4wI3kiKXjOMY04kYF+RBFhhSy/Gct8Aw8j4oVvtbqeYtDuEss0l9xuKFS5+0+yFwGcSmRYxi0i1YjECnMwg8y1m58Ukwgqy2y2rRkrUEz/l1QNugWK5QrAlq8sS1J5bmxOArPH4yPZua2+ODpPGGn5Xa34Tt8w8u4LhJqzHGmNzcPMnnOLcL/ebp/Ikkko5H/JFvEI+32IGXS65PrnffgyyFwpaAwz+0KylChjQa6uCPd6mkocemS3lLQiqIujNOJkQicSNnLrVd7LsmdGJHI+5IV/DrL12+OEaRAnP2QYLSrBFVg==
Descifrado: mensaje
```
