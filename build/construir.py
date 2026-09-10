#!/usr/bin/env python3
"""Genera public/index.html autocontenido desde plantilla, aplicaciones y datos validados."""
from __future__ import annotations
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
PLANTILLA=ROOT/'build'/'plantilla.html'; APP=ROOT/'build'/'app.js'; AVERIA=ROOT/'build'/'averia.js'; FASE5=ROOT/'build'/'fase5.js'; FASE6=ROOT/'build'/'fase6.js'; PERFILES=ROOT/'build'/'perfiles.js'; SALIDA=ROOT/'public'/'index.html'
CURSO=ROOT/'datos'/'curso.json'; PARTES=ROOT/'datos'/'curso_partes'
def compactar(x): return json.dumps(x,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
def archivo(p): return compactar(json.loads(p.read_text(encoding='utf-8')))
def curso():
    if CURSO.exists(): data=json.loads(CURSO.read_text(encoding='utf-8'))
    else:
        ps=sorted(PARTES.glob('curso.*.part'))
        if not ps: raise SystemExit('Faltan los datos del curso')
        try: data=json.loads(''.join(p.read_text(encoding='utf-8') for p in ps))
        except json.JSONDecodeError as e: raise SystemExit(f'No se pudo reensamblar datos/curso_partes ({len(ps)} partes): {e}') from e
    assert len(data.get('sesiones',[]))==20, 'Se esperaban 20 sesiones'
    assert sum(len(s.get('checkpoint',[])) for s in data['sesiones'])==101, 'Se esperaban 101 checkpoints'
    assert sum(len(s.get('miniQuiz',[])) for s in data['sesiones'])==71, 'Se esperaban 71 preguntas'
    return compactar(data)
def js(p): return p.read_text(encoding='utf-8').replace('</script>','<\\/script>')
def main():
    html=PLANTILLA.read_text(encoding='utf-8')
    rep={'__CURSO_JSON__':curso(),'__REGLAS_JSON__':archivo(ROOT/'datos'/'reglas.json'),'__INSTALA_JSON__':archivo(ROOT/'datos'/'instala.json'),'__RIEL_JSON__':archivo(ROOT/'datos'/'riel.json'),'__APP_JS__':js(APP)}
    for k,v in rep.items():
        if k not in html: raise SystemExit(f'Falta marcador {k}')
        html=html.replace(k,v)
    extra=''.join('<script>'+js(p)+'</script>' for p in (AVERIA,FASE5,FASE6,PERFILES))
    if '</body>' not in html: raise SystemExit('La plantilla no contiene </body>')
    html=html.replace('</body>',extra+'</body>',1)
    SALIDA.parent.mkdir(parents=True,exist_ok=True); SALIDA.write_text(html,encoding='utf-8'); print(f'OK {SALIDA} ({SALIDA.stat().st_size/1024:.1f} KB)')
if __name__=='__main__': main()
