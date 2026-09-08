/**
 * Pruebas del enrutado del Worker `docs/worker-psforgis-ocg.js`.
 *
 * Ese archivo es el que se pega en Cloudflare y REEMPLAZA al Worker entero, así
 * que un error suyo deja al visor sin capas (`/ogc`) o sin lectura con IA
 * (`/ia-plano`). Aquí se comprueba, sin red, que las dos rutas siguen
 * respondiendo lo que deben y que el resto de rutas conserva la respuesta que
 * el Worker daba antes de añadir la IA.
 *
 * No se llama a ningún servicio externo: todos los casos se detienen en las
 * validaciones previas a la petición saliente.
 *
 * Uso: node scripts/worker_router.test.mjs
 */
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

// El repositorio no declara `type: module`, así que un `.js` se interpretaría
// como CommonJS. Se carga por data: URL para evaluarlo como módulo ES.
const RAIZ = join(dirname(fileURLToPath(import.meta.url)), '..');
const fuente = readFileSync(join(RAIZ, 'docs/worker-psforgis-ocg.js'), 'utf8');
const { default: worker } = await import(
  'data:text/javascript;charset=utf-8,' + encodeURIComponent(fuente)
);

let ok=0, mal=0;
const ctx={ waitUntil(){} };
async function prueba(nombre, req, env, esperado){
  let r;
  try { r = await worker.fetch(req, env, ctx); }
  catch(e){ console.log(`  ❌ ${nombre}: lanzó ${e.message}`); mal++; return; }
  const cuerpo = await r.text();
  const bien = r.status===esperado.status && (!esperado.incluye || cuerpo.includes(esperado.incluye));
  if(bien){ console.log(`  ✅ ${nombre} → ${r.status}`); ok++; }
  else { console.log(`  ❌ ${nombre} → ${r.status} «${cuerpo.slice(0,80)}», se esperaba ${esperado.status}/«${esperado.incluye||''}»`); mal++; }
}
const P=(url,init={})=>new Request(url,init);
const B='https://psforgis-ocg.psforestal.workers.dev';

console.log('Ruta /ogc (la que ya existía)');
await prueba('/ogc sin parámetro u', P(B+'/ogc'), {}, {status:400, incluye:'Missing query parameter'});
await prueba('/ogc con destino no permitido', P(B+'/ogc?u=https://evil.example.com/x'), {}, {status:403, incluye:'Host not allowed'});
await prueba('/ogc con IP privada', P(B+'/ogc?u=http://192.168.1.1/x'), {}, {status:403, incluye:'Host not allowed'});
await prueba('/ogc con esquema file:', P(B+'/ogc?u=file:///etc/passwd'), {}, {status:400, incluye:'Only http/https'});
await prueba('/ogc con método PUT', P(B+'/ogc?u=https://snitcr.go.cr/x',{method:'PUT'}), {}, {status:405});
await prueba('/ogc preflight OPTIONS', P(B+'/ogc',{method:'OPTIONS'}), {}, {status:204});

console.log('Ruta /ia-plano (la nueva)');
await prueba('/ia-plano sin secreto configurado', P(B+'/ia-plano',{method:'POST',body:'{}'}), {}, {status:503, incluye:'no está configurado'});
await prueba('/ia-plano con GET', P(B+'/ia-plano'), {IA_API_KEY:'x'}, {status:405, incluye:'use POST'});
await prueba('/ia-plano preflight OPTIONS', P(B+'/ia-plano',{method:'OPTIONS'}), {IA_API_KEY:'x'}, {status:204});
await prueba('/ia-plano cuerpo vacío', P(B+'/ia-plano',{method:'POST',body:'{}'}), {IA_API_KEY:'x'}, {status:400, incluye:'tipo inválido'});
await prueba('/ia-plano tipo desconocido', P(B+'/ia-plano',{method:'POST',body:JSON.stringify({tipo:'otro'})}), {IA_API_KEY:'x'}, {status:400, incluye:'tipo inválido'});
await prueba('/ia-plano sin imagen', P(B+'/ia-plano',{method:'POST',body:JSON.stringify({tipo:'coords',formato:'image/png'})}), {IA_API_KEY:'x'}, {status:400, incluye:'falta la imagen'});
await prueba('/ia-plano imagen que no es base64', P(B+'/ia-plano',{method:'POST',body:JSON.stringify({tipo:'coords',formato:'image/png',imagen:'@@@no@@@'})}), {IA_API_KEY:'x'}, {status:400, incluye:'no es base64'});
await prueba('/ia-plano imagen demasiado grande', P(B+'/ia-plano',{method:'POST',body:JSON.stringify({tipo:'coords',formato:'image/png',imagen:'A'.repeat(8*1024*1024+1)})}), {IA_API_KEY:'x'}, {status:413});
await prueba('/ia-plano origen no permitido', P(B+'/ia-plano',{method:'POST',body:'{}',headers:{Origin:'https://sitio-ajeno.example'}}), {IA_API_KEY:'x'}, {status:403, incluye:'origen no permitido'});
await prueba('/ia-plano origen permitido pasa el filtro', P(B+'/ia-plano',{method:'POST',body:'{}',headers:{Origin:'https://psforestal-rgb.github.io'}}), {IA_API_KEY:'x'}, {status:400, incluye:'tipo inválido'});

console.log('Cualquier otra ruta');
await prueba('raíz devuelve el mensaje de siempre', P(B+'/'), {}, {status:200, incluye:'OGC Proxy OK'});
await prueba('ruta inventada devuelve el mensaje de siempre', P(B+'/loquesea'), {}, {status:200, incluye:'OGC Proxy OK'});

console.log(`\nRESULTADO: ${ok} ok, ${mal} fallo(s)`);
process.exit(mal?1:0);
