#!/usr/bin/env python3
from __future__ import annotations
import json,re,unicodedata
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
TEXTOS=ROOT/'datos'/'textos.json'
JS=[ROOT/'build'/n for n in ('app.js','averia.js','fase5.js','fase6.js','perfiles.js')]
TPL=ROOT/'build'/'plantilla.html'
BUILD=ROOT/'build'/'construir.py'
ACC=re.compile(r'[áéíóúñüÁÉÍÓÚÑÜ¿¡]')


def flatten(x,p=''):
    out={}
    if isinstance(x,dict):
        for k,v in x.items():
            if str(k).startswith('_') and k!='_renombres':
                continue
            if k=='_renombres':
                continue
            q=f'{p}.{k}' if p else k
            out.update(flatten(v,q))
    elif isinstance(x,str):
        out[p]=x
    return out

def marker(k): return f'__T:{k}__'

def obvious_code(q):
    if re.search(r'https?://',q): return True
    if q.startswith(('#','.','/','[','{')) and not re.search(r'\s',q): return True
    if re.fullmatch(r'[A-Za-z0-9_.:/#@-]+',q) and q[:1].islower(): return True
    if (';' in q and ':' in q) or re.search(r'^[A-Za-z-]+\s*:',q): return True
    return False

def plain_candidate(s):
    q=s.strip()
    if not q or '__T:' in q or not re.search(r'[A-Za-zÁÉÍÓÚÑÜáéíóúñü¿¡]',q): return False
    if obvious_code(q): return False
    if q in {'true','false','null','undefined','object','boolean','string','number','open','active','main','text','bash','html','ini','nginx','yaml','dockerfile','es-ES','GET','POST'}: return False
    if ACC.search(q): return True
    if re.search(r'\s',q): return True
    if q[:1].isupper() and re.fullmatch(r'[A-Za-z]+',q): return True
    return False

def split_tags(s):
    return re.split(r'(<[^>]*>)',s)

def transform_static(s,ensure):
    parts=split_tags(s)
    for i,p in enumerate(parts):
        if not p: continue
        if p.startswith('<') and p.endswith('>'):
            def ar(m):
                pre,val,post=m.group(1),m.group(2),m.group(3)
                return pre+(marker(ensure(val)) if plain_candidate(val) else val)+post
            parts[i]=re.sub(r'((?:aria-label|title|placeholder|alt)=["\'])(.*?)(["\'])',ar,p,flags=re.S)
        else:
            lead=p[:len(p)-len(p.lstrip())];trail=p[len(p.rstrip()):];core=p.strip()
            if plain_candidate(core): parts[i]=lead+marker(ensure(core))+trail
    return ''.join(parts)

def find_quote_end(src,start,quote):
    i=start+1
    while i<len(src):
        c=src[i]
        if c=='\\': i+=2;continue
        if c==quote:return i
        i+=1
    return len(src)-1

def find_expr_end(body,start):
    depth=1;i=start
    while i<len(body):
        c=body[i]
        if c=='\\':i+=2;continue
        if c in "'\"`":
            j=find_quote_end(body,i,c);i=j+1;continue
        if c=='{':depth+=1
        elif c=='}':
            depth-=1
            if depth==0:return i
        i+=1
    return len(body)-1

def transform_template_body(body,ensure):
    # No tocar hojas de estilo incrustadas.
    if body.count('{')>=3 and ';' in body and ':' in body and '<' not in body:
        return body
    out=[];i=0;last=0
    while i<len(body)-1:
        if body[i]=='$' and body[i+1]=='{' and (i==0 or body[i-1]!='\\'):
            out.append(transform_static(body[last:i],ensure))
            end=find_expr_end(body,i+2)
            out.append(body[i:end+1]);i=end+1;last=i
        else:i+=1
    out.append(transform_static(body[last:],ensure))
    return ''.join(out)

def transform_quoted(src,ensure):
    out=[];i=0;last=0
    while i<len(src):
        q=src[i]
        if q not in "'\"`":i+=1;continue
        # Saltar comillas que forman parte de comentarios no es necesario: solo
        # se transforma si el contenido parece copia humana.
        end=find_quote_end(src,i,q)
        body=src[i+1:end]
        new=transform_template_body(body,ensure) if q=='`' else transform_static(body,ensure)
        out.append(src[last:i+1]);out.append(new);out.append(q)
        i=end+1;last=i
    out.append(src[last:])
    return ''.join(out)

def deaccent_comments(src):
    def norm(s):return ''.join(c for c in unicodedata.normalize('NFKD',s) if not unicodedata.combining(c)).replace('¿','').replace('¡','')
    lines=[]
    for line in src.splitlines(True):
        p=line.find('//')
        if p>=0 and ACC.search(line[p:]):line=line[:p]+norm(line[p:])
        lines.append(line)
    return ''.join(lines)

def transform_js(src,filekey,data):
    flat=flatten(data);rev={v:k for k,v in flat.items()};ren=data.get('_renombres',{});counter=0
    def ensure(value):
        nonlocal counter
        value=ren.get(value,value)
        if value in rev:return rev[value]
        counter+=1;k=f'extra.{filekey}.{counter:03d}'
        data.setdefault('extra',{}).setdefault(filekey,{})[f'{counter:03d}']=value
        rev[value]=k
        return k
    # Primero los renombres obligatorios; luego toda copia ya canónica.
    for old,new in sorted(((k,v) for k,v in ren.items() if not k.startswith('_')),key=lambda x:len(x[0]),reverse=True):
        src=src.replace(old,marker(ensure(new)))
    for k,v in sorted(flatten(data).items(),key=lambda kv:len(kv[1]),reverse=True):
        if len(v)>=2:src=src.replace(v,marker(k))
    src=transform_quoted(src,ensure)
    return deaccent_comments(src)

def transform_html(src,data):
    flat=flatten(data);rev={v:k for k,v in flat.items()};ren=data.get('_renombres',{});counter=0
    def ensure(value):
        nonlocal counter
        value=ren.get(value,value)
        if value in rev:return rev[value]
        counter+=1;k=f'extra.plantilla.{counter:03d}'
        data.setdefault('extra',{}).setdefault('plantilla',{})[f'{counter:03d}']=value
        rev[value]=k;return k
    for old,new in sorted(((k,v) for k,v in ren.items() if not k.startswith('_')),key=lambda x:len(x[0]),reverse=True):src=src.replace(old,marker(ensure(new)))
    for k,v in sorted(flatten(data).items(),key=lambda kv:len(kv[1]),reverse=True):
        if len(v)>=2:src=src.replace(v,marker(k))
    chunks=re.split(r'(<style[\s\S]*?</style>|<script[\s\S]*?</script>)',src,flags=re.I)
    for i,ch in enumerate(chunks):
        if re.match(r'<(?:style|script)',ch,re.I):continue
        chunks[i]=transform_static(ch,ensure)
    return ''.join(chunks)

def write_build():
    BUILD.write_text('''#!/usr/bin/env python3\n"""Genera public/index.html autocontenido desde plantilla, aplicaciones y datos validados."""\nfrom __future__ import annotations\nimport html,json,re\nfrom pathlib import Path\nROOT=Path(__file__).resolve().parent.parent\nPLANTILLA=ROOT/'build'/'plantilla.html'; APP=ROOT/'build'/'app.js'; AVERIA=ROOT/'build'/'averia.js'; FASE5=ROOT/'build'/'fase5.js'; FASE6=ROOT/'build'/'fase6.js'; PERFILES=ROOT/'build'/'perfiles.js'; SALIDA=ROOT/'public'/'index.html'\nCURSO=ROOT/'datos'/'curso.json'; PARTES=ROOT/'datos'/'curso_partes'; TEXTOS=ROOT/'datos'/'textos.json'\ndef compactar(x): return json.dumps(x,ensure_ascii=False,separators=(',',':')).replace('</','<\\\\/')\ndef archivo(p): return compactar(json.loads(p.read_text(encoding='utf-8')))\ndef curso():\n    if CURSO.exists(): data=json.loads(CURSO.read_text(encoding='utf-8'))\n    else:\n        ps=sorted(PARTES.glob('curso.*.part'))\n        if len(ps)!=6: raise SystemExit(f'Curso incompleto: se esperaban 6 partes y hay {len(ps)}')\n        try:data=json.loads(''.join(p.read_text(encoding='utf-8') for p in ps))\n        except json.JSONDecodeError as e:raise SystemExit(f'No se pudo reensamblar el curso: {e}') from e\n    assert len(data.get('sesiones',[]))==20, 'Se esperaban 20 sesiones'\n    assert sum(len(s.get('checkpoint',[])) for s in data['sesiones'])==101, 'Se esperaban 101 checkpoints'\n    assert sum(len(s.get('miniQuiz',[])) for s in data['sesiones'])==71, 'Se esperaban 71 preguntas'\n    return compactar(data)\ndef plano(x,p=''):\n    r={}\n    if isinstance(x,dict):\n        for k,v in x.items():\n            if str(k).startswith('_'):continue\n            q=f'{p}.{k}' if p else k;r.update(plano(v,q))\n    elif isinstance(x,str):r[p]=x\n    return r\ndef cargar_textos():return json.loads(TEXTOS.read_text(encoding='utf-8'))\ndef js_escape(s):\n    safe=[]\n    for c in s:\n        if c=='\\n':safe.append('\\\\n')\n        elif c=='\\r':safe.append('\\\\r')\n        elif c=='\\t':safe.append('\\\\t')\n        elif ord(c)>126 or c in '\\\\"\\\'`$':safe.append(f'\\\\u{ord(c):04x}')\n        else:safe.append(c)\n    return ''.join(safe)\ndef resolver(src,textos,modo):\n    flat=plano(textos)\n    def sub(m):\n        k=m.group(1)\n        if k not in flat:raise SystemExit(f'Falta texto {k}')\n        return html.escape(flat[k],quote=True) if modo=='html' else js_escape(flat[k])\n    out=re.sub(r'__T:([A-Za-z0-9_.-]+)__',sub,src)\n    if '__T:' in out:raise SystemExit('Quedaron referencias de texto sin resolver')\n    return out\ndef js(p,textos):return resolver(p.read_text(encoding='utf-8'),textos,'js').replace('</script>','<\\\\/script>')\ndef main():\n    textos=cargar_textos();html_src=PLANTILLA.read_text(encoding='utf-8');html=resolver(html_src,textos,'html')\n    rep={'__CURSO_JSON__':curso(),'__REGLAS_JSON__':archivo(ROOT/'datos'/'reglas.json'),'__INSTALA_JSON__':archivo(ROOT/'datos'/'instala.json'),'__RIEL_JSON__':archivo(ROOT/'datos'/'riel.json'),'__TEXTOS_JSON__':compactar(textos),'__APP_JS__':js(APP,textos)}\n    for k,v in rep.items():\n        if k not in html:raise SystemExit(f'Falta marcador {k}')\n        html=html.replace(k,v)\n    extra=''.join('<script>'+js(p,textos)+'</script>' for p in (AVERIA,FASE5,FASE6,PERFILES))\n    if '</body>' not in html:raise SystemExit('La plantilla no contiene </body>')\n    html=html.replace('</body>',extra+'</body>',1)\n    SALIDA.parent.mkdir(parents=True,exist_ok=True);SALIDA.write_text(html,encoding='utf-8');print(f'OK {SALIDA} ({SALIDA.stat().st_size/1024:.1f} KB)')\nif __name__=='__main__':main()\n''',encoding='utf-8')

def ensure_textos_marker(src):
    if '__TEXTOS_JSON__' in src:return src
    tag='<script id="textosData" type="application/json">__TEXTOS_JSON__</script>'
    pos=src.find('<script id="cursoData"')
    if pos<0:raise SystemExit('No encuentro cursoData en plantilla.html')
    return src[:pos]+tag+'\n'+src[pos:]

def audit(data):
    forbidden=[k for k in data.get('_renombres',{}) if not k.startswith('_')]
    bad=[];accents=0
    for p in JS:
        s=p.read_text(encoding='utf-8');accents+=len(ACC.findall(s))
        for old in forbidden:
            if old in s:bad.append(f'{p.name}: renombre prohibido: {old}')
        # Segunda pasada lineal: cualquier string humano sin marcador queda reportado.
        i=0
        while i<len(s):
            q=s[i]
            if q not in "'\"`":i+=1;continue
            end=find_quote_end(s,i,q);body=s[i+1:end]
            if q!='`' and plain_candidate(body) and '__T:' not in body and '<' not in body:bad.append(f'{p.name}: copia residual: {body[:80]}')
            i=end+1
    print(f'AUDIT_ACCENTS={accents}')
    print(f'AUDIT_RESIDUAL={len(bad)}')
    for x in bad[:80]:print('  '+x)
    if accents or bad:raise SystemExit('Auditoría de copia no pasó')

def main():
    data=json.loads(TEXTOS.read_text(encoding='utf-8'))
    for p in JS:p.write_text(transform_js(p.read_text(encoding='utf-8'),p.stem,data),encoding='utf-8')
    tpl=ensure_textos_marker(TPL.read_text(encoding='utf-8'));TPL.write_text(transform_html(tpl,data),encoding='utf-8')
    TEXTOS.write_text(json.dumps(data,ensure_ascii=False,indent=1)+'\n',encoding='utf-8')
    write_build();audit(data);print('FASE_A_OK')

if __name__=='__main__':main()
