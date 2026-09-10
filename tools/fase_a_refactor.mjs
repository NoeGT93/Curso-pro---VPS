import fs from 'node:fs';
import path from 'node:path';
import {parse} from '@babel/parser';
import traverseModule from '@babel/traverse';
import generateModule from '@babel/generator';

const traverse=traverseModule.default||traverseModule;
const generate=generateModule.default||generateModule;
const ROOT=process.cwd();
const TEXTOS=path.join(ROOT,'datos','textos.json');
const FILES=['app.js','averia.js','fase5.js','fase6.js','perfiles.js'].map(n=>path.join(ROOT,'build',n));
const TPL=path.join(ROOT,'build','plantilla.html');
const ACC=/[áéíóúñüÁÉÍÓÚÑÜ¿¡]/;
const SPANISH=/\b(?:semana|sesion|servidor|progreso|copia|archivo|guardar|abrir|cerrar|borrar|eliminar|respuesta|pregunta|tarjeta|nueva|hoy|dias|dia|recuperacion|robustez|herramientas|datos|estado|salida|revisar|copiar|perfil|cuentas|curso|avance|marcado|marcar|dominado|dominadas|repaso|fallo|fallar|validado|importado|exportado|bloque|actual|total|desde|hasta|todavia|puedes|puede|quieres|quiero|ninguna|ningun|ninguno|primero|ultima|ultimo|aqui|atras|delante|vacio|disponible)\b/i;
const data=JSON.parse(fs.readFileSync(TEXTOS,'utf8'));

function flatten(x,p='',out={}){
  if(x&&typeof x==='object'&&!Array.isArray(x)){
    for(const [k,v] of Object.entries(x)){
      if(k.startsWith('_'))continue;
      const q=p?`${p}.${k}`:k;
      flatten(v,q,out);
    }
  }else if(typeof x==='string')out[p]=x;
  return out;
}
let flat=flatten(data),rev=new Map(Object.entries(flat).map(([k,v])=>[v,k]));
const ren=data._renombres||{};
const counters={};
const marker=k=>`__T:${k}__`;

function applyRenames(v){
  let s=v;
  const pairs=Object.entries(ren).filter(([k])=>!k.startsWith('_')).sort((a,b)=>b[0].length-a[0].length);
  for(const [old,nuevo] of pairs)if(s===old)return nuevo;
  s=s.replace(/Tu regreso/g,ren['Tu regreso']||'Mi progreso');
  s=s.replace(/Regreso/g,ren.Regreso||'Mi progreso');
  s=s.replace(/Fase final/g,ren['Fase final']||'Cierre del curso');
  s=s.replace(/Bitácora y recuperación/g,ren['Bitácora y recuperación']||'Bitácora');
  s=s.replace(/Autocorrector/g,ren.Autocorrector||'Revisar salida');
  s=s.replace(/Modo Avería/g,ren.Avería||'Practicar averías');
  return s;
}
function looksCode(q){
  if(/https?:\/\//.test(q))return true;
  if(/^([.#/\[{]|--)/.test(q)&&!(/\s/.test(q)))return true;
  if(/^[a-z][A-Za-z0-9_.:/#@-]*$/.test(q))return true;
  if((q.includes(';')&&q.includes(':'))||/^[A-Za-z-]+\s*:/.test(q))return true;
  if(/^cursoVps[A-Za-z0-9]+$/.test(q))return true;
  return false;
}
function candidate(v){
  const q=String(v).trim();
  if(!q||q.includes('__T:')||!/[A-Za-zÁÉÍÓÚÑÜáéíóúñü¿¡]/.test(q))return false;
  if(looksCode(q))return false;
  if(['true','false','null','undefined','object','boolean','string','number','open','active','main','text','bash','html','ini','nginx','yaml','dockerfile','es-ES','GET','POST'].includes(q))return false;
  if(ACC.test(q))return true;
  if(/\s/.test(q))return true;
  return /^[A-Z][A-Za-z]+$/.test(q);
}
function ensure(value,filekey){
  const cleaned=applyRenames(String(value).trim());
  if(rev.has(cleaned))return rev.get(cleaned);
  counters[filekey]=(counters[filekey]||0)+1;
  const n=String(counters[filekey]).padStart(3,'0');
  data.extra=data.extra||{};
  data.extra[filekey]=data.extra[filekey]||{};
  while(Object.prototype.hasOwnProperty.call(data.extra[filekey],n)){
    counters[filekey]++;
    return ensure(value,filekey);
  }
  data.extra[filekey][n]=cleaned;
  const k=`extra.${filekey}.${n}`;
  flat[k]=cleaned;rev.set(cleaned,k);
  return k;
}
function splitSentinels(s){return s.split(/(\u0001E\d+\u0002)/g).filter(x=>x!=='')}
function textPiece(s,filekey,aggressive=false){
  const lead=s.match(/^\s*/)?.[0]||'',trail=s.match(/\s*$/)?.[0]||'',core=s.slice(lead.length,s.length-trail.length);
  const human=aggressive?Boolean(core&&!core.includes('__T:')&&/[A-Za-zÁÉÍÓÚÑÜáéíóúñü¿¡]/.test(core)&&!looksCode(core)):candidate(core);
  if(!human)return s;
  return lead+marker(ensure(core,filekey))+trail;
}
function transformTextWithSentinels(s,filekey,aggressive=false){
  return splitSentinels(s).map(x=>/^\u0001E\d+\u0002$/.test(x)?x:textPiece(x,filekey,aggressive)).join('');
}
function transformTag(tag,filekey){
  return tag.replace(/\b(aria-label|title|placeholder|alt)=(['"])([\s\S]*?)\2/g,(m,name,q,val)=>`${name}=${q}${transformTextWithSentinels(val,filekey,true)}${q}`);
}
function transformHtmlish(value,filekey){
  let v=applyRenames(String(value));
  if(!(v.includes('<')&&v.includes('>')))return transformTextWithSentinels(v,filekey,true);
  let out='',i=0;
  while(i<v.length){
    if(v[i]==='<'){
      const j=v.indexOf('>',i+1);
      if(j<0){out+=v.slice(i);break}
      out+=transformTag(v.slice(i,j+1),filekey);i=j+1;
    }else{
      const j=v.indexOf('<',i),end=j<0?v.length:j;
      out+=transformTextWithSentinels(v.slice(i,end),filekey,true);i=end;
    }
  }
  return out;
}
function skipCss(pathObj){
  const p=pathObj.parentPath;
  return Boolean(p?.isVariableDeclarator?.()&&p.node.id?.type==='Identifier'&&/css|style/i.test(p.node.id.name));
}
function refactorJs(file){
  const filekey=path.basename(file,'.js'),src=fs.readFileSync(file,'utf8');
  const ast=parse(src,{sourceType:'script',allowReturnOutsideFunction:true,plugins:['optionalChaining','nullishCoalescingOperator']});
  traverse(ast,{
    StringLiteral(p){
      if(p.parentPath?.isObjectProperty?.()&&p.parentPath.node.key===p.node&&!p.parentPath.node.computed)return;
      const value=p.node.value;
      if(value.includes('<')&&value.includes('>')){
        const nv=transformHtmlish(value,filekey);if(nv!==value)p.node.value=nv;
      }else if(candidate(value))p.node.value=marker(ensure(value,filekey));
    },
    TemplateLiteral(p){
      if(skipCss(p))return;
      const token=i=>`\u0001E${i}\u0002`;let joined='';
      p.node.quasis.forEach((q,i)=>{joined+=(q.value.cooked??q.value.raw);if(i<p.node.expressions.length)joined+=token(i)});
      const nv=transformHtmlish(joined,filekey),parts=nv.split(/\u0001E\d+\u0002/g);
      if(parts.length!==p.node.quasis.length)throw new Error(`No pude separar template en ${file}`);
      p.node.quasis.forEach((q,i)=>{q.value.cooked=parts[i];q.value.raw=parts[i].replace(/`/g,'\\`').replace(/\$\{/g,'\\${')});
    }
  });
  fs.writeFileSync(file,generate(ast,{comments:false,compact:false,retainLines:true,jsescOption:{minimal:true}},src).code+'\n','utf8');
}
function transformHtmlSource(src){
  const filekey='plantilla';let s=src;
  for(const [old,nuevo] of Object.entries(ren).filter(([k])=>!k.startsWith('_')).sort((a,b)=>b[0].length-a[0].length))if(s.includes(old))s=s.split(old).join(marker(ensure(nuevo,filekey)));
  for(const [k,v] of Object.entries(flat).sort((a,b)=>b[1].length-a[1].length))if(v.length>1&&s.includes(v))s=s.split(v).join(marker(k));
  const chunks=s.split(/(<style[\s\S]*?<\/style>|<script[\s\S]*?<\/script>)/ig);
  for(let i=0;i<chunks.length;i++){
    if(/^<(style|script)/i.test(chunks[i]))continue;
    chunks[i]=chunks[i].replace(/\b(aria-label|title|placeholder|alt)=(['"])([\s\S]*?)\2/g,(m,name,q,val)=>`${name}=${q}${transformTextWithSentinels(val,filekey,true)}${q}`);
    chunks[i]=chunks[i].replace(/>([^<>]+)</g,(m,val)=>`>${textPiece(val,filekey,true)}<`);
  }
  s=chunks.join('');
  if(!s.includes('__TEXTOS_JSON__')){
    const re=/<script[^>]*\bid=['"]cursoData['"][^>]*>/i,m=s.match(re);
    if(!m)throw new Error('No encuentro cursoData en plantilla.html');
    const at=m.index;s=s.slice(0,at)+'<script type="application/json" id="textosData">__TEXTOS_JSON__</script>\n'+s.slice(at);
  }
  return s;
}
function cleanForAudit(v){
  return String(v).replace(/__T:[A-Za-z0-9_.-]+__/g,'').replace(/<[^>]*>/g,' ').replace(/\s+/g,' ').trim();
}
function auditJs(file){
  const src=fs.readFileSync(file,'utf8'),ast=parse(src,{sourceType:'script',plugins:['optionalChaining','nullishCoalescingOperator']});
  const residual=[];
  traverse(ast,{
    StringLiteral(p){
      if(p.parentPath?.isObjectProperty?.()&&p.parentPath.node.key===p.node&&!p.parentPath.node.computed)return;
      const q=cleanForAudit(p.node.value);if(q&&!looksCode(q)&&SPANISH.test(q))residual.push(q);
    },
    TemplateLiteral(p){
      if(skipCss(p))return;
      const q=cleanForAudit(p.node.quasis.map(x=>x.value.cooked??x.value.raw).join(' '));if(q&&!looksCode(q)&&SPANISH.test(q))residual.push(q);
    }
  });
  return residual;
}

for(const f of FILES)refactorJs(f);
fs.writeFileSync(TPL,transformHtmlSource(fs.readFileSync(TPL,'utf8')),'utf8');
fs.writeFileSync(TEXTOS,JSON.stringify(data,null,1)+'\n','utf8');

let accents=0,forbidden=[],residual=[];
for(const f of FILES){
  const s=fs.readFileSync(f,'utf8');accents+=(s.match(/[áéíóúñüÁÉÍÓÚÑÜ¿¡]/g)||[]).length;
  for(const old of Object.keys(ren).filter(k=>!k.startsWith('_')))if(s.includes(old))forbidden.push(`${path.basename(f)}:${old}`);
  for(const q of auditJs(f))residual.push(`${path.basename(f)}:${q}`);
}
console.log(`AUDIT_ACCENTS=${accents}`);
console.log(`AUDIT_FORBIDDEN=${forbidden.length}`);
console.log(`AUDIT_RESIDUAL=${residual.length}`);
if(forbidden.length)console.log(forbidden.join('\n'));
if(residual.length)console.log(residual.slice(0,100).join('\n'));
if(accents||forbidden.length||residual.length)process.exitCode=2;
else console.log('FASE_A_REFACTOR_OK');
