#!/usr/bin/env python3
"""Genera public/index.html autocontenido desde plantilla, aplicaciones y datos validados."""
from __future__ import annotations
import html as html_lib
import json
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
PLANTILLA=ROOT/'build'/'plantilla.html'; APP=ROOT/'build'/'app.js'; ENTRADA=ROOT/'build'/'entrada.js'; AVERIA=ROOT/'build'/'averia.js'; FASE5=ROOT/'build'/'fase5.js'; FASE6=ROOT/'build'/'fase6.js'; PERFILES=ROOT/'build'/'perfiles.js'; SALIDA=ROOT/'public'/'index.html'
CURSO=ROOT/'datos'/'curso.json'; PARTES=ROOT/'datos'/'curso_partes'; TEXTOS=ROOT/'datos'/'textos.json'
RE_TEXTO=re.compile(r'__T:([A-Za-z0-9_.-]+)__')

def compactar(x): return json.dumps(x,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
def archivo(p): return compactar(json.loads(p.read_text(encoding='utf-8')))

def curso():
    if CURSO.exists(): data=json.loads(CURSO.read_text(encoding='utf-8'))
    else:
        ps=sorted(PARTES.glob('curso.*.part'))
        if len(ps)!=6: raise SystemExit(f'Curso incompleto: se esperaban 6 partes y hay {len(ps)}')
        try: data=json.loads(''.join(p.read_text(encoding='utf-8') for p in ps))
        except json.JSONDecodeError as e: raise SystemExit(f'No se pudo reensamblar datos/curso_partes ({len(ps)} partes): {e}') from e
    assert len(data.get('sesiones',[]))==20, 'Se esperaban 20 sesiones'
    assert sum(len(s.get('checkpoint',[])) for s in data['sesiones'])==101, 'Se esperaban 101 checkpoints'
    assert sum(len(s.get('miniQuiz',[])) for s in data['sesiones'])==71, 'Se esperaban 71 preguntas'
    return compactar(data)

def plano(x,prefijo=''):
    out={}
    if isinstance(x,dict):
        for k,v in x.items():
            if str(k).startswith('_'): continue
            clave=f'{prefijo}.{k}' if prefijo else str(k)
            out.update(plano(v,clave))
    elif isinstance(x,str): out[prefijo]=x
    return out

def js_escape(texto):
    out=[]
    for c in texto:
        n=ord(c)
        if c=='\n': out.append('\\n')
        elif c=='\r': out.append('\\r')
        elif c=='\t': out.append('\\t')
        elif n<32 or n>126 or c in "\\'\"`$": out.append(f'\\u{{{n:x}}}')
        else: out.append(c)
    return ''.join(out)

def resolver(src,textos,modo):
    flat=plano(textos)
    def repl(m):
        clave=m.group(1)
        if clave not in flat: raise SystemExit(f'Falta texto de interfaz: {clave}')
        valor=flat[clave]
        return html_lib.escape(valor,quote=True) if modo=='html' else js_escape(valor)
    resultado=RE_TEXTO.sub(repl,src)
    if '__T:' in resultado: raise SystemExit('Quedaron referencias de texto sin resolver')
    return resultado

def js(p,textos):
    return resolver(p.read_text(encoding='utf-8'),textos,'js').replace('</script>','<\\/script>')

def main():
    textos=json.loads(TEXTOS.read_text(encoding='utf-8'))
    html=resolver(PLANTILLA.read_text(encoding='utf-8'),textos,'html')
    rep={
        '__CURSO_JSON__':curso(),
        '__REGLAS_JSON__':archivo(ROOT/'datos'/'reglas.json'),
        '__INSTALA_JSON__':archivo(ROOT/'datos'/'instala.json'),
        '__RIEL_JSON__':archivo(ROOT/'datos'/'riel.json'),
        '__TEXTOS_JSON__':compactar(textos),
        '__APP_JS__':js(APP,textos),
    }
    for k,v in rep.items():
        if k not in html: raise SystemExit(f'Falta marcador {k}')
        html=html.replace(k,v)
    extra=''.join('<script>'+js(p,textos)+'</script>' for p in (ENTRADA,AVERIA,FASE5,FASE6,PERFILES))
    if '</body>' not in html: raise SystemExit('La plantilla no contiene </body>')
    html=html.replace('</body>',extra+'</body>',1)
    SALIDA.parent.mkdir(parents=True,exist_ok=True)
    SALIDA.write_text(html,encoding='utf-8')
    print(f'OK {SALIDA} ({SALIDA.stat().st_size/1024:.1f} KB)')

if __name__=='__main__': main()
