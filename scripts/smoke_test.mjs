/* Smoke test del visor BTMM-Visados con Playwright/Chromium.
 *
 * Verifica el flujo crítico completo:
 *   1. index.html carga y las 11 librerías externas pasan la validación SRI.
 *   2. La splash cede el paso y el mapa Leaflet se inicializa.
 *   3. sql.js compila su WASM bajo la CSP.
 *   4. PDF.js abre un PDF con isEvalSupported:false.
 *   5. Se carga un polígono GeoJSON de prueba dentro del PNLQ y el análisis
 *      de cobertura produce resultados.
 *   6. No hay violaciones de CSP, fallos de integridad ni errores de página.
 *
 * Modos:
 *   node scripts/smoke_test.mjs                  # red real (CI): CDN verdadero
 *   OFFLINE_ASSETS=/ruta node scripts/smoke_test.mjs
 *       # sin red: sirve las librerías desde paquetes npm extraídos en /ruta
 *       # (misma estructura x-<paquete>/package/... que genera `npm pack`).
 *
 * Requiere: `npm i playwright` y un servidor local del repo en el puerto 8791
 * (el script lo levanta solo con python3 -m http.server si no existe).
 */
import { chromium } from 'playwright';
import fs from 'fs';
import path from 'path';
import { spawn } from 'child_process';
import { fileURLToPath } from 'url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const PORT = process.env.SMOKE_PORT || 8791;
const OFFLINE = process.env.OFFLINE_ASSETS || '';

const OFFLINE_MAP = {
  '/npm/leaflet@1.9.4/dist/leaflet.css': ['x-leaflet-1.9.4/package/dist/leaflet.css', 'text/css'],
  '/npm/leaflet@1.9.4/dist/leaflet.js': ['x-leaflet-1.9.4/package/dist/leaflet.js', 'application/javascript'],
  '/npm/pako@2.1.0/dist/pako.min.js': ['x-pako-2.1.0/package/dist/pako.min.js', 'application/javascript'],
  '/npm/@turf/turf@6.5.0/turf.min.js': ['x-turf-turf-6.5.0/package/turf.min.js', 'application/javascript'],
  '/npm/shpjs@4.0.4/dist/shp.js': ['x-shpjs-4.0.4/package/dist/shp.js', 'application/javascript'],
  '/npm/jszip@3.10.1/dist/jszip.min.js': ['x-jszip-3.10.1/package/dist/jszip.min.js', 'application/javascript'],
  '/npm/@mapbox/togeojson@0.16.0/togeojson.js': ['x-mapbox-togeojson-0.16.0/package/togeojson.js', 'application/javascript'],
  '/npm/proj4@2.9.2/dist/proj4.js': ['x-proj4-2.9.2/package/dist/proj4.js', 'application/javascript'],
  '/npm/sql.js@1.10.3/dist/sql-wasm.js': ['x-sql.js-1.10.3/package/dist/sql-wasm.js', 'application/javascript'],
  '/npm/sql.js@1.10.3/dist/sql-wasm.wasm': ['x-sql.js-1.10.3/package/dist/sql-wasm.wasm', 'application/wasm'],
  '/npm/pdfjs-dist@3.11.174/build/pdf.min.js': ['x-pdfjs-dist-3.11.174/package/build/pdf.min.js', 'application/javascript'],
  '/npm/pdfjs-dist@3.11.174/build/pdf.worker.min.js': ['x-pdfjs-dist-3.11.174/package/build/pdf.worker.min.js', 'application/javascript'],
  '/npm/utif@3.1.0/UTIF.js': ['x-utif-3.1.0/package/UTIF.js', 'application/javascript'],
};

async function ensureServer() {
  try {
    const r = await fetch(`http://127.0.0.1:${PORT}/version.json`);
    if (r.ok) return null;
  } catch {}
  const srv = spawn('python3', ['-m', 'http.server', String(PORT)], { cwd: ROOT, stdio: 'ignore' });
  await new Promise((r) => setTimeout(r, 1200));
  return srv;
}

const fallos = [];
const notas = [];

function fallo(msg) { fallos.push(msg); console.log('  ❌ ' + msg); }
function ok(msg) { console.log('  ✅ ' + msg); }

const srv = await ensureServer();
const launchOpts = { headless: true };
if (fs.existsSync('/opt/pw-browsers/chromium')) launchOpts.executablePath = '/opt/pw-browsers/chromium';
const browser = await chromium.launch(launchOpts);
const page = await browser.newPage();

page.on('pageerror', (e) => fallo('pageerror: ' + String(e).slice(0, 200)));
page.on('console', (m) => {
  const t = m.text();
  if (/Refused|integrity|Content.Security.Policy/i.test(t)) fallo('consola: ' + t.slice(0, 200));
  else if (m.type() === 'error' && !/net::ERR|Failed to load resource/.test(t)) notas.push(t.slice(0, 120));
});

if (OFFLINE) {
  await page.route('**/*', async (route) => {
    const url = new URL(route.request().url());
    if (url.hostname === 'cdn.jsdelivr.net' && OFFLINE_MAP[url.pathname]) {
      const [rel, ct] = OFFLINE_MAP[url.pathname];
      return route.fulfill({ status: 200, contentType: ct, body: fs.readFileSync(path.join(OFFLINE, rel)) });
    }
    if (url.hostname === '127.0.0.1' || url.hostname === 'localhost') return route.continue();
    return route.abort();
  });
}

console.log(`Smoke test (${OFFLINE ? 'OFFLINE' : 'red real'}) sobre http://127.0.0.1:${PORT}/index.html`);
await page.goto(`http://127.0.0.1:${PORT}/index.html`, { waitUntil: 'load', timeout: 90000 });
await page.waitForTimeout(3000);

console.log('1) Librerías externas (SRI)');
const libs = await page.evaluate(() => ({
  leaflet: !!window.L, pako: !!window.pako, turf: !!(window.turf && window.turf.intersect),
  shp: !!window.shp, jszip: !!window.JSZip, togeojson: !!window.toGeoJSON,
  proj4: !!window.proj4, sqljs: typeof window.initSqlJs === 'function', pdfjs: !!window.pdfjsLib,
  version: window.BTMM_APP_VERSION, errlog: typeof window.btmmReporteErrores === 'function',
}));
for (const [k, v] of Object.entries(libs)) {
  if (k === 'version') { ok('APP_VERSION: ' + v); continue; }
  v ? ok(k) : fallo('librería/función no disponible: ' + k);
}

console.log('2) Splash, bienvenida y mapa');
const bienvenida = await page.$eval('#splash-welcome', (el) => el.innerText).catch(() => '');
['ÁREA DE CONSERVACIÓN CENTRAL', 'BLOQUE TAPANTÍ MACIZO DE LA MUERTE', 'PARQUE NACIONAL LOS QUETZALES', 'Ing. Pablo César Sánchez Núñez']
  .forEach((linea) => bienvenida.includes(linea) ? ok('bienvenida: ' + linea) : fallo('falta línea de bienvenida: ' + linea));
(await page.$('#splash-video')) ? ok('botón de videotutorial general presente') : fallo('sin botón #splash-video');
const btn = await page.$('#splash-enter, #splash button, button:has-text("Entrar")');
if (btn) await btn.click();
await page.waitForTimeout(1500);
(await page.$('.leaflet-container')) ? ok('mapa Leaflet inicializado') : fallo('sin contenedor Leaflet');
const nVid = await page.$$eval('.btn-video-tut', (els) => els.length);
nVid === 7 ? ok('7 botones de video tutorial por módulo') : fallo('botones de video por módulo: ' + nVid);
await page.click('#panel-carga .btn-video-tut');
await page.waitForTimeout(300);
const toastVid = await page.$eval('#toast', (el) => el.innerText).catch(() => '');
/en desarrollo/i.test(toastVid) ? ok('aviso «en desarrollo» al pulsar el botón') : fallo('toast de video: ' + toastVid.slice(0, 80));

console.log('3) sql.js / WASM bajo CSP');
const wasm = await page.evaluate(async () => {
  try { const SQL = await getSQL(); const db = new SQL.Database(); db.run('CREATE TABLE t(a)'); db.close(); return 'ok'; }
  catch (e) { return 'fail: ' + e; }
});
wasm === 'ok' ? ok('WASM compila y ejecuta') : fallo('sql.js: ' + wasm);

console.log('4) PDF.js con isEvalSupported:false');
const pdf = await page.evaluate(async () => {
  try {
    const raw = `%PDF-1.1\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj\n2 0 obj<</Type/Pages/Kids[3 0 R]/Count 1>>endobj\n3 0 obj<</Type/Page/Parent 2 0 R/MediaBox[0 0 200 200]>>endobj\nxref\n0 4\n0000000000 65535 f \ntrailer<</Size 4/Root 1 0 R>>\nstartxref\n0\n%%EOF`;
    const doc = await pdfjsLib.getDocument({ data: new TextEncoder().encode(raw), isEvalSupported: false }).promise;
    const n = doc.numPages; await doc.destroy(); return n === 1 ? 'ok' : 'fail: pages=' + n;
  } catch (e) { return 'fail: ' + String(e).slice(0, 150); }
});
pdf === 'ok' ? ok('PDF de prueba abierto') : fallo('PDF.js: ' + pdf);

console.log('5) Carga de polígono y análisis de cobertura');
const gj = JSON.stringify({ type: 'FeatureCollection', features: [{ type: 'Feature', properties: {},
  geometry: { type: 'Polygon', coordinates: [[[-83.755, 9.555], [-83.752, 9.555], [-83.752, 9.558], [-83.755, 9.558], [-83.755, 9.555]]] } }] });
await page.setInputFiles('#fi', { name: 'predio_smoke.geojson', mimeType: 'application/geo+json', buffer: Buffer.from(gj) });
try {
  await page.waitForFunction(() => !document.getElementById('btn-analyze').disabled, { timeout: 30000 });
  ok('polígono cargado');
  await page.evaluate(() => runAnalysis());
  await page.waitForFunction(() => {
    const rb = document.getElementById('rb');
    return rb && rb.innerText.length > 100;
  }, { timeout: 120000 });
  const txt = await page.evaluate(() => document.getElementById('rb').innerText);
  txt.includes('MAPA 1') ? ok('análisis de cobertura produjo resultados') : fallo('resultados inesperados: ' + txt.slice(0, 120));
} catch (e) {
  fallo('análisis: ' + String(e).slice(0, 200));
}

console.log('6) Revisión local de seguridad de archivos');
const scan = await page.evaluate(async () => {
  const out = {};
  const enc = (s) => new TextEncoder().encode(s).buffer;
  out.pdfLimpio = _revisarPdf(enc('%PDF-1.4\nhola mundo\n%%EOF')).nivel;
  out.pdfConJs = _revisarPdf(enc('%PDF-1.4 /OpenAction /JavaScript (app.alert(1))')).nivel;
  out.noPdf = _revisarPdf(enc('MZ ejecutable')).nivel;
  out.imgFalsa = _revisarImagen(enc('no soy png'), 'plano.png').nivel;
  const zip = new JSZip(); zip.file('[Content_Types].xml', '<Types/>'); zip.file('word/document.xml', '<w/>');
  out.docxLimpio = (await _revisarDocx(await zip.generateAsync({ type: 'arraybuffer' }))).nivel;
  zip.file('word/vbaProject.bin', 'x');
  out.docxMacros = (await _revisarDocx(await zip.generateAsync({ type: 'arraybuffer' }))).nivel;
  return out;
});
const esperado = { pdfLimpio: 'ok', pdfConJs: 'peligro', noPdf: 'peligro', imgFalsa: 'peligro', docxLimpio: 'ok', docxMacros: 'peligro' };
for (const [k, v] of Object.entries(esperado)) {
  scan[k] === v ? ok(`${k}: ${scan[k]}`) : fallo(`revisión ${k}: esperado ${v}, obtuvo ${scan[k]}`);
}
const modalOk = await (async () => {
  const flujo = page.evaluate(() => revisarArchivoAntesDeUsar(new Blob(['%PDF-1.4 hola']), 'pdf', 'prueba.pdf'));
  await page.waitForSelector('#scan-modal #scan-ok', { timeout: 10000 });
  const sha = await page.$eval('#scan-modal', (el) => /Huella SHA-256/.test(el.innerText));
  await page.click('#scan-modal #scan-ok');
  return (await flujo) === true && sha;
})().catch(() => false);
modalOk ? ok('modal de revisión muestra SHA-256 y confirma') : fallo('flujo del modal de revisión');

console.log('7) Registro de errores runtime');
const rep = await page.evaluate(() => window.btmmReporteErrores(false));
rep && rep.herramienta === 'BTMM-Visados' ? ok(`reporte generado (${rep.totalErrores} errores registrados)`) : fallo('btmmReporteErrores no devolvió reporte');

await browser.close();
if (srv) srv.kill();

console.log();
if (notas.length) console.log(`(notas no bloqueantes: ${notas.length})`);
if (fallos.length) {
  console.log(`RESULTADO: ${fallos.length} fallo(s)`);
  process.exit(1);
}
console.log('RESULTADO: smoke test OK');
