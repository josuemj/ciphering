## Desafío 1: Logs y Configuración

### Objetivo
Encontrar flags ocultas en archivos del sistema, logs y configuraciones dentro del contenedor `challenge1_ctf`.

### Proceso realizado
1. Se enumeraron usuarios con `cat /etc/passwd` y se identificó `hacker` como usuario con shell (`/bin/bash`).
2. Se exploraron rutas principales (`/`, `/home`, `/etc`, `/var/log`) y se hicieron búsquedas por palabras clave (`flag`, `ctf`, `token`, `secret`).
3. Se encontró una credencial en `/etc/hidden_config.txt`:
   - `Contraseña: LinuxForHackers`
4. Se cambió a `hacker` con `su - hacker` usando esa contraseña.
5. En `/home/hacker` se localizaron archivos ocultos y se detectó `.flag.txt`.
6. Se extrajo la bandera desde `/home/hacker/.flag.txt`.

### Resultado
Flag encontrada:

`FLAG{LINUX_BASICS}`

### Evidencia
- Credencial: `/etc/hidden_config.txt`
- Bandera: `/home/hacker/.flag.txt`

### Imagen
![Evidencia](img/challenge-1.png)