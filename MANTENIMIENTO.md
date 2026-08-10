# Guía de mantenimiento — BTMM-Visados

Documento operativo para mantener el visor con el mínimo de intervenciones.
Complementa el `README.md` (funcional) y `SECURITY.md` (seguridad).

## Arquitectura en una frase

Sitio **100 % estático** en GitHub Pages: un `index.html` autosuficiente
(datos de cobertura embebidos gzip+base64) generado por `gen_v3.py`, más
capas GPKG en `data/` que se descargan bajo demanda. **No hay backend, base
de datos, variables de entorno ni secretos**; todo el geoproceso corre en el
navegador. La única pieza de infraestructura propia es el proxy OGC
(Cloudflare Worker `psforgis-ocg`), que solo añade CORS y caché a servicios
públicos.

## Instalar / ejecutar

No hay instalación. Opciones:

- **Producción:** https://psforestal-rgb.github.io/BTMM-Visados/
- **Local:** `python3 -m http.server 8791` en la raíz y abrir
  `http://127.0.0.1:8791/index.html` (también funciona abriendo el archivo
  directamente, con módulos de red limitados).

## Probar

```bash
python3 scripts/check_consistency.py       # invariantes del repo (sin red)
python3 scripts/check_cdn_integrity.py     # contrato con el CDN (necesita red)
node scripts/plano_import.test.mjs         # núcleo «Importar predio desde plano» (sin red)
npm i playwright && npx playwright install chromium
node scripts/smoke_test.mjs                # E2E: carga, SRI, CSP, análisis
```

`plano_import.test.mjs` extrae el núcleo determinista embebido en `index.html`
(marcadores `__PI_CORE_START__`/`__PI_CORE_END__`) y lo prueba en Node sin red:
rumbo→azimut (W y O como oeste), G/M/S, coma/punto decimal, construcción y error
de cierre, traslación/rotación sin alterar el área, área CRTM05 de un
FeatureCollection y clasificación de CRS.

Los tres se ejecutan automáticamente en GitHub Actions (`ci.yml` en cada
push/PR; `vigilancia-dependencias.yml` cada lunes).

## Desplegar

Merge a `main` publica automáticamente en GitHub Pages. Para forzar que los
navegadores tomen la versión nueva: subir `APP_VERSION` en `index.html` **y**
`gen_v3.py`, y `version` en `version.json` (los tres deben coincidir;
`check_consistency.py` lo verifica y el CI bloquea si difieren).

**Convención de versión (obligatoria): fecha de la última actualización.** El
string de versión tiene el formato `AAAA-MM-DD-<slug>-v<N>`, donde `AAAA-MM-DD`
es **la fecha real en que se hace la actualización** (no una fecha heredada) y
`<N>` es un contador que aumenta en cada publicación. En `version.json`, el
campo `updated` debe llevar esa misma fecha. `check_consistency.py` verifica que
la fecha del string de versión coincida con `updated` (el CI bloquea si no).
Ejemplo: una actualización hecha el 10 de agosto de 2026 usa
`2026-08-10-<slug>-v<N>` y `"updated": "2026-08-10T..."`.

## Rollback

```bash
git revert <commit>   # o git revert <rango>
git push origin main
```
Al ser un sitio estático sin estado, revertir el commit ES el rollback
completo. Subir versión en `version.json` para forzar la recarga de clientes.

## Regenerar index.html

`gen_v3.py` requiere `layers_b64.json` y `membrete_sinac.dotx` (el primero
**no** está en el repo por tamaño/sensibilidad; consérvese en respaldo
privado — sin él solo se puede editar `index.html` a mano, replicando cada
cambio en `gen_v3.py` para no perder la fuente). El script imprime ~100
auto-verificaciones (✅/❌) del HTML generado; no publicar si alguna falla.

## Dependencias

### Críticas (fijadas por versión exacta + hash SRI, servidas por jsDelivr)

| Librería | Versión | Rol | Riesgo si falta |
|---|---|---|---|
| Leaflet | 1.9.4 | mapa | total |
| Turf.js | 6.5.0 | geoproceso (intersecciones, áreas) | análisis |
| proj4js | 2.9.2 | reproyección CRTM05 | áreas erróneas |
| sql.js | 1.10.3 | lectura GPKG (WASM) | carga de predios |
| pako | 2.1.0 | descompresión de datos embebidos | total |
| shpjs / JSZip / togeojson | 4.0.4 / 3.10.1 / 0.16.0 | formatos de entrada | carga de predios |
| PDF.js | 3.11.174 | plano PDF (con `isEvalSupported:false`) | módulo plano |
| UTIF | 3.1.0 | plano TIFF (carga diferida) | módulo plano |
| Tesseract.js | 5.1.1 | OCR local del asistente «Importar predio desde plano» (carga diferida + SRI en el script principal; worker, core WASM y `eng.traineddata` los carga la propia librería desde jsDelivr, dentro de la CSP y en un Web Worker) | módulo importar-plano (degrada a transcripción manual) |

**Decisiones tomadas para minimizar cambios futuros:**

- Versiones **exactas** en la URL + **SRI sha384**: ninguna actualización del
  CDN o del paquete puede cambiar el código que ejecuta el visor. El visor no
  se rompe por actualizaciones de terceros; solo puede romperse si el CDN
  *retira* un archivo, y eso lo detecta la vigilancia semanal antes que los
  usuarios (jsDelivr mantiene versiones antiguas indefinidamente).
- jsDelivr sirve **byte a byte** los paquetes de npm: los hashes son
  verificables contra `npm pack <paquete>@<versión>`.
- **Política de actualización: manual y deliberada** (no automática). Las
  librerías solo se actualizan por (a) CVE que afecte al visor o (b)
  necesidad funcional. No hay valor en perseguir versiones nuevas de un
  visor estable; cada cambio de versión exige regenerar hashes y pasar el
  smoke test. Dependabot solo vigila las GitHub Actions (mensual).

### Cómo actualizar una librería

1. `npm pack <paquete>@<versión-nueva>` y extraer el archivo dist.
2. Hash: `openssl dgst -sha384 -binary <archivo> | openssl base64 -A`.
3. Actualizar URL + `integrity` en `index.html` **y** `gen_v3.py` (misma
   cadena en ambos).
4. `python3 scripts/check_consistency.py && node scripts/smoke_test.mjs`.
5. Subir versión (v-siguiente) en los tres archivos de versión y publicar.

Nota: PDF.js ≥ 4.x es solo módulos ES; migrarlo requiere cambiar la forma de
carga (ver «Riesgos residuales» en el informe de revisión). Mientras tanto,
`isEvalSupported:false` neutraliza CVE-2024-4367 en la 3.11.174.

## Servicios externos (runtime)

| Servicio | Uso | Si falla |
|---|---|---|
| Proxy OGC `psforgis-ocg.psforestal.workers.dev` | CORS/caché para SNIT y Dirección de Agua | ortofotos SNIT y dictámenes no cargan; análisis local sigue |
| SNIT (`geos0/geos1.snitcr.go.cr`) | ortofotos WMS/WMTS | mini-mapas sin fondo histórico; hay fallback EOX |
| Dirección de Agua (`mapas.da.go.cr`) | WMS dictámenes | tarjeta de fuentes sin capas WMS |
| Esri (`*.arcgis.com`) | imagen aérea, referencias, Wayback | fondos y referencias no cargan |
| EOX (`tiles.maps.eox.at`) | fallback Sentinel-2 | sin fallback de imagen |

El visor ya degrada por capa (tesela transparente en error, fallback de
ortofoto tras 2 errores, mensajes por tarjeta). La caída de un servicio
**nunca** debe bloquear el análisis local: eso es un bug reportable.

## Errores registrados

- **Runtime (usuarios):** el visor captura errores no manejados y rechazos
  de promesas en memoria, sanitizados (sin URLs completas ni rutas). En la
  consola del navegador (F12): `btmmReporteErrores()` descarga un JSON para
  adjuntar al issue «Reporte de error». No se envía nada a ningún servidor.
- **Issues automáticos:** el workflow semanal de vigilancia abre o actualiza
  **un único** issue etiquetado `vigilancia-automatica` cuando el contrato
  SRI con el CDN se rompe (severidad alta), OSV.dev reporta una CVE conocida
  contra la versión exacta de un paquete npm fijado (severidad alta) o un
  servicio externo no responde (severidad media). Deduplica comentando en el
  issue abierto existente. Se desactiva con la variable de repositorio
  `VIGILANCIA_ISSUES=off`. Usa el `GITHUB_TOKEN` efímero del workflow con
  permiso mínimo (`issues: write`); no hay tokens personales que configurar.
- **Interpretación:** issue de integridad o de CVE ⇒ actuar ya (sección «Cómo
  actualizar una librería»); issue de servicio ⇒ verificar si es transitorio
  (reintentar el workflow con *Run workflow*) antes de tocar código.

## Ante una vulnerabilidad

Ver `SECURITY.md`. Regla rápida: si es de una librería fijada, actualizar esa
librería con el procedimiento de arriba; si es del visor, corregir en
`index.html` + `gen_v3.py` y subir versión; si es del Worker, corregirla en
Cloudflare (el código del Worker no vive en este repo).
