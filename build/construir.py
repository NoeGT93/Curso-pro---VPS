#!/usr/bin/env python3
"""Genera public/index.html desde la plantilla y los datos validados.

En el repositorio, curso.json puede almacenarse en partes de texto para evitar
límites de transporte. Durante el build se reconstruye en memoria y el HTML final
sigue siendo un único archivo autocontenido.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PLANTILLA = ROOT / "build" / "plantilla.html"
SALIDA = ROOT / "public" / "index.html"
CURSO = ROOT / "datos" / "curso.json"
CURSO_PARTES = ROOT / "datos" / "curso_partes"


def compactar(data: object) -> str:
    return json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def cargar_archivo(path: Path) -> str:
    return compactar(json.loads(path.read_text(encoding="utf-8")))


def cargar_curso() -> str:
    if CURSO.exists():
        data = json.loads(CURSO.read_text(encoding="utf-8"))
    else:
        partes = sorted(CURSO_PARTES.glob("curso.*.part"))
        if not partes:
            raise SystemExit("No existe datos/curso.json ni datos/curso_partes/curso.*.part")
        texto = "".join(p.read_text(encoding="utf-8") for p in partes)
        data = json.loads(texto)
    if len(data.get("sesiones", [])) != 20:
        raise SystemExit("Curso inválido: se esperaban 20 sesiones")
    if sum(len(s.get("checkpoint", [])) for s in data["sesiones"]) != 101:
        raise SystemExit("Curso inválido: se esperaban 101 checkpoints")
    if sum(len(s.get("miniQuiz", [])) for s in data["sesiones"]) != 71:
        raise SystemExit("Curso inválido: se esperaban 71 preguntas")
    return compactar(data)


def main() -> None:
    html = PLANTILLA.read_text(encoding="utf-8")
    reemplazos = {
        "__CURSO_JSON__": cargar_curso(),
        "__REGLAS_JSON__": cargar_archivo(ROOT / "datos" / "reglas.json"),
        "__INSTALA_JSON__": cargar_archivo(ROOT / "datos" / "instala.json"),
        "__RIEL_JSON__": cargar_archivo(ROOT / "datos" / "riel.json"),
    }
    for marcador, valor in reemplazos.items():
        if marcador not in html:
            raise SystemExit(f"Falta marcador {marcador} en {PLANTILLA}")
        html = html.replace(marcador, valor)
    SALIDA.parent.mkdir(parents=True, exist_ok=True)
    SALIDA.write_text(html, encoding="utf-8")
    print(f"OK  {SALIDA}")
    print(f"    {SALIDA.stat().st_size / 1024:.1f} KB")


if __name__ == "__main__":
    main()
