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

console.log('1b) Casos adversarios de parser (endurecidos)');
t('15.030 → 15.03 (no 15030)', () => assert(near(PI.parseNumber('15.030'), 15.03)));
t('15,030 → 15.03 (no 15030)', () => assert(near(PI.parseNumber('15,030'), 15.03)));
t('N 120 E → inválido (null)', () => assert(PI.parseBearing('N 120 E') === null));
t('10° 75\' → NaN (minutos ≥ 60)', () => assert(Number.isNaN(PI.parseDMS('10° 75\''))));
t('N 10° 75\' W → null (rumbo con minutos inválidos)', () => assert(PI.parseBearing('N 10° 75\' W') === null));
t('azimut 400 fuera de rango → null', () => assert(PI.parseBearing('400') === null));
t('intercambio E/N detectado (E≈1e6 > N)', () => assert(PI.likelySwappedEN([[1050000, 512000], [1050100, 512100]]) === true));
t('orden correcto no marca intercambio', () => assert(PI.likelySwappedEN([[512000, 1050000], [512100, 1050100]]) === false));

console.log('1d) parseCoord — separador de miles único en coordenadas (P1 revisión)');
t('512.345 → 512345 (miles, proyectada)', () => assert(PI.parseCoord('512.345') === 512345));
t('1.050.000 → 1050000', () => assert(PI.parseCoord('1.050.000') === 1050000));
t('9.555 → 9.555 (geográfica decimal)', () => assert(near(PI.parseCoord('9.555'), 9.555)));
t('-83.750 → -83.75 (geográfica decimal)', () => assert(near(PI.parseCoord('-83.750'), -83.75)));
t('512345,67 → 512345.67', () => assert(near(PI.parseCoord('512345,67'), 512345.67)));
t('E 512.345 / N 1.050.000 consistentes (no a 100s de km)', () => { const e = PI.parseCoord('512.345'), n = PI.parseCoord('1.050.000'); assert(e === 512345 && n === 1050000); });

console.log('1e) splitLeg — separa la distancia antes del rumbo (P1 revisión)');
t('«123.5 50» → azimut 123.5 y dist 50 (no 124.33°)', () => { const l = PI.splitLeg('123.5 50'); assert(l.dir === '123.5' && l.dist === 50 && near(PI.parseBearing(l.dir).azimuth, 123.5)); });
t('«N 14° 00\' W 50» → N14W y dist 50', () => { const l = PI.splitLeg('N 14° 00\' W 50'); assert(near(PI.parseBearing(l.dir).azimuth, 346) && l.dist === 50); });
t('«N14°00\'O» sin distancia', () => { const l = PI.splitLeg('N14°00\'O'); assert(near(PI.parseBearing(l.dir).azimuth, 346) && Number.isNaN(l.dist)); });

console.log('1c) Similitud desde pares (georreferencia de cuadrícula)');
t('2 pares: pixel→mundo exacto, escala 1', () => {
  const T = PI.similarityFromPairs([{ src: [0, 0], dst: [500000, 1000000] }, { src: [100, 0], dst: [500100, 1000000] }]);
  const w = PI.applySimilarity(T, [50, 0]);
  assert(near(w[0], 500050) && near(w[1], 1000000), 'w=' + w);
  assert(near(T.scale, 1));
});
t('similitud con eje Y de imagen invertido', () => {
  const T = PI.similarityFromPairs([{ src: [0, 0], dst: [0, 100] }, { src: [0, 100], dst: [0, 0] }]);
  assert(near(PI.applySimilarity(T, [0, 50])[1], 50));
});

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

console.log('4b) Miscerradura y compensación de referencia');
const LEGS_BAD = [{ azimuth: 0, distance: 100 }, { azimuth: 90, distance: 100 }, { azimuth: 180, distance: 100 }, { azimuth: 270, distance: 99 }];
t('diagnoseClosure cuantifica la miscerradura (1 m, 1:399)', () => {
  const dg = PI.diagnoseClosure(LEGS_BAD, [0, 0]);
  assert(near(dg.misAbs, 1), 'mis=' + dg.misAbs);
  assert(near(dg.rel, 399, 1e-6), 'rel=' + dg.rel);
});
t('cuadrado perfecto: miscerradura ≈ 0', () => {
  const dg = PI.diagnoseClosure([{ azimuth: 0, distance: 100 }, { azimuth: 90, distance: 100 }, { azimuth: 180, distance: 100 }, { azimuth: 270, distance: 100 }], [0, 0]);
  assert(near(dg.misAbs, 0), 'mis=' + dg.misAbs);
});
t('compensateBowditch cierra y da área plausible', () => {
  const c = PI.compensateBowditch(LEGS_BAD, [0, 0]);
  assert.strictEqual(c.vertices.length, 4);
  assert(Math.abs(c.area - 9950) < 200, 'área Bowditch=' + c.area);
});
t('compensateTransit devuelve polígono válido', () => {
  const c = PI.compensateTransit(LEGS_BAD, [0, 0]);
  assert.strictEqual(c.vertices.length, 4);
  assert(c.area > 9000 && c.area < 11000, 'área Tránsito=' + c.area);
});
t('compensación no altera un cuadrado ya cerrado', () => {
  const perfect = [{ azimuth: 0, distance: 100 }, { azimuth: 90, distance: 100 }, { azimuth: 180, distance: 100 }, { azimuth: 270, distance: 100 }];
  assert(near(PI.compensateBowditch(perfect, [0, 0]).area, 10000, 1e-6));
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
t('CR-SIRGAS por texto → 8908', () => { const c = PI.classifyCRS([[512000, 1050000], [512100, 1050100]], 'CR-SIRGAS CRTM05'); assert(c.best === 'EPSG:8908' && !c.needsUser); });
t('CRTM05 genérico → ambiguo 5367/8908 (exige confirmar)', () => { const c = PI.classifyCRS([[512000, 1050000], [512100, 1050100]], 'Coordenadas CRTM05'); const top2 = c.candidates.slice(0, 2).map(k => k.crs).sort(); assert(c.needsUser && c.ambiguous && top2[0] === 'EPSG:5367' && top2[1] === 'EPSG:8908'); });
t('inCostaRica / crsPlacesInCR (geográficas)', () => { assert(PI.inCostaRica(-83.75, 9.55) === true && PI.inCostaRica(-70, 40) === false); assert(PI.crsPlacesInCR(-83.75, 9.55, 'EPSG:4326') === true); });
t('contención geográfica penaliza el CRS que saca el predio del país', () => {
  const prev = globalThis.proj4;
  // proj4 simulado: 5367/8908 → CR; 32616 → fuera del país
  globalThis.proj4 = (from, to, p) => (from === 'EPSG:32616' ? [-95, 20] : [-83.75, 9.55]);
  try {
    const c = PI.classifyCRS([[512000, 1050000], [512100, 1050100]]);
    const utm = c.candidates.filter(k => k.crs === 'EPSG:32616')[0];
    assert(utm && utm.inCR === false, 'UTM16 debería marcarse fuera de CR');
    assert(c.best === 'EPSG:5367' || c.best === 'EPSG:8908', 'CRTM05 debería ganar: ' + c.best);
  } finally { globalThis.proj4 = prev; }
});

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

console.log('9) estimateSkew — enderezado por perfil de proyección');
function makeSkewImg(w, h, alphaDeg, spacing) {
  const s = Math.tan(alphaDeg * Math.PI / 180), pix = new Uint8Array(w * h).fill(255);
  for (let y = 0; y < h; y++) for (let x = 0; x < w; x++) {
    const xr = x - s * (y - h / 2);
    if (Math.abs(((xr % spacing) + spacing) % spacing) < 1.5) pix[y * w + x] = 0;
  }
  return pix;
}
t('detecta +3° (±0.5)', () => { const a = PI.estimateSkew(makeSkewImg(200, 200, 3, 20), 200, 200, 8, 0.25); assert(near(a, 3, 0.5), 'a=' + a); });
t('detecta -2.5° (±0.5)', () => { const a = PI.estimateSkew(makeSkewImg(200, 200, -2.5, 20), 200, 200, 8, 0.25); assert(near(a, -2.5, 0.5), 'a=' + a); });
t('imagen derecha → ~0°', () => { const a = PI.estimateSkew(makeSkewImg(200, 200, 0, 20), 200, 200, 8, 0.25); assert(near(a, 0, 0.5), 'a=' + a); });
t('imagen vacía → 0 (sin datos)', () => assert(PI.estimateSkew(new Uint8Array(200 * 200).fill(255), 200, 200) === 0));

console.log('10) cluster1D — agrupación de posiciones de línea');
t('agrupa por cercanía y promedia el centro', () => {
  const c = PI.cluster1D([10, 11, 50, 51, 52, 90], 5);
  assert.strictEqual(c.length, 3);
  assert(near(c[0].pos, 10.5) && c[0].n === 2, 'c0=' + JSON.stringify(c[0]));
  assert(near(c[1].pos, 51) && c[1].n === 3, 'c1=' + JSON.stringify(c[1]));
  assert(near(c[2].pos, 90) && c[2].n === 1, 'c2=' + JSON.stringify(c[2]));
});
t('lista vacía → []', () => assert.strictEqual(PI.cluster1D([], 5).length, 0));
t('desordenada se ordena antes de agrupar', () => {
  const c = PI.cluster1D([52, 10, 90, 11, 50, 51], 5);
  assert(c.length === 3 && near(c[0].pos, 10.5) && near(c[2].pos, 90));
});

console.log('11) detectGridLines — cuadrícula por perfiles de proyección');
function makeGridImg(w, h, xs, ys, thick, bg, ink) {
  bg = bg == null ? 255 : bg; ink = ink == null ? 0 : ink; thick = thick || 1;
  const g = new Uint8Array(w * h).fill(bg);
  xs.forEach(x => { for (let t = 0; t < thick; t++) { const xx = x + t; if (xx < 0 || xx >= w) continue; for (let y = 0; y < h; y++) g[y * w + xx] = ink; } });
  ys.forEach(y => { for (let t = 0; t < thick; t++) { const yy = y + t; if (yy < 0 || yy >= h) continue; for (let x = 0; x < w; x++) g[yy * w + x] = ink; } });
  return g;
}
t('5 verticales × 4 horizontales → 20 intersecciones', () => {
  const g = makeGridImg(400, 300, [60, 120, 180, 240, 300], [50, 110, 170, 230], 2);
  const r = PI.detectGridLines(g, 400, 300);
  assert.strictEqual(r.vX.length, 5, 'vX=' + r.vX.length + ' (' + r.vX + ')');
  assert.strictEqual(r.hY.length, 4, 'hY=' + r.hY.length + ' (' + r.hY + ')');
  assert.strictEqual(r.intersections.length, 20, 'inter=' + r.intersections.length);
  assert(near(r.vX[0], 60.5, 1) && near(r.hY[0], 50.5, 1), 'pos=' + r.vX[0] + ',' + r.hY[0]);
  assert(r.inkDark === true, 'inkDark debería ser true en fondo blanco');
});
t('texto/manchas cortas no generan líneas falsas', () => {
  const g = makeGridImg(400, 300, [60, 120, 180, 240, 300], [50, 110, 170, 230], 2);
  for (let y = 200; y < 220; y++) for (let x = 20; x < 60; x++) g[y * 400 + x] = 0;   // bloque 40×20
  const r = PI.detectGridLines(g, 400, 300);
  assert(r.vX.length === 5 && r.hY.length === 4, 'v=' + r.vX.length + ' h=' + r.hY.length);
});
t('escaneo invertido (líneas claras sobre fondo oscuro)', () => {
  const g = makeGridImg(400, 300, [60, 120, 180, 240, 300], [50, 110, 170, 230], 2, 0, 255);
  const r = PI.detectGridLines(g, 400, 300);
  assert(r.inkDark === false, 'inkDark debería ser false');
  assert(r.vX.length === 5 && r.hY.length === 4, 'v=' + r.vX.length + ' h=' + r.hY.length);
});
t('imagen en blanco → sin líneas', () => {
  const r = PI.detectGridLines(new Uint8Array(200 * 200).fill(255), 200, 200);
  assert(r.vX.length === 0 && r.hY.length === 0, 'v=' + r.vX.length + ' h=' + r.hY.length);
});

console.log('12) simplifyDP — Douglas–Peucker sobre anillo cerrado');
t('recta colineal → 2 puntos', () => assert.strictEqual(PI.simplifyDP([[0, 0], [1, 0], [2, 0], [3, 0]], 0.5).length, 2));
t('cuadrado con puntos intermedios → 4 esquinas (sin vértice espurio)', () => {
  const r = PI.simplifyDP([[0, 0], [5, 0], [10, 0], [10, 5], [10, 10], [5, 10], [0, 10], [0, 5]], 0.5);
  assert.strictEqual(r.length, 4, 'len=' + r.length + ' ' + JSON.stringify(r));
});

console.log('13) traceContour — contorno del predio desde una semilla interior');
function rectImg(w, h, x0, y0, x1, y1, thick) {
  thick = thick || 2;
  const g = new Uint8Array(w * h).fill(255);
  const put = (x, y) => { if (x >= 0 && y >= 0 && x < w && y < h) g[y * w + x] = 0; };
  for (let x = x0; x <= x1; x++) for (let k = 0; k < thick; k++) { put(x, y0 + k); put(x, y1 - k); }
  for (let y = y0; y <= y1; y++) for (let k = 0; k < thick; k++) { put(x0 + k, y); put(x1 - k, y); }
  return g;
}
function polyOutline(w, h, V, thick) {
  const g = new Uint8Array(w * h).fill(255);
  const seg = (x0, y0, x1, y1) => {
    const n = Math.max(Math.abs(x1 - x0), Math.abs(y1 - y0));
    for (let i = 0; i <= n; i++) {
      const x = Math.round(x0 + (x1 - x0) * i / n), y = Math.round(y0 + (y1 - y0) * i / n);
      for (let a = -(thick - 1); a <= thick - 1; a++) for (let b = -(thick - 1); b <= thick - 1; b++) {
        const xx = x + a, yy = y + b; if (xx >= 0 && yy >= 0 && xx < w && yy < h) g[yy * w + xx] = 0;
      }
    }
  };
  for (let i = 0; i < V.length; i++) seg(V[i][0], V[i][1], V[(i + 1) % V.length][0], V[(i + 1) % V.length][1]);
  return g;
}
t('rectángulo → 4 vértices, área ≈ interior', () => {
  const w = 300, h = 220, g = rectImg(w, h, 40, 30, 240, 180, 2);
  const r = PI.traceContour(g, w, h, [140, 100], { close: 1, tol: 3 });
  assert(!r.leaked && r.ring && r.ring.length === 4, 'v=' + (r.ring && r.ring.length) + ' leaked=' + r.leaked);
  const ap = Math.abs(PI.shoelaceArea(r.ring)), expect = (240 - 40 - 4) * (180 - 30 - 4);
  assert(Math.abs(ap - expect) / expect < 0.07, 'areaPx=' + ap + ' esperado≈' + expect);
});
t('L (6 vértices) → 6 vértices', () => {
  const w = 300, h = 300;
  const g = polyOutline(w, h, [[50, 50], [250, 50], [250, 150], [150, 150], [150, 250], [50, 250]], 2);
  const r = PI.traceContour(g, w, h, [80, 80], { close: 1, tol: 4 });
  assert(!r.leaked && r.ring && r.ring.length === 6, 'v=' + (r.ring && r.ring.length) + ' ' + JSON.stringify(r.ring));
});
t('lindero abierto → leaked=true', () => {
  const w = 200, h = 200, g = rectImg(w, h, 30, 30, 170, 170, 2);
  for (let x = 80; x < 120; x++) for (let y = 28; y < 34; y++) g[y * w + x] = 255;   // hueco arriba
  assert.strictEqual(PI.traceContour(g, w, h, [100, 100], { close: 0 }).leaked, true);
});
t('hueco pequeño se cierra con close=3', () => {
  const w = 200, h = 200, g = rectImg(w, h, 30, 30, 170, 170, 2);
  for (let x = 95; x < 100; x++) for (let y = 28; y < 34; y++) g[y * w + x] = 255;   // hueco 5px
  const r = PI.traceContour(g, w, h, [100, 100], { close: 3, tol: 4 });
  assert(!r.leaked && r.ring && r.ring.length === 4, 'v=' + (r.ring && r.ring.length) + ' leaked=' + r.leaked);
});
t('semilla sobre la línea → error explicativo', () => {
  const r = PI.traceContour(rectImg(200, 200, 30, 30, 170, 170, 3), 200, 200, [30, 100], { close: 0 });
  assert(r.ring === null && /línea/.test(r.error || ''), 'error=' + r.error);
});
t('georreferencia con similitud (píxel→E,N con reflexión N-S)', () => {
  // cuadrado en píxeles; grid: 2 pares que definen 1 m/px, N hacia arriba
  const ring = [[100, 100], [300, 100], [300, 260], [100, 260]];   // px (y hacia abajo)
  const pairs = [{ src: [0, -0], dst: [1000, 5000] }, { src: [200, -160], dst: [1200, 5160] }];
  const T = PI.similarityFromPairs(pairs);
  const world = ring.map(p => PI.applySimilarity(T, [p[0], -p[1]]));
  // área en el mundo debe ser 200*160 = 32000 m² y positiva (orientación correcta)
  const a = Math.abs(PI.shoelaceArea(world));
  assert(near(a, 200 * 160, 1), 'área m²=' + a);
});

console.log('14) numericVariants — lecturas alternativas por confusión de OCR');
t('160 incluye 100 (6↔0) sin repetir el original', () => {
  const v = PI.numericVariants('160').map((x) => x.value);
  assert(v.includes(100) && !v.includes(160), JSON.stringify(v));
});
t('respeta decimales (45,8 genera variantes finitas)', () => {
  const v = PI.numericVariants('45,8');
  assert(v.length > 0 && v.every((x) => isFinite(x.value)), 'variantes: ' + JSON.stringify(v));
});

console.log('15) suggestClosureFix — decodificador de cierre (derroteros)');
const sqLegs = (d) => [{ dir: '90', dist: d[0] }, { dir: '180', dist: d[1] }, { dir: '270', dist: d[2] }, { dir: '0', dist: d[3] }];
t('cuadrado que cierra → ok:true', () => {
  const r = PI.suggestClosureFix(sqLegs(['100', '100', '100', '100']), 'azimut');
  assert(r && r.ok === true, JSON.stringify(r));
});
t('distancia mal leída (160↔100) → menor cambio corrige el lado inflado', () => {
  const r = PI.suggestClosureFix(sqLegs(['100', '100', '160', '100']), 'azimut');
  assert(r && r.suggestion, JSON.stringify(r));
  assert(r.suggestion.field === 'dist' && r.suggestion.closureAfter < 0.5, JSON.stringify(r.suggestion));
  assert(r.suggestion.rowIndex === 2 && near(r.suggestion.toValue, 100), 'elegida: ' + JSON.stringify(r.suggestion));
  assert(r.suggestion.alternatives === 2, 'alternativas=' + r.suggestion.alternatives);
});

console.log('16) suggestCoordFix — decodificador de coordenadas');
const rect8 = [[0, 0], [100, 0], [200, 0], [200, 50], [200, 100], [100, 100], [0, 100], [0, 50]];
const toRows = (pts) => pts.map((p) => ({ e: String(p[0]), n: String(p[1]) }));
t('polígono correcto → sin atípico (ok:true)', () => {
  const r = PI.suggestCoordFix(toRows(rect8));
  assert(r && r.ok === true, JSON.stringify(r));
});
t('dígito extra (E 200→290, 0↔9) → sugiere 200 en ese vértice', () => {
  const r = PI.suggestCoordFix(toRows(rect8.map((p, i) => (i === 3 ? [290, 50] : p))));
  assert(r && r.suggestion, JSON.stringify(r));
  assert(r.suggestion.rowIndex === 3 && r.suggestion.field === 'e' && near(r.suggestion.toValue, 200), JSON.stringify(r.suggestion));
});

console.log('17) confidence — semáforo por evidencia');
t('verde: todo coherente', () => assert(PI.confidence({ hasData: true, inCR: true, fromCoords: true }).level === 'green'));
t('ámbar: CRS ambiguo', () => assert(PI.confidence({ hasData: true, inCR: true, crsNeedsUser: true }).level === 'amber'));
t('ámbar: cierre con sugerencia', () => assert(PI.confidence({ hasData: true, inCR: true, fromCoords: false, closureAbs: 12, perimeter: 400, suggestion: {} }).level === 'amber'));
t('rojo: fuera de Costa Rica', () => assert(PI.confidence({ hasData: true, inCR: false }).level === 'red'));
t('rojo: cierre sin corrección', () => assert(PI.confidence({ hasData: true, inCR: true, fromCoords: false, closureAbs: 30, perimeter: 400 }).level === 'red'));

console.log('\nRESULTADO: ' + pass + ' ok, ' + fail + ' fallo(s)');
process.exit(fail ? 1 : 0);
