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
| FONAFIFO 2005 | FONAFIFO | cobertura | Ajustada +210 m X / −150 m Y (CRTM05) respecto a FONAFIFO 2000; traslación rígida, sin modificar geometría interna. Uso agropecuario / No forestal se simboliza en amarillo |
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
- Carga de plano PDF o imagen como capa referencial, con selección previa del modo
  de georreferenciación. El modo **Automático** detecta el contorno, recorta el
  dibujo y valida el calce sin alterar la geometría oficial ni los cálculos.
- El modo **Manual** precarga el plano completo y habilita la captura de pares
  plano/vector, con ajuste al vértice vectorial más cercano y transformación afín
  a partir de tres o más pares. Si el modo automático falla, conserva el plano y
  activa esta ruta manual.
- Módulo **Importar predio desde plano**: asistente que deriva el polígono del
  predio a partir de un plano (PDF/TIF/PNG/JPG) por **listado de coordenadas
  Este–Norte**, **derrotero de rumbo y distancia** o **azimut y distancia**. El
  plano pasa por la revisión local de seguridad; PDF.js lo convierte en imagen y
  el usuario elige página, rota, recorta y selecciona el recuadro a leer. El
  **OCR es local y bajo demanda** (Tesseract.js en un Web Worker; sin servicios
  externos de OCR) y siempre desemboca en una **tabla editable con confirmación
  humana** (la escritura manuscrita se trata como transcripción asistida). Detecta
  CRS solo con evidencia (CRTM05/EPSG:5367, Lambert Norte/Sur, UTM 16/17N o
  geográficas) y **exige selección del usuario si es incierto**. Calcula área,
  perímetro y **error de cierre absoluto y relativo** (nunca ajusta el cierre ni
  las distancias en silencio) y la diferencia frente al área escrita en el plano.
  La ubicación es por coordenadas absolutas, punto de amarre o cuadrícula del
  minimapa («ubicación aproximada derivada del recuadro cartográfico»), con
  **ajuste final rígido** (traslación Este/Norte y rotación, sin escalar ni mover
  vértices, con deshacer/restablecer) sobre Leaflet. Al aceptar, el resultado se
  incorpora vía `addUser()` y continúa por el flujo normal de análisis e informe.
  El GeoJSON conserva la procedencia (archivo fuente, tipo de extracción, CRS
  original, datos transcritos, área y cierre, método de ubicación, traslación y
  rotación, confianza e indicación «geometría derivada de plano»).
- Capa de referencias transparente (topónimos, límites y vías) con etiquetas
  priorizadas en un pane superior y líneas suavizadas para evitar solapes.
- Exportación a documento **Word** (.docx) sobre el **membrete institucional
  oficial SINAC-ACC** (encabezado y pie en todas las páginas). El informe reúne
  únicamente los módulos seleccionados en el checklist del panel **Informe final**,
  entre aquellos cuyos análisis ya estén listos. Los resultados se organizan en el
  mismo orden que los módulos del visor, con sus mapas y tablas en una sola columna.
  **Cada mapa ocupa una página independiente**, junto con su título, fuente y un
  espacio para comentario. En el encabezado se agrega el título
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
- **Revisión de seguridad de archivos**: antes de usar un plano PDF/imagen y antes
  de descargar el informe Word, el visor ejecuta una verificación local en el
  navegador (estructura, indicadores de contenido activo —JavaScript, adjuntos,
  ejecutables, macros— y huella SHA-256, sin enviar el archivo a ningún servicio)
  y muestra el resultado con opción de continuar o cancelar. No sustituye a un
  antivirus: la huella SHA-256 permite verificar el archivo en el antivirus
  corporativo o en virustotal.com sin subir el documento.

## Estructura del repositorio

```
index.html          Visor completo y autónomo (datos y membrete embebidos)
gen_v3.py           Pipeline Python que genera index.html a partir de los GPKG
data/               GPKG locales de los módulos ASP y Fincas estatales y PNE (se sirven y cargan en runtime)
scripts/            Verificaciones: consistencia, integridad CDN (SRI) y smoke test E2E
.github/            CI, vigilancia semanal de dependencias, Dependabot y plantillas de issues
membrete_sinac.dotx Plantilla Word del membrete institucional SINAC-ACC (export .docx)
version.json        Versión publicada para forzar actualización del navegador
favicon.ico         Icono del sitio
logo.png            Logo institucional (512 px optimizado)
MANTENIMIENTO.md    Guía operativa: probar, desplegar, actualizar dependencias, rollback
SECURITY.md         Modelo de seguridad y cómo reportar vulnerabilidades
README.md           Este archivo
.gitignore
```

## Mantenimiento, seguridad y verificación

- Librerías de terceros **fijadas por versión + SRI sha384** (jsDelivr) y
  **Content-Security-Policy** restrictiva: las actualizaciones de terceros no
  pueden alterar el código que ejecuta el visor.
- **CI** en cada push/PR: consistencia del repo, smoke test E2E en Chromium y
  escaneo de secretos. **Vigilancia semanal** del contrato con el CDN y de los
  servicios externos, con apertura de issue deduplicado si algo se rompe.
- Errores en runtime: el visor los registra sanitizados en memoria;
  `btmmReporteErrores()` en la consola (F12) descarga un JSON para adjuntar a
  un issue.
- Detalles en [MANTENIMIENTO.md](MANTENIMIENTO.md) y [SECURITY.md](SECURITY.md).

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
- **Bibliotecas:** Leaflet, Turf.js, proj4js, shpjs, sql.js, pako, JSZip,
  togeojson, PDF.js, UTIF y Tesseract.js (OCR local, carga diferida solo al abrir
  el asistente «Importar predio desde plano»).

SINAC — Área de Conservación Central — Bloque Tapantí Macizo de la Muerte.
