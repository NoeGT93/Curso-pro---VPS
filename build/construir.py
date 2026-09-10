#!/usr/bin/env python3
"""Genera y valida public/index.html autocontenido desde plantilla, módulos y datos."""
from __future__ import annotations
import json
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
PLANTILLA=ROOT/'build'/'plantilla.html'; APP=ROOT/'build'/'app.js'; AVERIA=ROOT/'build'/'averia.js'; FASE5=ROOT/'build'/'fase5.js'; FASE6=ROOT/'build'/'fase6.js'; SALIDA=ROOT/'public'/'index.html'
CURSO=ROOT/'datos'/'curso.json'; PARTES=ROOT/'datos'/'curso_partes'
def compactar(x): return json.dumps(x,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
def archivo(p): return compactar(json.loads(p.read_text(encoding='utf-8')))
def curso():
    if CURSO.exists(): data=json.loads(CURSO.read_text(encoding='utf-8'))
    else:
        ps=sorted(PARTES.glob('curso.*.part'))
        if not ps: raise SystemExit('Faltan los datos del curso')
        data=json.loads(''.join(p.read_text(encoding='utf-8') for p in ps))
    assert len(data.get('sesiones',[]))==20, 'Se esperaban 20 sesiones'
    assert sum(len(s.get('checkpoint',[])) for s in data['sesiones'])==101, 'Se esperaban 101 checkpoints'
    assert sum(len(s.get('miniQuiz',[])) for s in data['sesiones'])==71, 'Se esperaban 71 preguntas'
    assert len(data.get('snapshots',[]))==6, 'Se esperaban 6 snapshots'
    assert len(data.get('tarjetas',[]))==12, 'Se esperaban 12 tarjetas'
    return compactar(data)
def js(p): return p.read_text(encoding='utf-8').replace('</script>','<\\/script>')
def validar_html(html):
    marcadores=re.findall(r'__[A-Z0-9_]+__',html)
    if marcadores: raise SystemExit('Quedaron marcadores sin sustituir: '+', '.join(sorted(set(marcadores))))
    if re.search(r'<script\b[^>]*\bsrc\s*=',html,re.I): raise SystemExit('La salida contiene JavaScript externo')
    if re.search(r'<link\b[^>]*rel=["\']?stylesheet[^>]*href=["\']?https?://',html,re.I): raise SystemExit('La salida contiene una hoja de estilo externa')
    for token in ('cursoVpsEstadoV3','cursoVpsAveriaV1','cursoVpsBitacoraV1','cursoVpsFase6V1'):
        if token not in html: raise SystemExit(f'Falta módulo/estado esperado: {token}')
    if '<html lang="es">' not in html: raise SystemExit('Falta lang=es')
def main():
    html=PLANTILLA.read_text(encoding='utf-8')
    rep={'__CURSO_JSON__':curso(),'__REGLAS_JSON__':archivo(ROOT/'datos'/'reglas.json'),'__INSTALA_JSON__':archivo(ROOT/'datos'/'instala.json'),'__RIEL_JSON__':archivo(ROOT/'datos'/'riel.json'),'__APP_JS__':js(APP)}
    for k,v in rep.items():
        if k not in html: raise SystemExit(f'Falta marcador {k}')
        html=html.replace(k,v)
    extra=''.join('<script>'+js(p)+'</script>' for p in (AVERIA,FASE5,FASE6))
    if '</body>' not in html: raise SystemExit('La plantilla no contiene </body>')
    html=html.replace('</body>',extra+'</body>',1)
    validar_html(html)
    SALIDA.parent.mkdir(parents=True,exist_ok=True); SALIDA.write_text(html,encoding='utf-8'); print(f'OK {SALIDA} ({SALIDA.stat().st_size/1024:.1f} KB)')
if __name__=='__main__': main()
