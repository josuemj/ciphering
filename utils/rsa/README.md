# Escenario

Plataforma de Transferencia de Documentos Legales Una firma de abogados necesita transferir documentos confidenciales entre sus oficinas de Guatemala
City, Miami y Madrid. Los documentos contienen contratos, acuerdos de confidencialidad y datos personales.

El sistema debe garantizar:
- Solo el destinatario pueda leer el documento

### 1. El sistema usa RSA como mecanismo de intercambio de clave, protegiendo una clave AES que cifra el documento real.
- RSA no soporta archivos grandes de forma directa: con una clave típica (p. ej., RSA‑2048) solo puedes cifrar unos cientos de bytes por operación; un contrato/PDF requiere partirlo en muchos bloques, lo que complica el diseño.
- Sería muy lento y caro computacionalmente: cifrar megabytes con RSA es muchísimo más lento que con AES, especialmente si hay muchos documentos y usuarios.

### 2. Generación de claves RSA en `generar_claves.py`

Generar claves y guardar los PEM en `utils/rsa/assets/` (ejemplo con la passphrase requerida `lab04uvg`):
```bash
python3 utils/rsa/generar_claves.py --passphrase lab04uvg
```

Archivos generados:
- `utils/rsa/assets/private_key.pem` (protegida con passphrase)
- `utils/rsa/assets/public_key.pem`

Opcional (cambiar bits):
```bash
python3 utils/rsa/generar_claves.py --bits 3072 --passphrase lab04uvg
```

¿Qué información contiene un archivo .pem?
- Un archivo .pem (Privacy-Enhanced Mail) es un contenedor en texto ASCII que guarda datos criptográficos (clave pública, clave privada, certificado X.509, cadena de certificados, CSR, etc.) en este formato:
- Una línea de inicio: -----BEGIN ...-----
- Un bloque de Base64 (que es el binario real en formato DER/ASN.1, pero “armored”texto)
- Una línea de fin: -----END ...-----
