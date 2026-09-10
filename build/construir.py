#!/usr/bin/env python3
"""Genera public/index.html a partir de la plantilla y los datos validados.

No edites public/index.html a mano. Toda modificación de interfaz debe hacerse en
build/plantilla.html y todo cambio de contenido en contenido/CURSO_VPS_v3.md.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLANTILLA = ROOT / "build" / "plantilla.html"
SALIDA = ROOT / "public" / "index.html"
FUENTES = {
    "__CURSO_JSON__": ROOT / "datos" / "curso.json",
    "__REGLAS_JSON__": ROOT / "datos" / "reglas.json",
    "__INSTALA_JSON__": ROOT / "datos" / "instala.json",
    "__RIEL_JSON__": ROOT / "datos" / "riel.json",
}


def cargar_json(path: Path) -> str:
    data = json.loads(path.read_text(encoding="utf-8"))
    # Evita que una cadena con </script> cierre el bloque de datos incrustado.
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def main() -> None:
    html = PLANTILLA.read_text(encoding="utf-8")
    for marcador, path in FUENTES.items():
        if marcador not in html:
            raise SystemExit(f"Falta marcador {marcador} en {PLANTILLA}")
        html = html.replace(marcador, cargar_json(path))

    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(html, encoding="utf-8")
    print(f"OK  {SALIDA}")
    print(f"    {SALIDA.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
