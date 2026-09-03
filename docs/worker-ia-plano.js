/**
 * Worker `psforgis-ocg` — endpoint `/ia-plano`
 * Lectura asistida por IA del recuadro de un plano catastrado.
 *
 * ESTE ARCHIVO NO SE EJECUTA EN EL VISOR. Es el código que hay que desplegar en
 * Cloudflare Workers, junto al endpoint `/ogc` que ya existe. Vive aquí para que
 * el contrato quede versionado con el cliente que lo consume
 * (`piRunAI()` en index.html); la infraestructura sigue administrándose en
 * Cloudflare y fuera del repositorio (ver SECURITY.md § Alcance).
 *
 * ── Por qué un Worker y no una llamada directa desde el navegador ────────────
 * El visor es un sitio estático sin secretos: no puede guardar la clave del
 * proveedor de IA. El Worker sí, como secreto de Cloudflare. A cambio, el
 * endpoint queda público, así que aquí se concentran la lista blanca de
 * orígenes, los límites de tamaño y el limitador de tasa.
 *
 * ── Contrato ────────────────────────────────────────────────────────────────
 * POST /ia-plano
 *   Content-Type: application/json
 *   {
 *     "tipo":    "coords" | "rumbo" | "azimut",
 *     "formato": "image/png" | "image/jpeg",
 *     "imagen":  "<base64 SIN el prefijo data:>",
 *     "version": "<APP_VERSION del visor, informativo>"
 *   }
 *
 * 200 →
 *   {
 *     "rows":   [ {"p":"1","e":"512345.67","n":"1098765.43","conf":92}, ... ]   // coords
 *           |   [ {"dir":"N 45° 30' 00\" E","dist":"125.40","conf":88}, ... ]   // rumbo/azimut
 *     "notas":  "texto breve del modelo (p. ej. «la fila 7 está borrosa»)",
 *     "modelo": "gemini-2.5-flash",
 *     "texto":  "transcripción literal del recuadro (opcional, para cotejar)"
 *   }
 *
 * 4xx/5xx → { "error": "mensaje corto" }
 *
 * El cliente NO confía en esta respuesta: la valida con `PI.sanitizeAIRows`
 * (forma, tipos, tamaño, caracteres de control) y la lleva siempre a la tabla
 * editable, nunca directo al polígono.
 *
 * ── Despliegue ──────────────────────────────────────────────────────────────
 *   wrangler secret put IA_API_KEY          # clave de Google AI Studio
 *   wrangler deploy
 *
 * wrangler.toml (añadir a lo que ya tenga el Worker):
 *   [vars]
 *   IA_MODELO = "gemini-2.5-flash"
 *   IA_ORIGENES = "https://psforestal-rgb.github.io,http://127.0.0.1:8791,http://localhost:8791"
 *
 *   # Limitador de tasa nativo (opcional pero MUY recomendable: la cuota
 *   # gratuita es compartida por todos los usuarios del visor).
 *   [[ratelimits]]
 *   binding = "LIMITADOR"
 *   namespace_id = "1001"
 *   simple = { limit = 20, period = 60 }
 */

const TIPOS = new Set(['coords', 'rumbo', 'azimut']);
const FORMATOS = new Set(['image/png', 'image/jpeg']);
const MAX_B64 = 8 * 1024 * 1024;        // ~6 MB de imagen decodificada
const MODELO_POR_DEFECTO = 'gemini-2.5-flash';

/* Esquema de salida: obliga al modelo a devolver JSON con la forma esperada, en
   lugar de prosa que después habría que adivinar. */
const ESQUEMA = {
  type: 'OBJECT',
  properties: {
    rows: {
      type: 'ARRAY',
      items: {
        type: 'OBJECT',
        properties: {
          p: { type: 'STRING' },
          e: { type: 'STRING' },
          n: { type: 'STRING' },
          dir: { type: 'STRING' },
          dist: { type: 'STRING' },
          conf: { type: 'NUMBER' },
        },
      },
    },
    notas: { type: 'STRING' },
    texto: { type: 'STRING' },
  },
  required: ['rows'],
};

const REGLAS_COMUNES = [
  'Eres un asistente de topografía que transcribe planos catastrados de Costa Rica.',
  'La imagen es UN RECORTE del plano que contiene el cuadro de datos que hay que leer.',
  'Transcribe EXACTAMENTE lo que está escrito. No corrijas, no completes, no interpoles',
  'y no inventes filas: si un valor es ilegible, deja la celda vacía y explícalo en "notas".',
  'Conserva el separador decimal tal como aparece (coma o punto) y no agrupes miles.',
  'Ignora encabezados, totales, notas al pie, sellos y firmas: solo filas de datos.',
  'En "conf" pon 0-100 según lo seguro que estés de esa fila (bajo si está borrosa,',
  'tachada, manuscrita o parcialmente tapada).',
  'En "texto" pon la transcripción literal del recuadro, línea por línea.',
].join(' ');

function instruccion(tipo) {
  if (tipo === 'coords') {
    return REGLAS_COMUNES + ' ' + [
      'El recuadro es una TABLA DE COORDENADAS. Devuelve una fila por vértice con:',
      '"p" = número o nombre del punto (vacío si no lo hay),',
      '"e" = coordenada Este / X, "n" = coordenada Norte / Y.',
      'Respeta la asignación de columnas del encabezado (ESTE/NORTE, X/Y, E/N).',
      'Las coordenadas CRTM05 de Costa Rica tienen el Este en torno a 300000-660000',
      'y el Norte en torno a 880000-1250000: si tu lectura de una columna no encaja',
      'con ese orden de magnitud, revísala antes de responder, pero NO la ajustes a la fuerza.',
      'No rellenes "dir" ni "dist".',
    ].join(' ');
  }
  const cual = tipo === 'rumbo' ? 'RUMBOS (cuadrante, p. ej. N 45° 30\' 00" E)'
    : 'AZIMUTES (0° a 360°)';
  return REGLAS_COMUNES + ' ' + [
    'El recuadro es un DERROTERO con ' + cual + ' y distancias.',
    'Devuelve una fila por línea del derrotero, en el orden en que aparecen, con:',
    '"dir" = el rumbo o azimut tal como está escrito (incluye N/S, E/O/W, grados,',
    'minutos y segundos si los hay), "dist" = la distancia en metros, solo el número.',
    'En Costa Rica el oeste se escribe indistintamente O o W: conserva la letra original.',
    'No rellenes "p", "e" ni "n".',
  ].join(' ');
}

function cors(origen, permitidos) {
  const ok = permitidos.includes(origen);
  return {
    'Access-Control-Allow-Origin': ok ? origen : permitidos[0] || 'null',
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '86400',
    Vary: 'Origin',
  };
}

function json(obj, status, cabeceras) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: { 'Content-Type': 'application/json; charset=utf-8', 'Cache-Control': 'no-store', ...cabeceras },
  });
}

export async function manejarIaPlano(request, env, ctx) {
  const permitidos = String(env.IA_ORIGENES || 'https://psforestal-rgb.github.io')
    .split(',').map((s) => s.trim()).filter(Boolean);
  const origen = request.headers.get('Origin') || '';
  const h = cors(origen, permitidos);

  if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: h });
  if (request.method !== 'POST') return json({ error: 'use POST' }, 405, h);
  if (origen && !permitidos.includes(origen)) return json({ error: 'origen no permitido' }, 403, h);
  if (!env.IA_API_KEY) return json({ error: 'el servicio de IA no está configurado' }, 503, h);

  // Limitador de tasa por IP: la cuota gratuita del proveedor es compartida.
  if (env.LIMITADOR) {
    const ip = request.headers.get('CF-Connecting-IP') || 'anon';
    const { success } = await env.LIMITADOR.limit({ key: ip });
    if (!success) return json({ error: 'demasiadas peticiones; espere un minuto' }, 429, h);
  }

  let cuerpo;
  try { cuerpo = await request.json(); }
  catch { return json({ error: 'cuerpo JSON inválido' }, 400, h); }

  const tipo = String(cuerpo?.tipo || '');
  const formato = String(cuerpo?.formato || 'image/png');
  const imagen = typeof cuerpo?.imagen === 'string' ? cuerpo.imagen : '';
  if (!TIPOS.has(tipo)) return json({ error: 'tipo inválido' }, 400, h);
  if (!FORMATOS.has(formato)) return json({ error: 'formato inválido' }, 400, h);
  if (!imagen) return json({ error: 'falta la imagen' }, 400, h);
  if (imagen.length > MAX_B64) return json({ error: 'la imagen supera el límite' }, 413, h);
  if (!/^[A-Za-z0-9+/=\s]+$/.test(imagen)) return json({ error: 'la imagen no es base64' }, 400, h);

  const modelo = String(env.IA_MODELO || MODELO_POR_DEFECTO);
  const url = 'https://generativelanguage.googleapis.com/v1beta/models/'
    + encodeURIComponent(modelo) + ':generateContent';

  const peticion = {
    contents: [{
      role: 'user',
      parts: [
        { text: instruccion(tipo) },
        { inline_data: { mime_type: formato, data: imagen.replace(/\s+/g, '') } },
      ],
    }],
    generationConfig: {
      temperature: 0,                    // transcripción, no redacción
      maxOutputTokens: 8192,
      responseMimeType: 'application/json',
      responseSchema: ESQUEMA,
    },
  };

  let upstream;
  try {
    upstream = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', 'x-goog-api-key': env.IA_API_KEY },
      body: JSON.stringify(peticion),
      signal: AbortSignal.timeout(55000),
    });
  } catch (e) {
    return json({ error: 'no se pudo contactar el servicio de IA' }, 502, h);
  }

  if (!upstream.ok) {
    // 429 = cuota agotada: hay que decírselo al visor tal cual para que sugiera
    // el OCR local en vez de reintentar.
    const estado = upstream.status === 429 ? 429 : 502;
    return json({ error: 'el servicio de IA respondió ' + upstream.status }, estado, h);
  }

  let datos;
  try { datos = await upstream.json(); }
  catch { return json({ error: 'respuesta ilegible del servicio de IA' }, 502, h); }

  const texto = datos?.candidates?.[0]?.content?.parts?.map((p) => p?.text || '').join('') || '';
  let salida;
  try { salida = JSON.parse(texto); }
  catch { return json({ error: 'el modelo no devolvió JSON interpretable' }, 502, h); }
  if (!salida || !Array.isArray(salida.rows)) return json({ error: 'el modelo no devolvió filas' }, 502, h);

  return json({
    rows: salida.rows.slice(0, 400),
    notas: typeof salida.notas === 'string' ? salida.notas.slice(0, 400) : '',
    texto: typeof salida.texto === 'string' ? salida.texto.slice(0, 20000) : '',
    modelo,
  }, 200, h);
}

/* Enrutado. Si el Worker ya tiene su propio `fetch`, basta con enganchar la ruta
   `/ia-plano` a `manejarIaPlano(request, env, ctx)` y dejar el resto como está. */
export default {
  async fetch(request, env, ctx) {
    const { pathname } = new URL(request.url);
    if (pathname === '/ia-plano') return manejarIaPlano(request, env, ctx);
    return new Response('not found', { status: 404 });
  },
};
