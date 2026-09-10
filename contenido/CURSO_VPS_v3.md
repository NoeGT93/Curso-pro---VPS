# VPS desde cero absoluto

## Un curso de 4 semanas para pasar de "nunca he usado una terminal" a desplegar, romper y recuperar tu primer servidor

---

# Antes de empezar

Este curso no asume que sabes Linux.

No asume que sabes qué es SSH.

No asume que sabes qué significa "abrir un puerto".

Y no espera que memorices comandos.

La meta es otra:

> **Ver una avería, ubicarla en una capa y saber cuál es la siguiente pregunta correcta.**

Al terminar deberías poder explicar, con tus propias palabras, este recorrido:

```text
Mi computadora
    ↓
Internet
    ↓
DNS
    ↓
IP del VPS
    ↓
Firewall
    ↓
HTTPS / TLS
    ↓
Nginx
    ↓
Aplicación
    ↓
systemd o Docker
    ↓
Ubuntu
    ↓
VPS del proveedor
```

Ese dibujo será nuestro "mapa del mundo". Vas a volver a él en cada sesión.

---

## Qué necesitas para empezar

| Cosa | Detalle | ¿Cuándo? |
|---|---|---|
| Una computadora | Windows, Mac o Linux, cualquiera sirve | Sesión 1 |
| Conexión a Internet | Nada especial | Siempre |
| Tarjeta o método de pago | Los proveedores de VPS piden uno al registrarse | Sesión 2 |
| Un dominio | Puede ser el más barato que encuentres | Sesión 6 |
| 45 minutos al día | Cinco días a la semana | Semanas 1 a 4 |

No necesitas una computadora potente. El trabajo pesado ocurre en el servidor, no en tu máquina.

---

## El presupuesto real del mes

Vale la pena verlo completo antes de empezar, para que no haya sorpresas en el estado de cuenta.

```text
VPS pequeño                      ~US$5 a US$7 al mes
Dominio                          ~US$10 a US$15 al año
Snapshots del laboratorio        centavos al mes, mientras existan
Certificado HTTPS                gratis (Let's Encrypt)
GitHub                           gratis para lo que haremos
Total del primer mes             alrededor de US$18 a US$22
```

El VPS es el gasto recurrente. El dominio es un pago anual que se amortiza.

**Tres advertencias que evitan cobros no deseados:**

1. En varios proveedores, **un servidor apagado sigue cobrando**. Apagar no es lo mismo que destruir. Si querés dejar de pagar, hay que destruir el recurso.
2. Los **snapshots cobran por almacenamiento** mientras existen. Diez snapshots olvidados cuestan más que el propio servidor.
3. Muchos precios anunciados son **promocionales del primer periodo** y renuevan más caro. Buscá el precio de renovación antes de comprar.

La última sesión del curso incluye el cierre de cuentas: qué borrar, qué conservar y cómo comprobar que ya no te están cobrando.

---

# Cómo funciona cada sesión

Todas las sesiones tienen exactamente los mismos seis bloques, siempre en el mismo orden:

| Bloque | Qué es |
|---|---|
| **Idea** | Una sola cosa nueva, explicada en dos o tres frases |
| **Misión** | Algo que haces de verdad en tu máquina o en el servidor |
| **Salida sana** | Cómo se ve la pantalla cuando salió bien |
| **Señal de alarma** | Cómo se ve cuando salió mal, y qué significa |
| **Checkpoint** | Una comprobación corta antes de seguir |
| **Mini quiz** | Dos o tres preguntas con la respuesta escondida |

Algunas sesiones añaden un séptimo bloque:

> 📸 **SNAPSHOT** — crea un punto de restauración antes de continuar.

No avances porque "el comando corrió".

Avanza cuando puedas contestar:

> **¿Qué comprobé con ese comando?**

---

## El ritmo

```text
Semana 1    sesiones 1 a 5      entrar sin encerrarte fuera
Semana 2    sesiones 6 a 10     que Internet vea algo
Semana 3    sesiones 11 a 15    HTTPS, Git y Docker
Semana 4    sesiones 16 a 20    automatizar sin perder el mapa
```

Cinco sesiones por semana. Sábado para recuperar lo atrasado, domingo libre.

Los dos días de colchón no son opcionales ni son premio. Están ahí porque algo va a fallar, y necesitás espacio para arreglarlo sin sentir que perdiste el curso.

---

# Las cinco reglas del laboratorio

## Regla 1 — Nunca cierres tu única puerta

Cuando estés cambiando SSH:

```text
Terminal A = sesión que ya funciona
Terminal B = sesión nueva para probar
```

No cierres A hasta haber comprobado que B funciona.

## Regla 2 — Consola del proveedor antes que hardening

Antes de desactivar contraseñas, root, tocar firewall o modificar SSH, debes saber entrar por la consola web o el modo de recuperación de tu proveedor.

Tu primera recuperación debe ser **de práctica**, no durante una emergencia.

## Regla 3 — Snapshot antes de una operación riesgosa

Cuando veas la señal 📸, crea un punto de restauración.

Un snapshot es excelente para el laboratorio, pero **no sustituye un backup independiente de tus datos**.

## Regla 4 — Copiar no es entender

Puedes copiar un comando.

Pero antes de pulsar Enter, intenta decir en voz alta qué crees que va a hacer.

Después mira la salida y compárala con lo que esperabas.

## Regla 5 — No arregles cinco cosas a la vez

Si algo falla:

```text
1 cambio
→ 1 prueba
→ observar
→ decidir
```

No cambies DNS, firewall, Nginx y Docker al mismo tiempo. Si funciona, no vas a saber cuál lo arregló. Si se rompe más, tampoco.

---

# Tu barra de progreso

Marca cada casilla solo cuando puedas hacerlo sin seguir una receta ciegamente.

```text
[ ] Nivel 0 — Puedo moverme por una terminal.
[ ] Nivel 1 — Entiendo IP, puerto, DNS, firewall y SSH.
[ ] Nivel 2 — Puedo entrar y recuperar un VPS.
[ ] Nivel 3 — Puedo servir una página por HTTP y HTTPS.
[ ] Nivel 4 — Puedo publicar una app detrás de Nginx.
[ ] Nivel 5 — Puedo operar una app con systemd.
[ ] Nivel 6 — Puedo empaquetarla con Docker.
[ ] Nivel 7 — Puedo desplegar desde GitHub.
[ ] Nivel 8 — Puedo diagnosticar una caída por capas.
[ ] Nivel 9 — Puedo reconstruir el servidor desde cero.
```

Los niveles miden lo que puedes hacer, no cuántas horas pasaste leyendo. Un nivel sin marcar no es un fracaso, es información.

---

# Mapa de las doce piezas

Esta tabla es tu glosario. Cada concepto responde siempre las mismas cinco preguntas:

- ¿qué es?
- ¿dónde vive?
- ¿cómo se ve cuando está sano?
- ¿cómo suele fallar?
- ¿con qué lo compruebo?

| Pieza | Qué hace | Vive principalmente en | Comprobación |
|---|---|---|---|
| [Terminal](#1-terminal) | Te deja dar órdenes a un sistema | Tu PC y el VPS | `pwd`, `whoami` |
| [VPS](#2-vps) | Es tu computadora alquilada en Internet | Proveedor cloud | panel + `hostname` |
| [IP](#3-ip) | Dirección de una máquina en una red | Red | `ip addr` |
| [Puerto](#4-puerto) | Puerta numerada de un servicio | Sistema operativo | `ss -lntp` |
| [DNS](#5-dns) | Traduce nombre a IP | Proveedor DNS | `dig +short` |
| [Firewall](#6-firewall) | Decide qué tráfico puede entrar | Proveedor + Ubuntu | `ufw status` |
| [SSH](#7-ssh) | Acceso remoto cifrado | Cliente + servidor | `ssh`, `sshd -t` |
| [Proceso/servicio](#8-proceso-y-servicio) | Programa que está ejecutándose | Ubuntu | `systemctl status` |
| [HTTP/HTTPS](#9-http-y-https) | Protocolo web | Cliente/servidor | `curl -I` |
| [TLS](#10-tls) | Cifra y autentica HTTPS | Nginx/certificado | `curl -Iv` |
| [Proxy inverso](#11-proxy-inverso) | Recibe web pública y la pasa a tu app | Nginx/Traefik/Caddy | `nginx -t` |
| [Contenedor](#12-contenedor) | Empaqueta app y dependencias | Docker | `docker compose ps` |

---
# Capítulo 0 — El mundo antes del VPS

## 1. Terminal

Una terminal es una ventana donde escribes órdenes de texto.

En Windows puedes usar PowerShell, Windows Terminal o WSL. En este curso basta con poder abrir una terminal local y escribir comandos.

### Anatomía de un comando

```bash
ls -lah /tmp
```

Léelo así:

```text
ls      = programa
-lah    = opciones
/tmp    = objetivo
```

### Primera misión

Ejecuta en una terminal Linux/WSL o más adelante dentro del VPS:

```bash
pwd
whoami
hostname
```

Una salida razonable podría parecerse a:

```text
/home/sergio
sergio
mi-computadora
```

No tienen que ser esos valores.

La idea es:

```text
pwd      → ¿dónde estoy?
whoami   → ¿quién soy?
hostname → ¿en qué máquina estoy?
```

---

## 2. VPS

VPS significa **Virtual Private Server**.

Para este curso puedes imaginarlo como:

> Una computadora Linux que vive encendida en el centro de datos de otra empresa y a la que entras por Internet.

No es exactamente una computadora física solo para ti. Normalmente es una máquina virtual sobre un servidor físico mayor.

Cuando compras un VPS recibes, como mínimo:

```text
CPU
RAM
disco
una IP
un sistema operativo
una forma de administrarlo
```

---

## 3. IP

Una IP identifica una interfaz en una red.

Ejemplo ficticio:

```text
203.0.113.10
```

Tu dominio puede cambiar.

Tu aplicación puede cambiar.

Pero para que Internet llegue a tu VPS necesita saber a qué dirección dirigirse.

Comprobación:

```bash
ip addr
```

No intentes entender toda la salida el primer día.

Solo reconoce que verás interfaces y direcciones.

---

## 4. Puerto

Una IP identifica la máquina.

Un puerto ayuda a identificar **qué servicio dentro de esa máquina** quieres alcanzar.

Tres puertos aparecerán constantemente:

```text
22   SSH
80   HTTP
443  HTTPS
```

Analogía:

```text
IP     = dirección del edificio
puerto = número de puerta
```

Comprobación:

```bash
sudo ss -lntp
```

Una línea parecida a esta:

```text
LISTEN 0 4096 0.0.0.0:22 0.0.0.0:* ...
```

significa, simplificando:

> Hay algo escuchando conexiones TCP en el puerto 22.

---

## 5. DNS

DNS evita que las personas tengan que memorizar IP.

```text
app.ejemplo.com
        ↓
203.0.113.10
```

Un registro `A` apunta un nombre a IPv4.

Un `AAAA` apunta a IPv6.

Un `CNAME` convierte un nombre en alias de otro nombre.

Comprobación:

```bash
dig +short app.ejemplo.com A
```

Salida sana esperada:

```text
203.0.113.10
```

Salida vacía:

```text
<no aparece nada>
```

Eso no significa automáticamente “el VPS está roto”.

Significa:

> Primero investigo DNS.

---

## 6. Firewall

El firewall decide qué tráfico se permite.

En este curso tendrás dos capas posibles:

```text
Firewall del proveedor
        +
UFW dentro de Ubuntu
```

Piensa en ellas como dos controles de acceso distintos.

Para nuestro laboratorio, normalmente queremos:

```text
22   permitido para SSH
80   permitido para HTTP
443  permitido para HTTPS
```

---

## 7. SSH

SSH es el protocolo que utilizarás para entrar remotamente al VPS.

Tu terminal local:

```text
ssh deploy@203.0.113.10
```

conecta con:

```text
sshd en el VPS
```

SSH puede autenticarte con contraseña o con criptografía de clave pública.

La ruta principal del curso terminará usando **claves**, no contraseña.

---

## 8. Proceso y servicio

Un proceso es un programa ejecutándose.

Un servicio es, en este contexto, un programa que el sistema administra para que pueda arrancar, detenerse, reiniciarse y volver a levantarse.

Ejemplo:

```bash
systemctl status nginx
```

Pregunta que responde:

> ¿Nginx está vivo según systemd?

---

## 9. HTTP y HTTPS

HTTP es la conversación web.

HTTPS es HTTP protegido por TLS.

Cuando escribes:

```text
https://app.ejemplo.com
```

tu navegador necesita que varias piezas funcionen:

```text
DNS correcto
↓
red accesible
↓
443 abierto
↓
TLS válido
↓
proxy respondiendo
↓
app respondiendo
```

---

## 10. TLS

TLS cifra la conexión y ayuda a demostrar que el servidor que responde por un dominio tiene un certificado válido para ese dominio.

En este curso usaremos Let's Encrypt + Certbot.

No pidas el certificado hasta que HTTP y DNS ya funcionen.

---

## 11. Proxy inverso

Tu aplicación puede escuchar en:

```text
127.0.0.1:3000
```

Eso significa que solo el propio VPS puede llegar directamente a ella.

Nginx escucha públicamente en:

```text
80
443
```

y pasa la petición a la app:

```text
Internet
   ↓
Nginx :443
   ↓
127.0.0.1:3000
   ↓
tu app
```

Ese intermediario es el proxy inverso.

---

## 12. Contenedor

Docker crea entornos aislados para ejecutar aplicaciones con sus dependencias.

Antes de Docker:

```text
Ubuntu
└── Node instalado
    └── app
```

Con Docker:

```text
Ubuntu
└── Docker
    └── contenedor
        ├── runtime
        └── app
```

Docker no reemplaza DNS, firewall, HTTPS ni la necesidad de comprender qué puerto está expuesto.

---

# Tu primera prueba del mapa

Sin mirar arriba, completa:

```text
dominio
   ↓
________
   ↓
firewall
   ↓
________
   ↓
proxy
   ↓
________
```

<details>
<summary>Ver respuesta</summary>

```text
dominio
   ↓
DNS / IP
   ↓
firewall
   ↓
TLS / HTTPS
   ↓
proxy
   ↓
aplicación
```

</details>

---

# Semana 1 — Entrar sin encerrarte fuera

Al final de esta semana vas a tener un servidor tuyo en Internet, vas a poder entrar con una llave en vez de una contraseña, y vas a saber cómo volver a entrar si algo se rompe.

---

## Sesión 1 — La terminal sin miedo

### Idea

Una terminal es una conversación. Escribes una orden, la máquina contesta.

Hay dos tipos de orden, y distinguirlas es la mitad del trabajo de este mes:

```text
órdenes que solo MIRAN      ls, pwd, cat, curl, dig
órdenes que CAMBIAN cosas   mkdir, rm, nano, systemctl restart
```

Las que solo miran no pueden romper nada. Puedes correrlas todas las veces que quieras.

### Misión

**Paso 1 — Abre una terminal según tu sistema.**

Si usas **Mac**: abre Spotlight con `Cmd + espacio`, escribe `Terminal`, Enter. Ya está.

Si usas **Linux**: `Ctrl + Alt + T` en la mayoría de escritorios. Ya está.

Si usas **Windows**: aquí hay una decisión que conviene tomar ahora y no a mitad del curso.

Windows trae PowerShell, y PowerShell sí puede conectarse por SSH. Pero no es Linux, y varios comandos del curso simplemente no existen ahí. El más importante es `ssh-copy-id`, que vas a necesitar en la sesión 4. Si llegas a esa sesión sin una terminal tipo Linux, te vas a trabar.

Por eso, en Windows, instala WSL. Abre PowerShell como administrador y ejecuta:

```powershell
wsl --install
```

Reinicia cuando te lo pida. Después vas a tener "Ubuntu" en tu menú de inicio, y esa es la terminal que usarás todo el curso.

Si por alguna razón no puedes instalar WSL, puedes seguir el curso desde PowerShell, pero en la sesión 4 tendrás que copiar la clave pública a mano en vez de usar `ssh-copy-id`.

**Paso 2 — Oriéntate.**

```bash
pwd
whoami
ls
ls -lah
```

**Paso 3 — Muévete.**

```bash
cd /
pwd
cd ~
pwd
clear
```

**Paso 4 — Crea y borra algo tuyo.**

```bash
mkdir -p ~/curso-vps/prueba
cd ~/curso-vps/prueba
touch hola.txt
ls -lah
```

Y ahora deshazlo:

```bash
rm hola.txt
cd ~
rmdir ~/curso-vps/prueba
```

### Salida sana

`pwd` responde con una ruta, algo como:

```text
/home/tunombre
```

`whoami` responde con un nombre de usuario, no con un error.

Después de `touch hola.txt`, el `ls -lah` incluye una línea con `hola.txt`.

### Señal de alarma

```text
command not found
```

Significa que ese programa no existe en esta máquina. No es que hiciste algo mal, es que ese comando no está instalado o no aplica a tu sistema. En Windows con PowerShell vas a ver esto seguido, y es justamente la razón de instalar WSL.

```text
Permission denied
```

Significa que el comando existe, pero tu usuario no tiene permiso para hacer eso ahí. Son cosas distintas y conviene no confundirlas.

### Checkpoint

```text
[ ] Puedo abrir una terminal en mi computadora.
[ ] Sé qué usuario soy.
[ ] Sé en qué carpeta estoy.
[ ] Puedo crear y borrar una carpeta.
[ ] Entiendo que un comando puede observar o modificar.
```

### Mini quiz

1. ¿Qué responde `pwd`?
2. ¿Qué diferencia hay entre `/` y `~`?
3. ¿`ls` observa o modifica?
4. Ves `command not found`. ¿El comando falló o el comando no existe?

<details>
<summary>Ver respuestas</summary>

1. La ruta de la carpeta donde estás parado en este momento.
2. `/` es la raíz de todo el sistema. `~` es el atajo a la carpeta personal de tu usuario.
3. Observa. Lista lo que hay, sin cambiarlo.
4. No existe. El sistema ni siquiera intentó ejecutarlo, porque no encontró un programa con ese nombre.

</details>

---

## Sesión 2 — Comprar el VPS y probar la salida de emergencia

### Idea

Antes de que te den las llaves de una casa, conviene saber dónde está la ventana.

En un servidor, esa ventana es la **consola del proveedor**: una forma de entrar que no depende de SSH ni de la red del servidor. Es lo que te salva el día que te equivoques configurando SSH, y ese día va a llegar.

Por eso hoy compras el servidor y practicas la salida de emergencia, sin tocar nada más.

### Misión

**Paso 1 — Antes de pagar, mira el precio de renovación.**

Muchos proveedores anuncian un precio promocional del primer periodo. Busca cuánto cuesta el segundo. Anota los dos.

**Paso 2 — Crea el servidor con esta configuración.**

```text
Ubuntu:          24.04 LTS
Arquitectura:    AMD64
IPv4:            sí
IPv6:            no por ahora
Tamaño:          el más pequeño disponible
Autenticación:   clave SSH si el proveedor lo permite
Nombre:          lab-vps-01
Región:          la más cercana a vos
```

Para la ruta manual de este curso, 1 GB de RAM alcanza.

Ojo con una cosa: si más adelante quieres instalar Coolify, su documentación pide un mínimo de 2 CPU y 2 GB de RAM. No planifiques ese paso sobre esta misma máquina.

**Paso 3 — Guarda estos datos donde no los pierdas.**

```text
Proveedor:
Nombre del VPS:
Región:
IPv4:
Ubuntu:
Fecha de creación:
Precio primer periodo:
Precio de renovación:
```

**Paso 4 — Encuentra las dos consolas.**

En el panel de tu proveedor busca:

```text
1. Consola web normal
2. Recovery console / rescue / consola fuera de banda
```

No todos usan los mismos nombres. Lo importante es la diferencia:

```text
Consola normal
→ puede seguir dependiendo de la red o de un agente del sistema

Recovery / rescue
→ sirve aunque la red o sshd estén rotos
```

**Paso 5 — Practica entrar por ahí, hoy, sin romper nada.**

Solo verifica que sabes:

```text
dónde se abre
qué credenciales pide
cómo salir
cómo volver al arranque normal
```

**Paso 6 — Escribe tu propio procedimiento.**

Crea un archivo `RECOVERY.md` en tu computadora:

```text
RECOVERY.md

Proveedor:
Ruta en el panel:
Botón u opción exacta:
Qué credenciales pide:
Cómo regreso al disco normal:
```

Este archivo vale más que cualquier comando del curso. Es lo primero que vas a abrir el día malo.

### 📸 SNAPSHOT S0 — "VPS recién creado"

Crea tu primer snapshot antes de tocar nada. Nómbralo:

```text
S0-fresh-ubuntu
```

Recordá que los snapshots cobran mientras existan. Al terminar el curso los borras.

### Salida sana

El panel muestra el servidor como activo, con una dirección IPv4 asignada.

La consola de recuperación abre y te pide credenciales o te muestra un prompt.

El snapshot aparece listado con su nombre.

### Señal de alarma

Si la consola de recuperación te pide una contraseña de root que nunca configuraste, deténte y búscala ahora en el panel de tu proveedor. Algunos la envían por correo al crear el servidor, otros te dejan restablecerla desde el panel.

Descubrir esto hoy toma cinco minutos. Descubrirlo el día que quedes fuera, con el sitio caído, es otra cosa.

### Checkpoint

```text
[ ] Conozco la IP de mi servidor.
[ ] Sé el precio de renovación, no solo el promocional.
[ ] Sé abrir la consola web del proveedor.
[ ] Sé dónde está el modo recovery o rescue.
[ ] Tengo escrito mi RECOVERY.md.
[ ] Tengo el snapshot S0.
```

### Mini quiz

1. ¿Cuál es la diferencia entre la consola normal y la de recuperación?
2. Apagas el servidor desde el panel para ahorrar. ¿Deja de cobrarte?
3. ¿Por qué practicamos la recuperación hoy y no cuando falle algo?

<details>
<summary>Ver respuestas</summary>

1. La normal puede depender de que la red o un agente del sistema funcionen. La de recuperación está pensada justamente para cuando eso ya no funciona.
2. En varios proveedores, no. Un servidor apagado sigue reservando recursos y sigue cobrando. Para dejar de pagar hay que destruirlo.
3. Porque una recuperación se aprende leyendo con calma, no con el sitio caído y el pulso acelerado. Hoy es un ejercicio. Después sería una emergencia.

</details>

---

## Sesión 3 — Tu primera conexión y tu propio usuario

### Idea

`root` es el usuario que puede hacer absolutamente todo, incluido destruir el sistema sin preguntar.

Por eso no se trabaja como root. Se trabaja como un usuario normal que puede *pedir permiso* cuando lo necesita. Ese permiso se pide con `sudo`.

### Misión

**Paso 1 — Entra por primera vez.**

Según lo que use tu proveedor:

```bash
ssh root@TU_IP
```

o:

```bash
ssh ubuntu@TU_IP
```

La primera vez vas a ver algo así:

```text
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

No es un error. Es SSH preguntándote si confías en la identidad de ese servidor. Escribe `yes`.

**Paso 2 — Mira dónde estás parado.**

```bash
whoami
hostname
cat /etc/os-release
```

**Paso 3 — Actualiza el sistema.**

```bash
sudo apt update
sudo apt upgrade -y
```

**Paso 4 — Crea tu usuario del curso.**

```bash
sudo adduser deploy
sudo usermod -aG sudo deploy
id deploy
```

**Paso 5 — Compruébalo desde otra terminal.**

Sin cerrar la que ya tienes abierta:

```bash
ssh deploy@TU_IP
whoami
sudo whoami
```

### Salida sana

En `cat /etc/os-release` te interesa reconocer esta línea entre las demás:

```text
VERSION_ID="24.04"
```

En el paso 5:

```text
deploy
root
```

Eso significa exactamente esto:

```text
trabajo normal          → deploy
acción administrativa   → sudo, y solo cuando hace falta
```

En `id deploy` debe aparecer `sudo` dentro de la lista de grupos.

### Señal de alarma

```text
deploy is not in the sudoers file
```

El usuario existe pero no quedó en el grupo `sudo`. Vuelve a correr `usermod -aG sudo deploy` desde la sesión de root que todavía tienes abierta, y cierra y vuelve a abrir la sesión de deploy para que el grupo tome efecto.

```text
Connection refused
```

Nadie contestó en el puerto 22. Revisa que el servidor esté encendido y que la IP sea la correcta.

### Checkpoint

```text
[ ] Entré al servidor por SSH.
[ ] El servidor corre Ubuntu 24.04.
[ ] El sistema está actualizado.
[ ] Existe el usuario deploy.
[ ] deploy puede usar sudo.
```

### Mini quiz

1. ¿Qué hace `sudo`?
2. ¿Por qué no trabajar siempre como root?
3. `whoami` responde `deploy` y `sudo whoami` responde `root`. ¿Está bien o está mal?

<details>
<summary>Ver respuestas</summary>

1. Ejecuta una sola orden con privilegios elevados, cuando tu usuario tiene autorización para pedirlos. No te convierte en root de forma permanente.
2. Porque root no pide confirmación. Un comando mal escrito borra cosas sin preguntar, y no hay deshacer.
3. Está perfecto. Es exactamente el resultado que buscábamos: identidad normal para el día a día, privilegio solo cuando lo pides.

</details>

---

## Sesión 4 — Llaves SSH y cerrar la puerta sin dejarte afuera

### Idea

Una llave SSH son dos archivos que nacen juntos.

```text
clave privada   se queda en TU computadora, nunca se copia a ningún lado
clave pública   se guarda en el servidor
```

El servidor puede comprobar que tienes la privada sin que tú se la mandes. Por eso es más segura que una contraseña: nunca viaja.

Hoy instalas la llave y después apagas los métodos de acceso que ya no necesitas. El orden importa: primero comprobar que la llave funciona, después cerrar lo demás.

### Misión

**Paso 1 — Crea la llave en TU computadora, no en el servidor.**

```bash
ssh-keygen -t ed25519 -C "curso-vps"
```

Acepta la ruta por defecto. Puedes ponerle una frase de paso o dejarla vacía.

**Paso 2 — Instala la pública en el servidor.**

```bash
ssh-copy-id deploy@TU_IP
```

Si estás en PowerShell sin WSL, `ssh-copy-id` no existe. En ese caso copia el contenido de tu archivo `.pub` y pégalo dentro de `/home/deploy/.ssh/authorized_keys` en el servidor.

**Paso 3 — La prueba de las dos terminales.**

```text
Terminal A → la sesión que ya tienes abierta, déjala así
Terminal B → ssh deploy@TU_IP
             sudo whoami
```

Solo continúas si B funciona. Si B no funciona, no sigas. Arregla eso primero.

### 📸 SNAPSHOT S1 — "antes-de-hardening-ssh"

Este es el snapshot más importante del curso. Lo que sigue es lo que más gente deja encerrada afuera.

**Paso 4 — Ahora sí, cierra lo que sobra.**

```bash
sudo nano /etc/ssh/sshd_config.d/00-hardening.conf
```

Contenido:

```text
PermitRootLogin no
PasswordAuthentication no
KbdInteractiveAuthentication no
PubkeyAuthentication yes
MaxAuthTries 3
```

**Paso 5 — Valida ANTES de reiniciar.**

```bash
sudo sshd -t
```

**Paso 6 — Solo si el paso 5 no dijo nada, reinicia.**

```bash
sudo systemctl restart ssh.service
```

**Paso 7 — Comprueba en la Terminal B antes de cerrar la A.**

```bash
ssh deploy@TU_IP
```

Si entra, ya puedes cerrar A.

### Salida sana

`sudo sshd -t` no imprime absolutamente nada.

En este comando, el silencio es la buena noticia. Significa que la configuración es válida.

Después del reinicio, la Terminal B entra sin pedirte contraseña.

### Señal de alarma

```text
/etc/ssh/sshd_config.d/00-hardening.conf line 3: Bad configuration option
```

**No reinicies SSH.** Corrige el archivo y vuelve a correr `sshd -t` hasta que calle.

Si reinicias con la configuración rota, sshd puede no volver a levantar, y entras por la consola de recuperación.

```text
Permission denied (publickey)
```

Llegaste al servidor, pero la llave no fue aceptada. No es lo mismo que un timeout. Revisa que copiaste la llave al usuario correcto.

### Sobre el puerto 22 y `ssh.socket`

En este curso **no cambiamos el puerto 22**. Añade riesgo y no aporta nada al aprendizaje.

Si algún día lo cambias, hay un detalle propio de Ubuntu 24.04 que rompe a mucha gente: el sistema arranca SSH por activación de socket. Editar `sshd_config` y reiniciar `ssh.service` no basta para cambiar el puerto. Hay que hacer esto:

```bash
sudo sshd -t
sudo systemctl daemon-reload
sudo systemctl restart ssh.socket
```

Y antes de intentarlo: snapshot, consola de recuperación probada, regla de firewall para el puerto nuevo ya creada, sesión anterior abierta y segunda terminal lista.

### ¿Y Fail2Ban?

No lo instalamos todavía, y conviene saber por qué.

Fail2Ban bloquea direcciones que fallan muchos intentos seguidos. Es útil contra ruido automatizado, pero no sustituye una autenticación fuerte. Nuestro control principal ya es más sólido:

```text
PasswordAuthentication no
+
clave pública
```

Sin contraseñas activadas, no hay contraseñas que adivinar. Lo veremos como defensa opcional en la semana 4.

### Checkpoint

```text
[ ] Tengo una clave Ed25519 en mi computadora.
[ ] La clave pública está instalada en el servidor.
[ ] Entro sin que me pida contraseña.
[ ] sshd -t no dice nada.
[ ] Root y contraseñas están desactivados.
[ ] Tengo el snapshot S1.
```

### Mini quiz

1. ¿Cuál de las dos llaves se copia al servidor?
2. `sshd -t` no imprimió nada. ¿Falló?
3. ¿Por qué la regla es tener dos terminales abiertas?
4. ¿Qué diferencia hay entre `Connection refused` y `Permission denied (publickey)`?

<details>
<summary>Ver respuestas</summary>

1. La pública. La privada nunca sale de tu computadora.
2. No. En ese comando, ninguna salida significa que la configuración es válida. Si hubiera error, lo diría.
3. Porque si el cambio rompe SSH, la terminal que ya está abierta sigue funcionando y te permite deshacerlo. Si cierras las dos, tu única entrada es la consola del proveedor.
4. `Connection refused` significa que nadie contestó, así que el problema está en red, firewall o servicio. `Permission denied (publickey)` significa que sí contestó, y el problema es la autenticación. Son capas distintas.

</details>

---

## Sesión 5 — Firewall y aprender a leer puertos

### Idea

Hay dos cosas que parecen la misma y no lo son:

```text
que el firewall PERMITA un puerto
que exista un servicio ESCUCHANDO en ese puerto
```

El firewall es la puerta. El servicio es alguien adentro que contesta.

Puedes tener la puerta abierta y la casa vacía. Puedes tener a alguien adentro y la puerta tapiada. Confundir las dos es la causa número uno de perder una tarde.

### Misión

**Paso 1 — Antes de tocar el firewall, confirma que SSH funciona en una segunda terminal.**

Esta regla vuelve cada vez que toques red o acceso.

**Paso 2 — Instala UFW.**

```bash
sudo apt install ufw
```

**Paso 3 — Escribe las reglas SIN activar todavía.**

```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

**Paso 4 — Revísalas antes de encender.**

```bash
sudo ufw show added
```

Lee la lista. ¿Está el 22 ahí? Si no está, no actives nada todavía.

**Paso 5 — Ahora sí, activa.**

```bash
sudo ufw enable
sudo ufw status verbose
```

**Paso 6 — Mira quién está escuchando de verdad.**

```bash
sudo ss -lntp
```

### Salida sana

`sudo ufw status verbose` muestra `Status: active` y una lista que incluye 22, 80 y 443.

`sudo ss -lntp` muestra algo escuchando en el puerto 22.

Es muy probable que **no** haya nada en 80 ni en 443 todavía. Eso está bien y es justo el punto de esta sesión: el firewall ya permite ese tráfico, pero aún no hay nadie adentro para contestarlo. Lo pondremos en la sesión 7.

### Señal de alarma

Si activas UFW y tu sesión SSH se congela, es que la regla del 22 no estaba puesta.

Ahí es donde entra la consola del proveedor que practicaste en la sesión 2. Entras por ahí y ejecutas:

```bash
sudo ufw allow 22/tcp
```

Por eso el paso 4 existe. Revisar la lista antes de encender cuesta diez segundos.

### Checkpoint

```text
[ ] UFW está activo.
[ ] 22, 80 y 443 están permitidos.
[ ] Sigo pudiendo entrar por SSH.
[ ] Puedo leer la salida de ss -lntp.
[ ] Entiendo que permitir un puerto no crea un servicio.
```

Y sin mirar arriba, completa el recorrido:

```text
mi laptop
→ ______
→ VPS
→ ______
→ sshd
```

<details>
<summary>Ver una respuesta válida</summary>

```text
mi laptop
→ Internet
→ IP del VPS
→ firewall
→ sshd :22
```

</details>

### Mini quiz

1. UFW permite el 443 pero el navegador no abre nada. ¿Qué falta?
2. ¿Qué pregunta responde `ss -lntp`?
3. ¿Por qué revisamos las reglas antes de `ufw enable`?

<details>
<summary>Ver respuestas</summary>

1. Un servicio escuchando en el 443. El firewall abrió la puerta, pero adentro todavía no hay nadie.
2. Qué programas están escuchando ahora mismo, en qué puertos y en qué dirección. Es la foto de quién está adentro.
3. Porque activar UFW sin permitir el 22 te desconecta al instante, y recuperarte requiere la consola del proveedor.

</details>

---

## Fin de la semana 1

**Sábado:** recupera cualquier sesión atrasada y relee el capítulo 0.

**Domingo:** descanso. No se penaliza no tocar el VPS.

Deberías poder marcar:

```text
[x] Nivel 0 — Puedo moverme por una terminal.
[x] Nivel 1 — Entiendo IP, puerto, DNS, firewall y SSH.
[x] Nivel 2 — Puedo entrar y recuperar un VPS.
```

---
# Semana 2 — Que Internet vea algo

Esta semana un desconocido va a poder escribir tu dominio y ver una página tuya. Y vas a provocar tu primer error a propósito para aprender a leerlo.

---

## Sesión 6 — DNS sin magia

### Idea

Nadie memoriza direcciones numéricas. Por eso existe el DNS: una guía telefónica pública que traduce un nombre a una IP.

Un detalle que confunde a todo el mundo al principio:

```text
el DNS NO aloja tu página
el DNS solo dice dónde está
```

Cambiar el DNS no arregla una aplicación caída, igual que cambiar la dirección en un sobre no arregla una casa sin luz.

### Misión

**Paso 1 — En el panel de tu proveedor de dominio, crea el registro.**

```text
Tipo:    A
Nombre:  app
Valor:   TU_IP
TTL:     300 o 600 mientras aprendes
```

El resultado que buscas:

```text
app.tudominio.com → TU_IP
```

**Paso 2 — Comprueba desde tu computadora, no desde el servidor.**

```bash
dig +short app.tudominio.com A
```

**Paso 3 — Entiende el TTL.**

El TTL es cuántos segundos puede quedarse guardada esa respuesta en las cachés del mundo antes de volver a preguntar. Con 300 tus cambios tardan hasta cinco minutos en verse.

Por eso durante el curso lo dejamos bajo. Cuando todo esté estable, lo puedes subir.

**Paso 4 — No publiques AAAA todavía.**

Un registro `AAAA` apunta a una dirección IPv6. Si lo publicas y tu servicio no responde por IPv6, algunos visitantes verán un sitio caído y vos vas a ver todo bien desde tu máquina. Es un error difícil de diagnosticar.

Lo dejamos para después.

### Salida sana

```text
$ dig +short app.tudominio.com A
203.0.113.10
```

Una sola línea, con exactamente tu IP.

### Señal de alarma

**Respuesta vacía:**

```text
$ dig +short app.tudominio.com A
$
```

El nombre no existe o todavía no se propagó. Espera el TTL y revisa que escribiste bien el subdominio.

**Otra IP:**

```text
$ dig +short app.tudominio.com A
198.51.100.7
```

Está apuntando a otro lado. Suele ser un registro viejo que quedó del registrador, o que editaste el dominio equivocado.

En los dos casos, la regla es la misma: **no toques Nginx si DNS está mal.** Estás en otra capa.

### Checkpoint

```text
[ ] Creé el registro A.
[ ] dig +short devuelve mi IP y ninguna otra.
[ ] Entiendo qué es el TTL.
[ ] Entiendo que DNS no aloja nada, solo indica.
```

### Mini quiz

1. Tu navegador no encuentra `app.tudominio.com` y `dig +short` está vacío. ¿Cuál es la primera capa a investigar?
2. Cambiaste el registro A hace un minuto y `dig` sigue mostrando el valor viejo. ¿Está roto?
3. ¿Por qué no publicar un AAAA "por si acaso"?

<details>
<summary>Ver respuestas</summary>

1. DNS. Todavía no hay ninguna razón para culpar a Nginx, a Docker ni a tu aplicación. Ni siquiera se llegó a ellos.
2. No. Es el TTL haciendo su trabajo. La respuesta anterior sigue guardada hasta que expire.
3. Porque anuncia una dirección IPv6 a la que quizá tu servicio no responde. Los visitantes que usen IPv6 verán el sitio caído y vos no vas a poder reproducir el error.

</details>

---

## Sesión 7 — Nginx y una página extremadamente simple

### Idea

Nginx es el recepcionista del edificio. Es lo único que atiende al público, y decide a quién le pasa cada visita.

Hoy solo lo encendemos y comprobamos que contesta. Todavía no hay aplicación detrás. Primero que exista el recepcionista, después le damos a quién pasarle las visitas.

### Misión

**Paso 1 — Instala y enciende.**

```bash
sudo apt install nginx
sudo systemctl enable --now nginx
sudo systemctl status nginx --no-pager
```

**Paso 2 — Prueba desde adentro del servidor.**

```bash
curl -I http://127.0.0.1
```

**Paso 3 — Prueba desde tu computadora, por IP.**

```bash
curl -I http://TU_IP
```

**Paso 4 — Prueba desde tu computadora, por dominio.**

```bash
curl -I http://app.tudominio.com
```

Estos tres pasos parecen repetidos y no lo son. Cada uno prueba una capa distinta, y en qué paso falle te dice exactamente dónde está el problema.

### Salida sana

En `systemctl status nginx` buscas esta línea:

```text
Active: active (running)
```

En los tres `curl`:

```text
HTTP/1.1 200 OK
Server: nginx
```

### Señal de alarma

Esta es la tabla más útil de la semana. Según en qué paso falle:

```text
127.0.0.1 funciona, TU_IP no
→ firewall, o Nginx escuchando solo en loopback

TU_IP funciona, dominio no
→ DNS. Volvé a la sesión 6.

ninguno funciona
→ Nginx no está corriendo. Mirá systemctl status.
```

Fíjate en lo que acabas de hacer: no adivinaste. Tres pruebas te dijeron la capa.

### 📸 SNAPSHOT S2 — "nginx-http-ok"

### Checkpoint

```text
[ ] Nginx está activo.
[ ] curl responde 200 desde dentro del servidor.
[ ] curl responde 200 desde mi computadora por IP.
[ ] curl responde 200 desde mi computadora por dominio.
[ ] Sé qué significa que falle cada uno.
[ ] Tengo el snapshot S2.
```

### Mini quiz

1. `curl -I http://127.0.0.1` responde 200 pero `curl -I http://TU_IP` no responde. ¿Qué capa revisas?
2. Los dos anteriores funcionan pero el dominio no. ¿Qué capa revisas?
3. ¿Qué significa el `200` de `HTTP/1.1 200 OK`?

<details>
<summary>Ver respuestas</summary>

1. Red. El servicio existe y contesta localmente, pero el tráfico de afuera no llega. Firewall o a qué dirección está atado Nginx.
2. DNS. La máquina responde perfectamente, lo que falla es la traducción del nombre.
3. Que el servidor entendió la petición y la respondió correctamente. Es el código de "todo bien".

</details>

---

## Sesión 8 — Tu primera aplicación, escondida a propósito

### Idea

Tu aplicación **no** debe estar expuesta directamente a Internet.

Va a escuchar en `127.0.0.1:3000`, que significa "solo acepto conexiones que vengan de esta misma máquina".

¿Por qué esconderla? Porque así solo hay una puerta al público, la de Nginx, y una sola puerta es mucho más fácil de vigilar que dos.

### Misión

**Paso 1 — Pon a correr una app pequeña en el servidor.**

Puede ser un proyecto tuyo, o algo mínimo de Node. Lo que importa no es qué app sea, sino esta condición:

```text
escucha en 127.0.0.1:3000
```

**Paso 2 — Compruébala desde adentro del servidor.**

```bash
curl -v http://127.0.0.1:3000
```

**Paso 3 — Mira quién está escuchando.**

```bash
sudo ss -lntp | grep :3000
```

**Paso 4 — Intenta llegar desde tu computadora.**

```bash
curl -I http://TU_IP:3000
```

Esto **debe fallar**. Si funciona, tu app está expuesta al público y hay que arreglarlo.

### Salida sana

Desde adentro:

```text
< HTTP/1.1 200 OK
```

Y en `ss -lntp`, una línea con `127.0.0.1:3000`.

Desde tu computadora, el paso 4 falla. Eso es éxito, no error.

### Señal de alarma

```text
Connection refused
```

en el paso 2 significa que no hay nada aceptando conexiones ahí en este momento. La app no arrancó, se cayó, o está en otro puerto.

Y la señal que sí debe preocuparte:

```text
0.0.0.0:3000
```

en la salida de `ss -lntp`. Eso significa que la app está escuchando en **todas** las interfaces, o sea abierta al mundo. Hay que atarla a `127.0.0.1`.

### Checkpoint

```text
[ ] La app responde en 127.0.0.1:3000 desde adentro.
[ ] ss -lntp la muestra en 127.0.0.1, no en 0.0.0.0.
[ ] Desde mi computadora NO puedo alcanzar el puerto 3000.
[ ] Entiendo por qué eso último es lo correcto.
```

### Mini quiz

1. Si `localhost:3000` falla, ¿deberías revisar DNS?
2. ¿Qué diferencia hay entre `127.0.0.1:3000` y `0.0.0.0:3000`?
3. ¿Por qué queremos que la app NO sea accesible desde afuera?

<details>
<summary>Ver respuestas</summary>

1. No. El problema está más adentro: la aplicación, el runtime o el puerto. DNS es la capa más externa y ni siquiera participa en una prueba local.
2. `127.0.0.1` solo acepta conexiones de la propia máquina. `0.0.0.0` acepta de cualquier interfaz de red, o sea del mundo.
3. Para tener una sola puerta pública. Nginx atiende, filtra, pone HTTPS y decide. Si la app también está abierta, esa segunda puerta se salta todo eso.

</details>

---

## Sesión 9 — systemd: que la app sobreviva

### Idea

Ahora mismo tu app corre porque tienes una terminal abierta. Si la cierras, se muere. Si el servidor se reinicia, no vuelve.

systemd resuelve las dos cosas: mantiene tu app encendida, la vuelve a levantar si se cae y la arranca sola cuando el servidor reinicia.

Y trae una distinción que vas a usar el resto de tu vida:

```text
status  = ¿está vivo?
logs    = ¿qué dijo cuando se murió?
```

### Misión

**Paso 1 — Crea el archivo de servicio.**

```bash
sudo nano /etc/systemd/system/miapp.service
```

```ini
[Unit]
Description=Mi aplicación
After=network.target

[Service]
Type=simple
User=deploy
Group=deploy
WorkingDirectory=/srv/miapp
EnvironmentFile=/etc/miapp.env
ExecStart=/usr/bin/npm start
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
```

**Paso 2 — Cárgalo y enciéndelo.**

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now miapp
sudo systemctl status miapp --no-pager
```

**Paso 3 — Prueba que sobrevive.**

```bash
sudo systemctl restart miapp
curl -I http://127.0.0.1:3000
```

**Paso 4 — Aprende a preguntarle a los logs.**

```bash
sudo journalctl -u miapp -n 100 --no-pager
```

### Salida sana

```text
Active: active (running)
```

Y después del restart, el `curl` sigue respondiendo.

### Señal de alarma

```text
Active: failed (Result: exit-code)
```

No adivines por qué. Pregúntale a los logs:

```bash
sudo journalctl -u miapp -n 100 --no-pager
```

Las causas más comunes, en orden:

```text
ruta equivocada en WorkingDirectory
ExecStart apunta a un binario que no existe
falta el archivo de EnvironmentFile
permisos: el usuario deploy no puede leer esa carpeta
```

Y esta otra:

```text
Active: activating (auto-restart)
```

Significa que arranca, se muere y vuelve a arrancar en bucle. `Restart=on-failure` está haciendo su trabajo, pero algo la mata cada vez. También ahí, los logs.

### Checkpoint

```text
[ ] Mi app arranca con systemctl.
[ ] Sigue viva después de reiniciar el servicio.
[ ] Arranca sola si reinicio el servidor.
[ ] Sé leer journalctl.
[ ] Sé la diferencia entre status y logs.
```

### Mini quiz

1. ¿Qué pregunta responde `systemctl status`?
2. ¿Qué pregunta responden los logs?
3. El servicio dice `activating (auto-restart)` una y otra vez. ¿Qué pasa?

<details>
<summary>Ver respuestas</summary>

1. Si el servicio está vivo en este momento. Es una foto del presente.
2. Qué dijo el programa antes de morirse. Es la grabación del pasado. Por eso el status te dice que hay un problema y los logs te dicen cuál.
3. Que arranca y se cae en bucle. systemd lo revive, se vuelve a caer. El problema no es systemd, es lo que mata a la app cada vez. Está en los logs.

</details>

---

## Sesión 10 — Proxy inverso y tu primer 502

### Idea

Hoy conectas las dos piezas: Nginx adelante, tu app atrás.

Y después rompes la conexión a propósito, para ver qué error produce y aprender a leerlo. Un 502 no es un error de Nginx. Es Nginx diciéndote "yo estoy bien, el de atrás no contestó".

### Misión

**Paso 1 — Crea la configuración del sitio.**

```bash
sudo nano /etc/nginx/sites-available/app.tudominio.com
```

```nginx
server {
    listen 80;
    listen [::]:80;

    server_name app.tudominio.com;

    location / {
        proxy_pass http://127.0.0.1:3000;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Paso 2 — Actívala.**

```bash
sudo ln -s /etc/nginx/sites-available/app.tudominio.com \
  /etc/nginx/sites-enabled/app.tudominio.com

sudo nginx -t
sudo systemctl reload nginx
```

**Paso 3 — Prueba por capas, de adentro hacia afuera.**

```bash
curl -I http://127.0.0.1:3000
curl -I http://app.tudominio.com
```

**Paso 4 — El boss fight. Rompe la conexión a propósito.**

```bash
sudo systemctl stop miapp
```

Ahora abre `http://app.tudominio.com` en tu navegador.

**Paso 5 — Antes de arreglarlo, contesta:**

```text
¿DNS estaba necesariamente roto?     ______
¿Nginx estaba necesariamente roto?   ______
¿Qué faltaba?                        ______
```

**Paso 6 — Confirma tu hipótesis con un comando, no con una corazonada.**

```bash
curl -I http://127.0.0.1:3000
```

**Paso 7 — Repara y vuelve a probar.**

```bash
sudo systemctl start miapp
curl -I http://app.tudominio.com
```

### Salida sana

`sudo nginx -t`:

```text
syntax is ok
test is successful
```

Y el dominio responde `200 OK` cuando la app está viva.

### Señal de alarma

```text
502 Bad Gateway
```

Nginx está perfectamente vivo. Recibió la visita, intentó pasársela a `127.0.0.1:3000` y nadie contestó.

```text
504 Gateway Timeout
```

Distinto. Sí contestó, pero tardó demasiado. La app está viva pero lenta o colgada.

```text
nginx: [emerg] ...
```

Error de sintaxis en tu archivo. `nginx -t` te dice la línea. Nginx no recarga hasta que lo arregles, lo cual es bueno: prefiere no aplicar una configuración rota.

### Tu primer reflejo de diagnóstico

Guárdate esto. Es lo más valioso de la semana:

```text
502
↓
¿el backend responde?
↓
curl http://127.0.0.1:3000
↓
si no responde → el problema está en la app o el runtime
si responde    → el problema está en la configuración del proxy
```

### Checkpoint

```text
[ ] nginx -t pasa sin errores.
[ ] Mi dominio muestra la app.
[ ] Provoqué un 502 a propósito.
[ ] Supe decir en qué capa estaba antes de arreglarlo.
[ ] Lo confirmé con un comando, no adivinando.
[ ] Lo reparé.
```

### Mini quiz

1. Ves un 502. ¿Qué compruebas primero: DNS o el backend?
2. ¿Qué diferencia hay entre 502 y 504?
3. `nginx -t` da error. ¿Deberías recargar Nginx igual?

<details>
<summary>Ver respuestas</summary>

1. El backend. Un 502 solo puede ocurrir si la petición ya llegó hasta Nginx, y para eso el DNS tuvo que funcionar. Revisar DNS ahí es perder tiempo en una capa que ya sabes que está bien.
2. En el 502 el backend no contestó nada. En el 504 contestó demasiado tarde. Uno es "está muerto", el otro es "está lento o colgado".
3. No. Recargar con la configuración rota puede dejar el sitio caído. `nginx -t` existe precisamente para que compruebes antes de aplicar.

</details>

---

## Fin de la semana 2

**Sábado:** recupera lo atrasado. Si tu 502 no salió como esperabas, repite el ejercicio de la sesión 10.

**Domingo:** descanso.

Deberías poder marcar:

```text
[x] Nivel 3 — Puedo servir una página por HTTP.
[x] Nivel 4 — Puedo publicar una app detrás de Nginx.
[x] Nivel 5 — Puedo operar una app con systemd.
```

---
# Semana 3 — HTTPS, Git y Docker

Ya tienes algo publicado. Esta semana lo ciframos, ponemos el código donde debe estar y empaquetamos la aplicación.

---

## Sesión 11 — HTTPS con Certbot

### Idea

El candado del navegador es un certificado. Let's Encrypt los emite gratis, pero con una condición: tiene que poder comprobar que el dominio es tuyo, y lo hace visitándolo por el puerto 80.

De ahí sale la regla de esta sesión:

```text
si HTTP todavía no funciona, HTTPS no va a funcionar
```

No intentes cifrar algo que aún no responde.

### Misión

**Paso 1 — Confirma que la capa de abajo ya está sana.**

```bash
dig +short app.tudominio.com
curl -I http://app.tudominio.com
```

El primero debe devolver tu IP. El segundo debe llegar a tu Nginx. Si alguno falla, para aquí y vuelve a la sesión 6 o 7.

**Paso 2 — Instala Certbot.**

```bash
sudo snap install --classic certbot
```

Si el comando `certbot` no se encuentra después:

```bash
sudo ln -s /snap/bin/certbot /usr/bin/certbot
```

**Paso 3 — Pide el certificado.**

```bash
sudo certbot --nginx -d app.tudominio.com
```

Certbot edita tu configuración de Nginx por vos y recarga.

**Paso 4 — Compruébalo.**

```bash
curl -I https://app.tudominio.com
```

**Paso 5 — Comprueba que la renovación automática también funciona.**

```bash
sudo certbot renew --dry-run
```

Este paso es el que casi nadie hace, y es el que evita que el sitio se muera solo a los noventa días.

### Salida sana

```text
$ curl -I https://app.tudominio.com
HTTP/2 200
```

Y en el dry-run, una línea diciendo que la simulación de renovación tuvo éxito.

En el navegador, candado cerrado sin advertencias.

### Señal de alarma

```text
Timeout during connect (likely firewall problem)
```

Let's Encrypt no pudo llegar a tu servidor por el puerto 80. Revisa el firewall del proveedor y UFW.

```text
DNS problem: NXDOMAIN looking up A for app.tudominio.com
```

El nombre no existe todavía en el DNS. Es la capa 6, no la 11.

Y una advertencia importante: **si Certbot falla, no repitas el comando veinte veces.** Let's Encrypt tiene límites de intentos por dominio y te puede bloquear por horas. Diagnostica primero:

```bash
dig +short app.tudominio.com
curl -I http://app.tudominio.com
sudo ufw status
```

La pregunta siempre es la misma: *¿puede Let's Encrypt llegar al nombre que estoy intentando certificar?*

### 📸 SNAPSHOT S3 — "https-ok"

### Checkpoint

```text
[ ] https:// abre con candado y sin advertencias.
[ ] certbot renew --dry-run pasa.
[ ] Entiendo por qué el puerto 80 debe seguir abierto.
[ ] Tengo el snapshot S3.
```

### Mini quiz

1. ¿Por qué HTTP tiene que funcionar antes que HTTPS?
2. Cerraste el puerto 80 porque "ya todo va por HTTPS". ¿Qué se rompe y cuándo?
3. Certbot falla. ¿Repites el comando?

<details>
<summary>Ver respuestas</summary>

1. Porque Let's Encrypt comprueba que el dominio es tuyo visitándolo por el puerto 80. Si no puede llegar, no emite nada.
2. La renovación automática. Y no se rompe hoy: se rompe dentro de noventa días, cuando el certificado caduque y nadie haya avisado. Es el fallo más silencioso del curso.
3. No. Cada intento cuenta contra un límite y te pueden bloquear por horas. Diagnostica primero por capas.

</details>

---

## Sesión 12 — Git como única fuente de verdad

### Idea

Hay una tentación que arruina servidores: entrar por SSH, editar un archivo a mano para arreglar algo rápido, y seguir con la vida.

El problema no es el arreglo. Es que ahora el servidor y el repositorio dicen cosas distintas, y nadie sabe cuál es la versión buena. El siguiente despliegue borra tu arreglo y nadie entiende por qué volvió el error.

La regla:

```text
el código vive en Git
el servidor solo recibe copias
```

### Misión

**Paso 1 — Aprende a preguntarle al servidor qué versión tiene.**

```bash
git status
git log --oneline -5
git rev-parse HEAD
```

`git rev-parse HEAD` responde una pregunta muy concreta: *¿qué commit exacto está corriendo aquí?*

**Paso 2 — Practica el flujo correcto.**

Haz un cambio pequeño en tu app, pero desde tu computadora:

```text
código en tu máquina
→ commit
→ push a GitHub
→ pull en el VPS
→ reiniciar el servicio
```

**Paso 3 — Comprueba que la versión llegó.**

```bash
git rev-parse HEAD
```

Compara ese identificador con el de GitHub. Deben coincidir.

### Salida sana

`git status` en el servidor dice que no hay cambios locales:

```text
nothing to commit, working tree clean
```

Eso significa que nadie editó nada a mano ahí.

### Señal de alarma

```text
Changes not staged for commit:
  modified:   src/index.js
```

Alguien editó producción a mano. Puede que hayas sido vos hace tres semanas.

Ese archivo modificado es una bomba de tiempo: el próximo `git pull` va a dar conflicto, o el arreglo se va a perder sin dejar rastro.

La salida no es borrarlo sin mirar. Es ver qué cambió, llevar ese cambio al repositorio como corresponde, y dejar el servidor limpio.

### Checkpoint

```text
[ ] Sé qué commit está corriendo en el servidor.
[ ] git status en el servidor está limpio.
[ ] Hice un cambio pasando por GitHub, no editando en producción.
[ ] Entiendo por qué editar a mano en el servidor es un problema.
```

### Mini quiz

1. ¿Qué pregunta responde `git rev-parse HEAD`?
2. ¿Por qué es peligroso editar un archivo directamente en el servidor?
3. Tienes que arreglar algo urgente en producción. ¿Cuál es el camino?

<details>
<summary>Ver respuestas</summary>

1. Qué commit exacto está desplegado en esta máquina en este momento.
2. Porque el servidor y el repositorio dejan de coincidir. El arreglo existe solo ahí, no está registrado en ningún lado, y el próximo despliegue lo borra.
3. El mismo de siempre, solo que más rápido: código, commit, PR, merge, deploy. Saltarse el proceso por urgencia es lo que genera las urgencias siguientes.

</details>

---

## Sesión 13 — Docker: el concepto antes del comando

### Idea

Hoy no instalamos nada. Hoy entendemos qué problema resuelve Docker, porque instalarlo sin eso es memorizar comandos a ciegas.

Sin Docker, tu app depende de lo que haya instalado en el servidor:

```text
Ubuntu
├── Node (¿qué versión?)
├── npm
├── dependencias del sistema
└── tu app
```

Si tu máquina tiene Node 22 y el servidor tiene Node 18, tu app puede funcionar en una y fallar en la otra. Ese es el famoso "en mi máquina sí funciona".

Con Docker, la app viaja con todo lo que necesita:

```text
Ubuntu
└── Docker
    └── imagen reproducible
        └── contenedor corriendo
```

### Misión

Hoy la misión es de vocabulario. Estas seis palabras se confunden constantemente:

```text
Dockerfile   la receta escrita para construir
imagen       el paquete ya construido, congelado
contenedor   una instancia de esa imagen, corriendo
Compose      la forma de definir varios servicios juntos
volumen      datos que sobreviven cuando el contenedor muere
red          cómo se hablan los contenedores entre sí
```

La confusión más común es entre imagen y contenedor. Una analogía que funciona:

```text
Dockerfile  = la receta
imagen      = el pastel horneado
contenedor  = la rebanada que te estás comiendo
```

Puedes hacer muchas rebanadas del mismo pastel. Y si tiras la rebanada, el pastel sigue ahí.

### Salida sana

No hay comando hoy. La comprobación es que puedas explicar la diferencia entre imagen y contenedor con tus propias palabras, sin mirar.

### Señal de alarma

Si al leer la lista sentiste que "más o menos" entendías, vuelve a leerla. Docker se vuelve muy confuso muy rápido si estas seis palabras no están firmes.

### Checkpoint

```text
[ ] Puedo explicar qué problema resuelve Docker.
[ ] Sé la diferencia entre Dockerfile, imagen y contenedor.
[ ] Sé para qué sirve un volumen.
[ ] Entiendo que Docker no reemplaza mi mapa mental, solo sustituye una capa.
```

### Mini quiz

1. ¿Un `Dockerfile` es un contenedor?
2. Borras un contenedor. ¿Se borró la imagen?
3. ¿Qué pasa con los datos de una base de datos si el contenedor se destruye y no había volumen?

<details>
<summary>Ver respuestas</summary>

1. No. Es la receta que se usa para construir una imagen. El contenedor es una instancia de esa imagen, ya corriendo.
2. No. La imagen sigue ahí y puedes crear otro contenedor desde ella. Es el pastel y la rebanada.
3. Se perdieron. Sin volumen, todo lo que el contenedor escribió muere con él. Por eso los datos importantes siempre van en volúmenes.

</details>

---

## Sesión 14 — Instalar Docker sin abrir media máquina

### Idea

Aquí hay una trampa que muerde a casi todo el mundo, y es la razón por la que esta sesión existe aparte.

Docker escribe sus propias reglas de red, y **el tráfico hacia un puerto publicado por Docker puede saltarse tus reglas de UFW**. Puedes tener UFW diciendo que el 3000 está bloqueado, y el puerto abierto al mundo igual.

No es un fallo de Docker ni de UFW. Es que trabajan en niveles distintos. Pero si no lo sabés, publicás una base de datos a Internet sin enterarte.

### Misión

**Paso 1 — Instala desde el repositorio oficial de Docker para Ubuntu 24.04.**

No uses el script de conveniencia para algo que vaya a producción. Sigue la documentación oficial, que está en las referencias al final del curso.

**Paso 2 — Comprueba la instalación.**

```bash
sudo systemctl status docker
sudo docker run --rm hello-world
sudo docker compose version
```

**Paso 3 — Aprende la línea que importa.**

Esto publica tu app al mundo entero:

```yaml
ports:
  - "3000:3000"
```

Esto la deja solo accesible desde la propia máquina:

```yaml
ports:
  - "127.0.0.1:3000:3000"
```

En nuestra arquitectura siempre queremos la segunda, porque quien atiende al público es Nginx:

```text
Internet → Nginx 80/443 → localhost:3000 → contenedor
```

y nunca:

```text
Internet → 3000 directamente
```

**Paso 4 — Verifica con tus propios ojos.**

```bash
sudo ss -lntp
```

### Salida sana

`hello-world` imprime un mensaje de bienvenida y termina.

En `ss -lntp`, cualquier puerto de aplicación aparece atado a `127.0.0.1`, no a `0.0.0.0`.

### Señal de alarma

```text
0.0.0.0:3000
```

en la salida de `ss -lntp`. Ese puerto está expuesto a Internet, y UFW puede no estar deteniéndolo aunque su estado diga lo contrario.

Arréglalo cambiando la línea de `ports` y levantando de nuevo el contenedor. No confíes en que el firewall lo tape.

### 📸 SNAPSHOT S4 — "docker-installed"

### Checkpoint

```text
[ ] Docker está instalado desde el repositorio oficial.
[ ] hello-world corre.
[ ] docker compose version responde.
[ ] Entiendo por qué Docker puede saltarse UFW.
[ ] Sé escribir un puerto atado a 127.0.0.1.
[ ] Tengo el snapshot S4.
```

### Mini quiz

1. ¿Qué debería asustarte más en `ss -lntp`: `127.0.0.1:3000` o `0.0.0.0:3000`?
2. UFW dice que el 3000 está bloqueado, pero desde afuera se puede abrir. ¿Está roto UFW?
3. ¿Por qué atamos los puertos a `127.0.0.1` si ya tenemos firewall?

<details>
<summary>Ver respuestas</summary>

1. `0.0.0.0:3000`, porque significa que el servicio acepta conexiones desde cualquier interfaz de red del servidor.
2. No. Docker publicó ese puerto con sus propias reglas, y el tráfico pasa antes de llegar a donde UFW mira. Los dos funcionan, en niveles distintos.
3. Porque no queremos depender de una sola capa. Si el firewall falla o se configura mal, la app sigue sin ser alcanzable desde afuera porque ni siquiera está escuchando ahí.

</details>

---

## Sesión 15 — Dockerizar la app

### Idea

Ahora Docker sustituye una pieza concreta de tu mapa, y solo una:

```text
antes    Nginx → localhost:3000 → app corriendo con systemd
después  Nginx → localhost:3000 → app corriendo en un contenedor
```

Todo lo demás sigue igual. DNS, firewall, TLS, Nginx: nada de eso cambia. Docker no borra tu mapa, solo reemplaza el último tramo.

### Misión

**Paso 1 — Escribe el Dockerfile.**

```dockerfile
FROM node:22-alpine AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

FROM node:22-alpine AS build
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM node:22-alpine AS runtime
WORKDIR /app
ENV NODE_ENV=production
COPY --from=build /app ./
EXPOSE 3000
CMD ["npm", "start"]
```

Son tres etapas a propósito: la imagen final no carga con las herramientas de construcción, así que pesa mucho menos.

**Paso 2 — Escribe el Compose.**

```yaml
services:
  app:
    build:
      context: .
    restart: unless-stopped
    env_file:
      - .env
    ports:
      - "127.0.0.1:3000:3000"
```

Fíjate en el `127.0.0.1` de la sesión anterior.

**Paso 3 — Levanta.**

```bash
sudo docker compose up -d --build
sudo docker compose ps
```

**Paso 4 — Comprueba que el mapa sigue funcionando de punta a punta.**

```bash
curl -I http://127.0.0.1:3000
curl -I https://app.tudominio.com
```

### Salida sana

En `docker compose ps`, el servicio aparece como `Up` o `running`.

Y tu dominio sigue respondiendo `200`, exactamente igual que antes. Ese es el punto: cambiaste el motor y el resto del mapa ni se enteró.

### Señal de alarma

```text
Restarting (1) 5 seconds ago
```

El contenedor arranca y se muere en bucle.

Casi nunca es culpa de Docker. Mira los logs:

```bash
sudo docker compose logs --tail=100
```

Las causas más comunes:

```text
falta una variable de entorno
la base de datos no es alcanzable
el puerto interno no es el que creías
error en el código
el comando de arranque está mal
```

```text
exit code 137
```

Ese número significa que al proceso lo mataron por falta de memoria. En un servidor de 1 GB pasa seguido al construir imágenes. Es el motivo por el que en la semana 4 vamos a construir fuera del VPS.

### Checkpoint

```text
[ ] Mi app corre en un contenedor.
[ ] El puerto está atado a 127.0.0.1.
[ ] El dominio sigue respondiendo por HTTPS.
[ ] Sé leer docker compose logs.
[ ] Entiendo que solo cambió una capa del mapa.
```

### Mini quiz

1. El contenedor reinicia en bucle. ¿Culpas a Docker?
2. ¿Qué capas del mapa cambiaron al dockerizar?
3. ¿Qué significa `exit code 137`?

<details>
<summary>Ver respuestas</summary>

1. No, casi nunca. Docker está haciendo su trabajo: intenta levantarlo y algo lo mata. La causa está en los logs de la aplicación.
2. Solo la última, el runtime. DNS, firewall, TLS y Nginx quedaron exactamente igual.
3. Que el sistema mató el proceso por falta de memoria. En servidores pequeños suele pasar durante la construcción de la imagen.

</details>

---

## Fin de la semana 3

**Sábado:** recupera lo atrasado.

**Domingo:** descanso.

Deberías poder marcar:

```text
[x] Nivel 3 — Puedo servir una página por HTTP y HTTPS.
[x] Nivel 6 — Puedo empaquetarla con Docker.
```

---

# Semana 4 — Automatizar sin perder el mapa

Última semana. Automatizas el despliegue, practicas el día malo y cierras las cuentas.

---

## Sesión 16 — CI antes de CD

### Idea

Son dos preguntas distintas y conviene no mezclarlas mientras las aprendes:

```text
CI  ¿este cambio se construye y pasa sus pruebas?
CD  ¿y ahora cómo llega esa versión al servidor?
```

Hoy solo la primera. Un pipeline que despliega código roto es peor que no tener pipeline, porque ahora rompe producción automáticamente y más rápido.

### Misión

**Paso 1 — Crea el archivo del workflow.**

En tu repositorio, `.github/workflows/ci.yml`:

```yaml
name: CI

on:
  pull_request:
  push:
    branches:
      - main

permissions:
  contents: read

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: npm

      - run: npm ci
      - run: npm test
      - run: npm run build
```

**Paso 2 — Sobre esos números de versión.**

`@v4` es la versión mayor de la acción. Estos números avanzan cada cierto tiempo, y un curso escrito hoy queda viejo en unos meses.

No memorices el número. Aprende dónde verificarlo: cada acción tiene su página en el GitHub Marketplace donde dice cuál es la mayor actual. Antes de copiar un workflow de cualquier tutorial, incluido este, revisa ahí.

**Paso 3 — Haz un PR y mira correr el pipeline.**

Cambia algo pequeño, abre un pull request y observa la pestaña de Actions.

**Paso 4 — Rómpelo a propósito.**

Haz que una prueba falle y comprueba que el pipeline se pone en rojo y bloquea el merge. Un CI que nunca falla no te está protegiendo de nada.

### Salida sana

El job aparece en verde y el PR muestra que las comprobaciones pasaron.

### Señal de alarma

```text
npm ci can only install packages when your package.json and
package-lock.json are in sync
```

El archivo de bloqueo no coincide con las dependencias. Corre `npm install` localmente, haz commit del lock actualizado.

Y una señal de un tipo distinto: si tu pipeline pasa siempre, incluso cuando rompes cosas a propósito, es que no está ejecutando pruebas de verdad.

### Checkpoint

```text
[ ] Tengo un workflow de CI.
[ ] Corre al abrir un PR.
[ ] Verifiqué las versiones de las acciones en el Marketplace.
[ ] Lo hice fallar a propósito y se puso en rojo.
[ ] Sé la diferencia entre CI y CD.
```

### Mini quiz

1. ¿Qué pregunta responde CI y cuál responde CD?
2. ¿Por qué es mala idea desplegar sin CI?
3. Tu pipeline siempre pasa en verde. ¿Buena o mala señal?

<details>
<summary>Ver respuestas</summary>

1. CI pregunta si el cambio se construye y pasa sus pruebas. CD pregunta cómo esa versión llega al entorno.
2. Porque automatizas también los errores. Sin CI, un despliegue automático publica código roto más rápido de lo que podrías hacerlo a mano.
3. Sospechosa. Haz fallar algo a propósito. Si sigue en verde, las pruebas no se están ejecutando.

</details>

---

## Sesión 17 — Desplegar desde GitHub sin regalar las llaves

### Idea

Dos reglas para esta sesión.

La primera es de seguridad: **una clave privada nunca se guarda en el repositorio.** Va en los secrets de GitHub, que están cifrados y no aparecen en los logs.

La segunda es práctica y es propia de servidores pequeños: **no construyas la imagen dentro del VPS.**

Construir consume mucha memoria. En una máquina de 1 GB, un build de Node puede quedarse sin memoria y, de paso, tumbar la aplicación que está sirviendo a tus visitantes. Construyes en GitHub, que tiene máquinas de sobra, y el servidor solo baja el resultado ya hecho.

```text
mal    push → el VPS compila → el VPS sirve
bien   push → GitHub compila → el VPS solo descarga y arranca
```

### Misión

**Paso 1 — Crea los secrets en tu repositorio.**

```text
VPS_HOST
VPS_USER
VPS_SSH_KEY
VPS_KNOWN_HOSTS
```

**Paso 2 — Usa un entorno de producción.**

En GitHub, crea un `environment: production`. Te permite separar los secretos de producción y añadir controles, como requerir aprobación antes de desplegar.

**Paso 3 — El flujo correcto.**

```text
rama
→ PR
→ CI en verde
→ merge a main
→ construir la imagen en GitHub
→ publicarla al registro
→ el VPS la descarga
→ docker compose up
→ comprobación de salud
```

**Paso 4 — Guarda la versión, para poder volver atrás.**

Etiqueta cada imagen con el identificador del commit. Así, si algo sale mal, volver a la versión anterior es descargar otra etiqueta, no rehacer un despliegue completo.

### Salida sana

Después del merge, el despliegue termina y tu dominio responde `200` con la versión nueva.

Y esta comprobación en el servidor:

```bash
git rev-parse HEAD
```

coincide con el commit que acabas de mergear.

### Señal de alarma

```yaml
password: "mi-password-real"
```

Si encuentras algo así dentro de un workflow, deténte. Ese valor ya quedó en el historial del repositorio. No basta con borrarlo en el siguiente commit: hay que rotar la credencial, porque cualquiera con acceso al historial puede recuperarla.

```text
exit code 137
```

durante el build. Te quedaste sin memoria. Si estás construyendo dentro del VPS, esta es exactamente la razón por la que hay que sacar el build afuera.

### Checkpoint

```text
[ ] Los secretos están en GitHub, no en el repositorio.
[ ] Existe un environment de producción.
[ ] La imagen se construye fuera del VPS.
[ ] El VPS solo descarga y arranca.
[ ] Cada imagen está etiquetada con su commit.
[ ] Puedo volver a la versión anterior.
```

### Mini quiz

1. ¿Por qué no construir la imagen en el VPS?
2. Encuentras una contraseña dentro de un workflow. ¿Basta con borrarla en el siguiente commit?
3. ¿Para qué sirve etiquetar las imágenes con el commit?

<details>
<summary>Ver respuestas</summary>

1. Porque construir consume mucha memoria y puede tumbar la aplicación que está sirviendo en ese mismo servidor. GitHub tiene máquinas dedicadas para eso.
2. No. Ya quedó en el historial y se puede recuperar. Hay que rotar esa credencial, o sea generar una nueva y anular la vieja.
3. Para poder volver atrás rápido. Si la versión nueva falla, arrancas la etiqueta anterior en vez de rehacer todo el despliegue bajo presión.

</details>

---

## Sesión 18 — Vercel, VPS y Coolify: qué problema resuelve cada uno

### Idea

No son competidores. Son tres puntos distintos en una misma línea: cuánto trabajo operativo haces vos y cuánto lo hace otro.

Hoy no instalas nada. Hoy decides.

### Misión

**Paso 1 — Ubica quién hace qué.**

```text
VPS manual       vos administras Ubuntu, SSH, firewall, proxy,
                 TLS, runtime, deploy, logs y backups
                 → control total, y todo el trabajo es tuyo

Vercel           te da Git, previews, producción, dominio y TLS
                 administrados, muy cómodo para frontend
                 → menos control, casi nada de operación

Coolify          una capa tipo PaaS sobre infraestructura tuya
                 administra repos, builds, deploys, dominios,
                 proxy, certificados y variables
                 → punto intermedio, pero el VPS sigue debajo
```

La frase clave es la última. Si Coolify falla, el mapa que aprendiste este mes sigue siendo exactamente lo que necesitas para diagnosticarlo.

**Paso 2 — Mira los requisitos reales de Coolify antes de ilusionarte.**

```text
2 CPU
2 GB RAM
30 GB de espacio libre
```

Y tus aplicaciones necesitan recursos **además** de eso.

Esto tiene una consecuencia directa para tu laboratorio: el VPS pequeño con el que hiciste todo el curso es una excelente clase de Linux, pero está por debajo del mínimo de Coolify. No lo instales ahí y concluyas que Coolify es malo.

**Paso 3 — ¿Uno o dos servidores?**

```text
1 VPS                 aprender, portafolio, primeros proyectos
2º VPS de build       cuando compilar perjudica a producción
2+ VPS con balanceador cuando la disponibilidad justifica el costo
```

No empieces comprando dos por teoría. Empieza sabiendo operar uno.

**Paso 4 — Escribe tu decisión.**

En una frase, para tu propio proyecto: qué vas a usar y por qué. Guárdalo en tu cuaderno.

### Salida sana

No hay comando. La comprobación es que puedas responder, para tu caso concreto, qué te conviene y con qué argumento.

### Señal de alarma

Si tu respuesta es "Coolify porque es más fácil", falta la mitad. Más fácil, ¿a cambio de qué? ¿Qué pasa el día que Coolify no abra?

Si tu respuesta es "VPS manual porque es más profesional", también falta. Operar todo a mano cuesta tiempo real cada semana.

Las dos respuestas buenas incluyen un costo, no solo un beneficio.

### Checkpoint

```text
[ ] Sé qué administra cada opción.
[ ] Sé los requisitos mínimos de Coolify.
[ ] Sé por qué mi VPS de laboratorio no es buen host para Coolify.
[ ] Escribí mi decisión con su razón y su costo.
```

### Mini quiz

1. ¿Qué capa agrega Coolify y cuál no elimina?
2. ¿Por qué no instalar Coolify en el VPS del curso?
3. ¿Cuándo tiene sentido un segundo servidor solo para construir?

<details>
<summary>Ver respuestas</summary>

1. Agrega una capa de administración sobre tu infraestructura. No elimina el VPS de abajo: Ubuntu, red, disco y Docker siguen siendo tuyos y siguen pudiendo fallar.
2. Porque su mínimo documentado son 2 CPU y 2 GB, y el del curso es más pequeño. Correría mal y llegarías a una conclusión equivocada sobre la herramienta.
3. Cuando construir en la misma máquina que sirve a los usuarios empieza a degradar el servicio. Antes de eso, es complejidad y costo sin beneficio.

</details>

---

## Sesión 19 — El día malo, practicado en un día bueno

### Idea

Todo lo del curso apuntaba aquí.

La diferencia entre alguien que "tiene algo desplegado" y alguien que sabe operar no es cuántos comandos memorizó. Es qué hace en los primeros cinco minutos de una caída.

Y la respuesta correcta casi nunca es arreglar. Es **restaurar el servicio primero, investigar después.**

### Misión

### 📸 SNAPSHOT S5 — "antes-recovery-lab"

**Escenario A — No puedo entrar por SSH.**

No hace falta romperlo de verdad. Practica la secuencia mental y ejecuta cada comprobación desde la consola del proveedor:

```text
SSH no conecta
↓
¿la IP responde?
↓
¿el puerto 22 llega?
↓
¿ssh.socket y ssh.service están sanos?
↓
¿sshd_config valida?
↓
¿el firewall lo bloqueó?
```

Desde la consola de recuperación:

```bash
sudo sshd -t
sudo systemctl status ssh.socket
sudo systemctl status ssh.service
sudo ufw status verbose
sudo journalctl -u ssh -n 100 --no-pager
```

**Escenario B — Volver a un estado conocido.**

El orden importa:

```text
1. entrar por consola o rescue
2. revertir el último cambio
3. validar
4. recuperar SSH
5. investigar con calma
```

Fijate en que investigar es el paso cinco, no el uno.

**Escenario C — Restaurar un snapshot.**

Restaura uno de laboratorio, o crea un servidor nuevo a partir de él, según permita tu proveedor.

Después comprueba, en orden:

```text
¿arranca?
¿SSH funciona?
¿Nginx funciona?
¿la app está donde esperabas?
¿el certificado sigue válido?
```

**Escenario D — Provoca un 502 y cronométrate.**

Detén la app, abre el sitio y mide cuánto tardas en ubicar la capa. No en arreglar: en ubicar.

Repítelo hasta que sea menos de un minuto.

### Salida sana

Entras por la consola de recuperación sin buscar el botón.

Sabes qué comando corresponde a cada capa sin mirar el curso.

Ubicas la capa de un 502 en menos de un minuto.

### Señal de alarma

Si tu primer impulso ante una caída es reiniciar el servidor entero, para.

Reiniciar a veces arregla, pero borra la evidencia y no te enseña nada. La próxima vez que pase, vas a saber exactamente lo mismo que hoy.

Y si tu impulso es cambiar tres cosas a la vez, recordá la regla 5. Un cambio, una prueba.

### Snapshot no es backup

Un snapshot captura el disco en un punto del tiempo. Es perfecto para rebobinar un laboratorio.

Una estrategia real de datos tiene que pensar además en:

```text
base de datos
archivos de usuario
secretos
copias fuera del VPS
restauración probada de verdad
```

Un respaldo que nunca restauraste no es un respaldo. Es un archivo del que asumís cosas.

### Checkpoint

```text
[ ] Entré por la consola de recuperación sin ayuda.
[ ] Sé la secuencia de comprobación de SSH.
[ ] Restauré un snapshot y verifiqué que todo volvió.
[ ] Ubico la capa de un 502 en menos de un minuto.
[ ] Entiendo por qué restaurar va antes que investigar.
[ ] Tengo el snapshot S5.
```

### Mini quiz

1. Tu sitio está caído. ¿Cuál es la prioridad: entender por qué o restaurar el servicio?
2. ¿Por qué un snapshot no reemplaza un backup de datos?
3. ¿Por qué es mala idea reiniciar el servidor como primera reacción?

<details>
<summary>Ver respuestas</summary>

1. Restaurar. La investigación se hace después, con el servicio arriba y sin presión. Diagnosticar con el sitio caído lleva a decisiones apuradas.
2. Porque captura el disco de una máquina en un momento, pero no es una estrategia de datos. No cubre copias fuera del servidor ni te garantiza que la restauración funcione si nunca la probaste.
3. Porque a veces arregla el síntoma y siempre borra la evidencia. Si no sabés qué pasó, va a volver a pasar y vas a saber lo mismo que hoy.

</details>

---

## Sesión 20 — Capstone y cierre de cuentas

### Idea

Hay dos formas de terminar este curso.

Una es tener el sitio arriba. La otra es poder reconstruirlo desde cero siguiendo tu propia documentación, sin improvisar.

La segunda es la que cuenta. Y hoy además cerramos las cuentas, para que el laboratorio no te siga cobrando el resto del año.

### Misión

**Paso 1 — Escribe tu runbook.**

Con tus palabras, sin copiar del curso:

```text
1.  crear VPS Ubuntu 24.04
2.  comprobar consola y rescue
3.  actualizar el sistema
4.  crear el usuario deploy
5.  instalar la clave SSH
6.  validar con sshd -t y aplicar hardening
7.  configurar el firewall
8.  apuntar el DNS
9.  instalar Nginx
10. levantar la app
11. HTTPS con Certbot
12. systemd o Docker
13. deploy desde GitHub
14. comprobación de salud
15. prueba de recuperación
```

**Paso 2 — Contesta el examen final.**

Está al final de esta sesión, en el bloque de preguntas. Hazlo sin mirar el curso y antes de reconstruir nada.

**Paso 3 — La prueba de verdad.**

Destruye el laboratorio y reconstruilo siguiendo únicamente tu runbook.

Si en algún paso tuviste que volver al curso, ese paso está mal escrito en tu runbook. Corrígelo.

**Paso 4 — Cierra las cuentas.**

Esto es parte del curso, no un anexo. Decidí qué hacer con cada cosa:

```text
[ ] ¿Voy a conservar el VPS o destruirlo?
    Apagarlo no siempre deja de cobrar. Destruir sí.

[ ] Borrar los snapshots S0 a S5 que ya no necesite.
    Cobran mientras existan.

[ ] Revisar si el dominio tiene renovación automática activada.

[ ] Anotar la fecha de renovación del VPS y su precio real,
    no el promocional.

[ ] Guardar fuera del servidor: RECOVERY.md, el runbook
    y las claves SSH.

[ ] Revisar el estado de cuenta del proveedor y confirmar
    que no queda nada cobrando que no quiera.
```

Si decidís conservar el servidor, ya no es un laboratorio: es infraestructura tuya. Aplicá el checklist de producción que está más adelante en este documento.

### Salida sana

Reconstruiste el servidor siguiendo tu runbook, sin abrir el curso.

Contestaste las doce preguntas sin mirar.

Tu estado de cuenta muestra exactamente lo que esperabas que mostrara.

### Señal de alarma

Si al reconstruir tuviste que improvisar en algún paso, todavía no terminaste. No es un fracaso: es que encontraste el hueco exacto de tu documentación, que era justamente el objetivo del ejercicio.

### Checkpoint

```text
[ ] Tengo un runbook escrito con mis palabras.
[ ] Reconstruí el servidor usando solo mi runbook.
[ ] Contesté el examen sin mirar.
[ ] Cerré las cuentas y sé cuánto voy a pagar el mes que viene.
[ ] Guardé RECOVERY.md, el runbook y las claves fuera del servidor.
```

### Mini quiz

El examen final. Doce preguntas, sin mirar.

1. ¿Qué diferencia hay entre una IP y un puerto?
2. ¿Qué comprueba `dig`?
3. ¿Qué comprueba `ss -lntp`?
4. ¿Qué diferencia hay entre que UFW permita el 443 y que exista un servicio en el 443?
5. Si hay un 502, ¿qué compruebas antes: DNS o backend?
6. ¿Qué hace `nginx -t` y por qué se corre antes de recargar?
7. ¿Qué pregunta responde `systemctl status`?
8. ¿Qué pregunta responden los logs?
9. ¿Por qué `0.0.0.0:3000` puede ser peligroso?
10. ¿Por qué un snapshot no reemplaza un backup?
11. ¿Qué haces antes de tocar SSH?
12. ¿Qué capa agrega Coolify y cuál no elimina?

<details>
<summary>Ver respuestas</summary>

1. La IP identifica la máquina; el puerto identifica cuál servicio dentro de esa máquina. La dirección de un edificio y el número de apartamento.
2. Qué IP devuelve el DNS para un nombre. Solo eso: no dice si el servidor funciona.
3. Qué programas están escuchando ahora mismo, en qué puertos y en qué dirección.
4. UFW permitiendo el 443 es la puerta abierta. Un servicio en el 443 es alguien adentro que contesta. Puedes tener una sin la otra.
5. El backend. Para que salga un 502, la petición ya recorrió DNS, red y Nginx correctamente.
6. Comprueba que la configuración es válida. Se corre antes de recargar para no aplicar un archivo roto y dejar el sitio caído.
7. Si el servicio está vivo en este momento.
8. Qué dijo el programa antes de morirse. El status es el presente, los logs son el pasado.
9. Porque el servicio acepta conexiones desde cualquier interfaz de red, o sea desde Internet, en vez de solo desde la propia máquina.
10. Porque captura el disco de una máquina en un punto del tiempo, pero no cubre copias fuera del servidor ni te garantiza que la restauración funcione si nunca la probaste.
11. Snapshot, consola de recuperación probada, sesión anterior abierta y una segunda terminal para verificar antes de cerrar la primera.
12. Agrega una capa de administración sobre tu infraestructura. No elimina el VPS de abajo: Ubuntu, red, disco y Docker siguen siendo tuyos y siguen pudiendo fallar.

</details>

### Graduación

No "aprendiste VPS" porque instalaste todo.

Aprendiste el nivel inicial cuando puedes hacer esto, en este orden:

```text
observar
→ ubicar la capa
→ formular una hipótesis
→ comprobar una sola cosa
→ reparar
→ documentar
```

```text
[x] Nivel 7 — Puedo desplegar desde GitHub.
[x] Nivel 8 — Puedo diagnosticar una caída por capas.
[x] Nivel 9 — Puedo reconstruir el servidor desde cero.
```

---
# Las 12 tarjetas de avería

Úsalas sin mirar la respuesta.

## Tarjeta 1 — SSH hace timeout

**Frente**

```text
ssh deploy@IP
→ timeout
```

¿Capa?

<details>
<summary>Reverso</summary>

Empieza por red/firewall/puerto/servicio.

```bash
sudo ss -lntp | grep :22
sudo ufw status verbose
sudo systemctl status ssh.socket
```

Si no puedes entrar por SSH, usa la consola/rescue del proveedor.

</details>

---

## Tarjeta 2 — `Permission denied (publickey)`

**Frente**

¿Es lo mismo que timeout?

<details>
<summary>Reverso</summary>

No.

Llegaste a SSH, pero falló autenticación.

Desde tu PC:

```bash
ssh -vvv deploy@IP
```

En recuperación revisa:

```text
usuario
authorized_keys
propietario/permisos
configuración sshd
```

</details>

---

## Tarjeta 3 — El dominio no devuelve IP

<details>
<summary>Reverso</summary>

Capa DNS.

```bash
dig +short app.tudominio.com A
```

No pierdas tiempo reiniciando Docker.

</details>

---

## Tarjeta 4 — La IP abre, el dominio no

<details>
<summary>Reverso</summary>

Probablemente DNS o configuración `server_name`.

Primero:

```bash
dig +short app.tudominio.com
```

</details>

---

## Tarjeta 5 — Certbot no puede validar

<details>
<summary>Reverso</summary>

Para HTTP-01 comprueba:

```bash
dig +short app.tudominio.com
curl -I http://app.tudominio.com
sudo ufw status
```

El puerto 80 debe ser alcanzable durante la validación HTTP-01.

</details>

---

## Tarjeta 6 — 502 Bad Gateway

<details>
<summary>Reverso</summary>

El proxy respondió, pero no pudo obtener una respuesta adecuada del backend.

Primero:

```bash
curl -I http://127.0.0.1:3000
sudo ss -lntp | grep :3000
```

Luego app/systemd/Docker.

</details>

---

## Tarjeta 7 — 504 Gateway Timeout

<details>
<summary>Reverso</summary>

El proxy llega a esperar al backend, pero la respuesta tarda demasiado o no completa.

Revisa:

```text
logs Nginx
logs app
DB/dependencias
carga CPU
memoria
```

</details>

---

## Tarjeta 8 — El contenedor reinicia una y otra vez

<details>
<summary>Reverso</summary>

```bash
sudo docker compose ps
sudo docker compose logs --tail=200
```

Busca primero el error de la app.

</details>

---

## Tarjeta 9 — Disco lleno

<details>
<summary>Reverso</summary>

```bash
df -h
sudo du -xh /var | sort -h | tail
sudo docker system df
```

No ejecutes automáticamente:

```bash
docker system prune -a --volumes
```

Puedes borrar datos que sí importaban.

</details>

---

## Tarjeta 10 — “Desplegué, pero veo la versión vieja”

<details>
<summary>Reverso</summary>

Pregunta qué versión está realmente en producción.

```bash
git rev-parse HEAD
git log -1
```

Si usas imágenes, comprueba tag/digest/commit que desplegaste.

</details>

---

## Tarjeta 11 — UFW dice “deny”, pero un puerto Docker aparece accesible

<details>
<summary>Reverso</summary>

Docker administra sus propias reglas de firewall y el tráfico de puertos publicados puede saltarse la ruta que esperabas de UFW.

Revisa el `ports:` de Compose y liga servicios internos a loopback cuando corresponda:

```yaml
ports:
  - "127.0.0.1:3000:3000"
```

Usa también el firewall del proveedor como barrera externa.

</details>

---

## Tarjeta 12 — Coolify no abre

<details>
<summary>Reverso</summary>

No digas “Coolify está roto” todavía.

Recorre:

```text
DNS
→ firewall
→ 80/443
→ proxy
→ servicios/containers de Coolify
→ recursos del sistema
```

Comprueba también:

```bash
free -h
df -h
sudo docker ps
```

</details>

---

# Troubleshooting con salidas: aprender a leer, no solo a ejecutar

## `systemctl status`

### Sano

```text
Active: active (running)
```

### Malo

```text
Active: failed
```

Siguiente pregunta:

```text
¿por qué?
```

Comando:

```bash
journalctl -u NOMBRE -n 100 --no-pager
```

---

## `curl`

### Sano

```text
HTTP/1.1 200 OK
```

### Redirect normal posible

```text
HTTP/1.1 301 Moved Permanently
```

o:

```text
HTTP/2 301
```

No todo lo que no sea 200 es un fallo.

### Backend inexistente

```text
curl: (7) Failed to connect...
```

---

## `dig +short`

### Sano

```text
203.0.113.10
```

### Sospechoso

```text
<vacío>
```

o una IP que no es la tuya.

---

## `nginx -t`

### Sano

```text
syntax is ok
test is successful
```

### Malo

```text
nginx: [emerg] ...
test failed
```

No recargues Nginx hasta corregir.

---

## `ss -lntp`

### Buena señal para una app interna

```text
127.0.0.1:3000
```

### Señal que merece pregunta

```text
0.0.0.0:3000
```

No significa automáticamente vulnerabilidad, pero sí:

> El servicio está escuchando en interfaces externas. ¿Eso era intencional?

---

## `df -h`

### Sano

No hay un porcentaje universal perfecto, pero quieres margen.

Ejemplo:

```text
/dev/vda1  25G  8G  16G  34% /
```

### Riesgo

```text
/dev/vda1  25G  25G  0  100% /
```

Un disco al 100 % puede romper logs, builds, bases de datos y servicios.

---

## `free -h`

No interpretes “poca memoria free” como desastre sin mirar `available`.

Linux utiliza RAM como caché.

Mira especialmente:

```text
available
swap
procesos que crecen
OOM en logs
```

---

# Fail2Ban: decisión consciente, no casilla automática

Fail2Ban observa logs y puede bloquear temporalmente IPs que realizan intentos repetidos.

Es útil en ciertos escenarios.

Pero el curso no lo trata como sustituto de:

```text
claves SSH
contraseñas SSH desactivadas
root SSH desactivado
firewall
actualizaciones
```

Con SSH por llave, instalar Fail2Ban es una defensa adicional contra ruido/abuso, no el pilar de autenticación.

Si lo quieres como laboratorio:

```bash
sudo apt install fail2ban
sudo systemctl status fail2ban
```

Antes de copiar una configuración de Internet, entiende qué jail estás activando y qué log está leyendo.

---

# El protocolo anti‑bloqueo SSH

Imprime mentalmente esta secuencia:

```text
ANTES
[ ] recovery/rescue probado
[ ] snapshot reciente
[ ] Terminal A abierta
[ ] clave de deploy funciona
[ ] firewall permite SSH

CAMBIO
[ ] editar snippet
[ ] sshd -t

PRUEBA
[ ] reiniciar/reload apropiado
[ ] Terminal B conecta
[ ] sudo funciona

DESPUÉS
[ ] recién ahora cierro Terminal A
```

Para cambio de `Port` en Ubuntu 24.04:

```text
[ ] añadir el puerto nuevo al firewall ANTES
[ ] sshd -t
[ ] systemctl daemon-reload
[ ] systemctl restart ssh.socket
[ ] probar puerto nuevo en Terminal B
[ ] retirar puerto anterior solo después
```

---

# El protocolo de snapshots del curso

Nombres sugeridos:

```text
S0-fresh-ubuntu
S1-before-ssh-hardening
S2-nginx-http-ok
S3-https-ok
S4-docker-installed
S5-before-recovery-lab
```

Cuándo crear uno:

```text
cambio de acceso remoto
cambio de firewall importante
instalación de plataforma que toca muchas piezas
práctica deliberadamente destructiva
```

Cuándo NO confiar solo en uno:

```text
base de datos crítica
archivos de usuario
secretos
copias de largo plazo
recuperación entre proveedores
```

---

# Tu tablero de 4 semanas

| Semana | Lunes | Martes | Miércoles | Jueves | Viernes | Fin de semana |
|---|---|---|---|---|---|---|
| 1 | Terminal | VPS + recovery | SSH + usuario | Claves + hardening | Firewall | Recuperar / descansar |
| 2 | DNS | Nginx | App local | systemd | Proxy + 502 | Recuperar / descansar |
| 3 | HTTPS | Git | Conceptos Docker | Instalar Docker | Compose | Recuperar / descansar |
| 4 | CI | Deploy GitHub | Vercel/Coolify | Recovery real | Capstone | Libre |

No hay “día perdido”.

Si una sesión se complica:

```text
muévela al sábado
```

Si dos se complican:

```text
quita Coolify del capstone
```

El objetivo del mes es dominar el VPS manual.

Coolify es bonus.

---

# Cuaderno de evidencias

Crea una carpeta local:

```text
curso-vps/
├── 00-mapa.md
├── 01-comandos.md
├── 02-recovery.md
├── 03-dns.md
├── 04-nginx.md
├── 05-docker.md
├── 06-incidentes.md
└── 07-runbook-final.md
```

En cada sesión registra solo:

```text
Qué intenté:
Qué esperaba:
Qué ocurrió:
Qué comando confirmó la causa:
Qué arregló el problema:
Qué aprendí:
```

Eso vale más que pegar 500 líneas de terminal.

---

# Checklist de producción inicial

Antes de llamar “producción” a una app:

```text
[ ] Ubuntu soportado y actualizado
[ ] usuario normal con sudo
[ ] acceso por clave
[ ] login root SSH desactivado
[ ] contraseña SSH desactivada después de probar claves
[ ] recovery/rescue conocido
[ ] firewall proveedor configurado
[ ] UFW revisado
[ ] puertos públicos intencionales
[ ] app interna no expuesta innecesariamente
[ ] DB no pública
[ ] DNS correcto
[ ] HTTPS válido
[ ] renovación de certificado probada
[ ] secretos fuera de Git
[ ] deploy reproducible
[ ] logs revisables
[ ] almacenamiento con margen
[ ] backup de datos
[ ] restauración probada
[ ] runbook de recuperación
```

---

# Comandos de bolsillo

## Identidad

```bash
whoami
hostname
pwd
```

## Sistema

```bash
cat /etc/os-release
uptime
free -h
df -h
```

## Red

```bash
ip addr
ip route
sudo ss -lntp
```

## DNS

```bash
dig +short app.tudominio.com A
dig +short app.tudominio.com AAAA
```

## HTTP

```bash
curl -I http://app.tudominio.com
curl -Iv https://app.tudominio.com
curl -I http://127.0.0.1:3000
```

## Nginx

```bash
sudo nginx -t
sudo systemctl status nginx --no-pager
sudo journalctl -u nginx -n 100 --no-pager
```

## App systemd

```bash
sudo systemctl status miapp --no-pager
sudo journalctl -u miapp -n 100 --no-pager
```

## Docker

```bash
sudo docker compose ps
sudo docker compose logs --tail=200
sudo docker system df
```

## SSH

```bash
sudo sshd -t
sudo systemctl status ssh.socket
sudo systemctl status ssh.service
sudo journalctl -u ssh -n 100 --no-pager
```

## Firewall

```bash
sudo ufw status verbose
```

---

# Referencias con URL

Estas son fuentes para consultar cuando el curso te envíe al manual o necesites confirmar comportamiento actual.

## Ubuntu

- Ubuntu 24.04 LTS release notes  
  https://documentation.ubuntu.com/release-notes/24.04/

- Ubuntu Server — OpenSSH  
  https://ubuntu.com/server/docs/how-to/security/openssh-server/

- Ubuntu Server — Firewall / UFW  
  https://documentation.ubuntu.com/server/how-to/security/firewalls/

- Ubuntu Security — automatic security updates  
  https://documentation.ubuntu.com/security/security-updates/

## Docker

- Install Docker Engine on Ubuntu  
  https://docs.docker.com/engine/install/ubuntu/

- Packet filtering and firewalls  
  https://docs.docker.com/engine/network/packet-filtering-firewalls/

- Port publishing  
  https://docs.docker.com/engine/network/port-publishing/

- Linux post-installation  
  https://docs.docker.com/engine/install/linux-postinstall/

## Nginx, TLS y Certbot

- Nginx proxy module  
  https://nginx.org/en/docs/http/ngx_http_proxy_module.html

- Let's Encrypt — Challenge Types  
  https://letsencrypt.org/docs/challenge-types/

- Certbot instructions  
  https://certbot.eff.org/instructions

## GitHub

- GitHub Actions secrets  
  https://docs.github.com/en/actions/concepts/security/secrets

- Using secrets in Actions  
  https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets

- Deployment environments  
  https://docs.github.com/en/actions/concepts/workflows-and-actions/deployment-environments

- GITHUB_TOKEN  
  https://docs.github.com/en/actions/concepts/security/github_token

- Publishing Docker images  
  https://docs.github.com/en/actions/tutorials/publish-packages/publish-docker-images

## Vercel

- Git deployments  
  https://vercel.com/docs/git

- Domains  
  https://vercel.com/docs/domains

- SSL certificates  
  https://vercel.com/docs/domains/working-with-ssl

- Rollback production deployment  
  https://vercel.com/docs/deployments/rollback-production-deployment

## Coolify

- Start with self-hosted / requirements  
  https://next.coolify.io/docs/start-with-self-hosted

- Firewall  
  https://next.coolify.io/docs/core/infrastructure/servers/firewall

- GitHub preview deploys  
  https://next.coolify.io/docs/applications/deployments/preview-deployments

## Recuperación y snapshots: ejemplos de proveedor

- DigitalOcean Recovery Console  
  https://docs.digitalocean.com/products/droplets/how-to/recovery/recovery-console/

- DigitalOcean snapshots — crear/restaurar  
  https://docs.digitalocean.com/products/snapshots/how-to/create-and-restore-droplets/

- Hetzner Rescue System  
  https://docs.hetzner.com/cloud/servers/getting-started/rescue-system/

- Hetzner Backups/Snapshots overview  
  https://docs.hetzner.com/cloud/servers/backups-snapshots/overview/

## Fail2Ban

- Ubuntu manpage — Fail2Ban  
  https://manpages.ubuntu.com/manpages/noble/man1/fail2ban.1.html

---

# Última página

El error más peligroso de un principiante no es escribir un comando incorrecto.

Es no saber **qué capa acaba de modificar**.

Por eso, cuando algo falle, vuelve siempre al mapa:

```text
DNS
↓
red
↓
TLS
↓
proxy
↓
app
↓
runtime
↓
Ubuntu
↓
VPS
```

No necesitas saberlo todo.

Necesitas saber cuál es la siguiente pregunta.
