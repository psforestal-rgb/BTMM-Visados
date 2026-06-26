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

> **Fecha real de la imagen aérea.** El rótulo de cada versión Wayback es su fecha
> de *publicación*, no la de *captura*. En zonas remotas (como el PNLQ) Esri suele
> reutilizar la misma imagen durante varias versiones, por lo que 2021 y 2023 pueden
> verse idénticas pese a sus rótulos. Por eso el título de cada mini-mapa muestra la
> **fecha real de captura** consultada en tiempo de ejecución a la capa de metadatos
> de la versión elegida (`World_Imagery_Metadata_*`); si ambas versiones comparten la
> misma imagen, se muestra un aviso y la misma fecha real en los dos mini-mapas. La
> imagen "más reciente / dibujo del plano" toma su fecha del servicio World Imagery
> vigente.

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
- Módulo **Terrenos forestales**: relieve (7 clases de pendiente) e inundación. El
  cálculo de relieve usa **estadística zonal ráster**: una grilla de clases de 1 byte
  a 5 m en CRTM05/EPSG:5367 (`data/btmm_relieve_clases_5m.bin.gz`, ~3.9 MB, descarga
  única) que se muestrea por celda dentro del predio — instantáneo y sin cargar el
  vector pesado. Reporta área y % por clase e inclinación promedio/mín/máx.
- Módulo **Fuentes de agua y AP**: capa local de **cauces y drenaje** (líneas) que
  muestra el nombre del cauce al pasar el cursor (sin geoproceso), y capas del **WMS
  de la Dirección de Agua** (`mapas.da.go.cr`) descubiertas automáticamente vía el
  proxy OGC, con toggles por capa y control de opacidad.
- Módulo **Fincas estatales y PNE**: carga de cuatro capas locales (Buffer 2 km
  Carretera Interamericana, PNE del SNIT, Terrenos sobre 3000 m y Fincas del Estado
  ACC) y análisis "Info PNE" que genera un mini-mapa del predio por capa y la tabla
  de estimación de traslape (área en ha y % del predio; con número de finca e
  información del plano para PNE del SNIT y Fincas del Estado ACC).
- Botón de zoom al polígono cargado, disponible en todas las pestañas con visor.
- Capa opcional de **imagen aérea reciente** (Esri World Imagery, con sobreampliación)
  como fondo del visor, activable desde la tarjeta de Referencias en todas las pestañas.
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
  oficial SINAC-ACC** (encabezado y pie en todas las páginas). El informe reúne
  los resultados de **todos los análisis realizados**, **organizados en el mismo
  orden que los módulos del visor** (Áreas Silvestres Protegidas → Fincas/PNE →
  Cobertura Forestal → Terrenos forestales → Fuentes de agua y AP), con sus mapas
  y tablas en una sola columna. Cada mapa y su título se mantienen en la misma
  página (sin grandes espacios en blanco) y debajo de cada mapa se deja un
  **espacio para comentario** (~5 líneas). En el encabezado se agrega el título
  **«Anexo a informe N.° ____ — pág. n de N»** (con campos de paginación
  automática de Word). Cada mapa incorpora **grilla de coordenadas CRTM05/EPSG:5367**
  (dos líneas verticales y dos horizontales en valores enteros terminados en 00,
  con etiquetas E/N), **escala numérica** (denominador terminado en 00) y **escala
  gráfica**, además de flecha de norte, simbología por vista e indicación de
  **proyección y fuentes** usadas. El cuerpo del informe se incrusta en la
  plantilla oficial (`membrete_sinac.dotx`) mediante `altChunk`; para ver el
  contenido incrustado se recomienda abrir el archivo con Microsoft Word.
- La ventana de resultados permanece abierta al cambiar de pestaña (se cierra con
  el botón ✕ o al limpiar el predio).

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

Fuentes de información por capa (información actualizada al **2026-06-25**):

- **Relieve:** elaboración propia a partir de curvas de nivel a 10 m de la
  cartografía 1:25.000 publicada en SNIT.
- **Cobertura forestal:** datos vectoriales descargados de servicios WMS —
  Cobertura 2021 y 2023 del SNIT; FONAFIFO 2000 y 2005 del CENIGA.
- **Cauce y drenaje:** datos vectoriales descargados de servicios WMS de la
  cartografía 1:25.000 publicada en SNIT.
- **Potencial de inundación:** información de la Comisión Nacional de
  Emergencias (CNE) publicada en SNIT.
- **Áreas Silvestres Protegidas y Patrimonio Natural del Estado (PNE):** datos
  vectoriales descargados de servicios WMS de la información del SINAC publicada
  en SNIT.
- **Fincas del Estado (ACC):** capa proporcionada por el Área de Conservación
  Central (ACC).
- **Imágenes aéreas recientes:** Esri World Imagery. Ortofotos: IGN / SNIT — Costa Rica.
- **Bibliotecas:** Leaflet, Turf.js, proj4js, shpjs, sql.js, pako, JSZip, togeojson.

SINAC — Área de Conservación Central — Bloque Tapantí Macizo de la Muerte.
