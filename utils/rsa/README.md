# Escenario

Plataforma de Transferencia de Documentos Legales Una firma de abogados necesita transferir documentos confidenciales entre sus oficinas de Guatemala
City, Miami y Madrid. Los documentos contienen contratos, acuerdos de confidencialidad y datos personales.

El sistema debe garantizar:
- Solo el destinatario pueda leer el documento

### 1. El sistema usa RSA como mecanismo de intercambio de clave, protegiendo una clave AES que cifra el documento real.
- RSA no soporta archivos grandes de forma directa: con una clave típica (p. ej., RSA‑2048) solo puedes cifrar unos cientos de bytes por operación; un contrato/PDF requiere partirlo en muchos bloques, lo que complica el diseño.
- Sería muy lento y caro computacionalmente: cifrar megabytes con RSA es muchísimo más lento que con AES, especialmente si hay muchos documentos y usuarios.