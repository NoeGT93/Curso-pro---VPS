# VPS desde cero absoluto

Plataforma estática y autocontenida para estudiar el curso **VPS desde cero absoluto** sin depender de Internet. El contenido vive en `contenido/CURSO_VPS_v3.md`; `public/index.html` es un archivo generado y **no debe editarse a mano**. Para regenerar los datos: `python3 build/parse_curso.py contenido/CURSO_VPS_v3.md datos/curso.json`. Para regenerar la web: `python3 build/construir.py`. Vercel sirve directamente el directorio `public/`.

> Nota: cuando se implemente persistencia, el avance guardado al abrir el HTML localmente y el guardado en el sitio publicado serán almacenamientos distintos porque pertenecen a orígenes distintos. Exportar/importar será el puente entre ambos.
