#!/usr/bin/env python3
"""Verificación de consistencia interna del repositorio BTMM-Visados.

Comprueba invariantes que deben mantenerse en cada cambio:
  1. La versión está sincronizada entre index.html, gen_v3.py y version.json.
  2. Todo <script src> y <link rel=stylesheet> externo lleva integrity + crossorigin (SRI).
  3. No quedan referencias a cdnjs (el CDN canónico es jsDelivr, espejo byte a byte de npm).
  4. La meta CSP existe e incluye las directivas de contención mínimas.
  5. Los archivos locales referenciados (data/, favicon, logo) existen.
  6. gen_v3.py compila.
  7. El registro de errores runtime está presente en ambos archivos.

Uso: python3 scripts/check_consistency.py   (sale con código 1 si algo falla)
"""
import json
import os
import py_compile
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FALLOS = []


def fallo(msg):
    FALLOS.append(msg)
    print(f"  ❌ {msg}")


def ok(msg):
    print(f"  ✅ {msg}")


def leer(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


def main():
    html = leer("index.html")
    gen = leer("gen_v3.py")

    print("1) Sincronización de versiones")
    ver_data = json.loads(leer("version.json"))
    ver_json = ver_data["version"]
    m_html = re.search(r"const APP_VERSION='([^']+)'", html)
    m_gen = re.search(r"const APP_VERSION='([^']+)'", gen)
    if not (m_html and m_gen):
        fallo("No se encontró APP_VERSION en index.html o gen_v3.py")
    elif m_html.group(1) == m_gen.group(1) == ver_json:
        ok(f"Versión única: {ver_json}")
    else:
        fallo(f"Versiones distintas: html={m_html.group(1)} gen={m_gen.group(1)} json={ver_json}")

    # Convención: el string de versión comienza con la FECHA de la última
    # actualización (AAAA-MM-DD) y debe coincidir con el campo `updated` de
    # version.json. Así cada publicación queda fechada de forma coherente.
    m_fecha = re.match(r"(\d{4}-\d{2}-\d{2})", ver_json)
    updated = str(ver_data.get("updated", ""))
    if not m_fecha:
        fallo(f"La versión '{ver_json}' no comienza con una fecha AAAA-MM-DD")
    elif updated[:10] != m_fecha.group(1):
        fallo(f"La fecha de la versión ({m_fecha.group(1)}) no coincide con 'updated' ({updated[:10]}) en version.json")
    else:
        ok(f"Fecha de última actualización coherente: {m_fecha.group(1)}")

    print("2) SRI en recursos externos")
    externos = re.findall(r'<(?:script|link)[^>]+(?:src|href)="(https://[^"]+)"[^>]*>', html)
    sin_sri = []
    for url in externos:
        tag = re.search(r'<[^>]+"' + re.escape(url) + r'"[^>]*>', html).group(0)
        if 'integrity="sha384-' not in tag or 'crossorigin="anonymous"' not in tag:
            sin_sri.append(url)
    if sin_sri:
        for u in sin_sri:
            fallo(f"Recurso externo sin SRI: {u}")
    else:
        ok(f"{len(externos)} recursos externos estáticos con integrity+crossorigin")
    n_dyn = len(re.findall(r"loadScriptOnce\('https://[^']+','sha384-[^']+'\)", html))
    n_dyn_all = len(re.findall(r"loadScriptOnce\('https://", html))
    if n_dyn == n_dyn_all:
        ok(f"{n_dyn} carga(s) diferida(s) con SRI")
    else:
        fallo("Hay loadScriptOnce de URL externa sin hash de integridad")

    print("3) CDN canónico")
    for f, s in (("index.html", html), ("gen_v3.py", gen)):
        if "cdnjs.cloudflare.com" in s:
            fallo(f"Referencia a cdnjs en {f} (usar jsDelivr con SRI)")
        else:
            ok(f"{f} sin referencias a cdnjs")

    print("4) Content-Security-Policy")
    csp = re.search(r'<meta http-equiv="Content-Security-Policy" content="([^"]+)"', html)
    if not csp:
        fallo("Falta la meta CSP en index.html")
    else:
        contenido = csp.group(1)
        for directiva in ("default-src 'self'", "object-src 'none'", "frame-src 'none'",
                          "base-uri 'self'", "script-src"):
            if directiva in contenido:
                ok(f"CSP incluye: {directiva}")
            else:
                fallo(f"CSP no incluye: {directiva}")

    print("5) Activos locales referenciados")
    locales = set(re.findall(r"'(data/[^']+)'", html)) | {"favicon.ico", "logo.png", "version.json"}
    # btmm_relieve.gpkg.gz se declara pero el módulo usa la grilla binaria; avisar sin fallar
    for rel in sorted(locales):
        if os.path.exists(os.path.join(ROOT, rel)):
            ok(rel)
        elif rel == "data/btmm_relieve.gpkg.gz":
            print(f"  ⚠️  {rel} declarado pero ausente (el relieve usa la grilla binaria; revisar si se reactiva el vector)")
        else:
            fallo(f"Referenciado pero ausente: {rel}")

    print("6) Compilación de gen_v3.py")
    try:
        py_compile.compile(os.path.join(ROOT, "gen_v3.py"), doraise=True)
        ok("gen_v3.py compila")
    except py_compile.PyCompileError as e:
        fallo(f"gen_v3.py no compila: {e}")

    print("7) Registro de errores runtime")
    for f, s in (("index.html", html), ("gen_v3.py", gen)):
        if all(t in s for t in ("btmmReporteErrores", "unhandledrejection", "_errSan")):
            ok(f"Colector de errores presente en {f}")
        else:
            fallo(f"Colector de errores ausente o incompleto en {f}")

    print("8) Plantilla de capas de gen_v3.py sigue siendo una plantilla")
    marcadores = ["{{FN2000}}", "{{FN2005}}", "{{CF2021}}", "{{CF2023}}", "{{TB2012}}"]
    # Los marcadores también aparecen, inevitablemente, como argumento del propio
    # HTML.replace(...) y en los autochequeos de más abajo: buscarlos en todo el
    # archivo siempre "encuentra" algo y no detecta el bug real (datos ya resueltos
    # horneados en el cuerpo de la plantilla). Hay que aislar el cuerpo de la
    # plantilla (todo lo anterior a la línea que hace el reemplazo) y buscar ahí.
    marca_fin_plantilla = '\nHTML = HTML.replace("{{CF2021}}"'
    if marca_fin_plantilla not in gen:
        fallo("No se encontró el límite esperado de la plantilla HTML en gen_v3.py (¿cambió el mecanismo de reemplazo?)")
        faltantes = marcadores
    else:
        cuerpo_plantilla = gen[:gen.index(marca_fin_plantilla)]
        faltantes = [m for m in marcadores if m not in cuerpo_plantilla]
    if faltantes:
        fallo(
            "gen_v3.py ya no contiene el(los) marcador(es) "
            f"{faltantes}: el .replace() correspondiente sería un no-op y "
            "la regeneración dejaría datos de capa obsoletos sin avisar "
            "(revisar que nadie haya pegado HTML ya renderizado sobre la plantilla)"
        )
    else:
        ok(f"{len(marcadores)} marcador(es) de capa presentes y sustituibles")
    if "/mnt/user-data/outputs/" in gen or "/home/claude/" in gen:
        fallo(
            "gen_v3.py conserva una ruta de entorno de análisis hardcodeada "
            "(/mnt/user-data/outputs/ o /home/claude/); debe escribir junto "
            "al script salvo que se indique GEN_OUTPUT_PATH/LAYERS_B64_PATH"
        )
    else:
        ok("Sin rutas hardcodeadas de entorno de análisis")

    print()
    if FALLOS:
        print(f"RESULTADO: {len(FALLOS)} fallo(s)")
        sys.exit(1)
    print("RESULTADO: todo consistente")


if __name__ == "__main__":
    main()
