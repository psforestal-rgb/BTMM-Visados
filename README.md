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

## Actualización y caché

El visor consulta `version.json` con `cache: "no-store"` y agrega `?v=<version>` a
la URL cuando detecta una versión nueva. Para forzar una actualización publicada,
actualizar el valor `version` en `version.json` y el `APP_VERSION` embebido en
`index.html` / `gen_v3.py`.

## Funciones

- Carga de polígono: SHP, GPKG, GPX, KML, KMZ, GeoJSON (con reproyección automática).
- Intersección espacial y cuadro de superficies (ha y % del predio), solo clases > 0.01 ha.
- Mini-mapas por capa, cada uno sobre su ortofoto del período correspondiente.
- Capa de referencias transparente (topónimos, hidrografía, vías) con etiquetas
  priorizadas en un pane superior y líneas suavizadas para evitar solapes.
- Exportación a documento **Word** (.doc) con mapas y tablas.

## Estructura del repositorio

```
index.html      Visor completo y autónomo (datos embebidos)
gen_v3.py       Pipeline Python que genera index.html a partir de los GPKG
version.json    Versión publicada para forzar actualización del navegador
favicon.ico     Icono del sitio
README.md       Este archivo
.gitignore
```

> `gen_v3.py` requiere los GeoPackage originales y `layers_b64.json` (no incluidos por
> tamaño/sensibilidad). El visor publicado (`index.html`) es autosuficiente.

## Créditos y fuentes

- Datos de cobertura: SINAC / FONAFIFO.
- Ortofotos: Instituto Geográfico Nacional (IGN) / SNIT — Costa Rica.
- Imágenes recientes: Esri World Imagery.
- Bibliotecas: Leaflet, Turf.js, proj4js, shpjs, sql.js, pako, JSZip, togeojson.

SINAC — Área de Conservación Central — Bloque Tapantí Macizo de la Muerte.
