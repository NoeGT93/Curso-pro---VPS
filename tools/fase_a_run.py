#!/usr/bin/env python3
import re
import fase_a_refactor as f

def ensure_textos_marker(src):
    if '__TEXTOS_JSON__' in src:
        return src
    tag='<script type="application/json" id="textosData">__TEXTOS_JSON__</script>\n'
    m=re.search(r'<script[^>]*\bid=["\']cursoData["\'][^>]*>',src,re.I)
    if not m:
        raise SystemExit('No encuentro el bloque de datos del curso en plantilla.html')
    return src[:m.start()]+tag+src[m.start():]

f.ensure_textos_marker=ensure_textos_marker
f.main()
