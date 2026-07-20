/* Pruebas del módulo «Importar predio desde plano» (BTMM-Visados).
 *
 * No requiere red ni navegador: extrae el núcleo determinista PI embebido en
 * index.html (entre los marcadores __PI_CORE_START__/__PI_CORE_END__) y las
 * funciones de área CRTM05, y los ejecuta en Node con proj4 simulado. Verifica:
 *   - rumbo → azimut (incluye W y O como oeste)
 *   - grados/minutos/segundos y decimal
 *   - números con coma y con punto
 *   - construcción de polígono y error de cierre (sin ajuste silencioso)
 *   - traslación y rotación sin alterar el área
 *   - área CRTM05 de un FeatureCollection (no cae al geodésico)
 *   - clasificación de CRS con evidencia / ambigüedad
 *   - flujo mínimo: filas → polígono → FeatureCollection → área
 *
 * Uso: node scripts/plano_import.test.mjs   (código 1 si algo falla)
 */
import assert from 'assert';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const html = fs.readFileSync(path.join(ROOT, 'index.html'), 'utf8');

// proj4 simulado (identidad) para que el área planar == fórmula del área en las
// mismas unidades; las pruebas de parsing/geometría no dependen de la proyección.
globalThis.proj4 = (a, b, c) => c;

// --- Carga del núcleo PI real embebido ---
const i0 = html.indexOf('/*__PI_CORE_START__');
const i1 = html.indexOf('/*__PI_CORE_END__*/');
assert(i0 > -1 && i1 > i0, 'No se encontró el bloque PI en index.html');
const coreSrc = html.slice(i0, i1);
(0, eval)(coreSrc);                 // define globalThis.PI
const PI = globalThis.PI;
assert(PI && typeof PI.parseBearing === 'function', 'PI no quedó disponible');

// --- Extrae las funciones de área CRTM05 tal como se publican ---
function extractFns(src, names) {
  let out = '';
  for (const name of names) {
    const i = src.indexOf('function ' + name + '(');
    assert(i > -1, 'no se encontró ' + name + ' en index.html');
    let k = src.indexOf('{', i), depth = 0;
    for (; k < src.length; k++) { if (src[k] === '{') depth++; else if (src[k] === '}') { depth--; if (depth === 0) { k++; break; } } }
    out += src.slice(i, k) + '\n';
  }
  return out;
}
const areaSrc = extractFns(html, ['areaHaGeo', 'ringAreaCRTM05', 'geomAreaCRTM05', 'areaHa']);
const areaFns = new Function('proj4', 'turf', 'isFinite', 'Math', areaSrc + '\nreturn {areaHa, areaHaGeo};');
const { areaHa, areaHaGeo } = areaFns((a, b, c) => c, { area: () => 424242 }, isFinite, Math);

let pass = 0, fail = 0;
function t(name, fn) { try { fn(); console.log('  ✅ ' + name); pass++; } catch (e) { console.log('  ❌ ' + name + ' — ' + e.message); fail++; } }
const near = (a, b, eps = 1e-6) => Math.abs(a - b) <= eps;

console.log('1) Números con coma y con punto');
t('512345,67 (coma decimal)', () => assert(near(PI.parseNumber('512345,67'), 512345.67)));
t('512345.67 (punto decimal)', () => assert(near(PI.parseNumber('512345.67'), 512345.67)));
t('512.345,67 (miles . / decimal ,)', () => assert(near(PI.parseNumber('512.345,67'), 512345.67)));
t('1,234.56 (miles , / decimal .)', () => assert(near(PI.parseNumber('1,234.56'), 1234.56)));

console.log('2) Grados/minutos/segundos');
t('14° 00\' 30" = 14.008333', () => assert(near(PI.parseDMS('14° 00\' 30"'), 14 + 30 / 3600, 1e-5)));
t('14 30 00 = 14.5', () => assert(near(PI.parseDMS('14 30 00'), 14.5)));
t('45°30\' con coma decimal 45°30,5\'', () => assert(near(PI.parseDMS('45°30\''), 45.5)));

console.log('3) Rumbo → azimut (W y O como oeste)');
t('N 14° 00\' W = 346°', () => assert(near(PI.parseBearing('N 14° 00\' W').azimuth, 346)));
t('N14°00\'O = 346° (O = oeste)', () => assert(near(PI.parseBearing('N14°00\'O').azimuth, 346)));
t('W y O coinciden', () => assert(near(PI.parseBearing('N14°00\'W').azimuth, PI.parseBearing('N14°00\'O').azimuth)));
t('S 45° 30\' E = 134.5°', () => assert(near(PI.parseBearing('S 45° 30\' E').azimuth, 134.5)));
t('S 45° W = 225°', () => assert(near(PI.parseBearing('S 45° W').azimuth, 225)));
t('azimut decimal 123,5', () => { const b = PI.parseBearing('123,5'); assert(b.kind === 'azimut' && near(b.azimuth, 123.5)); });

console.log('4) Construcción y cierre (sin ajuste silencioso)');
t('cuadrado 100 m cierra exacto, área 10000 m²', () => {
  const r = PI.buildTraverse([{ azimuth: 0, distance: 100 }, { azimuth: 90, distance: 100 }, { azimuth: 180, distance: 100 }, { azimuth: 270, distance: 100 }], [0, 0]);
  assert.strictEqual(r.vertices.length, 4);
  assert(near(r.area, 10000), 'área=' + r.area);
  assert(near(r.closureAbs, 0), 'cierre=' + r.closureAbs);
});
t('reporta error de cierre, no lo corrige', () => {
  const r = PI.buildTraverse([{ azimuth: 0, distance: 100 }, { azimuth: 90, distance: 100 }, { azimuth: 180, distance: 100 }, { azimuth: 270, distance: 99 }], [0, 0]);
  assert(near(r.closureAbs, 1), 'cierre=' + r.closureAbs);
  assert(near(r.perimeter, 399), 'perímetro=' + r.perimeter);
});
t('coordenadas: elimina cierre duplicado', () => {
  const b = PI.buildFromCoords([[0, 0], [100, 0], [100, 100], [0, 100], [0, 0]]);
  assert.strictEqual(b.vertices.length, 4);
  assert(near(b.area, 10000));
});

console.log('5) Traslación y rotación sin alterar el área');
t('rotar 37° + trasladar preserva área y perímetro', () => {
  const ring = [[0, 0], [100, 0], [100, 60], [0, 60]];
  const a0 = PI.shoelaceArea(ring), p0 = PI.perimeter(ring);
  const out = PI.transform(ring, 150, -80, 37);
  assert(near(PI.shoelaceArea(out), a0), 'área cambió');
  assert(near(PI.perimeter(out), p0), 'perímetro cambió');
});

console.log('6) Área CRTM05 de FeatureCollection (fix publicado)');
t('areaHa(FeatureCollection) == suma planar, no geodésico', () => {
  const poly = { type: 'Polygon', coordinates: [[[0, 0], [0, 1000], [1000, 1000], [1000, 0], [0, 0]]] };
  const feat = { type: 'Feature', geometry: poly, properties: {} };
  const fc = { type: 'FeatureCollection', features: [feat] };
  assert(near(areaHa(feat), 100, 1e-3), 'feat=' + areaHa(feat));
  assert(near(areaHa(fc), areaHa(feat)), 'FC != feat');
  assert(areaHa(fc) !== areaHaGeo(fc), 'FC cayó al geodésico');
});

console.log('7) Clasificación de CRS');
t('geográficas detectadas', () => assert.strictEqual(PI.classifyCRS([[-83.75, 9.55], [-83.74, 9.56]]).best, 'EPSG:4326'));
t('CRTM05 por evidencia textual no exige usuario', () => { const c = PI.classifyCRS([[512000, 1050000], [512100, 1050100]], 'CRTM05 EPSG:5367'); assert(c.best === 'EPSG:5367' && !c.needsUser); });
t('proyectadas sin evidencia exigen selección', () => assert(PI.classifyCRS([[512000, 1050000], [512100, 1050100]]).needsUser));

console.log('8) Flujo mínimo: filas → polígono → FeatureCollection → área');
t('coordenadas → polígono cerrado → área CRTM05 coherente', () => {
  const ring = [[512000, 1050000], [512100, 1050000], [512100, 1050080], [512000, 1050080]];
  const b = PI.buildFromCoords(ring);
  const ll = PI.toLngLat(b.vertices, 'EPSG:5367');   // proj4 identidad
  const gj = [...ll.map(p => [p[0], p[1]]), [ll[0][0], ll[0][1]]];
  const fc = { type: 'FeatureCollection', features: [{ type: 'Feature', properties: {}, geometry: { type: 'Polygon', coordinates: [gj] } }] };
  assert.strictEqual(fc.features[0].geometry.coordinates[0].length, 5);
  assert(near(areaHa(fc), 100 * 80 / 10000, 1e-6), 'área=' + areaHa(fc));
});

console.log('\nRESULTADO: ' + pass + ' ok, ' + fail + ' fallo(s)');
process.exit(fail ? 1 : 0);
