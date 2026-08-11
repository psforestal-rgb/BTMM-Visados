# Investigación: automatizar la carga y georreferenciación de planos (PDF/imagen)

Síntesis de cinco informes de investigación profunda (Perplexity, Gemini y tres
variantes de Claude/GPT) sobre cómo reducir al máximo los pasos manuales del
módulo **«Importar predio desde plano»**, filtrada por las restricciones reales
de este repositorio y mapeada al código existente.

> Estado: documento de diseño / planificación. No cambia el visor. Sirve para
> decidir el orden de implementación.

---

## 1. Consenso de los cinco informes

Coinciden con fuerza en lo esencial:

1. **No usar un único modelo de IA.** La mejor relación precisión/peso/auditabilidad
   es una **cascada «determinista primero, ML solo donde aporta»**.
2. **Explotar primero la estructura que ya existe**, en este orden:
   `PDF con texto nativo → deskew/orientación → detección estructural de
   cuadrícula y tabla → OCR por celda/token → reconstrucción geométrica con
   restricciones (cierre) → contorno → registro → confianza por evidencia →
   una sola confirmación final`.
3. **OpenCV.js es la pieza central de visión** (Hough, contornos, morfología,
   `adaptiveThreshold`, estimadores afines con RANSAC). Carga diferida, en Web
   Worker, fijada por versión + SRI.
4. **Tesseract.js sigue siendo el OCR base**; lo que cambia es la *unidad* de
   reconocimiento: leer **celdas y tokens con tipo conocido** (whitelist por
   columna) y **no normalizar los números demasiado pronto** — mantener
   alternativas y desambiguar con la geometría (rango del CRS + error de cierre).
5. **PaddleOCR/ONNX = opcional y diferido**, reempacado con SRI, y **solo** tras
   medir que Tesseract + visión clásica fallan en una cohorte real. **TrOCR
   (~247 MB) se descarta**; la manuscrita queda como **transcripción asistida**.
6. **La automatización de mayor impacto es la lectura de la cuadrícula**
   (Hough + periodicidad + OCR de rótulos + afín/RANSAC): elimina el marcado
   manual de puntos de control, que es hoy el paso más costoso.
7. **Confianza = sistema de evidencia con procedencia, alternativas y
   residuales** (RMSE en px *y* en metros, nº de inliers), no un promedio ciego.
   Semáforo verde/ámbar/rojo; **ámbar = una pregunta específica**, no volver al
   flujo manual completo.
8. **Nunca ajustar el cierre en silencio** (ya es el principio actual): sugerir
   Bowditch/Transit/mínimos cuadrados, jamás imponer.

---

## 2. Verificación de hechos técnicos (para no decidir sobre supuestos)

Pesos y versiones reales (fuente: registro npm, agosto 2026):

| Paquete | Versión | Peso (unpacked) | Observación |
|---|---|---|---|
| `@techstark/opencv-js` | `5.0.0-release.1` | ~14.7 MB | build completo; servido gz es menos, pero es pesado para un archivo único. Considerar build recortado (core+imgproc+calib3d). |
| `tesseract.js` | `7.0.0` | ~1.4 MB (JS) | el repo usa 5.1.1; subir a 7 es opcional (afirma 15–35 % más rápido). |
| `tesseract.js-core` | `6.1.2` | ~30.6 MB | incluye varias variantes WASM; solo se carga una (~3 MB). |
| `onnxruntime-web` | `1.27.0` | ~137 MB (paquete) | se usan archivos sueltos: JS ~350 KB + WASM SIMD ~13 MB. |
| `@paddleocr/paddleocr-js` | `0.4.2` | ~23.8 MB | SDK oficial de navegador; incluye modelos. |

**CSP / SRI / `file://` (restricción dura, verificada):**

- Los `<script>`/`<link>` de jsDelivr con versión exacta + SRI ya funcionan (es
  el patrón actual del repo). Para `.wasm`, `.onnx`, `traineddata` y Workers,
  **el atributo `integrity` de HTML no aplica**: hay que usar
  `fetch(url, { integrity: "sha384-…" })` (metadatos de integridad del estándar
  Fetch), verificar y solo entonces entregar al runtime o convertir a `Blob`.
- `worker-src 'self' blob:` **no permite** construir un Worker desde una URL de
  jsDelivr: hay que cargar/verificar el código y crear un `blob:` Worker (o un
  Worker de primer nivel incluido en `index.html`). OpenCV.js/ORT/Tesseract
  encajan si se sigue este patrón.
- **`file://`**: la línea base debe seguir funcionando sin descargas (Canvas +
  parsers `PI.*` + tabla editable + confirmación manual). OpenCV/OCR/ONNX son
  mejoras *lazy-load* que requieren conectividad → se activan solo en modo
  GitHub Pages o mediante selector de archivos.

**CRS — corrección relevante y su alcance real:**

- Marco oficial CR: **CR‑SIRGAS** (referencia horizontal) + **CRTM05**
  (proyección). Códigos: `EPSG:5367` = CR05/CRTM05 (histórico, masivo en planos),
  `EPSG:8908` = CR‑SIRGAS/CRTM05, `EPSG:5456/5457` = Lambert Norte/Sur,
  `EPSG:32616/32617` = UTM 16/17N.
- **En este repo, `5367` y `8908` están definidos con la misma cadena proj4**
  (`+proj=tmerc … +ellps=WGS84`). La diferencia CR05↔CR‑SIRGAS es de
  *realización de datum* (sub‑métrica) → en la práctica del visor la
  reproyección es idéntica. Conclusión: tratar 8908 como **candidato etiquetado**
  (procedencia/UI y confirmación humana), no como una geometría distinta.

---

## 3. Decisiones abiertas (con recomendación)

| Tema | Recomendación |
|---|---|
| Empaquetado `file://` vs Pages | **Dos niveles**: núcleo determinista siempre local; OpenCV/OCR/ONNX diferidos solo con red. No prometer CDN en `file://`. |
| Peso de OpenCV.js | Empezar con `@techstark/opencv-js` fijado + SRI, carga diferida en Worker; si el peso molesta, **build recortado propio** (core+imgproc+calib3d) publicado como paquete versionado. Decidir antes de la Fase 2. |
| 5367 vs 8908 | Añadir 8908 como candidato en `PI.classifyCRS` (etiqueta + confirmación), reproyección idéntica. Si algún día se requiere el shift real de datum, añadir `towgs84`/pipeline específico. |
| Tesseract 5.1.1 → 7.0.0 | Opcional; revisar al tocar OCR. No es prioridad. |
| Registro contra vector (F) | Menor prioridad: el flujo principal **deriva** el polígono del plano (no hay vector previo). F aplica sobre todo al modo de georreferenciación del plano ya existente (`detectPdfPredioBox`). Priorizar A/B/C/E/G. |
| PaddleOCR / ORT | Solo tras medir % de planos en ámbar/rojo con Tesseract+geometría. Reempacar modelos en npm propio con SRI; ejecutar con ORT Web (`wasm`, `numThreads=1`) para no depender de COOP/COEP. |

---

## 4. Mapeo al código actual (qué reutilizar / extender)

| Punto | Dónde encaja hoy | Cambio |
|---|---|---|
| **E** deskew/orientación/recorte | `piWorkingCanvas()`, `piRotate()`, `piCrop*` | Nuevo módulo OpenCV.js (Hough/ángulo modal + cuadrilátero de página + warp) antes del recuadro manual. |
| **B** cuadrícula automática | paso «Ubicar» → `piGridCompute()`, `PI.similarityFromPairs` | Auto‑detectar intersecciones + OCR de rótulos en ROI; **subir de similitud a afín + RANSAC**. Reduce el marcado manual a confirmación visual. |
| **C** OCR por token + decoder | `piParseOCR`, `PI.parseNumber/parseCoord/parseDMS/parseBearing`, `PI.buildTraverse` | Añadir corto‑circuito `PDF.js getTextContent()`; mantener alternativas por token y beam‑search que use rango de CRS + cierre para desambiguar. |
| **A** contorno del lindero | `detectPdfPredioBox` (flood‑fill) | Añadir ruta OpenCV: supresión reversible de grilla/texto → morfología → contornos + grafo de segmentos → ranking por concordancia con C/G (`X`). |
| **D** CRS | `PI.classifyCRS` | Añadir candidato 8908; **prueba de contención geográfica** (reproyectar a WGS84 y verificar caja de Costa Rica); razón distancia‑coordenadas vs derrotero. |
| **G** cierre | paso «Polígono» / `PI.buildTraverse` (ya reporta cierre) | Diagnóstico *leave‑one‑out* del lado sospechoso; sugerir Bowditch/Transit/LS (solo mostrar). |
| **H** confianza | procedencia que ya escribe `piBuildProvenance` | Formalizar objeto de evidencia por etapa (value, alternatives, source, residuals, warnings); UI ámbar de «una pregunta». |

---

## 5. Roadmap priorizado (por tamaño de PR)

### Fase 1 — Victorias rápidas (sin dependencias nuevas; seguro en `file://` y CSP)
Reutilizan Canvas + `PI.*` + Tesseract + proj4 + Turf ya presentes.

1. **PDF con texto nativo**: `PDF.js getTextContent()` antes de rasterizar;
   si hay tabla/derrotero como texto, saltarse el OCR. *(Gran impacto, bajo esfuerzo.)*
2. **CRS por evidencias**: candidato 8908, contención geográfica en Costa Rica,
   razón coordenadas/derrotero; exigir confirmación cuando top‑2 estén cerca.
3. **Decoder de OCR**: conservar alternativas de token y desambiguar con rango de
   CRS y error de cierre (extender `piParseOCR` + construcción).
4. **Diagnóstico de cierre** *leave‑one‑out* + sugerencias Bowditch/Transit
   (solo visualización, nunca imposición).
5. **Objeto de confianza/evidencia** + flujo ámbar de «una pregunta».

### Fase 2 — Automatización geométrica (añade OpenCV.js diferido, modo Pages)
6. **Cargador OpenCV.js** (versión fija + SRI; Worker `blob:`; `.wasm` por
   `fetch{integrity}`) + **deskew/orientación/recorte (E)**.
7. **Cuadrícula automática (B)**: Hough + periodicidad + OCR de rótulos +
   afín/RANSAC → georreferencia sin clics. *(El mayor ahorro de tiempo.)*
8. **Contorno (A)**: morfología + grafo de segmentos + ranking por concordancia
   con la geometría de C/G.
9. **Registro contra vector (F)** para el modo de plano existente.

### Fase 3 — Apuestas mayores (solo si la Fase 1–2 deja muchos casos en ámbar/rojo)
- **PaddleOCR PP‑OCRv5 Latin** vía ORT Web, modelos reempacados con SRI, opt‑in.
- **Reconocedor CTC propio** para números/manuscrita catastral (entrenado
  offline, inferencia local).
- **Segmentación aprendida del lindero** solo si A geométrico falla de forma
  sistemática y hay máscaras etiquetadas.

**Criterio para cualquier «apuesta mayor»:** debe mejorar la métrica de producto
—*% de planos resueltos con 0 o 1 confirmación*— y no solo una demo de OCR. La
primera descarga de PP‑OCRv5 + ORT supera ~30 MB; hay que justificar ese costo
resolviendo una clase de planos que Tesseract + geometría realmente no resuelve.

---

## 6. Validación sin dataset etiquetado

1. **Sintético** (verdad exacta): dibujar un polígono conocido + tabla +
   derrotero + cuadrícula, y aplicar rotación, perspectiva, blur, JPEG, ruido,
   fondo amarillento, sellos, texto sobre lindero, recortes. Mide A/B/E/F y
   detecta regresiones.
2. **Silver por redundancia**: cuando tabla, derrotero, cuadrícula y dibujo del
   mismo plano coinciden de forma independiente, ese caso entra como validación
   semiautomática.
3. **Gold pequeño**: cada corrección humana confirmada (con política de
   privacidad) → CRS + polígono + unos GCP. Separar por **plano**, no por celda.

**Métricas:** OCR = CER y **exactitud exacta por campo** (un dígito mal en una
coordenada es más grave que varios en un nombre); georreferencia = **RMSE en
metros**, error de centroide, Hausdorff, error de área; y la métrica de producto:
**% resuelto con 0 / 1 / manual**. Convertir píxeles a metros con la **cuadrícula
detectada**, no con el DPI nominal.

---

## 7. Qué debe seguir siendo manual (inevitable)

- Confirmación final del predio y su ubicación (responsabilidad catastral).
- Elección **CR05 (5367) vs CR‑SIRGAS (8908)** cuando el texto solo dice «CRTM05».
- CRS intrínsecamente ambiguo o coordenadas sin sistema reconocible.
- Dibujo **sin anclaje absoluto** (forma/escala/orientación, pero no posición).
- Conflicto entre fuentes legales (tabla ≠ derrotero ≠ dibujo): el software
  diagnostica, no decide cuál prevalece.
- Manuscrita ilegible (transcripción asistida con alternativas).
- Curvas, servidumbres, segregaciones: identificar candidatos, no decidir cuál
  es jurídicamente el predio.
- Autorización de cualquier compensación de cierre.

---

## 8. Arquitectura objetivo

```
                         ┌─ PDF texto nativo ───────┐
Archivo ── E normaliza ──┼─ B grilla + OCR rótulos ─┼── D CRS
                         ├─ C tabla/derrotero OCR ──┤
                         └─ A linework/lindero ──────┘
                                      │
                              fusión de evidencias
                               /              \
                              G                F
                       cierre/diagnóstico   registro vector
                               \              /
                                └───── H ─────┘
                                       │
                           confirmación final única
```

El principio rector: el navegador no necesita «entender un plano» como un modelo
generalista; necesita **demostrar que varias descripciones independientes del
mismo predio (tabla, derrotero, cuadrícula, dibujo y, si existe, vector) son
geométricamente coherentes**. Esa redundancia es la fuente de precisión más
valiosa bajo CSP estricta, hardware modesto y cero salida de datos.

---

## 9. Fuentes (a verificar al implementar)

- OpenCV.js: docs oficiales (Hough, contours, morphologyEx, `findHomography`
  con RANSAC/LMeDS/RHO, `estimateAffinePartial2D`).
- Tesseract.js (Apache‑2.0), reutilizar un único Worker; core WASM aparte.
- ONNX Runtime Web 1.27.0 (WASM/WebGPU/WebNN; `wasm.numThreads=1` sin
  `crossOriginIsolated`).
- PaddleOCR.js (SDK navegador; modelos ONNX propios `.tar` con `inference.onnx`).
- IGN/SNIT Costa Rica: perfil EPSG (5367, 8908, 5456/5457), CR‑SIRGAS oficial.
- Estándar Fetch: `integrity` para verificar `.wasm`/`.onnx`/código dinámico.
- Bowditch/Transit; GNU Gama (referencia de ajuste por mínimos cuadrados).

*Las URLs y cifras de precisión de los informes deben re‑verificarse contra un
corpus real de planos costarricenses antes de comprometer una fase.*
