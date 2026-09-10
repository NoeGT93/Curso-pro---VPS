#!/usr/bin/env python3
from __future__ import annotations
import json,re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TEXTOS=ROOT/'datos'/'textos.json'
JS=[ROOT/'build'/n for n in ('app.js','averia.js','fase5.js','fase6.js','perfiles.js')]
TPL=ROOT/'build'/'plantilla.html'
BUILD=ROOT/'build'/'construir.py'
MARK_RE=re.compile(r'__T:([A-Za-z0-9_.-]+)__')
ACC=re.compile(r'[áéíóúñüÁÉÍÓÚÑÜ¿¡]')


def flatten(x,p=''):
    out={}
    if isinstance(x,dict):
        for k,v in x.items():
            if str(k).startswith('_'): continue
            q=f'{p}.{k}' if p else k
            out.update(flatten(v,q))
    elif isinstance(x,str): out[p]=x
    return out

def marker(k): return f'__T:{k}__'

def plain_candidate(s):
    q=s.strip()
    if not q or '__T:' in q or not re.search(r'[A-Za-zÁÉÍÓÚÑÜáéíóúñü¿¡]',q): return False
    if re.search(r'https?://|^[#.[/]|[{};=]|\\[nrt]|^\w+[-_:]\w+$',q): return False
    if q in {'true','false','null','undefined','object','boolean','string','number','open','active','main','text','bash','html','ini','nginx','yaml','dockerfile','es-ES','GET','POST'}: return False
    if ACC.search(q): return True
    if re.search(r'\s',q): return True
    if q[:1].isupper() and re.fullmatch(r'[A-Za-z]+',q): return True
    return False

def html_visible_transform(s,ensure):
    def attr(m):
        before,val,after=m.group(1),m.group(2),m.group(3)
        if plain_candidate(val): val=marker(ensure(val))
        return before+val+after
    s=re.sub(r'((?:aria-label|title|placeholder|alt)=["\'])(.*?)(["\'])',attr,s,flags=re.S)
    def node(m):
        val=m.group(1)
        lead=val[:len(val)-len(val.lstrip())]; trail=val[len(val.rstrip()):]
        core=val.strip()
        if plain_candidate(core): return '>'+lead+marker(ensure(core))+trail+'<'
        return m.group(0)
    return re.sub(r'>([^<>]+)<',node,s)

def transform_js(src,filekey,data):
    flat=flatten(data); rev={v:k for k,v in flat.items()}
    ren=data.get('_renombres',{})
    counter=0
    def ensure(value):
        nonlocal counter,flat,rev
        value=ren.get(value,value)
        if value in rev:return rev[value]
        counter+=1;k=f'_extra.{filekey}.{counter:03d}'
        data.setdefault('_extra',{}).setdefault(filekey,{})[f'{counter:03d}']=value
        flat[k]=value;rev[value]=k
        return k
    # Renombres obligatorios primero.
    for old,new in sorted(((k,v) for k,v in ren.items() if not k.startswith('_')),key=lambda x:len(x[0]),reverse=True):
        if old in src: src=src.replace(old,marker(ensure(new)))
    # Copia ya definida en textos.json.
    for k,v in sorted(flatten(data).items(),key=lambda kv:len(kv[1]),reverse=True):
        if len(v)>=2 and v in src: src=src.replace(v,marker(k))
    # Strings simples.
    str_re=re.compile(r'(["\'])(?P<body>(?:\\.|(?!\1).)*?)\1',re.S)
    def qs(m):
        quote=m.group(1); body=m.group('body')
        if '__T:' in body:return m.group(0)
        if '<' in body and '>' in body:
            nb=html_visible_transform(body,ensure)
            return quote+nb+quote
        if plain_candidate(body): return quote+marker(ensure(body))+quote
        return m.group(0)
    src=str_re.sub(qs,src)
    # Templates: texto visible HTML y fragmentos estáticos alrededor de ${...}.
    temp_re=re.compile(r'`((?:\\.|[^`])*)`',re.S)
    def qt(m):
        body=m.group(1)
        body=html_visible_transform(body,ensure)
        parts=re.split(r'(\$\{[^{}]*\})',body)
        for i,p in enumerate(parts):
            if p.startswith('${') or '__T:' in p: continue
            lead=p[:len(p)-len(p.lstrip())];trail=p[len(p.rstrip()):];core=p.strip()
            # No convertir trozos que son principalmente marcado HTML.
            if core and '<' not in core and '>' not in core and plain_candidate(core):
                parts[i]=lead+marker(ensure(core))+trail
        return '`'+''.join(parts)+'`'
    src=temp_re.sub(qt,src)
    return src

def transform_html(src,data):
    flat=flatten(data);rev={v:k for k,v in flat.items()};ren=data.get('_renombres',{});counter=0
    def ensure(value):
        nonlocal counter
        value=ren.get(value,value)
        if value in rev:return rev[value]
        counter+=1;k=f'_extra.plantilla.{counter:03d}'
        data.setdefault('_extra',{}).setdefault('plantilla',{})[f'{counter:03d}']=value
        rev[value]=k;return k
    for old,new in sorted(((k,v) for k,v in ren.items() if not k.startswith('_')),key=lambda x:len(x[0]),reverse=True):
        src=src.replace(old,marker(ensure(new)))
    for k,v in sorted(flatten(data).items(),key=lambda kv:len(kv[1]),reverse=True):
        if len(v)>=2:src=src.replace(v,marker(k))
    # No tocar CSS ni scripts; solo texto/atributos del HTML estructural.
    chunks=re.split(r'(<style[\s\S]*?</style>|<script[\s\S]*?</script>)',src,flags=re.I)
    for i,ch in enumerate(chunks):
        if re.match(r'<(?:style|script)',ch,re.I): continue
        chunks[i]=html_visible_transform(ch,ensure)
    return ''.join(chunks)

def write_build():
    BUILD.write_text('''#!/usr/bin/env python3\n"""Genera public/index.html autocontenido desde plantilla, aplicaciones y datos validados."""\nfrom __future__ import annotations\nimport html,json,re\nfrom pathlib import Path\nROOT=Path(__file__).resolve().parent.parent\nPLANTILLA=ROOT/'build'/'plantilla.html'; APP=ROOT/'build'/'app.js'; AVERIA=ROOT/'build'/'averia.js'; FASE5=ROOT/'build'/'fase5.js'; FASE6=ROOT/'build'/'fase6.js'; PERFILES=ROOT/'build'/'perfiles.js'; SALIDA=ROOT/'public'/'index.html'\nCURSO=ROOT/'datos'/'curso.json'; PARTES=ROOT/'datos'/'curso_partes'; TEXTOS=ROOT/'datos'/'textos.json'\ndef compactar(x): return json.dumps(x,ensure_ascii=False,separators=(',',':')).replace('</','<\\\\/')\ndef archivo(p): return compactar(json.loads(p.read_text(encoding='utf-8')))\ndef curso():\n    if CURSO.exists(): data=json.loads(CURSO.read_text(encoding='utf-8'))\n    else:\n        ps=sorted(PARTES.glob('curso.*.part'))\n        if len(ps)!=6: raise SystemExit(f'Curso incompleto: se esperaban 6 partes y hay {len(ps)}')\n        try:data=json.loads(''.join(p.read_text(encoding='utf-8') for p in ps))\n        except json.JSONDecodeError as e:raise SystemExit(f'No se pudo reensamblar el curso: {e}') from e\n    assert len(data.get('sesiones',[]))==20, 'Se esperaban 20 sesiones'\n    assert sum(len(s.get('checkpoint',[])) for s in data['sesiones'])==101, 'Se esperaban 101 checkpoints'\n    assert sum(len(s.get('miniQuiz',[])) for s in data['sesiones'])==71, 'Se esperaban 71 preguntas'\n    return compactar(data)\ndef plano(x,p=''):\n    r={}\n    if isinstance(x,dict):\n        for k,v in x.items():\n            if str(k).startswith('_'):continue\n            q=f'{p}.{k}' if p else k;r.update(plano(v,q))\n    elif isinstance(x,str):r[p]=x\n    return r\ndef cargar_textos():return json.loads(TEXTOS.read_text(encoding='utf-8'))\ndef js_escape(s):\n    return ''.join(('\\\\n' if c=='\\n' else '\\\\r' if c=='\\r' else '\\\\t' if c=='\\t' else f'\\\\u{ord(c):04x}' if ord(c)>126 or c in '\\\\"\\\'`$' else c) for c in s)\ndef resolver(src,textos,modo):\n    flat=plano(textos)\n    def sub(m):\n        k=m.group(1)\n        if k not in flat:raise SystemExit(f'Falta texto {k}')\n        return html.escape(flat[k],quote=True) if modo=='html' else js_escape(flat[k])\n    out=re.sub(r'__T:([A-Za-z0-9_.-]+)__',sub,src)\n    if '__T:' in out:raise SystemExit('Quedaron referencias de texto sin resolver')\n    return out\ndef js(p,textos):return resolver(p.read_text(encoding='utf-8'),textos,'js').replace('</script>','<\\\\/script>')\ndef main():\n    textos=cargar_textos();html_src=PLANTILLA.read_text(encoding='utf-8')\n    html=resolver(html_src,textos,'html')\n    rep={'__CURSO_JSON__':curso(),'__REGLAS_JSON__':archivo(ROOT/'datos'/'reglas.json'),'__INSTALA_JSON__':archivo(ROOT/'datos'/'instala.json'),'__RIEL_JSON__':archivo(ROOT/'datos'/'riel.json'),'__TEXTOS_JSON__':compactar(textos),'__APP_JS__':js(APP,textos)}\n    for k,v in rep.items():\n        if k not in html:raise SystemExit(f'Falta marcador {k}')\n        html=html.replace(k,v)\n    extra=''.join('<script>'+js(p,textos)+'</script>' for p in (AVERIA,FASE5,FASE6,PERFILES))\n    if '</body>' not in html:raise SystemExit('La plantilla no contiene </body>')\n    html=html.replace('</body>',extra+'</body>',1)\n    SALIDA.parent.mkdir(parents=True,exist_ok=True);SALIDA.write_text(html,encoding='utf-8');print(f'OK {SALIDA} ({SALIDA.stat().st_size/1024:.1f} KB)')\nif __name__=='__main__':main()\n''',encoding='utf-8')

def ensure_textos_marker(src):
    if '__TEXTOS_JSON__' in src:return src
    tag='<script id="textosData" type="application/json">__TEXTOS_JSON__</script>'
    pos=src.find('<script id="cursoData"')
    if pos<0: raise SystemExit('No encuentro cursoData en plantilla.html')
    return src[:pos]+tag+'\n'+src[pos:]

def audit(data):
    forbidden=[k for k in data.get('_renombres',{}) if not k.startswith('_')]
    bad=[]; accents=0
    for p in JS:
        s=p.read_text(encoding='utf-8')
        accents+=len(ACC.findall(s))
        for old in forbidden:
            if old in s:bad.append(f'{p.name}: renombre prohibido: {old}')
        # Candidatos residuales en strings: reporte conservador.
        for m in re.finditer(r'(["\'])(?P<b>(?:\\.|(?!\1).)*?)\1',s,re.S):
            if plain_candidate(m.group('b')) and '__T:' not in m.group('b') and '<' not in m.group('b'):
                bad.append(f'{p.name}: copia residual: {m.group("b")[:80]}')
    print(f'AUDIT_ACCENTS={accents}')
    print(f'AUDIT_RESIDUAL={len(bad)}')
    for x in bad[:80]:print('  '+x)
    if accents or bad:raise SystemExit('Auditoría de copia no pasó')


def main():
    data=json.loads(TEXTOS.read_text(encoding='utf-8'))
    for p in JS:
        p.write_text(transform_js(p.read_text(encoding='utf-8'),p.stem,data),encoding='utf-8')
    tpl=ensure_textos_marker(TPL.read_text(encoding='utf-8'))
    TPL.write_text(transform_html(tpl,data),encoding='utf-8')
    TEXTOS.write_text(json.dumps(data,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
    write_build()
    audit(data)
    print('FASE_A_OK')

if __name__=='__main__':main()
