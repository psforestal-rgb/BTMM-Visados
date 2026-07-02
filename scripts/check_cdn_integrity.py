#!/usr/bin/env python3
"""Prueba de contrato con el CDN: verifica que cada librería externa fijada
en index.html siga disponible y sirva exactamente los bytes esperados (SRI).

Detecta de forma temprana: archivos retirados del CDN, cambios de contenido
(supply chain) y roturas de red, antes de que un usuario las sufra. Un fallo
aquí NO rompe el visor publicado (el navegador ya bloquea contenido con hash
inválido); indica que hay que actuar.

También comprueba disponibilidad (solo estado HTTP) de los recursos sin SRI
posible: sql-wasm.wasm y pdf.worker.min.js, y de los servicios externos
críticos (proxy OGC, SNIT, Dirección de Agua).

Uso:
  python3 scripts/check_cdn_integrity.py             # red real (CI)
  python3 scripts/check_cdn_integrity.py --local-map DIR  # pruebas sin red:
      sirve cada URL desde DIR/<ruta-codificada> en lugar de descargarla.

Sale con código 1 si alguna verificación de integridad falla; los sondeos de
disponibilidad de servicios solo se reportan (código 2 si únicamente fallan
sondeos), para distinguir rotura de contrato de caída transitoria.
"""
import base64
import hashlib
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TIMEOUT = 30

# Recursos que se cargan en runtime sin SRI posible (worker / wasm):
# solo se sondea disponibilidad. Mantener alineado con index.html.
SOLO_DISPONIBILIDAD = [
    "https://cdn.jsdelivr.net/npm/sql.js@1.10.3/dist/sql-wasm.wasm",
    "https://cdn.jsdelivr.net/npm/pdfjs-dist@3.11.174/build/pdf.worker.min.js",
]

# Servicios externos de los que depende el visor en runtime (solo sondeo).
SERVICIOS = [
    ("Proxy OGC (Cloudflare Worker)", "https://psforgis-ocg.psforestal.workers.dev/"),
    ("SNIT WMS Ortofoto2017", "https://geos1.snitcr.go.cr/Ortofoto2017/wms?service=WMS&version=1.1.1&request=GetCapabilities"),
    ("Dirección de Agua WMS", "https://mapas.da.go.cr/geopc.php?service=WMS&version=1.1.1&request=GetCapabilities"),
    ("Esri World Imagery", "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer?f=json"),
]


def extraer_pares_sri(html):
    """[(url, sha384-...)] de scripts/links estáticos y cargas diferidas."""
    pares = []
    for m in re.finditer(r'<(?:script|link)[^>]+(?:src|href)="(https://[^"]+)"[^>]*integrity="([^"]+)"', html):
        pares.append((m.group(1), m.group(2)))
    for m in re.finditer(r"loadScriptOnce\('(https://[^']+)','(sha384-[^']+)'\)", html):
        pares.append((m.group(1), m.group(2)))
    return pares


def descargar(url, local_map):
    if local_map:
        nombre = re.sub(r"[^A-Za-z0-9.@-]", "_", url.split("://", 1)[1])
        with open(os.path.join(local_map, nombre), "rb") as fh:
            return fh.read()
    req = urllib.request.Request(url, headers={"User-Agent": "btmm-visados-ci"})
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        return r.read()


def sha384_b64(data):
    return "sha384-" + base64.b64encode(hashlib.sha384(data).digest()).decode()


def main():
    local_map = None
    if "--local-map" in sys.argv:
        local_map = sys.argv[sys.argv.index("--local-map") + 1]

    with open(os.path.join(ROOT, "index.html"), encoding="utf-8") as fh:
        html = fh.read()

    pares = extraer_pares_sri(html)
    if len(pares) < 10:
        print(f"❌ Solo se detectaron {len(pares)} recursos con SRI; se esperaban ≥ 11. ¿Cambió el formato de index.html?")
        sys.exit(1)

    fallos_integridad = []
    print(f"Integridad de {len(pares)} librerías fijadas:")
    for url, esperado in pares:
        try:
            data = descargar(url, local_map)
            real = sha384_b64(data)
            if real == esperado:
                print(f"  ✅ {url} ({len(data)//1024} KB)")
            else:
                print(f"  ❌ {url}\n     esperado {esperado}\n     recibido {real}")
                fallos_integridad.append(url)
        except Exception as e:
            print(f"  ❌ {url} — no descargable: {type(e).__name__}: {e}")
            fallos_integridad.append(url)

    fallos_sondeo = []
    if not local_map:
        print("\nDisponibilidad de recursos sin SRI:")
        for url in SOLO_DISPONIBILIDAD:
            try:
                data = descargar(url, None)
                print(f"  ✅ {url} ({len(data)//1024} KB)")
            except Exception as e:
                print(f"  ⚠️  {url} — {type(e).__name__}: {e}")
                fallos_sondeo.append(url)

        print("\nDisponibilidad de servicios externos:")
        for nombre, url in SERVICIOS:
            try:
                descargar(url, None)
                print(f"  ✅ {nombre}")
            except Exception as e:
                print(f"  ⚠️  {nombre} — {type(e).__name__}: {e}")
                fallos_sondeo.append(nombre)

    print()
    if fallos_integridad:
        print(f"RESULTADO: {len(fallos_integridad)} fallo(s) de integridad/contrato")
        sys.exit(1)
    if fallos_sondeo:
        print(f"RESULTADO: integridad OK; {len(fallos_sondeo)} servicio(s) no disponibles (posible caída transitoria)")
        sys.exit(2)
    print("RESULTADO: contrato con CDN y servicios externos OK")


if __name__ == "__main__":
    main()
