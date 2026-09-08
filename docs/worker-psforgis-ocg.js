/**
 * Worker `psforgis-ocg` — ARCHIVO COMPLETO, LISTO PARA DESPLEGAR
 * ═════════════════════════════════════════════════════════════════════════════
 * Este es el Worker entero, con sus DOS rutas. Se pega de una sola vez y
 * sustituye por completo al script actual:
 *
 *   /ogc       proxy de servicios OGC (WMS/WMTS/WFS/ArcGIS) de las
 *              instituciones costarricenses. YA ESTABA DESPLEGADO y se
 *              reproduce aquí sin cambios: el visor toma de él todas las
 *              capas del mapa.
 *   /ia-plano  lectura asistida por IA del recuadro de un plano catastrado.
 *              ES LA RUTA NUEVA (ver docs/ia-plano.md).
 *
 * ── Por qué un archivo único ────────────────────────────────────────────────
 * El editor del panel de Cloudflare reemplaza el script completo. Si se pega
 * solo el módulo `/ia-plano`, la ruta `/ogc` desaparece y el visor se queda sin
 * capas institucionales. Por eso las dos rutas viven aquí juntas.
 *
 * ── Despliegue ──────────────────────────────────────────────────────────────
 *   1. Guarde la clave del proveedor de IA como secreto (nunca en el código):
 *        wrangler secret put IA_API_KEY        # clave de Google AI Studio
 *   2. Añada a `wrangler.toml`:
 *        [vars]
 *        IA_MODELO   = "gemini-2.5-flash"
 *        IA_ORIGENES = "https://psforestal-rgb.github.io,http://127.0.0.1:8791,http://localhost:8791"
 *
 *        # Limitador de tasa nativo (opcional pero MUY recomendable: la cuota
 *        # gratuita del proveedor es compartida por todos los usuarios).
 *        [[ratelimits]]
 *        binding = "LIMITADOR"
 *        namespace_id = "1001"
 *        simple = { limit = 20, period = 60 }
 *   3. wrangler deploy
 *
 * Desde el panel de Cloudflare el equivalente es: pegar este archivo en el
 * editor del Worker, y declarar `IA_API_KEY` en Configuración → Variables como
 * variable CIFRADA (no de texto plano), más `IA_MODELO` e `IA_ORIGENES` como
 * variables normales.
 *
 * ── Comprobación después de desplegar ───────────────────────────────────────
 *   curl "https://psforgis-ocg.psforestal.workers.dev/ogc"        → «OGC Proxy OK…»
 *   curl -X POST "https://psforgis-ocg.psforestal.workers.dev/ia-plano" \
 *        -H 'Content-Type: application/json' -d '{}'              → 400 «cuerpo… tipo inválido»
 * Un 400 en la segunda es la respuesta correcta: significa que la ruta existe y
 * está validando la entrada. Un 404 significa que no se desplegó.
 *
 * ── Procedencia ─────────────────────────────────────────────────────────────
 * El bloque `/ia-plano` es copia literal de `docs/worker-ia-plano.js` (entre sus
 * marcadores `__IA_PLANO_START__` / `__IA_PLANO_END__`); `scripts/check_consistency.py`
 * falla si los dos se separan. El bloque `/ogc` es copia literal de lo que había
 * desplegado en Cloudflare el 20-feb-2026.
 *
 * ESTE ARCHIVO NO SE EJECUTA EN EL VISOR. La infraestructura se administra en
 * Cloudflare, fuera del repositorio (ver SECURITY.md § Alcance); vive aquí para
 * que el contrato quede versionado junto al cliente que lo consume
 * (`piRunAI()` en index.html).
 */

/* ══════════════════════════════════════════════════════════════════════════
   RUTA 1 — `/ogc`: proxy de servicios OGC (WMS / WMTS / WFS / ArcGIS)
   ──────────────────────────────────────────────────────────────────────────
   Copia literal de lo que el Worker `psforgis-ocg` ya tenía desplegado
   (última modificación en Cloudflare: 20-feb-2026). NO se ha tocado nada:
   se reproduce aquí para que el archivo se pueda pegar completo sin perder
   esta ruta, de la que el visor toma TODAS las capas institucionales.

   Si en el futuro edita `/ogc` desde el panel de Cloudflare, actualice también
   esta copia para que el repositorio siga reflejando lo desplegado.
   ══════════════════════════════════════════════════════════════════════════ */

const ROUTE_PATH = '/ogc';
const MAX_URL_LENGTH = 8192;
const UPSTREAM_TIMEOUT_MS = 25000;
const MAX_RESPONSE_BYTES = 15 * 1024 * 1024;
const RETRYABLE_METHOD = 'GET';
const MAX_REDIRECTS = 5;

const ALLOWED_DOMAIN_SUFFIXES = [
  'snitcr.go.cr',
  'sirefor.go.cr',
  'sinac.go.cr',
  'da.go.cr',
  'mag.go.cr',
  'aya.go.cr',
  'cne.go.cr',
  'rnp.go.cr',
  'ucr.ac.cr',
  'una.ac.cr',
  'cenat.ac.cr',
  'arcgis.com',
  'arcgisonline.com',
  'esri.com',
];

function getCorsHeaders(request) {
  const origin = request.headers.get('Origin');
  const allowOrigin = !origin || origin === 'null' ? '*' : origin;
  const reqHeaders = request.headers.get('Access-Control-Request-Headers');

  const headers = {
    'Access-Control-Allow-Origin': allowOrigin,
    'Access-Control-Allow-Methods': 'GET,POST,HEAD,OPTIONS',
    'Access-Control-Allow-Headers': reqHeaders || 'Accept,Content-Type,Authorization,Range,If-None-Match,If-Modified-Since',
    'Access-Control-Max-Age': '86400',
    'Access-Control-Expose-Headers': 'Content-Type,Content-Length,ETag,Last-Modified,Cache-Control,Age,X-Proxy-Cache,X-Upstream-Status,X-Proxy-Reason',
    Vary: 'Origin, Access-Control-Request-Headers',
  };

  if (allowOrigin !== '*') {
    headers['Access-Control-Allow-Credentials'] = 'true';
  }

  return headers;
}

function withCors(request, response, extraHeaders = {}) {
  const out = new Response(response.body, response);
  const cors = getCorsHeaders(request);
  for (const [k, v] of Object.entries(cors)) out.headers.set(k, v);
  for (const [k, v] of Object.entries(extraHeaders)) out.headers.set(k, v);
  return out;
}

function isIpv4(hostname) {
  const parts = hostname.split('.');
  if (parts.length !== 4) return false;
  return parts.every((part) => {
    if (!/^\d+$/.test(part)) return false;
    const n = Number(part);
    return !Number.isNaN(n) && n >= 0 && n <= 255;
  });
}

function isPrivateIpv4(hostname) {
  if (!isIpv4(hostname)) return false;
  const parts = hostname.split('.').map(Number);
  if (parts.some((n) => Number.isNaN(n) || n < 0 || n > 255)) return true;

  const [a, b] = parts;
  return (
    a === 10 ||
    a === 127 ||
    (a === 172 && b >= 16 && b <= 31) ||
    (a === 192 && b === 168) ||
    (a === 169 && b === 254)
  );
}

function isPrivateIpv6(hostname) {
  const h = hostname.replace(/^\[|\]$/g, '').toLowerCase();
  return h === '::1' || h.startsWith('fc') || h.startsWith('fd') || h.startsWith('fe8') || h.startsWith('fe9') || h.startsWith('fea') || h.startsWith('feb');
}

function isAllowedHost(hostname) {
  if (!hostname) return false;
  const h = hostname.toLowerCase();

  if (h === 'localhost' || h.endsWith('.localhost')) return false;
  if (isPrivateIpv4(h) || isPrivateIpv6(h)) return false;

  return ALLOWED_DOMAIN_SUFFIXES.some((suffix) => h === suffix || h.endsWith(`.${suffix}`));
}

function ttlForTargetUrl(targetUrl) {
  const p = targetUrl.searchParams;
  const req = (p.get('request') || p.get('REQUEST') || '').toLowerCase();
  const service = (p.get('service') || p.get('SERVICE') || '').toLowerCase();
  const path = targetUrl.pathname.toLowerCase();

  if (req === 'getcapabilities') return 6 * 3600;
  if (req === 'describefeaturetype') return 24 * 3600;
  if (req === 'getlegendgraphic') return 6 * 3600;
  if (req === 'getmap') return 15 * 60;
  if (req === 'gettile') return 24 * 3600;
  if (req === 'getfeatureinfo') return 2 * 60;
  if (req === 'getfeature') return 2 * 60;

  if (path.includes('/mapserver/') && path.endsWith('/export')) return 10 * 60;
  if (path.includes('/featureserver/') && path.endsWith('/query')) return 60;

  if (service === 'wmts') return 24 * 3600;
  if (service === 'wms') return 10 * 60;
  if (service === 'wfs') return 60;

  return 5 * 60;
}

function buildUpstreamHeaders(request) {
  const headers = new Headers();
  const passthrough = [
    'accept',
    'accept-language',
    'content-type',
    'authorization',
    'range',
    'if-none-match',
    'if-modified-since',
  ];

  for (const name of passthrough) {
    const value = request.headers.get(name);
    if (value) headers.set(name, value);
  }

  headers.set('user-agent', 'Mozilla/5.0 (Cloudflare OGC Proxy)');
  return headers;
}

async function readBodyLimited(response, maxBytes) {
  const len = response.headers.get('content-length');
  if (len) {
    const n = Number(len);
    if (!Number.isNaN(n) && n > maxBytes) {
      return { tooLarge: true, body: null };
    }
  }

  if (!response.body) {
    return { tooLarge: false, body: null };
  }

  const reader = response.body.getReader();
  const chunks = [];
  let total = 0;

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;
    total += value.byteLength;
    if (total > maxBytes) {
      try { await reader.cancel(); } catch {}
      return { tooLarge: true, body: null };
    }
    chunks.push(value);
  }

  const out = new Uint8Array(total);
  let offset = 0;
  for (const chunk of chunks) {
    out.set(chunk, offset);
    offset += chunk.byteLength;
  }

  return { tooLarge: false, body: out };
}

async function fetchUpstream(targetUrl, request) {
  const upstreamHeaders = buildUpstreamHeaders(request);
  const method = request.method;
  const attempts = method === RETRYABLE_METHOD ? 2 : 1;
  let lastError = null;

  for (let i = 0; i < attempts; i++) {
    let currentUrl = targetUrl;
    let redirects = 0;

    while (redirects <= MAX_REDIRECTS) {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort('timeout'), UPSTREAM_TIMEOUT_MS);

      try {
        const response = await fetch(currentUrl.toString(), {
          method,
          headers: upstreamHeaders,
          body: method === 'POST' ? request.body : undefined,
          redirect: 'manual',
          signal: controller.signal,
        });

        clearTimeout(timeout);

        const isRedirect = [301, 302, 303, 307, 308].includes(response.status);
        if (isRedirect && (method === 'GET' || method === 'HEAD')) {
          const location = response.headers.get('location');
          if (!location) throw new Error('Redirect without location');

          const nextUrl = new URL(location, currentUrl);
          if (!['http:', 'https:'].includes(nextUrl.protocol) || !isAllowedHost(nextUrl.hostname)) {
            throw new Error('Redirect target blocked');
          }

          redirects += 1;
          currentUrl = nextUrl;
          continue;
        }

        if (method === RETRYABLE_METHOD && i < attempts - 1 && response.status >= 500) {
          lastError = new Error(`Upstream ${response.status}`);
          break;
        }

        return response;
      } catch (error) {
        clearTimeout(timeout);
        lastError = error;
        break;
      }
    }

    if (redirects > MAX_REDIRECTS) {
      lastError = new Error('Too many redirects');
    }
    if (i >= attempts - 1 && lastError) throw lastError;
  }

  throw lastError || new Error('Unknown upstream error');
}

async function manejarOgc(request, env, ctx) {
  const reqUrl = new URL(request.url);

  if (request.method === 'OPTIONS') {
    return withCors(request, new Response(null, { status: 204 }), {
      'X-Proxy-Cache': 'BYPASS',
      'X-Upstream-Status': 'NONE',
      'X-Proxy-Reason': 'preflight',
    });
  }

  if (!['GET', 'POST', 'HEAD'].includes(request.method)) {
    return withCors(request, new Response('Method not allowed', { status: 405 }), {
      'X-Proxy-Cache': 'BYPASS',
      'X-Upstream-Status': 'NONE',
      'X-Proxy-Reason': 'method-not-allowed',
    });
  }

  const targetParam = reqUrl.searchParams.get('u') || reqUrl.searchParams.get('url');
  if (!targetParam) {
    return withCors(request, new Response('Missing query parameter "u"', { status: 400 }), {
      'X-Proxy-Cache': 'BYPASS',
      'X-Upstream-Status': 'NONE',
      'X-Proxy-Reason': 'missing-u',
    });
  }

  if (targetParam.length > MAX_URL_LENGTH) {
    return withCors(request, new Response('Target URL too long', { status: 400 }), {
      'X-Proxy-Cache': 'BYPASS',
      'X-Upstream-Status': 'NONE',
      'X-Proxy-Reason': 'url-too-long',
    });
  }

  let targetUrl;
  try {
    targetUrl = new URL(targetParam);
  } catch {
    return withCors(request, new Response('Invalid target URL', { status: 400 }), {
      'X-Proxy-Cache': 'BYPASS',
      'X-Upstream-Status': 'NONE',
      'X-Proxy-Reason': 'invalid-url',
    });
  }

  if (!['http:', 'https:'].includes(targetUrl.protocol)) {
    return withCors(request, new Response('Only http/https are allowed', { status: 400 }), {
      'X-Proxy-Cache': 'BYPASS',
      'X-Upstream-Status': 'NONE',
      'X-Proxy-Reason': 'bad-scheme',
    });
  }

  if (!isAllowedHost(targetUrl.hostname)) {
    return withCors(request, new Response('Host not allowed', { status: 403 }), {
      'X-Proxy-Cache': 'BYPASS',
      'X-Upstream-Status': 'NONE',
      'X-Proxy-Reason': 'host-not-allowed',
    });
  }

  const sensitiveParamNames = new Set(['token', 'apikey', 'key', 'access_token']);
  const hasSensitiveQuery = [...targetUrl.searchParams.keys()].some((k) => sensitiveParamNames.has(k.toLowerCase()));
  const hasAuthHeader = Boolean(request.headers.get('authorization'));
  const canCache = request.method === 'GET' && !hasAuthHeader && !hasSensitiveQuery;
  const ttl = ttlForTargetUrl(targetUrl);
  const cacheKey = new Request(targetUrl.toString(), { method: 'GET' });

  if (canCache) {
    const cached = await caches.default.match(cacheKey);
    if (cached) {
      return withCors(request, cached, {
        'X-Proxy-Cache': 'HIT',
        'X-Upstream-Status': 'CACHED',
        'X-Proxy-Reason': 'cache-hit',
      });
    }
  }

  let upstream;
  try {
    upstream = await fetchUpstream(targetUrl, request);
  } catch (error) {
    console.error('Upstream fetch failed', error);
    return withCors(request, new Response('Upstream fetch failed', { status: 502 }), {
      'X-Proxy-Cache': 'BYPASS',
      'X-Upstream-Status': 'ERROR',
      'X-Proxy-Reason': 'upstream-failed',
    });
  }

  const limited = await readBodyLimited(upstream, MAX_RESPONSE_BYTES);
  if (limited.tooLarge) {
    return withCors(request, new Response('Upstream response too large', { status: 413 }), {
      'X-Proxy-Cache': 'BYPASS',
      'X-Upstream-Status': String(upstream.status),
      'X-Proxy-Reason': 'response-too-large',
    });
  }

  const outHeaders = new Headers(upstream.headers);
  outHeaders.delete('set-cookie');

  if (canCache && upstream.ok) {
    outHeaders.set('Cache-Control', `public, max-age=${ttl}`);
  }

  const out = withCors(
    request,
    new Response(limited.body, {
      status: upstream.status,
      statusText: upstream.statusText,
      headers: outHeaders,
    }),
    {
      'X-Proxy-Cache': canCache ? 'MISS' : 'BYPASS',
      'X-Upstream-Status': String(upstream.status),
      'X-Proxy-Reason': canCache ? 'cacheable-get' : 'non-cacheable-request',
    },
  );

  if (canCache && upstream.ok) {
    ctx.waitUntil(caches.default.put(cacheKey, out.clone()));
  }

  return out;
}

/* ══════════════════════════════════════════════════════════════════════════
   RUTA 2 — `/ia-plano`: lectura del recuadro de un plano con IA
   ──────────────────────────────────────────────────────────────────────────
   Copia literal de `docs/worker-ia-plano.js` (región marcada). El contrato de
   entrada y salida está documentado en la cabecera de ese archivo y en
   `docs/ia-plano.md`.

   Recuerde: el visor NO confía en lo que devuelve esta ruta. Lo valida con
   `PI.sanitizeAIRows` y lo lleva siempre a la tabla editable para que una
   persona lo confirme; nunca directo al polígono.
   ══════════════════════════════════════════════════════════════════════════ */

/*__IA_PLANO_START__*/
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

async function manejarIaPlano(request, env, ctx) {
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
/*__IA_PLANO_END__*/

/* ══════════════════════════════════════════════════════════════════════════
   ENRUTADO
   ──────────────────────────────────────────────────────────────────────────
   Cualquier ruta que no sea `/ogc` ni `/ia-plano` responde lo mismo que
   respondía el Worker antes de añadir la IA, para no romper a nadie que
   dependiera de ese comportamiento.
   ══════════════════════════════════════════════════════════════════════════ */
export default {
  async fetch(request, env, ctx) {
    const { pathname } = new URL(request.url);

    if (pathname === ROUTE_PATH) return manejarOgc(request, env, ctx);
    if (pathname === '/ia-plano') return manejarIaPlano(request, env, ctx);

    return withCors(
      request,
      new Response(`OGC Proxy OK. Use ${ROUTE_PATH}?u=<ENCODED_TARGET_URL>`, { status: 200 }),
      { 'Content-Type': 'text/plain; charset=utf-8' },
    );
  },
};
