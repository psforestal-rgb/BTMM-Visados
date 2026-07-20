# Política de seguridad — BTMM-Visados

## Modelo de seguridad

- Sitio estático público en GitHub Pages, **sin backend, sin autenticación,
  sin secretos y sin datos personales**: todas las capas publicadas son
  información pública (propietario «ESTADO» en fincas/PNE). Todo el
  geoproceso ocurre en el navegador; los polígonos analizados **no se suben
  a ningún servidor** (las teselas de mapa sí revelan la zona consultada a
  los servicios de mapas — inherente a usar mapas base en línea).
- Librerías de terceros fijadas por versión exacta + **SRI sha384** y
  **Content-Security-Policy** restrictiva (orígenes de script limitados a
  `self` + jsDelivr; `object-src 'none'`, `frame-src 'none'`).
- PDF.js opera con `isEvalSupported:false` (mitiga CVE-2024-4367: un PDF
  malicioso no puede ejecutar JavaScript).
- El asistente **«Importar predio desde plano»** procesa el plano y ejecuta el
  **OCR íntegramente en el navegador**: no hay servicio externo de OCR y ni el
  plano ni las coordenadas transcritas se envían a ningún servidor. Tesseract.js
  se carga **bajo demanda** (solo al abrir el asistente), con **SRI** en el script
  principal y en un **Web Worker**; sus recursos (worker, core WASM y modelo de
  idioma) se sirven desde jsDelivr, dentro de la CSP vigente (`script-src`/
  `connect-src` limitados a `self` + jsDelivr; `worker-src 'self' blob:`). El
  plano pasa antes por la **revisión local de seguridad** (misma que el módulo de
  plano), el texto del OCR se **escapa** antes de mostrarse y los workers, canvas
  e imágenes se liberan al terminar o cancelar. La geometría resultante se marca
  como «derivada de plano» y debe verificarse contra la cartografía oficial.
- El proxy OGC (Cloudflare Worker) tiene lista blanca de dominios destino,
  bloqueo de IPs privadas, límites de tamaño/tiempo y no maneja credenciales.

## Reportar una vulnerabilidad

1. **Preferido:** GitHub → pestaña *Security* → *Report a vulnerability*
   (reporte privado).
2. Alternativa: issue con la plantilla «Vulnerabilidad de seguridad», **sin
   detalles explotables** si el riesgo es alto.

Incluya: versión afectada (`BTMM_APP_VERSION` en la consola), componente,
impacto probable y pasos mínimos. No incluya tokens, datos personales ni
planos confidenciales.

## Verificaciones automáticas

- **CI (cada push/PR):** consistencia de versiones/SRI/CSP, smoke test en
  Chromium contra el CDN real y escaneo de secretos (gitleaks).
- **Semanal:** verificación de que el CDN sirve exactamente los bytes
  esperados (hash SRI) — detecta manipulación de la cadena de suministro —
  y sondeo de los servicios externos. Los fallos abren un issue etiquetado
  `vigilancia-automatica`.

## Alcance

Este repositorio cubre el visor (`index.html`, `gen_v3.py`, `data/`). El
Worker proxy se administra en Cloudflare y no forma parte del repo; los
servicios SNIT/Esri/Dirección de Agua son de terceros.
