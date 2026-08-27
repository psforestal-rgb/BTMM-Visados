# Lectura asistida por IA en «Importar predio desde plano»

Revisión de por qué fallaba el asistente, qué se corrigió sin depender de nada
externo, y cómo funciona (y cómo se activa) el canal opcional de lectura con un
modelo de visión.

Estado: implementado en `2026-08-27-ia-plano-v54`. El canal de IA **queda
inactivo hasta que se despliegue el endpoint `/ia-plano` en el Worker**
(`docs/worker-ia-plano.js`); mientras tanto el botón aparece y devuelve un error
claro, y el resto del asistente funciona igual que siempre.

---

## 1. Diagnóstico: por qué se equivocaba tanto el OCR

Cinco defectos concretos, en orden de impacto. Los cuatro primeros no tenían
nada que ver con el motor de OCR: eran de cómo se le pedían las cosas.

| # | Defecto | Dónde | Efecto en un plano real |
|---|---|---|---|
| 1 | **Lista blanca de caracteres única y demasiado estrecha** (`'0123456789.,°'"NSEWO nsewo-+ '`) | `piRunOCR` | Con lista blanca activa, Tesseract no descarta un glifo no permitido: lo **fuerza** al permitido más parecido. Las letras de los encabezados (`PUNTO`, `ESTE`, `NORTE`, `PTO`, `EST`) salían convertidas en dígitos y entraban en la tabla como si fueran datos. Y a la vez faltaban `G`, `M`, `S` y las comillas tipográficas (`’ ″ ´`), así que un derrotero escrito «S 12 G 30 M 00 S O» era ilegible. |
| 2 | **Segmentación de página automática (PSM 3)** | `piRunOCR` | PSM 3 hace análisis de *página completa* sobre lo que ya es un recorte de una tabla: mezcla columnas, parte renglones y reordena celdas. Para un bloque tabular acotado corresponde PSM 6. |
| 3 | **«Los dos últimos números de la línea son Este y Norte»** | `piParseOCR` | Cualquier número de más en el renglón —una cota, un nº de mojón, el ancho de una servidumbre, un resto de la columna vecina— **desplaza la fila en silencio** y coloca el vértice a cientos de metros. Sin ningún aviso. |
| 4 | **Binarización Otsu global** | `piRegionCanvas` | Un único umbral para todo el recorte. En un plano fotocopiado con sombra de encuadernación, gradiente de escáner o papel amarillento, media tabla se va a negro o a blanco. Es el caso normal, no el excepcional. |
| 5 | **Sobremuestreo insuficiente** (objetivo 1400 px, factor máximo ×2) | `piRegionCanvas` | Tesseract necesita ~30 px de altura de texto. Si el recorte ya medía 1400 px de ancho el factor quedaba en ×1 y las cifras entraban a 10-12 px: el error por carácter se dispara justo donde más caro sale (un dígito mal en una coordenada son cientos de metros). |

Defecto menor, también corregido: las confianzas por renglón se indexaban contra
`data.lines` usando el índice del texto **ya filtrado** (sin renglones vacíos),
así que el resaltado de «celda dudosa» señalaba filas equivocadas.

---

## 2. Lo que se corrigió sin depender de nada externo

Todo esto es determinista, no descarga nada nuevo y sigue funcionando en
`file://`. Va probado en `scripts/plano_import.test.mjs`.

- **Lista blanca por tipo de extracción** — `PI.ocrCharWhitelist(tipo)`:
  puramente numérica para tablas de coordenadas (ninguna letra que forzar), y
  con `N/S/E/O/W`, `G/M/S`, grados y comillas tipográficas para derroteros.
- **PSM 6** (`tessedit_pageseg_mode:'6'`), `preserve_interword_spaces:'1'` y
  `user_defined_dpi:'300'`.
- **Lectura por celdas** — `PI.wordsToLines` → `PI.detectColumns` →
  `PI.rowsFromWords`. Tesseract devuelve cada palabra con su caja; agrupando por
  Y se recuperan los renglones reales y agrupando por X las **columnas**. Este y
  Norte se toman de *su columna*, no de su posición en el renglón, así que un
  número intercalado ya no desplaza la fila. Para coordenadas, las columnas Este
  y Norte se identifican por **magnitud mediana** (son órdenes de magnitud
  mayores que un nº de punto o una distancia). Si la tabla no se reconstruye, se
  cae al camino anterior de texto plano.
- **Binarización local** (media por ventana con sesgo, estilo Bradley/Sauvola,
  con imagen integral para que sea O(1) por píxel) en vez de Otsu global.
- **Objetivo de 2200 px** de lado largo, factor hasta ×4, con interpolación de
  alta calidad.

---

## 3. El canal opcional de IA

### Qué resuelve y qué no

El OCR local, ya corregido, resuelve bien **una tabla impresa y nítida**. Lo que
no resuelve —y no va a resolver por más que se le ajusten parámetros— es la
clase de plano que llega en la práctica: fotocopia de fotocopia, sello encima de
la tabla, cuadro girado, cifras manuscritas, columnas sin líneas. Un modelo de
visión interpreta el recuadro **como tabla** (entiende el encabezado, sabe que
la columna que dice ESTE es el Este, sabe que «125,40 m» es una distancia en
metros), en lugar de reconocer glifos sueltos y dejar que un heurístico adivine
a qué columna pertenecen.

Lo que **no** cambia: la IA no decide nada. Su lectura entra en la misma tabla
editable, pasa por los mismos parsers deterministas, el mismo cálculo de área,
el mismo error de cierre y el mismo semáforo de confianza. Sigue habiendo una
confirmación humana única al final.

### Arquitectura

```
navegador                          Worker psforgis-ocg            proveedor
─────────                          ───────────────────            ─────────
recuadro marcado
  → PNG (≤1600 px)
  → POST /ia-plano  ──────────────►  lista blanca de origen
     {tipo,formato,imagen}           límite de tamaño
                                     limitador de tasa
                                     clave (secreto)  ──────────►  modelo de
                                                                   visión
                                  ◄──  JSON con esquema fijo  ─────
  ◄── {rows,notas,modelo,texto} ───
PI.sanitizeAIRows (valida)
  → tabla editable → confirmación humana
```

La clave del proveedor vive **solo** como secreto del Worker. El visor sigue sin
secretos (gitleaks en CI lo verifica) y el endpoint ya está dentro del
`connect-src` de la CSP, porque es el mismo origen del proxy OGC: **no hizo
falta relajar la CSP**.

### Qué sale del navegador

Únicamente **el recuadro que la persona marcó** en el paso «Recuadro a leer»,
reescalado a 1600 px de lado largo. No se envía la lámina completa, así que no
salen el nombre del propietario, la cédula ni el número de plano — salvo que
estén dentro del recuadro marcado, cosa que el aviso de la interfaz dice
explícitamente.

Además:

- Es **opt-in por sesión**: la primera vez pide confirmación con un aviso
  concreto de qué se envía y a dónde.
- El botón solo aparece con `http(s)`; en `file://` no existe.
- Nada se guarda: `sessionStorage` solo recuerda que ya se dio el
  consentimiento en esa pestaña.

### Por qué no se confía en la respuesta

Un modelo de visión puede devolver una cifra **plausible pero inventada**, que
es exactamente el modo de fallo más peligroso aquí: un OCR malo produce basura
evidente, un modelo malo produce un número que parece una coordenada. Por eso:

1. `PI.sanitizeAIRows` valida forma, tipos, número de filas (≤400), longitud de
   celda (≤64), elimina caracteres de control y descarta filas cuyas
   coordenadas no sean interpretables. Nunca se ejecuta ni se inserta como HTML;
   todo se escapa con `piEsc`.
2. La tabla muestra un aviso permanente de que la lectura la hizo una IA remota,
   con el modelo usado, e insiste en verificar vértice por vértice.
3. La procedencia del polígono registra `fuenteTexto: 'ia-remota'`, `iaModelo` y
   `iaEnviado: 'recuadro-marcado'`, de modo que el informe diga cómo se leyó.
4. La comprobación cruzada real sigue siendo geométrica: **área calculada contra
   el área escrita en el plano** y **error de cierre**. Una cifra inventada
   normalmente rompe una de las dos.

### Elección del proveedor

`docs/worker-ia-plano.js` viene configurado para **Gemini 2.5 Flash** de Google
AI Studio, que hoy es la opción con mejor relación entre lo que interesa aquí:

- tiene un **nivel gratuito real** (no solo créditos de prueba);
- lee tablas y documentos densos mejor que los modelos de visión generalistas
  de tamaño similar;
- admite **salida estructurada con esquema** (`responseSchema`), que evita tener
  que adivinar la forma de la respuesta;
- funciona bien en español.

Cambiar de proveedor es cambiar una función del Worker: el contrato con el visor
(`{tipo, formato, imagen}` → `{rows, notas, modelo, texto}`) no depende de
Google. Alternativas razonables si la cuota gratuita se queda corta:
`mistral-ocr` (OCR documental dedicado), OpenRouter (modelos `:free`, con
disponibilidad variable) o Groq (rápido, más flojo en tablas densas).

### Coste y cuota

La cuota gratuita es **compartida por todos los usuarios del visor**, porque la
clave es una sola. Por eso el Worker trae limitador de tasa por IP y por eso el
recorte se envía a 1600 px y no a resolución completa. Si la cuota se agota, el
proveedor responde 429, el Worker lo propaga y el visor sugiere el OCR local.

---

## 4. Cómo activarlo

1. Obtener una clave en Google AI Studio (nivel gratuito).
2. En el Worker `psforgis-ocg`, enganchar la ruta `/ia-plano` a
   `manejarIaPlano()` de `docs/worker-ia-plano.js`.
3. `wrangler secret put IA_API_KEY`.
4. Declarar en `wrangler.toml` las variables `IA_MODELO` e `IA_ORIGENES` y, muy
   recomendable, el binding `[[ratelimits]]` (ver cabecera del archivo).
5. `wrangler deploy`.

Comprobación rápida:

```bash
curl -s -X POST https://psforgis-ocg.psforestal.workers.dev/ia-plano \
  -H 'Content-Type: application/json' \
  -H 'Origin: https://psforestal-rgb.github.io' \
  -d '{"tipo":"coords","formato":"image/png","imagen":"'"$(base64 -w0 recorte.png)"'"}'
```

Sin desplegar nada, el visor sigue completo: OCR local corregido, texto nativo
de PDF, trazado de contorno y transcripción manual.

---

## 5. Qué medir antes de dar el canal por bueno

La métrica que importa no es el CER del OCR sino **el porcentaje de planos
resueltos con 0 o 1 correcciones manuales**. Sobre un lote real de planos
costarricenses, comparar los tres caminos (OCR local corregido, IA, y OCR local
anterior) en:

- exactitud **exacta por campo** (un dígito mal en una coordenada pesa mucho más
  que varios en un nombre);
- error de área contra el área escrita en el plano;
- error de cierre del derrotero;
- número de celdas que la persona tuvo que tocar.

Si el OCR local corregido ya deja la mayoría de los planos en verde, el canal de
IA se queda como lo que es: la salida para los casos difíciles, no el camino por
defecto.
