# BTMM-Visados — Visor de Cobertura Forestal (PNLQ)

Visor web autónomo de cobertura forestal para el **Parque Nacional Los Quetzales (PNLQ)**,
SINAC — Área de Conservación Central — Bloque Tapantí Macizo de la Muerte.

Permite cargar un polígono de análisis (predio) y calcular su intersección con cinco
capas de cobertura, a **resolución geométrica completa** y con **cálculo de áreas en
proyección CRTM05 / EPSG:5367** (coincidente con QGIS).

## Acceso

- **Visor en línea:** https://psforestal-rgb.github.io/BTMM-Visados/
- También funciona como archivo único abierto localmente (`index.html`).

## Capas de cobertura (orden cronológico)

| Capa | Fuente | Campo | Notas |
|------|--------|-------|-------|
| FONAFIFO 2000 | FONAFIFO | USO_COBERT | |
| FONAFIFO 2005 | FONAFIFO | cobertura | Ajustada +210 m X / −150 m Y (CRTM05) respecto a FONAFIFO 2000; traslación rígida, sin modificar geometría interna |
| Tipos de Bosque 2012 | SINAC | TipoBosque | |
| Cobertura Forestal 2021 | SINAC | Clase | |
| Cobertura Forestal 2023 | SINAC | Clase | Activa por defecto |

Los datos se embeben en el HTML comprimidos (gzip + base64), a resolución completa
(solo redondeo de coordenadas a 6 decimales ≈ 0.11 m, sin simplificación geométrica).

## Imágenes aéreas

Tarjeta "Imágenes aéreas" con ortofotos SNIT-IGN vía WMS/WMTS. Las capas SNIT se
enrutan por un proxy OGC (Cloudflare Worker) que añade CORS y caché:

- Ortofoto TERRA 1997 — WMTS SNIT-IGN
- Ortofoto 2005-2007 — WMS SNIT-IGN (`Mosaico5000`)
- Ortofoto 2014-2017 — WMS SNIT-IGN (`ortofoto2017_5000_altaresolucion`)
- Imagen aérea 2021 / 2023 — Esri World Imagery (Wayback)

> Las ortofotos del SNIT son de escala 1:5000: se deben ver acercando el zoom.
> Las imágenes Esri Wayback usan sobreampliación hasta zoom 22 cuando la fuente
> nativa no publica más detalle que zoom 19.

## Actualización y caché

El visor consulta `version.json` con `cache: "no-store"` y agrega `?v=<version>` a
la URL cuando detecta una versión nueva. Para forzar una actualización publicada,
actualizar el valor `version` en `version.json` y el `APP_VERSION` embebido en
`index.html` / `gen_v3.py`.

## Funciones

- Carga de polígono: SHP, GPKG, GPX, KML, KMZ, GeoJSON (con reproyección automática).
- Intersección espacial y cuadro de superficies (ha y % del predio), solo clases > 0.01 ha.
- Mini-mapas por capa, cada uno sobre su ortofoto del período correspondiente.
- Módulo **Áreas Silvestres Protegidas**: capa ASP local con simbología por área y
  análisis de traslape (mini-mapas sin imagen aérea y cuadro de área por ASP).
- Módulo **Fincas estatales y PNE**: carga de cuatro capas locales (Buffer 2 km
  Carretera Interamericana, PNE del SNIT, Terrenos sobre 3000 m y Fincas del Estado
  ACC) y análisis "Info PNE" que genera un mini-mapa del predio por capa y la tabla
  de estimación de traslape (área en ha y % del predio; con número de finca e
  información del plano para PNE del SNIT y Fincas del Estado ACC).
- Botón de zoom al polígono cargado, disponible en todas las pestañas con visor.
- Carga de plano PDF como capa referencial: detecta visualmente el contorno del
  predio en la primera página, recorta el dibujo, elimina el fondo blanco y lo
  muestra como dibujo transparente sobre todas las capas, sin alterar la geometría
  oficial ni los cálculos de cobertura. El recorte se valida contra el perímetro
  del polígono cargado para evitar montajes desplazados por rótulos del PDF.
- Si la detección automática del PDF no calza, el plano se carga de todos modos
  como referencia transparente. El botón **Ajuste manual** permite marcar pares
  de puntos plano/vector, con snapping al vértice vectorial más cercano, y aplicar
  un ajuste affine con un mínimo de tres pares.
- Capa de referencias transparente (topónimos, límites y vías) con etiquetas
  priorizadas en un pane superior y líneas suavizadas para evitar solapes.
- Exportación a documento **Word** (.docx) sobre el **membrete institucional
  oficial SINAC-ACC** (encabezado y pie en todas las páginas), con mapas
  combinados imagen/cobertura en una sola columna, centrados, con simbología por
  vista y flecha norte. El cuerpo del informe se incrusta en la plantilla oficial
  (`membrete_sinac.dotx`) mediante `altChunk`; para ver el contenido incrustado se
  recomienda abrir el archivo con Microsoft Word.

## Estructura del repositorio

```
index.html          Visor completo y autónomo (datos y membrete embebidos)
gen_v3.py           Pipeline Python que genera index.html a partir de los GPKG
data/               GPKG locales de los módulos ASP y Fincas estatales y PNE (se sirven y cargan en runtime)
membrete_sinac.dotx Plantilla Word del membrete institucional SINAC-ACC (export .docx)
version.json        Versión publicada para forzar actualización del navegador
favicon.ico         Icono del sitio
README.md           Este archivo
.gitignore
```

> `gen_v3.py` requiere los GeoPackage originales y `layers_b64.json` (no incluidos por
> tamaño/sensibilidad). Puede leer `layers_b64.json` junto al script o desde la
> variable `LAYERS_B64_PATH`. El membrete se toma de `membrete_sinac.dotx` (junto al
> script o desde `MEMBRETE_DOTX_PATH`) y se embebe en base64. El visor publicado
> (`index.html`) es autosuficiente.

## Créditos y fuentes

- Datos de cobertura: SINAC / FONAFIFO.
- Ortofotos: Instituto Geográfico Nacional (IGN) / SNIT — Costa Rica.
- Imágenes recientes: Esri World Imagery.
- Bibliotecas: Leaflet, Turf.js, proj4js, shpjs, sql.js, pako, JSZip, togeojson.

SINAC — Área de Conservación Central — Bloque Tapantí Macizo de la Muerte.
