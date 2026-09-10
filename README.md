# VPS desde cero absoluto

Plataforma estática y autocontenida para estudiar **VPS desde cero absoluto** sin framework, backend ni CDN. Vercel ejecuta `python3 build/construir.py` y publica el directorio `public/`.

## Fuente del curso y regeneración

La fuente canónica del contenido debe versionarse como `contenido/CURSO_VPS_v3.md` y su parser como `build/parse_curso.py`. La cadena completa prevista es:

```bash
python3 build/parse_curso.py contenido/CURSO_VPS_v3.md datos/curso.json
python3 build/construir.py
```

**Importante:** si esos dos archivos no están presentes en tu checkout, el despliegue todavía puede construirse desde el fallback `datos/curso_partes/`, pero el repositorio no puede regenerar los datos desde el Markdown original. No consideres completa la fuente del proyecto hasta que ambos archivos estén versionados.

Actualmente `datos/curso.json` puede estar dividido en `datos/curso_partes/curso.01.part` a `curso.06.part` por límites de transporte. `build/construir.py` concatena las partes en orden lexicográfico y después valida 20 sesiones, 101 checkpoints y 71 preguntas. No renombres las partes ni elimines una: una parte ausente rompe el reensamblado. Este mecanismo es un fallback de transporte, no la fuente canónica.

## Construir y abrir localmente

```bash
python3 build/construir.py
```

Después abre `public/index.html`. Ese archivo es **generado** y no se versiona para evitar que un HTML obsoleto contradiga al build actual.

## Progreso y perfiles

La persistencia ya está implementada con `localStorage`: sesión/bloque, checkpoints, quizzes, estado del VPS, Modo Avería, tarjetas, bitácora, recuperación, runbook y cierre final.

El progreso local y el de `https://curso-pro-vps.vercel.app` pertenecen a orígenes distintos. **Exportar/importar** es el puente entre navegadores u orígenes.

Al importar una copia hay dos opciones:

- **Abrir como otra persona**: crea un perfil aislado y conserva tu progreso principal. Es la opción indicada para revisar el avance de un amigo.
- **Reemplazar este perfil**: sustituye el perfil activo y guarda una copia para poder deshacer el último reemplazo.

Los perfiles funcionan sin backend: la aplicación conserva snapshots separados en `localStorage` y cambia temporalmente el conjunto activo para que todas las herramientas existentes funcionen igual dentro de cada perfil.

## Estructura relevante

```text
build/
  app.js          lector y progreso
  averia.js       Modo Avería, buscador y tarjetas
  fase5.js        bitácora, snapshots, recuperación y exportación
  fase6.js        cierre final, robustez y accesibilidad
  perfiles.js     perfiles aislados e importación segura
  construir.py    genera el HTML autocontenido
  plantilla.html  shell HTML/CSS

datos/
  curso_partes/   fallback del curso serializado
  instala.json
  reglas.json
  riel.json

public/
  index.html      generado por el build; ignorado por Git
```

El build de Vercel usa Python 3; esto ya quedó verificado por deployments reales del proyecto.
