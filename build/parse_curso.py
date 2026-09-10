#!/usr/bin/env python3
"""
parse_curso.py
Convierte CURSO_VPS_v3.md en curso.json, la estructura que lee la plataforma HTML.

Uso:  python3 parse_curso.py CURSO_VPS_v3.md curso.json

No inventa contenido. Si algo no calza con el formato esperado, lo reporta y
sale con codigo 1. El markdown es la fuente de verdad.
"""

import json
import re
import sys
from pathlib import Path

BLOQUES_CANONICOS = [
    ("idea", "Idea"),
    ("mision", "Misión"),
    ("salidaSana", "Salida sana"),
    ("senalAlarma", "Señal de alarma"),
    ("checkpoint", "Checkpoint"),
    ("miniQuiz", "Mini quiz"),
]

RE_SESION = re.compile(r"^## Sesión (\d+) — (.+)$", re.M)
RE_SEMANA = re.compile(r"^# Semana (\d+) — (.+)$", re.M)
RE_TARJETA = re.compile(r"^## Tarjeta (\d+) — (.+)$", re.M)
RE_SNAPSHOT = re.compile(r'^### 📸 SNAPSHOT (S\d) — "(.+)"$', re.M)
RE_H3 = re.compile(r"^### (.+)$", re.M)
RE_CHECK = re.compile(r"^\[ \] (.+)$", re.M)
RE_DETAILS = re.compile(r"<details>\s*\n<summary>(.*?)</summary>\s*\n(.*?)\n</details>", re.S)
RE_NUMERADO = re.compile(r"^(\d+)\. (.+?)(?=\n\d+\. |\n\n|\Z)", re.M | re.S)
RE_FENCE = re.compile(r"```(\w*)\n(.*?)```", re.S)

errores = []


def err(msg):
    errores.append(msg)


def slug(texto):
    t = texto.lower()
    reemplazos = {"á": "a", "é": "e", "í": "i", "ó": "o", "ú": "u", "ñ": "n", "ü": "u"}
    for k, v in reemplazos.items():
        t = t.replace(k, v)
    t = re.sub(r"[^a-z0-9]+", "-", t)
    return t.strip("-")


def cortar(texto, inicio, patron_fin):
    """Devuelve el trozo desde inicio hasta el siguiente match de patron_fin."""
    m = patron_fin.search(texto, inicio)
    return texto[inicio : m.start()] if m else texto[inicio:]


def limpiar(bloque):
    return bloque.strip().strip("-").strip()


def parse_checkpoint(cuerpo):
    """El checkpoint es un bloque ```text con lineas '[ ] cosa'."""
    items = []
    for _, contenido in RE_FENCE.findall(cuerpo):
        items.extend(RE_CHECK.findall(contenido))
    if not items:
        items = RE_CHECK.findall(cuerpo)
    return [i.strip() for i in items]


def parse_quiz(cuerpo):
    """Preguntas numeradas antes del <details>, respuestas numeradas adentro."""
    m = RE_DETAILS.search(cuerpo)
    antes = cuerpo[: m.start()] if m else cuerpo
    preguntas = [t.strip() for _, t in RE_NUMERADO.findall(antes)]
    respuestas = []
    if m:
        respuestas = [t.strip() for _, t in RE_NUMERADO.findall(m.group(2))]
    pares = []
    for i, p in enumerate(preguntas):
        pares.append({"pregunta": p, "respuesta": respuestas[i] if i < len(respuestas) else None})
    return pares


def parse_sesion(num, titulo, cuerpo):
    """Divide el cuerpo de una sesion en sus H3."""
    posiciones = [(m.start(), m.end(), m.group(1).strip()) for m in RE_H3.finditer(cuerpo)]
    trozos = []
    for i, (ini, fin, encabezado) in enumerate(posiciones):
        siguiente = posiciones[i + 1][0] if i + 1 < len(posiciones) else len(cuerpo)
        trozos.append((encabezado, cuerpo[fin:siguiente]))

    bloques = {}
    extras = []
    snapshot = None

    for encabezado, contenido in trozos:
        ms = RE_SNAPSHOT.match("### " + encabezado)
        if ms:
            snapshot = {"id": ms.group(1), "nombre": ms.group(2)}
            continue
        canonico = next((k for k, etiqueta in BLOQUES_CANONICOS if encabezado == etiqueta), None)
        if canonico:
            bloques[canonico] = limpiar(contenido)
        else:
            extras.append({"titulo": encabezado, "md": limpiar(contenido)})

    faltan = [etiqueta for k, etiqueta in BLOQUES_CANONICOS if k not in bloques]
    if faltan:
        err(f"Sesión {num} le faltan bloques: {faltan}")

    return {
        "num": num,
        "id": f"s{num:02d}",
        "titulo": titulo.strip(),
        "slug": slug(titulo),
        "idea": bloques.get("idea", ""),
        "mision": bloques.get("mision", ""),
        "salidaSana": bloques.get("salidaSana", ""),
        "senalAlarma": bloques.get("senalAlarma", ""),
        "checkpoint": parse_checkpoint(bloques.get("checkpoint", "")),
        "miniQuiz": parse_quiz(bloques.get("miniQuiz", "")),
        "extras": extras,
        "snapshot": snapshot,
    }


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)

    origen, destino = Path(sys.argv[1]), Path(sys.argv[2])
    md = origen.read_text(encoding="utf-8")

    # --- semanas -----------------------------------------------------------
    semanas = []
    for m in RE_SEMANA.finditer(md):
        semanas.append({"num": int(m.group(1)), "titulo": m.group(2).strip(), "pos": m.start()})

    def semana_de(pos):
        actual = None
        for s in semanas:
            if s["pos"] < pos:
                actual = s["num"]
        return actual

    # --- sesiones ----------------------------------------------------------
    sesiones = []
    marcas = list(RE_SESION.finditer(md))
    for i, m in enumerate(marcas):
        fin = marcas[i + 1].start() if i + 1 < len(marcas) else len(md)
        cuerpo = md[m.end() : fin]
        # cortar en el siguiente H1 o en 'Fin de la semana'
        corte = re.search(r"^(# |## Fin de la semana)", cuerpo, re.M)
        if corte:
            cuerpo = cuerpo[: corte.start()]
        s = parse_sesion(int(m.group(1)), m.group(2), cuerpo)
        s["semana"] = semana_de(m.start())
        sesiones.append(s)

    # --- niveles -----------------------------------------------------------
    bloque_niveles = re.search(r"# Tu barra de progreso.*?```text\n(.*?)```", md, re.S)
    niveles = []
    if bloque_niveles:
        for linea in RE_CHECK.findall(bloque_niveles.group(1)):
            mm = re.match(r"Nivel (\d+) — (.+)", linea)
            if mm:
                niveles.append({"num": int(mm.group(1)), "texto": mm.group(2).strip()})

    # --- piezas del mapa ---------------------------------------------------
    piezas = []
    bloque_mapa = re.search(r"# Mapa de las doce piezas.*?(?=\n# )", md, re.S)
    if bloque_mapa:
        for fila in re.findall(r"^\| \[(.+?)\]\(#(.+?)\) \| (.+?) \| (.+?) \| (.+?) \|$",
                               bloque_mapa.group(0), re.M):
            piezas.append({
                "nombre": fila[0],
                "ancla": fila[1],
                "hace": fila[2].strip(),
                "vive": fila[3].strip(),
                "comprobacion": fila[4].strip(),
            })

    # --- capitulo 0 --------------------------------------------------------
    cap0 = []
    bloque_cap0 = re.search(r"# Capítulo 0 — .*?(?=\n# Tu primera prueba)", md, re.S)
    if bloque_cap0:
        texto = bloque_cap0.group(0)
        marcas0 = list(re.finditer(r"^## (\d+)\. (.+)$", texto, re.M))
        for i, m in enumerate(marcas0):
            fin = marcas0[i + 1].start() if i + 1 < len(marcas0) else len(texto)
            cap0.append({
                "num": int(m.group(1)),
                "nombre": m.group(2).strip(),
                "md": limpiar(texto[m.end() : fin]),
            })

    # --- tarjetas de averia ------------------------------------------------
    tarjetas = []
    marcas_t = list(RE_TARJETA.finditer(md))
    for i, m in enumerate(marcas_t):
        fin = marcas_t[i + 1].start() if i + 1 < len(marcas_t) else len(md)
        cuerpo = md[m.end() : fin]
        corte = re.search(r"^# ", cuerpo, re.M)
        if corte:
            cuerpo = cuerpo[: corte.start()]
        d = RE_DETAILS.search(cuerpo)
        tarjetas.append({
            "num": int(m.group(1)),
            "id": f"t{int(m.group(1)):02d}",
            "sintoma": m.group(2).strip(),
            "reverso": limpiar(d.group(2)) if d else "",
        })
        if not d:
            err(f"Tarjeta {m.group(1)} no tiene reverso")

    # --- snapshots ---------------------------------------------------------
    snapshots = []
    for s in sesiones:
        if s["snapshot"]:
            snapshots.append({
                "id": s["snapshot"]["id"],
                "nombre": s["snapshot"]["nombre"],
                "sesion": s["num"],
            })

    # --- referencias -------------------------------------------------------
    referencias = []
    bloque_ref = re.search(r"# Referencias con URL.*?(?=\n# Última página)", md, re.S)
    if bloque_ref:
        # Formato real:  "- Título del recurso" y en la línea siguiente la URL cruda.
        seccion = None
        lineas = bloque_ref.group(0).split("\n")
        for i, linea in enumerate(lineas):
            if linea.startswith("## "):
                seccion = linea[3:].strip()
                continue
            if linea.startswith("- ") and i + 1 < len(lineas):
                siguiente = lineas[i + 1].strip()
                if siguiente.startswith("http"):
                    referencias.append({
                        "seccion": seccion,
                        "texto": linea[2:].strip(),
                        "url": siguiente,
                    })
        if not referencias:
            err("No se extrajo ninguna referencia")

    datos = {
        "meta": {
            "titulo": "VPS desde cero absoluto",
            "totalSesiones": len(sesiones),
            "totalSemanas": len(semanas),
            "generadoDesde": origen.name,
        },
        "semanas": [{"num": s["num"], "titulo": s["titulo"]} for s in semanas],
        "niveles": niveles,
        "piezas": piezas,
        "capitulo0": cap0,
        "sesiones": sesiones,
        "snapshots": snapshots,
        "tarjetas": tarjetas,
        "referencias": referencias,
    }

    # --- validacion --------------------------------------------------------
    if len(sesiones) != 20:
        err(f"Se esperaban 20 sesiones, se encontraron {len(sesiones)}")
    if len(tarjetas) != 12:
        err(f"Se esperaban 12 tarjetas, se encontraron {len(tarjetas)}")
    if len(snapshots) != 6:
        err(f"Se esperaban 6 snapshots, se encontraron {len(snapshots)}")
    if len(piezas) != 12:
        err(f"Se esperaban 12 piezas, se encontraron {len(piezas)}")
    if len(cap0) != 12:
        err(f"Se esperaban 12 conceptos en el capítulo 0, se encontraron {len(cap0)}")
    for s in sesiones:
        if not s["checkpoint"]:
            err(f"Sesión {s['num']} tiene checkpoint vacío")
        if not s["miniQuiz"]:
            err(f"Sesión {s['num']} tiene quiz vacío")
        for i, q in enumerate(s["miniQuiz"], 1):
            if q["respuesta"] is None:
                err(f"Sesión {s['num']} pregunta {i} sin respuesta")

    if errores:
        print("PARSER FALLÓ:")
        for e in errores:
            print("  -", e)
        sys.exit(1)

    destino.write_text(json.dumps(datos, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"OK  {destino}")
    print(f"    {len(sesiones)} sesiones, {len(semanas)} semanas, {len(niveles)} niveles")
    print(f"    {len(piezas)} piezas, {len(cap0)} conceptos, {len(snapshots)} snapshots")
    print(f"    {len(tarjetas)} tarjetas, {len(referencias)} referencias")
    print(f"    {sum(len(s['checkpoint']) for s in sesiones)} casillas de checkpoint")
    print(f"    {sum(len(s['miniQuiz']) for s in sesiones)} preguntas de quiz")


if __name__ == "__main__":
    main()
