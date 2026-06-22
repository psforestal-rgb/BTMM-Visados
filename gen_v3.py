import json
import os
from pathlib import Path


def _layers_b64_path():
    candidates = []
    env_path = os.environ.get("LAYERS_B64_PATH")
    if env_path:
        candidates.append(Path(env_path))
    candidates.append(Path(__file__).with_name("layers_b64.json"))
    candidates.append(Path("/home/claude/cobertura_fo/layers_b64.json"))
    for path in candidates:
        if path.exists():
            return path
    raise FileNotFoundError(
        "No se encontro layers_b64.json. Defina LAYERS_B64_PATH o coloque el archivo junto a gen_v3.py."
    )


with open(_layers_b64_path(), encoding="utf-8") as f:
    D = json.load(f)

CF2021,CF2023,FN2000,FN2005,TB2012 = D["cf2021"],D["cf2023"],D["fn2000"],D["fn2005"],D["tb2012"]

HTML = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate">
<meta http-equiv="Pragma" content="no-cache">
<meta http-equiv="Expires" content="0">
<title>Visor Cobertura Forestal – PNLQ / ACC-SINAC</title>
<link rel="icon" href="favicon.ico?v=2026-06-22-word-clean-wayback2021-v6">
<link rel="shortcut icon" href="favicon.ico?v=2026-06-22-word-clean-wayback2021-v6">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.css"/>
<style>
*{box-sizing:border-box;margin:0;padding:0}
:root{--bg:#0d1f0e;--sb:#0f2a10;--card:#1a3b1c;--acc:#3d8b3d;--acc2:#56b356;--gold:#d4a02a;--txt:#dff5de;--txt2:#9bc99a;--warn:#e17055;--red:#d63031}
body{font-family:'Segoe UI',system-ui,sans-serif;background:var(--bg);color:var(--txt);height:100vh;display:flex;flex-direction:column;overflow:hidden}

/* ── HEADER ── */
#header{background:linear-gradient(135deg,#0a2e0b 0%,#1a5e1c 50%,#0a2e0b 100%);padding:7px 16px;display:flex;align-items:center;gap:11px;border-bottom:2px solid var(--gold);flex-shrink:0}
#header h1{font-size:14px;font-weight:700;color:var(--gold);letter-spacing:.4px;line-height:1.2}
#header .sub{font-size:9px;color:var(--txt2);line-height:1.4;margin-top:1px}
#logo{width:34px;height:34px;background:var(--gold);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:17px;flex-shrink:0}

/* ── TABS ── */
#tabs{background:#071607;border-bottom:1px solid #1e4020;display:flex;padding:0 14px;gap:1px;flex-shrink:0}
.tab{background:none;border:none;border-bottom:3px solid transparent;color:var(--txt2);padding:9px 18px;font-size:11px;font-weight:600;cursor:pointer;transition:.15s;white-space:nowrap;letter-spacing:.2px;font-family:inherit}
.tab:hover{color:var(--txt);background:rgba(255,255,255,.04)}
.tab.active{color:var(--gold);border-bottom-color:var(--gold);background:rgba(212,160,42,.07)}
.tab .tb{font-size:12px;margin-right:5px}
.tab .soon{font-size:8px;padding:1px 5px;border-radius:8px;background:#1e3a20;color:#5a8a5c;margin-left:5px;font-weight:400;vertical-align:middle}

/* ── LAYOUT ── */
#main{display:flex;flex:1;overflow:hidden}

/* ── SIDEBAR ── */
#sidebar{width:268px;background:var(--sb);border-right:1px solid #1e4020;display:flex;flex-direction:column;overflow:hidden;flex-shrink:0}
.tab-panel{flex:1;overflow-y:auto;padding:7px 9px;display:flex;flex-direction:column;gap:6px}
.tab-panel::-webkit-scrollbar{width:3px}
.tab-panel::-webkit-scrollbar-thumb{background:#3d6040;border-radius:2px}
.tab-panel[style*="display:none"]{display:none!important}

/* sidebar panels */
.pnl{background:var(--card);border-radius:5px;padding:7px 9px;border:1px solid #204522}
.pt{font-size:10px;font-weight:700;color:var(--gold);text-transform:uppercase;letter-spacing:.7px;margin-bottom:5px}
.ltog{display:flex;align-items:center;gap:5px;cursor:pointer;padding:3px 4px;border-radius:3px;transition:.13s;font-size:11px}
.ltog:hover{background:#1e4020}
.ltog input{accent-color:var(--acc2);cursor:pointer}
.lbadge{font-size:8px;padding:1px 4px;border-radius:8px;background:#204522;color:var(--txt2)}
.legend-wrap{padding:2px 4px 2px 20px}
.lrow{display:flex;align-items:center;gap:4px;padding:1px 0}
.lsw{width:9px;height:9px;border-radius:1px;flex-shrink:0}
.ll{font-size:9px;color:var(--txt2)}
#dz{border:2px dashed #3d6040;border-radius:5px;padding:10px;text-align:center;cursor:pointer;transition:.18s;background:#0f2a10}
#dz:hover,#dz.drag-over{border-color:var(--acc2);background:#152e16}
#dz .di{font-size:20px}
#dz .dt{font-size:10px;color:var(--txt2)}
#dz .ds{font-size:8px;color:#4a6e4c;margin-top:2px}
#fi{display:none}
#uli{font-size:9.5px;color:var(--txt2);margin-top:5px;display:none}
#uli b{color:var(--acc2)}
.btn{width:100%;padding:7px;border:none;border-radius:4px;cursor:pointer;font-size:11px;font-weight:600;transition:.15s;margin-top:3px;font-family:inherit}
.bp{background:var(--acc);color:#fff}.bp:hover{background:var(--acc2)}
.bp:disabled{background:#204522;color:#5a8a5c;cursor:not-allowed}
.bd{background:#3b1515;color:#ff7979;border:1px solid #5c2020}.bd:hover{background:#5c2020}
.bs{background:#203d21;color:var(--txt2);border:1px solid #315f33}.bs:hover{background:#2a5a2a;color:var(--txt)}
.pdf-tools{display:none;margin-top:5px;border:1px solid #315f33;border-radius:4px;background:#102611;padding:6px}
.pdf-tools.on{display:block}
.pdf-tools .hint{font-size:8px;color:#9bc99a;line-height:1.35;margin-bottom:4px}
.pdf-tools .row{display:grid;grid-template-columns:1fr 1fr;gap:4px}
.pdf-tools .stat{font-size:8px;color:#d4a02a;line-height:1.35;margin-top:4px}
.pdf-pair-list{display:flex;flex-direction:column;gap:3px;margin-top:5px}
.pdf-pair{display:flex;align-items:center;justify-content:space-between;gap:4px;font-size:8px;color:#cde7c7;background:#0b1c0c;border:1px solid #244626;border-radius:3px;padding:3px 4px}
.pdf-pair button{border:1px solid #5a1d1d;background:#3b0c0c;color:#ff8f8f;border-radius:3px;font-size:8px;line-height:1;padding:3px 5px;cursor:pointer}

/* placeholder panels */
.placeholder-panel{display:flex;flex-direction:column;align-items:center;justify-content:center;flex:1;text-align:center;padding:20px 14px;gap:10px}
.ph-icon{font-size:40px;opacity:.5}
.ph-title{font-size:14px;font-weight:700;color:var(--gold)}
.ph-badge{font-size:9px;padding:3px 10px;border-radius:12px;background:#1e3a20;color:#5a8a5c;border:1px solid #2a5a2a;letter-spacing:.4px;text-transform:uppercase}
.ph-desc{font-size:10px;color:var(--txt2);line-height:1.6;max-width:200px}
.ph-items{width:100%;display:flex;flex-direction:column;gap:6px;margin-top:4px}
.ph-item{background:var(--card);border:1px solid #204522;border-left:3px solid #2a5a2a;border-radius:4px;padding:6px 8px;text-align:left}
.ph-item-title{font-size:9.5px;font-weight:700;color:var(--txt2)}
.ph-item-desc{font-size:8.5px;color:#4a6e4c;margin-top:2px;line-height:1.4}

/* ── MAP ── */
#map{flex:1;position:relative;background:#e8e8e0}
#mc{width:100%;height:100%}

/* ── RESULTS PANEL ── */
#rp{position:absolute;bottom:10px;right:10px;width:545px;max-height:80vh;background:rgba(9,22,10,.97);border:1px solid var(--acc);border-radius:7px;overflow:hidden;display:none;z-index:1000;box-shadow:0 4px 24px rgba(0,0,0,.65)}
#rh{background:var(--acc);padding:7px 12px;display:flex;align-items:center;justify-content:space-between;flex-shrink:0}
#rh h3{font-size:11.5px;font-weight:700;color:#fff}
#rc{display:flex;align-items:center;gap:8px}
#rc button{background:none;border:none;color:#fff;font-size:16px;cursor:pointer;line-height:1}
#rc .rh-btn{font-size:11px;font-weight:700;background:#0a2e0b;border:1px solid #fff;border-radius:4px;padding:3px 9px;transition:.15s}
#rc .rh-btn:hover{background:#fff;color:var(--acc)}
#rc .rh-btn:disabled{opacity:.5;cursor:wait}
#rb{overflow-y:auto;max-height:calc(80vh - 36px);padding:11px}
#rb::-webkit-scrollbar{width:4px}#rb::-webkit-scrollbar-thumb{background:#3d6040}

/* mini-maps */
#minimap-grid{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:13px}
.mm-wrap{display:flex;flex-direction:column}
.mm-title{font-size:9px;font-weight:700;color:var(--gold);margin-bottom:3px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.mm-div{height:130px;border-radius:4px;overflow:hidden;border:1px solid #204522}
.mm-div .leaflet-tile{filter:contrast(1.12) saturate(1.10) brightness(1.03)}

/* results table */
.rtbl{width:100%;border-collapse:collapse;font-size:9.5px;margin-bottom:10px}
.rtbl th{background:#1a3b1c;color:var(--txt2);padding:4px 5px;text-align:center;border:1px solid #2a5a2a;font-size:9px;vertical-align:middle}
.rtbl td{padding:3px 5px;border:1px solid #2a5a2a;color:var(--txt);vertical-align:middle}
.rtbl .td-layer{font-weight:700;text-align:center;background:#0f2a10;color:var(--gold);font-size:9px;line-height:1.4}
.rtbl .td-void{color:var(--warn);font-style:italic}
.rtbl .td-total td{background:#1a3b1c;color:var(--acc2);font-weight:700}
.td-num{text-align:right}
.bar-wrap{height:5px;background:#163318;border-radius:2px;overflow:hidden;margin-top:2px}
.bar-fill{height:100%;border-radius:2px;transition:width .35s}

/* progress */
#po{position:absolute;inset:0;background:rgba(0,0,0,.75);display:none;align-items:center;justify-content:center;z-index:2000;flex-direction:column;gap:8px}
#po.on{display:flex}
.pb{background:var(--card);border:1px solid var(--acc);border-radius:7px;padding:18px 28px;text-align:center}
.pb h3{color:var(--gold);font-size:12px;margin-bottom:7px}
.pbw{width:220px;height:7px;background:#163318;border-radius:3px;overflow:hidden}
.pbi{height:100%;background:var(--acc);width:0%;transition:width .3s;border-radius:3px}
.pm{font-size:10px;color:var(--txt2);margin-top:5px}

/* toast */
#toast{position:fixed;top:55px;left:50%;transform:translateX(-50%);background:#1a3b1c;border:1px solid var(--acc);color:var(--txt);padding:6px 15px;border-radius:18px;font-size:11px;display:none;z-index:9999;box-shadow:0 2px 10px rgba(0,0,0,.5)}
#toast.err{background:#3b1515;border-color:var(--red);color:#ff7979}
#stb{background:#0a1e0b;padding:3px 10px;font-size:9px;color:var(--txt2);border-top:1px solid #204522;flex-shrink:0;display:flex;gap:10px}
.coo{font-family:monospace}
.itt{background:rgba(10,25,11,.9)!important;border:1px solid var(--acc)!important;color:var(--txt)!important;font-size:10px!important}
</style>
</head>
<body>

<!-- HEADER -->
<div id="header">
  <div id="logo">🌲</div>
  <div>
    <h1>Visor de Cobertura Forestal — PNLQ</h1>
    <div class="sub">SINAC — Área de Conservación Central — Bloque Tapantí Macizo de la Muerte</div>
  </div>
</div>

<!-- MODULE TABS -->
<div id="tabs">
  <button class="tab active" data-tab="cobertura" onclick="switchTab('cobertura')"><span class="tb">🌿</span>Cobertura Forestal</button>
  <button class="tab" data-tab="suelos" onclick="switchTab('suelos')"><span class="tb">🌱</span>Suelos Forestales<span class="soon">Próximamente</span></button>
  <button class="tab" data-tab="antecedentes" onclick="switchTab('antecedentes')"><span class="tb">📋</span>Antecedentes y PNE<span class="soon">Próximamente</span></button>
</div>

<!-- MAIN -->
<div id="main">

<!-- SIDEBAR -->
<div id="sidebar">

  <!-- ①  PANEL: COBERTURA FORESTAL -->
  <div id="panel-cobertura" class="tab-panel">
    <div class="pnl">
      <div class="pt">🧭 Referencias</div>
      <label class="ltog"><input type="checkbox" id="cb-ref"><span style="flex:1">Nombres, límites y caminos</span></label>
      <div style="font-size:8px;color:#4a6e4c;padding:3px 4px 0;line-height:1.4">Capa de referencia transparente con etiquetas priorizadas sobre caminos y límites.</div>
      <div style="margin-top:5px"><div style="font-size:9px;color:var(--gold);text-transform:uppercase;letter-spacing:.5px;margin-bottom:2px">Opacidad referencias</div>
      <input type="range" id="ref-op" min="20" max="100" value="85" style="width:100%;accent-color:var(--acc2)">
      <div style="font-size:9px;color:var(--txt2);text-align:center"><span id="ref-opv">85</span>%</div></div>
    </div>
    <div class="pnl">
      <div class="pt">🌿 Capas de cobertura</div>
      <!-- FN2000 -->
      <div>
        <label class="ltog"><input type="checkbox" id="cb-fn2000" data-layer="fn2000">
          <span style="flex:1">FONAFIFO 2000</span><span class="lbadge">FONAFIFO</span>
        </label>
        <div id="lg-fn2000" class="legend-wrap" style="display:none">
          <div class="lrow"><span class="lsw" style="background:#276221"></span><span class="ll">Bosque</span></div>
          <div class="lrow"><span class="lsw" style="background:#c8a840"></span><span class="ll">Agropecuario</span></div>
          <div class="lrow"><span class="lsw" style="background:#8b5e9e"></span><span class="ll">Páramo</span></div>
          <div class="lrow"><span class="lsw" style="background:#3498db"></span><span class="ll">Agua</span></div>
          <div class="lrow"><span class="lsw" style="background:#e74c3c"></span><span class="ll">Deforestación</span></div>
          <div class="lrow"><span class="lsw" style="background:#95a5a6"></span><span class="ll">Nubes</span></div>
          <div class="lrow"><span class="lsw" style="background:#2ecc71"></span><span class="ll">Regeneración forestal</span></div>
        </div>
      </div>
      <!-- FN2005 -->
      <div>
        <label class="ltog"><input type="checkbox" id="cb-fn2005" data-layer="fn2005">
          <span style="flex:1">FONAFIFO 2005</span><span class="lbadge">FONAFIFO</span>
        </label>
        <div id="lg-fn2005" class="legend-wrap" style="display:none">
          <div class="lrow"><span class="lsw" style="background:#1e5c1a"></span><span class="ll">Forestal</span></div>
          <div class="lrow"><span class="lsw" style="background:#a0522d"></span><span class="ll">No forestal</span></div>
          <div class="lrow"><span class="lsw" style="background:#3aae56"></span><span class="ll">Bos. intermedio &gt;15 a.</span></div>
          <div class="lrow"><span class="lsw" style="background:#7b2d8b"></span><span class="ll">Páramo</span></div>
          <div class="lrow"><span class="lsw" style="background:#66b030"></span><span class="ll">Plantaciones forestales</span></div>
          <div class="lrow"><span class="lsw" style="background:#88cc55"></span><span class="ll">Bosque secundario</span></div>
          <div class="lrow"><span class="lsw" style="background:#8b4513"></span><span class="ll">Café</span></div>
          <div class="lrow"><span class="lsw" style="background:#cc3300"></span><span class="ll">Deforestación</span></div>
          <div class="lrow"><span class="lsw" style="background:#1a6fa0"></span><span class="ll">Agua</span></div>
          <div class="lrow"><span class="lsw" style="background:#666680"></span><span class="ll">Uso urbano</span></div>
          <div style="font-size:8px;color:var(--gold);background:rgba(212,160,42,.08);border:1px solid #4a3a18;border-radius:3px;padding:4px 5px;margin-top:5px;line-height:1.45">⚙️ <b>Capa ajustada:</b> traslación rígida de +210 m en X y −150 m en Y (CRTM05/EPSG:5367) respecto a FONAFIFO 2000. No se modificó la geometría interna: solo se desplazaron los polígonos como bloque, conservando áreas, vértices y topología.</div>
        </div>
      </div>
      <!-- TB2012 -->
      <div>
        <label class="ltog"><input type="checkbox" id="cb-tb2012" data-layer="tb2012">
          <span style="flex:1">Tipos de Bosque 2012</span><span class="lbadge">SINAC</span>
        </label>
        <div id="lg-tb2012" class="legend-wrap" style="display:none">
          <div class="lrow"><span class="lsw" style="background:#14692f"></span><span class="ll">Bosque maduro</span></div>
          <div class="lrow"><span class="lsw" style="background:#52b96a"></span><span class="ll">Bosque secundario</span></div>
          <div class="lrow"><span class="lsw" style="background:#86c93f"></span><span class="ll">Plantación forestal</span></div>
          <div class="lrow"><span class="lsw" style="background:#d4c84a"></span><span class="ll">Pastos</span></div>
          <div class="lrow"><span class="lsw" style="background:#a0703c"></span><span class="ll">No forestal</span></div>
          <div class="lrow"><span class="lsw" style="background:#8b5e9e"></span><span class="ll">Páramo</span></div>
          <div class="lrow"><span class="lsw" style="background:#b0b0b8"></span><span class="ll">Nubes</span></div>
          <div class="lrow"><span class="lsw" style="background:#7a7a85"></span><span class="ll">Sombra de nubes</span></div>
        </div>
      </div>
      <!-- CF2021 -->
      <div>
        <label class="ltog"><input type="checkbox" id="cb-cf2021" data-layer="cf2021">
          <span style="flex:1">Cobertura Forestal 2021</span><span class="lbadge">SINAC</span>
        </label>
        <div id="lg-cf2021" class="legend-wrap" style="display:none">
          <div class="lrow"><span class="lsw" style="background:#1a7c3e"></span><span class="ll">Bosque maduro</span></div>
          <div class="lrow"><span class="lsw" style="background:#5dba6e"></span><span class="ll">Bosque secundario</span></div>
        </div>
      </div>
      <!-- CF2023 -->
      <div>
        <label class="ltog"><input type="checkbox" id="cb-cf2023" checked data-layer="cf2023">
          <span style="flex:1">Cobertura Forestal 2023</span><span class="lbadge">SINAC</span>
        </label>
        <div id="lg-cf2023" class="legend-wrap">
          <div class="lrow"><span class="lsw" style="background:#0d5c2e"></span><span class="ll">Bosque maduro</span></div>
          <div class="lrow"><span class="lsw" style="background:#4aad62"></span><span class="ll">Bosque secundario</span></div>
        </div>
      </div>
    </div>
    <div class="pnl">
      <div class="pt">🛰️ Imágenes aéreas</div>
      <label class="ltog"><input type="checkbox" class="ortho-cb" id="ob-terra1997" data-ortho="terra1997"><span style="flex:1">Ortofoto TERRA 1997</span><span class="lbadge" id="st-terra1997" data-orig="IGN">IGN</span></label>
      <label class="ltog"><input type="checkbox" class="ortho-cb" id="ob-orto0507" data-ortho="orto0507"><span style="flex:1">Ortofoto 2005-2007</span><span class="lbadge" id="st-orto0507" data-orig="IGN">IGN</span></label>
      <label class="ltog"><input type="checkbox" class="ortho-cb" id="ob-orto1417" data-ortho="orto1417"><span style="flex:1">Ortofoto 2014-2017</span><span class="lbadge" id="st-orto1417" data-orig="IGN">IGN</span></label>
      <label class="ltog"><input type="checkbox" class="ortho-cb" id="ob-wb2021" data-ortho="wb2021"><span style="flex:1">Imagen aérea 2021</span><span class="lbadge" id="st-wb2021" data-orig="Esri">Esri</span></label>
      <label class="ltog"><input type="checkbox" class="ortho-cb" id="ob-wb2023" data-ortho="wb2023"><span style="flex:1">Imagen aérea 2023</span><span class="lbadge" id="st-wb2023" data-orig="Esri">Esri</span></label>
      <div style="font-size:8px;color:#4a6e4c;padding:4px 4px 0;line-height:1.4">Solo una imagen activa a la vez. Se muestra bajo las capas de cobertura. Las ortofotos del SNIT (1997, 2005-07, 2014-17) son de escala 1:5000: <b>acérquese</b> para que carguen. Fuente: SNIT-IGN y Esri Wayback (2021/2023).</div>
      <div style="margin-top:6px"><div style="font-size:9px;color:var(--gold);text-transform:uppercase;letter-spacing:.5px;margin-bottom:2px">Opacidad imagen</div>
      <input type="range" id="ortho-op" min="20" max="100" value="100" style="width:100%;accent-color:var(--acc2)">
      <div style="font-size:9px;color:var(--txt2);text-align:center"><span id="ortho-opv">100</span>%</div></div>
    </div>
    <div class="pnl">
      <div class="pt">📂 Polígono de análisis</div>
      <div id="dz" onclick="document.getElementById('fi').click()">
        <div class="di">⬆️</div>
        <div class="dt">Cargar polígono de análisis</div>
        <div class="ds">SHP · GPKG · GPX · KML · KMZ · GeoJSON</div>
        <div class="ds" style="color:#4a6e4c;margin-top:2px">Arrastre aquí o haga clic</div>
      </div>
      <input type="file" id="fi" accept=".shp,.gpkg,.gpx,.kml,.kmz,.geojson,.json,.zip">
      <div id="uli"><b id="uln"></b><br><span id="ulf"></span></div>
      <div style="margin:7px 0 5px;border-top:1px solid #28562b;padding-top:6px">
        <div style="font-size:9px;color:var(--gold);text-transform:uppercase;letter-spacing:.5px;margin-bottom:4px">Plano PDF</div>
        <button class="btn bp" id="btn-pdf-load" type="button" style="margin-top:0" onclick="document.getElementById('pdf-fi').click()">📄 Cargar PDF</button>
        <input type="file" id="pdf-fi" accept=".pdf" style="display:none">
        <label class="ltog" id="pdf-toggle-row" style="display:none;margin-top:5px">
          <input type="checkbox" id="cb-pdf-plan" checked><span style="flex:1">Imagen del plano</span><span class="lbadge">ref</span>
        </label>
        <button class="btn bs" id="btn-pdf-manual" style="display:none" onclick="togglePdfManualMode()">🎯 Ajuste manual</button>
        <div class="pdf-tools" id="pdf-tools">
          <div class="hint" id="pdf-manual-hint">Clic en un vértice del plano y luego en su vértice del polígono. El segundo clic se ajusta al vértice vectorial más cercano.</div>
          <div class="row">
            <button class="btn bs" id="btn-pdf-undo" onclick="undoPdfManualPoint()">↶ Último</button>
            <button class="btn bp" id="btn-pdf-apply" onclick="applyPdfManualFit()" disabled>Ajustar</button>
          </div>
          <div class="stat" id="pdf-manual-stat">0/3 pares mínimos</div>
          <div class="pdf-pair-list" id="pdf-pair-list"></div>
        </div>
        <button class="btn bd" id="btn-pdf-clear" style="display:none" onclick="clearPdfPlanLayer()">✖ Limpiar PDF</button>
        <div id="pdf-info" style="display:none;font-size:8px;color:#9bc99a;line-height:1.35;margin-top:4px"></div>
      </div>
      <button class="btn bp" id="btn-analyze" disabled onclick="runAnalysis()">🔬 Calcular intersección</button>
      <button class="btn bd" id="btn-clear" style="display:none" onclick="clearUserLayer()">✖ Limpiar capa</button>
    </div>
    <div class="pnl">
      <div class="pt">🔆 Opacidad</div>
      <input type="range" id="opr" min="10" max="100" value="75" style="width:100%;accent-color:var(--acc2)">
      <div style="font-size:9px;color:var(--txt2);text-align:center;margin-top:1px"><span id="opv">75</span>%</div>
    </div>
    <div style="font-size:8px;color:#3a5e3c;text-align:center;padding:3px">PNLQ–ACC-SINAC · v1.2 · Datos: SINAC / FONAFIFO<br>Resolución completa · áreas en CRTM05/EPSG:5367</div>
  </div>

  <!-- ②  PANEL: SUELOS FORESTALES -->
  <div id="panel-suelos" class="tab-panel" style="display:none">
    <div class="placeholder-panel">
      <div class="ph-icon">🌱</div>
      <div class="ph-title">Suelos Forestales</div>
      <div class="ph-badge">Módulo en preparación</div>
      <div class="ph-desc">Contenido por definir.<br>Comuníquese con el administrador del visor para activar este módulo.</div>
      <div class="ph-items">
        <div class="ph-item">
          <div class="ph-item-title">Capacidad de uso de suelos</div>
          <div class="ph-item-desc">Decreto 41960-MAG-MINAE · Clases I–VIII</div>
        </div>
        <div class="ph-item">
          <div class="ph-item-title">Aptitud forestal</div>
          <div class="ph-item-desc">Suelos con vocación forestal según clasificación INTA</div>
        </div>
        <div class="ph-item">
          <div class="ph-item-title">Análisis de pendientes</div>
          <div class="ph-item-desc">Modelo digital de elevaciones PNLQ</div>
        </div>
      </div>
    </div>
  </div>

  <!-- ③  PANEL: ANTECEDENTES Y PNE -->
  <div id="panel-antecedentes" class="tab-panel" style="display:none">
    <div class="placeholder-panel">
      <div class="ph-icon">📋</div>
      <div class="ph-title">Antecedentes y PNE</div>
      <div class="ph-badge">Módulo en preparación</div>
      <div class="ph-desc">Contenido por definir.<br>Comuníquese con el administrador del visor para activar este módulo.</div>
      <div class="ph-items">
        <div class="ph-item">
          <div class="ph-item-title">Patrimonio Natural del Estado</div>
          <div class="ph-item-desc">Art. 13 Ley Forestal 7575 · Áreas protegidas</div>
        </div>
        <div class="ph-item">
          <div class="ph-item-title">Antecedentes registrales</div>
          <div class="ph-item-desc">Consulta de planos catastrales e inscripción</div>
        </div>
        <div class="ph-item">
          <div class="ph-item-title">Afectaciones legales</div>
          <div class="ph-item-desc">Zonas de protección, restricciones y servidumbres</div>
        </div>
      </div>
    </div>
  </div>

</div><!-- /sidebar -->

<!-- MAP -->
<div id="map">
  <div id="mc"></div>
  <div id="rp">
    <div id="rh"><h3 id="rt">Resultados de intersección</h3><div id="rc"><button id="btn-word" class="rh-btn" onclick="exportWord()" title="Descargar informe en Word">⬇ Word</button><button onclick="closeResults()" title="Cerrar">✕</button></div></div>
    <div id="rb"></div>
  </div>
  <div id="po">
    <div class="pb"><h3>⚙️ Procesando intersección…</h3><div class="pbw"><div class="pbi" id="pbi"></div></div><div class="pm" id="pm">Iniciando…</div></div>
  </div>
</div>

</div><!-- /main -->

<div id="stb">
  <span id="zi">Zoom: --</span>
  <span id="ci" class="coo">CR05/CRTM05 E: -- | N: --</span>
  <span id="ls" style="color:var(--warn)"></span>
</div>
<div id="toast"></div>

<!-- SCRIPTS -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/pako/2.1.0/pako.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@turf/turf@6.5.0/turf.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/shpjs@4.0.4/dist/shp.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@mapbox/togeojson@0.16.0/togeojson.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/proj4js/2.9.2/proj4.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.10.3/sql-wasm.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>
<script>
const APP_VERSION='2026-06-22-word-clean-wayback2021-v6';
window.BTMM_APP_VERSION=APP_VERSION;
(function enforceFreshVersion(){
  if(location.protocol==='file:') return;
  fetch('version.json?ts='+Date.now(),{cache:'no-store'})
    .then(r=>r.ok?r.json():null)
    .then(info=>{
      const remote=info&&info.version;
      if(!remote) return;
      const u=new URL(location.href);
      if(u.searchParams.get('v')===remote) return;
      const key='btmm-visados-reloaded-'+remote;
      if(sessionStorage.getItem(key)) return;
      sessionStorage.setItem(key,'1');
      u.searchParams.set('v',remote);
      location.replace(u.toString());
    })
    .catch(()=>{});
})();
proj4.defs("EPSG:5367","+proj=tmerc +lat_0=0 +lon_0=-84 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs");
proj4.defs("EPSG:8908","+proj=tmerc +lat_0=0 +lon_0=-84 +k=0.9999 +x_0=500000 +y_0=0 +ellps=WGS84 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs");
proj4.defs("EPSG:32616","+proj=utm +zone=16 +datum=WGS84 +units=m +no_defs");
proj4.defs("EPSG:32617","+proj=utm +zone=17 +datum=WGS84 +units=m +no_defs");

/* ── LAYER METADATA (orden cronológico) ── */
const LM={
  fn2000:{label:"FONAFIFO 2000",source:"FONAFIFO",hasVoids:false,
    colors:{"Bosque":"#276221","Agropecuario":"#c8a840","Páramo":"#8b5e9e","Agua":"#3498db","Deforestación 97-00":"#e74c3c","Nubes":"#95a5a6","Regeneración forestal":"#2ecc71","_void":"#e17055"}},
  fn2005:{label:"FONAFIFO 2005",source:"FONAFIFO",hasVoids:false,
    colors:{"Forestal":"#1e5c1a","No forestal":"#a0522d","Bosque intermedio > 15 años":"#3aae56","Paramo":"#7b2d8b","Plantaciones forestales":"#66b030","Bosque secundario":"#88cc55","Cafe":"#8b4513","Deforestacion":"#cc3300","Agua":"#1a6fa0","Uso urbano":"#666680","_void":"#e17055"}},
  tb2012:{label:"Tipos de Bosque 2012",source:"SINAC",hasVoids:false,
    colors:{"Bosque maduro":"#14692f","Bosque secundario":"#52b96a","Plantación forestal":"#86c93f","Pastos":"#d4c84a","No forestal":"#a0703c","Páramo":"#8b5e9e","Nubes":"#b0b0b8","Sombra de nubes":"#7a7a85","_void":"#e17055"}},
  cf2021:{label:"Cobertura Forestal 2021",source:"SINAC",hasVoids:true,
    colors:{"Bosque maduro":"#1a7c3e","Bosque secundario":"#5dba6e","_void":"#e17055"}},
  cf2023:{label:"Cobertura Forestal 2023",source:"SINAC",hasVoids:true,
    colors:{"Bosque maduro":"#0d5c2e","Bosque secundario":"#4aad62","_void":"#e17055"}}
};

/* ── LAYER DATA (EMBEDDED, orden cronológico) ── */
const LD={
  fn2000:"{{FN2000}}",
  fn2005:"{{FN2005}}",
  tb2012:"{{TB2012}}",
  cf2021:"{{CF2021}}",
  cf2023:"{{CF2023}}"
};

const S={lfl:{},gjd:{},uGJ:null,uLfl:null,op:0.75,
  lastResults:null,lastUserGeoJSON:null,lastBounds:null,lastUserHa:0,lastUserN:0,lastAerialDate:null,
  pdfLayer:null,pdfPlanData:null,pdfName:null,pdfOpacity:1,pdfManual:{active:false,pairs:[],pending:null,markers:[]}};
const miniMaps={};
// Encuadre ajustado al predio para todos los mini-mapas (zoom al predio)
const MM_FIT={padding:[6,6],maxZoom:18};

/* ── MAP SETUP ── */
const map=L.map('mc',{center:[9.58,-83.85],zoom:11,maxZoom:22});

function createRefPane(name,zIndex){
  map.createPane(name);
  const pane=map.getPane(name);
  pane.style.zIndex=zIndex;
  pane.style.pointerEvents='none';
}
createRefPane('refLinePane',610);
createRefPane('refLabelPane',660);
createRefPane('pdfPlanPane',720);

/* ── CAPA DE REFERENCIAS (superposición transparente) ──
   Los servicios de Esri son tiles ya renderizados. Para evitar franjas y
   líneas encima del texto, se usan solo overlays con alfa limpio: caminos en
   un pane inferior y topónimos/límites en un pane superior. */
const TRANSPARENT_TILE='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR4nGNgYGBgAAAABQABpfZFQAAAAABJRU5ErkJggg==';
let refOpacity=0.85;
const refTileDefaults={maxNativeZoom:19,maxZoom:22,updateWhenIdle:true,keepBuffer:2,errorTileUrl:TRANSPARENT_TILE};
function referenceTile(url,opts,baseOpacity){
  const layer=L.tileLayer(url,Object.assign({},refTileDefaults,opts,{opacity:baseOpacity}));
  layer._refBaseOpacity=baseOpacity;
  return layer;
}
const refGroup=L.layerGroup([
  referenceTile('https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Transportation/MapServer/tile/{z}/{y}/{x}',
    {pane:'refLinePane',minZoom:13,attribution:'© Esri — Transportation'},0.42),
  referenceTile('https://server.arcgisonline.com/ArcGIS/rest/services/Reference/World_Boundaries_and_Places/MapServer/tile/{z}/{y}/{x}',
    {pane:'refLabelPane',attribution:'© Esri — Boundaries and Places'},0.95)
]);
function setRefOpacity(v){
  refOpacity=Number(v)||0;
  refGroup.eachLayer(l=>{if(l.setOpacity)l.setOpacity(refOpacity*(l._refBaseOpacity||1));});
}
document.getElementById('cb-ref').addEventListener('change',function(){
  if(this.checked){refGroup.addTo(map);setRefOpacity(refOpacity);toast('🧭 Referencias activadas');}
  else{map.removeLayer(refGroup);}
});
document.getElementById('ref-op').addEventListener('input',function(){
  document.getElementById('ref-opv').textContent=this.value;
  setRefOpacity(this.value/100);
});

map.on('mousemove',e=>{
  const p=proj4('EPSG:4326','EPSG:5367',[e.latlng.lng,e.latlng.lat]);
  document.getElementById('ci').textContent=`CR05/CRTM05 E: ${p[0].toFixed(2)} | N: ${p[1].toFixed(2)}`;
});
map.on('zoomend',()=>{document.getElementById('zi').textContent=`Zoom: ${map.getZoom()}`;});
document.getElementById('zi').textContent=`Zoom: ${map.getZoom()}`;

/*
   IMAGENES AEREAS (ortofotos SNIT-IGN via WMS/WMTS + Esri Wayback 2021/2023)
   - Las ortofotos SNIT se sirven como WMS o WMTS en EPSG:3857.
   - Esri Wayback 2021/2023 se autoconfigura en tiempo de ejecucion con respaldo si falla.
*/
const WB_BASE='https://wayback.maptiles.arcgis.com/arcgis/rest/services/World_Imagery/WMTS/1.0.0/default028mm/MapServer/tile/{rel}/{z}/{y}/{x}';

// Proxy OGC (Cloudflare Worker) — añade CORS y caché a los servicios SNIT.
// Resuelve el descubrimiento de capas (GetCapabilities) y permite capturar las
// teselas WMS sin "contaminar" el canvas (exportación a Word).
const OGC_PROXY='https://psforgis-ocg.psforestal.workers.dev/ogc?u=';
function viaProxy(u){ return OGC_PROXY+encodeURIComponent(u); }
const ORTHO={
  terra1997:{name:'Ortofoto TERRA 1997',short:'TERRA 1997',type:'wmts',
    url:'https://geos1.snitcr.go.cr/Ortofoto_TERRA_1997_40k/wmts?SERVICE=WMTS&VERSION=1.0.0&REQUEST=GetTile&LAYER=mosaico_ortofoto_terra_1997_40k&STYLE=_empty&FORMAT=image/png&TILEMATRIXSET=EPSG:3857&TILEMATRIX=EPSG:3857:{z}&TILEROW={y}&TILECOL={x}',
    capsUrl:'https://geos1.snitcr.go.cr/Ortofoto_TERRA_1997_40k/wmts?SERVICE=WMTS&VERSION=1.0.0&REQUEST=GetCapabilities',
    discoverLayer:false,
    attribution:'IGN / SNIT - Ortofotos TERRA 1997'},
  orto0507:{name:'Ortofoto 2005-2007',short:'Ortofoto 2005-2007',type:'wms',
    url:'https://geos0.snitcr.go.cr/cgi-bin/web',
    layers:'Mosaico5000',version:'1.1.1',extraParams:{map:'ortofoto.map'},
    attribution:'IGN / SNIT — Ortofoto 2005-2007 (PRCR)'},
  orto1417:{name:'Ortofoto 2014-2017',short:'Ortofoto 2014-2017',type:'wms',
    url:'https://geos1.snitcr.go.cr/Ortofoto2017/wms',
    layers:'ortofoto2017_5000_altaresolucion',version:'1.1.1',
    capsUrl:'https://geos1.snitcr.go.cr/Ortofoto2017/wms?service=WMS&version=1.1.1&request=GetCapabilities',
    discoverLayer:false,
    attribution:'IGN / SNIT - Ortofoto 2014-2017'},
  wb2021:{name:'Imagen aérea 2021 (Esri)',short:'Imagen aérea 2021 (Esri)',type:'xyz',dateLabel:'2021-11-30',
    rel:'48624',rel_fallback:'48624',discover:'2021',badRels:['26120'],
    attribution:'Esri World Imagery (Wayback 2021-11-30)'},
  wb2023:{name:'Imagen aérea 2023 (Esri)',short:'Imagen aérea 2023 (Esri)',type:'xyz',dateLabel:'2023-12-07',
    rel:'56102',rel_fallback:'56102',discover:'2023',
    attribution:'Esri World Imagery (Wayback 2023-12-07)'}
};
// Emparejamiento cronológico capa de cobertura → imagen aérea para los mini-mapas
const PAIR={fn2000:'terra1997', fn2005:'orto0507', tb2012:'orto1417', cf2021:'wb2021', cf2023:'wb2023'};

// Aclaración del ajuste aplicado a la capa FONAFIFO 2005
const FN2005_NOTE='La capa de cobertura 2005 fue ajustada respecto a FONAFIFO 2000 en CR05 / CRTM05, EPSG:5367, mediante una traslación rígida uniforme de +210 m en X y −150 m en Y. No se modificó la geometría interna: solo se desplazaron los polígonos como un bloque, conservando áreas, vértices y topología.';

const orthoLayers={}; // instancias Leaflet activas en el mapa principal
let activeOrtho=null;
let orthoOpacity=1.0;

// WMS que enruta cada tesela COMPLETA (con BBOX y demás parámetros) a través del
// proxy OGC, de modo que las ortofotos del SNIT lleguen con CORS y caché.
const ProxiedWMS=L.TileLayer.WMS.extend({
  getTileUrl:function(coords){
    const real=L.TileLayer.WMS.prototype.getTileUrl.call(this,coords);
    return OGC_PROXY+encodeURIComponent(real);
  }
});
function proxiedWms(url,options){ return new ProxiedWMS(url,options); }
const ProxiedTileLayer=L.TileLayer.extend({
  getTileUrl:function(coords){
    const real=L.TileLayer.prototype.getTileUrl.call(this,coords);
    return viaProxy(real);
  }
});
function proxiedTile(url,options){ return new ProxiedTileLayer(url,options); }

function buildOrthoLayer(key,opts){
  const c=ORTHO[key];
  opts=opts||{};
  const op=(opts.opacity!=null)?opts.opacity:orthoOpacity;
  let lyr;
  if(c.type==='wms'){
    const params=Object.assign({
      layers:c.layers, format:'image/png', transparent:true,
      version:c.version||'1.1.1', opacity:op,
      crossOrigin:opts.crossOrigin||'anonymous', maxZoom:opts.maxZoom||21,
      attribution:c.attribution
    }, c.extraParams||{});
    // Por defecto se usa el proxy (CORS + caché). opts.direct=true lo evita.
    lyr=opts.direct ? L.tileLayer.wms(c.url, params) : proxiedWms(c.url, params);
  } else if(c.type==='wmts'){
    const tileOpts={opacity:op, crossOrigin:opts.crossOrigin||'anonymous',
      maxNativeZoom:20, maxZoom:opts.maxZoom||21, attribution:c.attribution};
    // El WMTS de TERRA 1997 no publica CORS; por defecto pasa por el proxy OGC.
    lyr=opts.direct ? L.tileLayer(c.url,tileOpts) : proxiedTile(c.url,tileOpts);
  } else { // xyz (Esri Wayback) — over-zoom para acercamiento fino aunque la fuente nativa llegue a z19
    const url=(c.urlTemplate||WB_BASE.replace('{rel}', c.rel))
      .replace('{level}','{z}').replace('{row}','{y}').replace('{col}','{x}');
    lyr=L.tileLayer(url,{opacity:op, crossOrigin:opts.crossOrigin||null,
      maxNativeZoom:19, maxZoom:opts.maxZoom||22, attribution:c.attribution});
  }
  return lyr;
}

/* Mantiene el orden correcto: ortofoto debajo de las capas de cobertura */
function restackLayers(){
  // las ortofotos al fondo
  Object.values(orthoLayers).forEach(l=>{if(l&&l.bringToBack)l.bringToBack();});
  // luego las capas de cobertura por encima
  Object.keys(LM).forEach(k=>{if(S.lfl[k]&&map.hasLayer(S.lfl[k])&&S.lfl[k].bringToFront)S.lfl[k].bringToFront();});
  // el polígono del usuario siempre arriba
  if(S.uLfl&&S.uLfl.bringToFront)S.uLfl.bringToFront();
  // el plano PDF es line art transparente y se dibuja encima de todo
  if(S.pdfLayer&&map.hasLayer(S.pdfLayer)&&S.pdfLayer.bringToFront)S.pdfLayer.bringToFront();
}

function setOrtho(key,on){
  // Comportamiento exclusivo: al activar una, se desactivan las demás
  if(on){
    Object.keys(orthoLayers).forEach(k=>{
      if(k!==key){map.removeLayer(orthoLayers[k]);delete orthoLayers[k];
        const cb=document.getElementById('ob-'+k);if(cb)cb.checked=false;}
    });
    if(!orthoLayers[key]){
      orthoLayers[key]=buildOrthoLayer(key);
      orthoLayers[key].addTo(map);
      const st=document.getElementById('st-'+key);
      let errCount=0;
      orthoLayers[key].on('tileerror',()=>{
        errCount++;
        if(st&&errCount>=2){st.dataset.err='1';st.textContent='⚠';st.title='No se pudieron cargar teselas: verifique nombre de capa, cobertura o acerque el zoom.';}
      });
      orthoLayers[key].on('load',()=>{ if(st&&st.dataset.err){st.dataset.err='';st.textContent=st.dataset.orig||st.textContent;} });
    }
    activeOrtho=key;
    restackLayers();
    toast('🛰️ '+ORTHO[key].name);
  } else {
    if(orthoLayers[key]){map.removeLayer(orthoLayers[key]);delete orthoLayers[key];}
    if(activeOrtho===key)activeOrtho=null;
  }
}

document.querySelectorAll('.ortho-cb').forEach(cb=>{
  cb.addEventListener('change',function(){setOrtho(this.dataset.ortho,this.checked);});
});
document.getElementById('ortho-op').addEventListener('input',function(){
  orthoOpacity=this.value/100;
  document.getElementById('ortho-opv').textContent=this.value;
  Object.values(orthoLayers).forEach(l=>{if(l&&l.setOpacity)l.setOpacity(orthoOpacity);});
});

/* -- Descubrimiento en tiempo de ejecucion (capas WMS heredadas + Esri Wayback) -- */
function firstLeafLayerName(xml){
  // Devuelve el Name de la primera "Layer" hoja (sin sub-Layer) — robusto ante anidamiento
  const layers=Array.from(xml.getElementsByTagName('Layer'));
  for(const L of layers){
    const hasChild=Array.from(L.children).some(c=>c.tagName==='Layer'||c.localName==='Layer');
    if(!hasChild){
      const nameEl=Array.from(L.children).find(c=>c.tagName==='Name'||c.localName==='Name');
      if(nameEl&&nameEl.textContent&&nameEl.textContent.trim())return nameEl.textContent.trim();
    }
  }
  return null;
}
async function discoverWmsLayer(key){
  const c=ORTHO[key];
  if(!c||!c.capsUrl)return;
  if(c.discoverLayer===false)return;
  try{
    const r=await fetch(viaProxy(c.capsUrl),{cache:'force-cache'});
    if(!r.ok)return;
    const txt=await r.text();
    const xml=new DOMParser().parseFromString(txt,'text/xml');
    const name=firstLeafLayerName(xml);
    if(name){ c.layers=name; c._discovered=true; console.log('[imagen] '+key+' → capa "'+name+'"'); }
  }catch(e){ console.warn('[imagen] caps '+key+' (se usa valor por defecto):',e); }
}
async function discoverImageryConfig(){
  // 1) Esri Wayback: números de versión reales más cercanos a 2021 y 2023
  try{
    const r=await fetch('https://s3-us-west-2.amazonaws.com/config.maptiles.arcgis.com/waybackconfig.json',{cache:'force-cache'});
    if(r.ok){
      const cfg=await r.json();
      const entries=Array.isArray(cfg)?cfg.map((v,i)=>[String(v.releaseNum||i),v]):Object.entries(cfg);
      const items=entries.map(([k,v])=>{
        const rel=String(v.releaseNum||k||'').trim();
        const label=v.releaseDateLabel||v.itemTitle||'';
        const d=Number(v.releaseDatetime||0);
        const urlTemplate=v.itemURL||v.tileURL||'';
        return{rel,label,d,urlTemplate};
      });
      const pick=(year,badRels)=>{
        const bad=new Set((badRels||[]).map(String));
        const cand=items.filter(it=>String(it.label).includes(String(year))&&it.rel&&!bad.has(String(it.rel)));
        if(!cand.length)return null;
        cand.sort((a,b)=>b.d-a.d);
        return cand[0];
      };
      const p21=pick(2021,ORTHO.wb2021.badRels), p23=pick(2023,ORTHO.wb2023.badRels);
      if(p21){ORTHO.wb2021.rel=p21.rel;ORTHO.wb2021.urlTemplate=p21.urlTemplate;ORTHO.wb2021.attribution='Esri World Imagery (Wayback '+p21.label+')';ORTHO.wb2021.dateLabel=p21.label;}
      if(p23){ORTHO.wb2023.rel=p23.rel;ORTHO.wb2023.urlTemplate=p23.urlTemplate;ORTHO.wb2023.attribution='Esri World Imagery (Wayback '+p23.label+')';ORTHO.wb2023.dateLabel=p23.label;}
    }
  }catch(e){console.warn('Wayback config:',e);}
  // 2) Nombres de capa GeoServer cuando una ortofoto WMS no fija su capa manualmente
  await Promise.all([discoverWmsLayer('terra1997'), discoverWmsLayer('orto1417')]);
}

/* ── HELPERS ── */
function toast(msg,err=false,d=3000){const t=document.getElementById('toast');t.textContent=msg;t.className=err?'err':'';t.style.display='block';setTimeout(()=>t.style.display='none',d);}
function setProg(p,m){document.getElementById('pbi').style.width=p+'%';document.getElementById('pm').textContent=m;}
function showProg(v){document.getElementById('po').classList.toggle('on',v);}
function setLS(m){document.getElementById('ls').textContent=m;}
function getColor(k,cls){return LM[k].colors[cls]||'#aaa';}
// Área geodésica (Turf) como respaldo
function areaHaGeo(f){try{return turf.area(f)/10000;}catch(e){return 0;}}
// Área planar en EPSG:5367 (CRTM05) — coincide con el cálculo de QGIS sobre los
// datos originales. Reproyecta cada anillo a 5367 y aplica fórmula del área (shoelace).
function ringAreaCRTM05(ring){
  let s=0;
  const pts=ring.map(c=>proj4('EPSG:4326','EPSG:5367',[c[0],c[1]]));
  for(let i=0,n=pts.length;i<n;i++){
    const [x1,y1]=pts[i], [x2,y2]=pts[(i+1)%n];
    s+=(x1*y2 - x2*y1);
  }
  return Math.abs(s)/2; // m²
}
function geomAreaCRTM05(geom){
  if(!geom)return 0;
  let a=0;
  if(geom.type==='Polygon'){
    geom.coordinates.forEach((ring,i)=>{a += (i===0?1:-1)*ringAreaCRTM05(ring);});
  } else if(geom.type==='MultiPolygon'){
    geom.coordinates.forEach(poly=>poly.forEach((ring,i)=>{a += (i===0?1:-1)*ringAreaCRTM05(ring);}));
  } else if(geom.type==='GeometryCollection'){
    geom.geometries.forEach(g=>a+=geomAreaCRTM05(g));
  }
  return a; // m²
}
function areaHa(f){
  try{
    const g=f.geometry?f.geometry:f;
    const a=geomAreaCRTM05(g)/10000;
    if(isFinite(a)&&a>0)return a;
  }catch(e){}
  return areaHaGeo(f); // respaldo geodésico
}
function b64toGJ(s){const bin=atob(s),b=new Uint8Array(bin.length);for(let i=0;i<bin.length;i++)b[i]=bin.charCodeAt(i);return JSON.parse(pako.inflate(b,{to:'string'}));}

/* ── TAB SWITCHING ── */
function switchTab(tabName){
  document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
  document.querySelector(`.tab[data-tab="${tabName}"]`).classList.add('active');
  document.querySelectorAll('.tab-panel').forEach(p=>{p.style.display='none';});
  document.getElementById(`panel-${tabName}`).style.display='flex';
  if(tabName!=='cobertura')closeResults();
}

/* ── LOAD LAYERS ── */
async function loadLayers(){
  setLS('🌿 Descomprimiendo capas base…');
  for(const k of Object.keys(LD)){
    setLS(`Cargando ${LM[k].label}…`);
    await new Promise(r=>setTimeout(r,0));
    try{S.gjd[k]=b64toGJ(LD[k]);}catch(e){console.error(k,e);}
  }
  // Activa en el mapa las capas cuyo checkbox esté marcado por defecto
  Object.keys(LM).forEach(k=>{
    const cb=document.getElementById(`cb-${k}`);
    if(cb&&cb.checked)toggleLayer(k,true);
  });
  setLS('');
}

function makeLeafletLayer(k){
  if(!S.gjd[k])return null;
  return L.geoJSON(S.gjd[k],{
    style:f=>({color:getColor(k,f.properties.clase),fillColor:getColor(k,f.properties.clase),fillOpacity:S.op,weight:0.5,opacity:0.8}),
    onEachFeature:(f,l)=>{l.bindTooltip(`<b>${LM[k].label}</b><br>${f.properties.clase||'?'}`,{className:'itt',sticky:true});}
  });
}

function toggleLayer(k,show){
  const lg=document.getElementById(`lg-${k}`);
  if(show){if(!S.gjd[k])return;if(!S.lfl[k])S.lfl[k]=makeLeafletLayer(k);if(S.lfl[k])S.lfl[k].addTo(map);if(lg)lg.style.display='block';}
  else{if(S.lfl[k])map.removeLayer(S.lfl[k]);if(lg)lg.style.display='none';}
  if(typeof restackLayers==='function')restackLayers();
}
document.querySelectorAll('[data-layer]').forEach(cb=>{cb.addEventListener('change',function(){toggleLayer(this.dataset.layer,this.checked);if(this.dataset.layer==='fn2005'&&this.checked){toast('⚙️ FONAFIFO 2005: capa ajustada (+210 m X, −150 m Y) — ver nota en la leyenda',false,6500);}});});
document.getElementById('opr').addEventListener('input',function(){S.op=this.value/100;document.getElementById('opv').textContent=this.value;Object.keys(S.lfl).forEach(k=>{if(S.lfl[k]&&map.hasLayer(S.lfl[k]))S.lfl[k].setStyle({fillOpacity:S.op});});});

/* ── WKB PARSER ── */
class WKBParser{
  constructor(b){const ab=b.buffer?b.buffer.slice(b.byteOffset,b.byteOffset+b.byteLength):b;this.v=new DataView(ab);this.o=0;this.le=true;}
  u8(){return this.v.getUint8(this.o++);}
  u32(){const v=this.v.getUint32(this.o,this.le);this.o+=4;return v;}
  f64(){const v=this.v.getFloat64(this.o,this.le);this.o+=8;return v;}
  pt(){return[this.f64(),this.f64()];}
  ptZ(){const p=this.pt();this.f64();return p;}
  ptM(){const p=this.pt();this.f64();return p;}
  ptZM(){const p=this.pt();this.f64();this.f64();return p;}
  ring(z,m){const n=this.u32(),r=[];for(let i=0;i<n;i++)r.push(z&&m?this.ptZM():z?this.ptZ():m?this.ptM():this.pt());return r;}
  geom(){
    const bo=this.u8();this.le=bo===1;
    let gt=this.u32(),z=false,m=false,bt=gt;
    if(gt>3000){bt=gt-3000;z=true;m=true;}else if(gt>2000){bt=gt-2000;m=true;}else if(gt>1000){bt=gt-1000;z=true;}
    switch(bt){
      case 1:{const c=this.pt();if(z)this.f64();if(m)this.f64();return{type:'Point',coordinates:c};}
      case 2:return{type:'LineString',coordinates:this.ring(z,m)};
      case 3:{const n=this.u32(),rs=[];for(let i=0;i<n;i++)rs.push(this.ring(z,m));return{type:'Polygon',coordinates:rs};}
      case 4:{const n=this.u32(),ps=[];for(let i=0;i<n;i++)ps.push(this.geom().coordinates);return{type:'MultiPoint',coordinates:ps};}
      case 5:{const n=this.u32(),ls=[];for(let i=0;i<n;i++)ls.push(this.geom().coordinates);return{type:'MultiLineString',coordinates:ls};}
      case 6:{const n=this.u32(),mp=[];for(let i=0;i<n;i++)mp.push(this.geom().coordinates);return{type:'MultiPolygon',coordinates:mp};}
      case 7:{const n=this.u32(),gs=[];for(let i=0;i<n;i++)gs.push(this.geom());return{type:'GeometryCollection',geometries:gs};}
      default:throw new Error('WKB type '+gt);
    }
  }
}

function parseGPKGGeom(blob){
  const v=new DataView(blob.buffer,blob.byteOffset,blob.byteLength);
  if(v.getUint8(0)!==0x47||v.getUint8(1)!==0x50)throw new Error('No GPKG magic');
  const flags=v.getUint8(3),env=(flags>>1)&7,empty=(flags>>4)&1;
  if(empty)return null;
  let skip=8;
  if(env===1)skip+=32;else if(env===2||env===3)skip+=48;else if(env===4)skip+=64;
  return new WKBParser(blob.slice(skip)).geom();
}

function reprCoords(c,from,to){
  if(!c||c.length===0)return c;
  if(from===to||from===4326)return c;
  const fs=`EPSG:${from}`,ts=`EPSG:${to}`;
  if(typeof c[0]==='number'){const[x,y]=proj4(fs,ts,[c[0],c[1]]);return[x,y];}
  return c.map(cc=>reprCoords(cc,from,to));
}
function reprGeom(g,from){
  if(from===4326||!g)return g;
  const gg=JSON.parse(JSON.stringify(g));
  switch(gg.type){
    case 'Point':gg.coordinates=reprCoords(gg.coordinates,from,4326);break;
    case 'LineString':case 'MultiPoint':gg.coordinates=gg.coordinates.map(c=>reprCoords(c,from,4326));break;
    case 'Polygon':case 'MultiLineString':gg.coordinates=gg.coordinates.map(r=>r.map(c=>reprCoords(c,from,4326)));break;
    case 'MultiPolygon':gg.coordinates=gg.coordinates.map(p=>p.map(r=>r.map(c=>reprCoords(c,from,4326))));break;
    case 'GeometryCollection':gg.geometries=gg.geometries.map(g2=>reprGeom(g2,from));break;
  }
  return gg;
}

/* ── FILE PARSING ── */
async function parseFile(file){
  const n=file.name.toLowerCase();
  let gj=null;
  if(n.endsWith('.geojson')||n.endsWith('.json'))gj=JSON.parse(await file.text());
  else if(n.endsWith('.kml')){const dom=(new DOMParser).parseFromString(await file.text(),'text/xml');gj=toGeoJSON.kml(dom);}
  else if(n.endsWith('.gpx')){const dom=(new DOMParser).parseFromString(await file.text(),'text/xml');gj=toGeoJSON.gpx(dom);}
  else if(n.endsWith('.kmz')){
    const zip=await JSZip.loadAsync(await file.arrayBuffer());
    const kf=Object.keys(zip.files).find(x=>x.toLowerCase().endsWith('.kml'));
    if(!kf)throw new Error('KMZ sin KML');
    const dom=(new DOMParser).parseFromString(await zip.files[kf].async('string'),'text/xml');
    gj=toGeoJSON.kml(dom);
  }
  else if(n.endsWith('.shp')||n.endsWith('.zip')){const r=await shp(await file.arrayBuffer());gj=Array.isArray(r)?r[0]:r;}
  else if(n.endsWith('.gpkg'))gj=await parseGPKG(file);
  else throw new Error('Formato no soportado: '+n.split('.').pop().toUpperCase());
  if(gj&&gj.type==='Feature')gj={type:'FeatureCollection',features:[gj]};
  if(gj&&gj.features)gj.features=gj.features.filter(f=>f.geometry&&['Polygon','MultiPolygon'].includes(f.geometry.type));
  return gj;
}

let sqlL=null;
async function getSQL(){if(!sqlL)sqlL=await initSqlJs({locateFile:f=>`https://cdnjs.cloudflare.com/ajax/libs/sql.js/1.10.3/${f}`});return sqlL;}
async function parseGPKG(file){
  const SQL=await getSQL();
  const db=new SQL.Database(new Uint8Array(await file.arrayBuffer()));
  const res=db.exec("SELECT table_name,column_name,srs_id FROM gpkg_geometry_columns LIMIT 1");
  if(!res.length||!res[0].values.length)throw new Error('GPKG sin capas de geometría');
  const[tbl,gc,srs]=res[0].values[0];
  const epsg=parseInt(srs)||4326;
  const cp=db.exec(`PRAGMA table_info("${tbl}")`);
  const cols=cp[0].values.map(r=>r[1]).filter(c=>c!==gc);
  const rows=db.exec(`SELECT "${gc}",${cols.map(c=>`"${c}"`).join(',')} FROM "${tbl}"`);
  if(!rows.length)throw new Error('GPKG vacío');
  const features=[];
  for(const row of rows[0].values){
    const blob=row[0];if(!blob)continue;
    const ua=blob instanceof Uint8Array?blob:new Uint8Array(blob);
    try{
      let g=parseGPKGGeom(ua);
      if(!g)continue;
      if(epsg!==4326)g=reprGeom(g,epsg);
      if(!['Polygon','MultiPolygon'].includes(g.type))continue;
      const props={};cols.forEach((c,i)=>props[c]=row[i+1]);
      features.push({type:'Feature',geometry:g,properties:props});
    }catch(e){continue;}
  }
  db.close();
  return{type:'FeatureCollection',features};
}

/* ── UPLOAD ── */
const dz=document.getElementById('dz');
dz.addEventListener('dragover',e=>{e.preventDefault();dz.classList.add('drag-over');});
dz.addEventListener('dragleave',()=>dz.classList.remove('drag-over'));
dz.addEventListener('drop',e=>{e.preventDefault();dz.classList.remove('drag-over');if(e.dataTransfer.files.length)handleUpload(Array.from(e.dataTransfer.files));});
document.getElementById('fi').addEventListener('change',function(){if(this.files.length)handleUpload(Array.from(this.files));});
document.getElementById('pdf-fi').addEventListener('change',function(){if(this.files.length)handlePdfPlanUpload(this.files[0]);});
document.getElementById('cb-pdf-plan').addEventListener('change',function(){togglePdfPlan(this.checked);});

async function handleUpload(files){
  const main=files.find(f=>{const n=f.name.toLowerCase();return n.endsWith('.shp')||n.endsWith('.gpkg')||n.endsWith('.kml')||n.endsWith('.kmz')||n.endsWith('.gpx')||n.endsWith('.geojson')||n.endsWith('.json')||n.endsWith('.zip');});
  if(!main){toast('Archivo no reconocido',true);return;}
  showProg(true);setProg(20,'Leyendo archivo…');
  try{
    let gj;
    if(files.length>1&&main.name.toLowerCase().endsWith('.shp')){
      const z=new JSZip();for(const f of files)z.file(f.name,await f.arrayBuffer());
      const zb=await z.generateAsync({type:'arraybuffer'});
      const r=await shp(zb);gj=Array.isArray(r)?r[0]:r;
      if(gj&&gj.type==='Feature')gj={type:'FeatureCollection',features:[gj]};
      if(gj&&gj.features)gj.features=gj.features.filter(f=>f.geometry&&['Polygon','MultiPolygon'].includes(f.geometry.type));
    }else gj=await parseFile(main);
    setProg(60,'Validando geometría…');
    if(!gj||!gj.features||!gj.features.length)throw new Error('No se encontraron polígonos válidos en el archivo');
    setProg(80,'Añadiendo al mapa…');
    addUser(gj,main.name);
    setProg(100,'¡Cargado!');
    setTimeout(()=>showProg(false),300);
  }catch(e){showProg(false);toast('Error: '+e.message,true,5000);console.error(e);}
}

function addUser(gj,name){
  clearUserLayer();
  S.uGJ=gj;
  S.uLfl=L.geoJSON(gj,{
    style:{color:'#f0c040',fillColor:'#f0c040',fillOpacity:0.15,weight:2.5,dashArray:'6 3'},
    onEachFeature:(f,l)=>{l.bindTooltip(`<b>Polígono de análisis</b><br>${areaHa(f).toFixed(2)} ha`,{className:'itt',sticky:true});}
  }).addTo(map);
  const n=gj.features.length,ha=areaHa(gj);
  document.getElementById('uli').style.display='block';
  document.getElementById('uln').textContent=name;
  document.getElementById('ulf').textContent=`${n} polígono${n>1?'s':''} · ${ha.toFixed(2)} ha`;
  document.getElementById('btn-analyze').disabled=false;
  document.getElementById('btn-clear').style.display='block';
  map.fitBounds(S.uLfl.getBounds(),{padding:[20,20]});
  restackLayers();
  toast(`✅ Cargado: ${n} polígono${n>1?'s':''} (${ha.toFixed(2)} ha)`);
}

function clearUserLayer(){
  if(S.uLfl){map.removeLayer(S.uLfl);S.uLfl=null;}
  clearPdfPlanLayer();
  S.uGJ=null;
  document.getElementById('uli').style.display='none';
  document.getElementById('btn-analyze').disabled=true;
  document.getElementById('btn-clear').style.display='none';
  document.getElementById('fi').value='';
  closeResults();
}

function removePdfManualMarkers(){
  const m=S.pdfManual;
  (m.markers||[]).forEach(x=>{try{map.removeLayer(x);}catch(e){}});
  m.markers=[];m.pending=null;
}

function resetPdfManualControl(){
  const m=S.pdfManual;
  removePdfManualMarkers();
  m.active=false;m.pairs=[];m.pending=null;
  const tools=document.getElementById('pdf-tools');if(tools)tools.classList.remove('on');
  const btn=document.getElementById('btn-pdf-manual');if(btn)btn.textContent='🎯 Ajuste manual';
  updatePdfManualUi();
}

function updatePdfManualUi(){
  const m=S.pdfManual,n=(m.pairs||[]).length;
  const stat=document.getElementById('pdf-manual-stat');
  if(stat)stat.textContent=(m.pending?'Seleccione vértice vectorial · ':'')+n+' pares marcados · mínimo 3, puede agregar más';
  const apply=document.getElementById('btn-pdf-apply');
  if(apply)apply.disabled=n<3;
  const hint=document.getElementById('pdf-manual-hint');
  if(hint)hint.textContent=m.pending?
    'Ahora haga clic cerca del vértice correspondiente del polígono. El punto se ajustará al vértice vectorial más cercano.':
    'Clic en un vértice del plano y luego en su vértice del polígono. Repita al menos 3 veces; puede agregar más pares para mejorar el ajuste.';
  const list=document.getElementById('pdf-pair-list');
  if(list){
    list.innerHTML=(m.pairs||[]).map((p,i)=>
      '<div class="pdf-pair"><span>Par '+(i+1)+' · plano → vector</span><button type="button" onclick="removePdfManualPair('+i+')">Eliminar</button></div>'
    ).join('');
  }
}

function showPdfPlanControls(show){
  const row=document.getElementById('pdf-toggle-row');if(row)row.style.display=show?'flex':'none';
  const clear=document.getElementById('btn-pdf-clear');if(clear)clear.style.display=show?'block':'none';
  const allow=show&&S.pdfPlanData&&S.pdfPlanData.allowManual;
  const manual=document.getElementById('btn-pdf-manual');if(manual)manual.style.display=allow?'block':'none';
  const tools=document.getElementById('pdf-tools');
  if(!allow&&tools)tools.classList.remove('on');
}

function pdfAffinePoint(data,x,y){
  const a=data.affine;
  const p=L.point(a[0]*x+a[1]*y+a[2],a[3]*x+a[4]*y+a[5]);
  return L.CRS.EPSG3857.unproject(p);
}

function pdfAffineBounds(data){
  const w=data.imageWidth,h=data.imageHeight;
  return L.latLngBounds([
    pdfAffinePoint(data,0,0),pdfAffinePoint(data,w,0),
    pdfAffinePoint(data,0,h),pdfAffinePoint(data,w,h)
  ]);
}

const PdfAffineLayer=L.Layer.extend({
  initialize:function(data,options){
    this.data=data;L.setOptions(this,options||{});
  },
  onAdd:function(mapRef){
    this._map=mapRef;
    this._canvas=L.DomUtil.create('canvas','leaflet-zoom-animated');
    this._canvas.style.pointerEvents='none';
    this._canvas.style.opacity=this.options.opacity==null?1:this.options.opacity;
    const pane=mapRef.getPane(this.options.pane||'overlayPane');
    pane.appendChild(this._canvas);
    this._ctx=this._canvas.getContext('2d');
    this._img=new Image();
    this._img.onload=()=>{this._loaded=true;this._reset();};
    this._img.src=this.data.url;
    mapRef.on('move zoom resize viewreset zoomend moveend',this._reset,this);
    this._reset();
  },
  onRemove:function(mapRef){
    mapRef.off('move zoom resize viewreset zoomend moveend',this._reset,this);
    if(this._canvas&&this._canvas.parentNode)this._canvas.parentNode.removeChild(this._canvas);
  },
  setOpacity:function(op){
    this.options.opacity=op;
    if(this._canvas)this._canvas.style.opacity=op;
  },
  _reset:function(){
    if(!this._map||!this._canvas)return;
    const size=this._map.getSize(),topLeft=this._map.containerPointToLayerPoint([0,0]);
    if(this._canvas.width!==size.x)this._canvas.width=size.x;
    if(this._canvas.height!==size.y)this._canvas.height=size.y;
    L.DomUtil.setPosition(this._canvas,topLeft);
    const ctx=this._ctx;
    ctx.setTransform(1,0,0,1,0,0);
    ctx.clearRect(0,0,size.x,size.y);
    if(!this._loaded)return;
    const d=this.data,w=d.imageWidth,h=d.imageHeight;
    const p0=this._map.latLngToLayerPoint(pdfAffinePoint(d,0,0));
    const px=this._map.latLngToLayerPoint(pdfAffinePoint(d,w,0));
    const py=this._map.latLngToLayerPoint(pdfAffinePoint(d,0,h));
    ctx.setTransform((px.x-p0.x)/w,(px.y-p0.y)/w,(py.x-p0.x)/h,(py.y-p0.y)/h,p0.x-topLeft.x,p0.y-topLeft.y);
    ctx.drawImage(this._img,0,0);
    ctx.setTransform(1,0,0,1,0,0);
  }
});

function createPdfPlanLayer(data){
  if(data.affine)return new PdfAffineLayer(data,{pane:'pdfPlanPane',opacity:S.pdfOpacity});
  return L.imageOverlay(data.url,data.bounds,{pane:'pdfPlanPane',opacity:S.pdfOpacity,interactive:false});
}

function setPdfPlanData(data,infoText){
  if(S.pdfLayer){map.removeLayer(S.pdfLayer);S.pdfLayer=null;}
  S.pdfPlanData=data;
  S.pdfLayer=createPdfPlanLayer(data).addTo(map);
  S.pdfName=data.name;
  showPdfPlanControls(true);
  document.getElementById('cb-pdf-plan').checked=true;
  const info=document.getElementById('pdf-info');
  info.style.display='block';info.textContent=infoText;
  restackLayers();
}

function makePdfLineArtTransparent(canvas,threshold=242,bufferPx=2){
  const ctx=canvas.getContext('2d',{willReadFrequently:true});
  const img=ctx.getImageData(0,0,canvas.width,canvas.height);
  const d=img.data,w=canvas.width,h=canvas.height,total=w*h;
  const ink=new Uint8Array(total);
  for(let i=0;i<d.length;i+=4){
    const p=i/4;
    if(d[i+3]<20){d[i+3]=0;continue;}
    const lum=0.299*d[i]+0.587*d[i+1]+0.114*d[i+2];
    const maxc=Math.max(d[i],d[i+1],d[i+2]),minc=Math.min(d[i],d[i+1],d[i+2]);
    const saturated=(maxc-minc)>24;
    if(lum>=threshold&&!saturated){d[i+3]=0;continue;}
    const a=lum<215||saturated?255:Math.round(Math.max(90,Math.min(230,(threshold-lum)*6)));
    d[i+3]=Math.min(d[i+3],a);ink[p]=1;
    if(!saturated&&lum<90){d[i]=0;d[i+1]=0;d[i+2]=0;}
  }
  if(bufferPx>0){
    for(let y=0;y<h;y++){
      for(let x=0;x<w;x++){
        const p=y*w+x,o=p*4;
        if(ink[p])continue;
        let found=-1;
        for(let dy=-bufferPx;dy<=bufferPx&&found<0;dy++){
          const yy=y+dy;if(yy<0||yy>=h)continue;
          for(let dx=-bufferPx;dx<=bufferPx;dx++){
            const xx=x+dx;if(xx<0||xx>=w)continue;
            const q=yy*w+xx;
            if(ink[q]){found=q;break;}
          }
        }
        if(found>=0){
          const dist=Math.hypot((found%w)-x,Math.floor(found/w)-y);
          const alpha=Math.max(115,Math.round(230-(dist/Math.max(1,bufferPx))*75));
          d[o]=255;d[o+1]=255;d[o+2]=255;d[o+3]=alpha;
        }
      }
    }
  }
  ctx.putImageData(img,0,0);
}

function collectGeomCoords(geom,out){
  if(!geom)return out;
  if(geom.type==='Polygon')geom.coordinates.forEach(r=>r.forEach(c=>out.push(c)));
  else if(geom.type==='MultiPolygon')geom.coordinates.forEach(p=>p.forEach(r=>r.forEach(c=>out.push(c))));
  else if(geom.type==='GeometryCollection')geom.geometries.forEach(g=>collectGeomCoords(g,out));
  return out;
}

function projectCoordCRTM05(c){
  return (Math.abs(c[0])>180||Math.abs(c[1])>90)?[c[0],c[1]]:proj4('EPSG:4326','EPSG:5367',[c[0],c[1]]);
}

function collectProjectedRings(geom,out){
  if(!geom)return out;
  if(geom.type==='Polygon'){
    geom.coordinates.forEach(r=>{if(r.length>1)out.push(r.map(projectCoordCRTM05));});
  }else if(geom.type==='MultiPolygon'){
    geom.coordinates.forEach(p=>p.forEach(r=>{if(r.length>1)out.push(r.map(projectCoordCRTM05));}));
  }else if(geom.type==='GeometryCollection'){
    geom.geometries.forEach(g=>collectProjectedRings(g,out));
  }
  return out;
}

function userProjectedBBox(gj){
  const coords=[];
  (gj.features||[]).forEach(f=>collectGeomCoords(f.geometry,coords));
  if(!coords.length)throw new Error('El polígono cargado no tiene coordenadas válidas');
  const rings=[];
  (gj.features||[]).forEach(f=>collectProjectedRings(f.geometry,rings));
  let minX=Infinity,minY=Infinity,maxX=-Infinity,maxY=-Infinity;
  coords.forEach(c=>{
    const p=projectCoordCRTM05(c);
    minX=Math.min(minX,p[0]);minY=Math.min(minY,p[1]);maxX=Math.max(maxX,p[0]);maxY=Math.max(maxY,p[1]);
  });
  const width=maxX-minX,height=maxY-minY;
  if(width<=0||height<=0)throw new Error('No se pudo medir el polígono cargado');
  return{minX,minY,maxX,maxY,width,height,ratio:width/height,rings};
}

function getUserLatLngBounds(){
  if(S.uLfl&&S.uLfl.getBounds)return S.uLfl.getBounds();
  const b=turf.bbox(S.uGJ);
  return L.latLngBounds([b[1],b[0]],[b[3],b[2]]);
}

function qSorted(a,q){
  if(!a.length)return 0;
  const p=(a.length-1)*q,lo=Math.floor(p),hi=Math.ceil(p);
  if(lo===hi)return a[lo];
  return a[lo]+(a[hi]-a[lo])*(p-lo);
}

function robustComponentBox(xs,ys,pad,w,h){
  xs.sort((a,b)=>a-b);ys.sort((a,b)=>a-b);
  const q=xs.length>800?0.005:0;
  const x0=Math.floor(qSorted(xs,q))-pad;
  const y0=Math.floor(qSorted(ys,q))-pad;
  const x1=Math.ceil(qSorted(xs,1-q))+pad;
  const y1=Math.ceil(qSorted(ys,1-q))+pad;
  const x=Math.max(0,x0),y=Math.max(0,y0);
  return{x,y,w:Math.min(w-1,x1)-x+1,h:Math.min(h-1,y1)-y+1};
}

function targetRingSamples(target,box){
  const rings=[];
  const spacing=Math.max(6,Math.min(18,Math.round(Math.max(box.w,box.h)*0.012)));
  const toBox=p=>[
    ((p[0]-target.minX)/target.width)*(box.w-1),
    ((target.maxY-p[1])/target.height)*(box.h-1)
  ];
  (target.rings||[]).forEach(r=>{
    const n=(r.length>2&&r[0][0]===r[r.length-1][0]&&r[0][1]===r[r.length-1][1])?r.length-1:r.length;
    if(n<2)return;
    const pts=[];
    for(let i=0;i<n;i++){
      const a=toBox(r[i]),b=toBox(r[(i+1)%n]);
      const len=Math.hypot(b[0]-a[0],b[1]-a[1]);
      const steps=Math.max(1,Math.ceil(len/spacing));
      for(let s=0;s<steps;s++){
        const t=s/steps;
        pts.push([a[0]+(b[0]-a[0])*t,a[1]+(b[1]-a[1])*t]);
      }
    }
    if(pts.length)rings.push(pts);
  });
  return rings;
}

function hasDarkNear(occ,w,h,x,y,r){
  const cx=Math.round(x),cy=Math.round(y),rr=r*r;
  for(let yy=Math.max(0,cy-r);yy<=Math.min(h-1,cy+r);yy++){
    const dy=yy-cy,row=yy*w;
    for(let xx=Math.max(0,cx-r);xx<=Math.min(w-1,cx+r);xx++){
      const dx=xx-cx;
      if(dx*dx+dy*dy<=rr&&occ[row+xx])return true;
    }
  }
  return false;
}

function longestMissFraction(misses){
  if(!misses.length)return 1;
  let best=0,cur=0;
  for(let i=0;i<misses.length*2;i++){
    if(misses[i%misses.length]){cur++;best=Math.max(best,Math.min(cur,misses.length));}
    else cur=0;
  }
  return best/misses.length;
}

function pdfBoundaryFit(box,target,data,pageW,pageH,isDark){
  const occ=new Uint8Array(box.w*box.h);
  let ink=0;
  for(let yy=box.y;yy<box.y+box.h;yy++){
    const row=(yy-box.y)*box.w;
    for(let xx=box.x;xx<box.x+box.w;xx++){
      if(isDark(yy*pageW+xx)){occ[row+(xx-box.x)]=1;ink++;}
    }
  }
  const rings=targetRingSamples(target,box);
  const radius=Math.max(5,Math.min(24,Math.round(Math.max(box.w,box.h)*0.018)));
  let hits=0,total=0,maxGap=0;
  rings.forEach(samples=>{
    const misses=[];
    samples.forEach(p=>{
      const hit=hasDarkNear(occ,box.w,box.h,p[0],p[1],radius);
      if(hit)hits++;
      total++;
      misses.push(!hit);
    });
    maxGap=Math.max(maxGap,longestMissFraction(misses));
  });
  return{coverage:total?hits/total:0,maxGap,total,radius,ink};
}

function pdfBoxRatioErr(box,target){return Math.abs(Math.log((box.w/box.h)/target.ratio));}
function shrinkPdfBox(box,side,delta){
  const b=Object.assign({},box);
  if(side==='l'){b.x+=delta;b.w-=delta;}
  if(side==='r'){b.w-=delta;}
  if(side==='t'){b.y+=delta;b.h-=delta;}
  if(side==='b'){b.h-=delta;}
  return b;
}

function evalPdfBox(box,orig,target,data,pageW,pageH,isDark,minW,minH){
  if(box.w<minW||box.h<minH||box.x<0||box.y<0||box.x+box.w>pageW||box.y+box.h>pageH)return null;
  const ratioErr=pdfBoxRatioErr(box,target);
  if(ratioErr>0.85)return null;
  const fit=pdfBoundaryFit(box,target,data,pageW,pageH,isDark);
  const shrink=1-(box.w*box.h)/(orig.w*orig.h);
  const score=(1-fit.coverage)*8+fit.maxGap*4+ratioErr*2+shrink*0.45;
  return{box,fit,ratioErr,score};
}

function refinePdfBoxForTarget(seed,target,data,pageW,pageH,isDark,minW,minH){
  let best=evalPdfBox(seed,seed,target,data,pageW,pageH,isDark,minW,minH);
  if(!best)return null;
  const sides=['l','r','t','b'],fracs=[0.04,0.07,0.10,0.14,0.18,0.23,0.28,0.34];
  for(let pass=0;pass<3;pass++){
    let improved=false;
    for(const side of sides){
      const base=best.box;
      const span=(side==='l'||side==='r')?base.w:base.h;
      for(const f of fracs){
        const delta=Math.max(2,Math.round(span*f));
        const cand=evalPdfBox(shrinkPdfBox(base,side,delta),seed,target,data,pageW,pageH,isDark,minW,minH);
        if(cand&&cand.score<best.score-0.03){
          best=cand;improved=true;
        }
      }
    }
    if(!improved)break;
  }
  return best;
}

function detectPdfPredioBox(canvas,userGeoJSON){
  const target=userProjectedBBox(userGeoJSON);
  const ctx=canvas.getContext('2d',{willReadFrequently:true});
  const w=canvas.width,h=canvas.height,total=w*h;
  const data=ctx.getImageData(0,0,w,h).data;
  const seen=new Uint8Array(total);
  const stack=new Int32Array(total);
  const minW=Math.max(30,w*0.08),minH=Math.max(30,h*0.12);
  let best=null;
  const isDark=idx=>{
    const o=idx*4;
    return data[o+3]>20&&data[o]<135&&data[o+1]<135&&data[o+2]<135;
  };
  for(let yy=0;yy<h;yy++){
    for(let xx=0;xx<w;xx++){
      const start=yy*w+xx;
      if(seen[start]||!isDark(start)){seen[start]=1;continue;}
      let top=0,area=0,minX=xx,maxX=xx,minY=yy,maxY=yy;
      const xs=[],ys=[];
      seen[start]=1;stack[top++]=start;
      while(top){
        const idx=stack[--top];
        const y=(idx/w)|0,x=idx-y*w;
        area++;xs.push(x);ys.push(y);
        if(x<minX)minX=x;if(x>maxX)maxX=x;if(y<minY)minY=y;if(y>maxY)maxY=y;
        for(let dy=-1;dy<=1;dy++){
          const ny=y+dy;if(ny<0||ny>=h)continue;
          for(let dx=-1;dx<=1;dx++){
            if(dx===0&&dy===0)continue;
            const nx=x+dx;if(nx<0||nx>=w)continue;
            const nidx=ny*w+nx;
            if(!seen[nidx]){
              seen[nidx]=1;
              if(isDark(nidx))stack[top++]=nidx;
            }
          }
        }
      }
      const rawW=maxX-minX+1,rawH=maxY-minY+1;
      if(area<120||rawW<minW||rawH<minH)continue;
      if(minX<5||minY<5||maxX>w-6||maxY>h-6)continue;
      if(rawW>w*0.78||rawH>h*0.78)continue;
      const pad=Math.max(4,Math.round(Math.min(w,h)*0.004));
      const box=robustComponentBox(xs,ys,pad,w,h);
      if(box.w<minW||box.h<minH)continue;
      const roughRatioErr=pdfBoxRatioErr(box,target);
      if(roughRatioErr>0.85)continue;
      const refined=refinePdfBoxForTarget(box,target,data,w,h,isDark,minW,minH);
      if(!refined)continue;
      if(refined.fit.coverage<0.56||refined.fit.maxGap>0.38)continue;
      const ratio=refined.box.w/refined.box.h;
      const boxFrac=(refined.box.w*refined.box.h)/total;
      const score=refined.score-Math.log(area)/18-boxFrac;
      if(!best||score<best.score)best={
        score,box:refined.box,area,ratio,ratioErr:refined.ratioErr,targetRatio:target.ratio,
        fit:refined.fit
      };
    }
  }
  if(!best)throw new Error('No se cargó el plano: el contorno detectado no coincide lo suficiente con el polígono cargado. Así se evita montar una imagen desplazada o recortada por etiquetas del PDF.');
  return best;
}

function cropPdfToDetectedPredio(canvas,detected){
  const b=detected.box;
  const out=document.createElement('canvas');
  out.width=b.w;out.height=b.h;
  out.getContext('2d',{willReadFrequently:true}).drawImage(canvas,b.x,b.y,b.w,b.h,0,0,b.w,b.h);
  makePdfLineArtTransparent(out);
  return out;
}

async function renderPdfFirstPage(file){
  if(!window.pdfjsLib)throw new Error('No se pudo cargar PDF.js');
  if(pdfjsLib.GlobalWorkerOptions){
    pdfjsLib.GlobalWorkerOptions.workerSrc='https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
  }
  const pdf=await pdfjsLib.getDocument({data:await file.arrayBuffer()}).promise;
  if(!pdf.numPages)throw new Error('PDF sin páginas');
  const page=await pdf.getPage(1);
  const vp0=page.getViewport({scale:1});
  const scale=Math.min(2.4,Math.max(1.5,1800/Math.max(vp0.width,vp0.height)));
  const viewport=page.getViewport({scale});
  const canvas=document.createElement('canvas');
  canvas.width=Math.ceil(viewport.width);
  canvas.height=Math.ceil(viewport.height);
  const ctx=canvas.getContext('2d',{willReadFrequently:true});
  await page.render({canvasContext:ctx,viewport}).promise;
  const result={canvas,pages:pdf.numPages,width:canvas.width,height:canvas.height};
  try{await pdf.destroy();}catch(e){}
  return result;
}

function latLngToPdfPixel(data,latlng){
  if(data.affine){
    const p=L.CRS.EPSG3857.project(latlng),a=data.affine;
    const det=a[0]*a[4]-a[1]*a[3];
    if(Math.abs(det)<1e-9)return null;
    const dx=p.x-a[2],dy=p.y-a[5];
    return[(a[4]*dx-a[1]*dy)/det,(-a[3]*dx+a[0]*dy)/det];
  }
  const b=data.bounds,n=b.getNorth(),s=b.getSouth(),e=b.getEast(),w=b.getWest();
  const x=((latlng.lng-w)/(e-w))*data.imageWidth;
  const y=((n-latlng.lat)/(n-s))*data.imageHeight;
  return[x,y];
}

function pdfClickInsideImage(data,px){
  return px&&px[0]>=0&&px[1]>=0&&px[0]<=data.imageWidth&&px[1]<=data.imageHeight;
}

function collectUserVertices(){
  const out=[];
  function walk(g){
    if(!g)return;
    if(g.type==='Polygon')g.coordinates.forEach(r=>r.forEach(c=>out.push(L.latLng(c[1],c[0]))));
    else if(g.type==='MultiPolygon')g.coordinates.forEach(p=>p.forEach(r=>r.forEach(c=>out.push(L.latLng(c[1],c[0])))));
    else if(g.type==='GeometryCollection')g.geometries.forEach(walk);
  }
  (S.uGJ.features||[]).forEach(f=>walk(f.geometry));
  return out;
}

function nearestUserVertex(latlng){
  const p=map.latLngToContainerPoint(latlng);
  let best=null,bd=Infinity;
  collectUserVertices().forEach(v=>{
    const q=map.latLngToContainerPoint(v),d=p.distanceTo(q);
    if(d<bd){bd=d;best=v;}
  });
  return best?{latlng:best,dist:bd}:null;
}

function addPdfManualMarker(latlng,color,label){
  const marker=L.circleMarker(latlng,{radius:5,color,weight:2,fillColor:color,fillOpacity:.85,interactive:false,pane:'pdfPlanPane'}).addTo(map);
  marker.bindTooltip(label,{permanent:false,direction:'top',className:'itt'});
  S.pdfManual.markers.push(marker);
  return marker;
}

function togglePdfManualMode(){
  if(!S.pdfPlanData){toast('Cargue primero un PDF',true);return;}
  if(!S.pdfPlanData.allowManual){toast('El ajuste manual solo se habilita cuando el calce automático falla por incongruencias.',true,4500);return;}
  S.pdfManual.active=!S.pdfManual.active;
  const tools=document.getElementById('pdf-tools');
  if(tools)tools.classList.toggle('on',S.pdfManual.active);
  const btn=document.getElementById('btn-pdf-manual');
  if(btn)btn.textContent=S.pdfManual.active?'✓ Ajuste activo':'🎯 Ajuste manual';
  updatePdfManualUi();
  toast(S.pdfManual.active?'Ajuste manual activo: marque pares plano → vector':'Ajuste manual pausado',false,3500);
}

function undoPdfManualPoint(){
  const m=S.pdfManual;
  if(m.pending){
    const marker=m.pending.marker;
    m.pending=null;
    if(marker){try{map.removeLayer(marker);}catch(e){} m.markers=(m.markers||[]).filter(x=>x!==marker);}
  }else if(m.pairs.length){
    removePdfManualPair(m.pairs.length-1);
    return;
  }
  updatePdfManualUi();
}

function removePdfManualPair(idx){
  const m=S.pdfManual;
  if(idx<0||idx>=m.pairs.length)return;
  const pair=m.pairs[idx];
  (pair.markers||[]).forEach(marker=>{try{map.removeLayer(marker);}catch(e){}});
  m.markers=(m.markers||[]).filter(marker=>!(pair.markers||[]).includes(marker));
  m.pairs.splice(idx,1);
  updatePdfManualUi();
}

function solve3(A,b){
  const m=A.map((r,i)=>[r[0],r[1],r[2],b[i]]);
  for(let col=0;col<3;col++){
    let piv=col;
    for(let r=col+1;r<3;r++)if(Math.abs(m[r][col])>Math.abs(m[piv][col]))piv=r;
    if(Math.abs(m[piv][col])<1e-12)throw new Error('Los puntos de control no permiten calcular un ajuste estable');
    if(piv!==col){const tmp=m[col];m[col]=m[piv];m[piv]=tmp;}
    const div=m[col][col];
    for(let c=col;c<4;c++)m[col][c]/=div;
    for(let r=0;r<3;r++){
      if(r===col)continue;
      const f=m[r][col];
      for(let c=col;c<4;c++)m[r][c]-=f*m[col][c];
    }
  }
  return[m[0][3],m[1][3],m[2][3]];
}

function fitAffineFromPairs(pairs){
  const N=[[0,0,0],[0,0,0],[0,0,0]],bx=[0,0,0],by=[0,0,0];
  pairs.forEach(pair=>{
    const v=[pair.src[0],pair.src[1],1];
    const dst=L.CRS.EPSG3857.project(L.latLng(pair.dst[1],pair.dst[0]));
    for(let r=0;r<3;r++){
      bx[r]+=v[r]*dst.x;by[r]+=v[r]*dst.y;
      for(let c=0;c<3;c++)N[r][c]+=v[r]*v[c];
    }
  });
  const ax=solve3(N,bx),ay=solve3(N,by);
  return[ax[0],ax[1],ax[2],ay[0],ay[1],ay[2]];
}

function inverseAffinePixel(affine,latlng){
  const p=L.CRS.EPSG3857.project(latlng),a=affine;
  const det=a[0]*a[4]-a[1]*a[3];
  if(Math.abs(det)<1e-9)return null;
  const dx=p.x-a[2],dy=p.y-a[5];
  return[(a[4]*dx-a[1]*dy)/det,(-a[3]*dx+a[0]*dy)/det];
}

async function cropPdfDataAfterManualFit(baseData,affine,userGeoJSON){
  const verts=collectUserVertices();
  if(verts.length<3)return Object.assign({},baseData,{affine});
  const pts=verts.map(v=>inverseAffinePixel(affine,v)).filter(p=>p&&isFinite(p[0])&&isFinite(p[1]));
  if(pts.length<3)return Object.assign({},baseData,{affine});
  let minX=Infinity,minY=Infinity,maxX=-Infinity,maxY=-Infinity;
  pts.forEach(p=>{minX=Math.min(minX,p[0]);minY=Math.min(minY,p[1]);maxX=Math.max(maxX,p[0]);maxY=Math.max(maxY,p[1]);});
  const w=baseData.imageWidth,h=baseData.imageHeight;
  const pad=Math.max(14,Math.round(Math.max(maxX-minX,maxY-minY)*0.04));
  const x0=Math.max(0,Math.floor(minX-pad)),y0=Math.max(0,Math.floor(minY-pad));
  const x1=Math.min(w,Math.ceil(maxX+pad)),y1=Math.min(h,Math.ceil(maxY+pad));
  if(x1-x0<20||y1-y0<20)return Object.assign({},baseData,{affine});
  const img=await _loadImage(baseData.url);
  const out=document.createElement('canvas');
  out.width=x1-x0;out.height=y1-y0;
  out.getContext('2d',{willReadFrequently:true}).drawImage(img,x0,y0,out.width,out.height,0,0,out.width,out.height);
  const a=affine;
  const croppedAffine=[a[0],a[1],a[2]+a[0]*x0+a[1]*y0,a[3],a[4],a[5]+a[3]*x0+a[4]*y0];
  return Object.assign({},baseData,{
    url:out.toDataURL('image/png'),
    imageWidth:out.width,
    imageHeight:out.height,
    affine:croppedAffine,
    manualCrop:true
  });
}

function onPdfManualMapClick(e){
  const m=S.pdfManual;
  if(!m.active||!S.pdfPlanData)return;
  if(e.originalEvent)L.DomEvent.stop(e.originalEvent);
  if(!m.pending){
    const px=latLngToPdfPixel(S.pdfPlanData,e.latlng);
    if(!pdfClickInsideImage(S.pdfPlanData,px)){toast('Haga clic sobre la imagen del plano',true,3500);return;}
    m.pending={src:px,latlng:e.latlng,marker:addPdfManualMarker(e.latlng,'#f0c040','Plano '+(m.pairs.length+1))};
  }else{
    const snap=nearestUserVertex(e.latlng);
    if(!snap){toast('No hay vértices vectoriales para ajustar',true);return;}
    const dst=[snap.latlng.lng,snap.latlng.lat];
    const dstMarker=addPdfManualMarker(snap.latlng,'#56b356','Vector '+(m.pairs.length+1));
    m.pairs.push({src:m.pending.src,dst,markers:[m.pending.marker,dstMarker]});
    m.pending=null;
    if(snap.dist>35)toast('Vértice ajustado al punto vectorial más cercano',false,2500);
  }
  updatePdfManualUi();
}
map.on('click',onPdfManualMapClick);

async function applyPdfManualFit(){
  const m=S.pdfManual;
  if(!S.pdfPlanData||m.pairs.length<3){toast('Marque al menos 3 pares plano/vector',true);return;}
  try{
    const affine=fitAffineFromPairs(m.pairs);
    let data=await cropPdfDataAfterManualFit(S.pdfPlanData,affine,S.uGJ);
    data.allowManual=false;
    data.manualAdjusted=true;
    data.bounds=pdfAffineBounds(data);
    setPdfPlanData(data,(S.pdfName||'PDF cargado')+' · ajuste manual con '+m.pairs.length+' pares · recortado · fondo transparente');
    removePdfManualMarkers();
    m.active=false;m.pairs=[];m.pending=null;
    const tools=document.getElementById('pdf-tools');if(tools)tools.classList.remove('on');
    const btn=document.getElementById('btn-pdf-manual');if(btn)btn.textContent='🎯 Ajuste manual';
    map.fitBounds(data.bounds,{padding:[25,25]});
    toast('Plano ajustado manualmente',false,4500);
  }catch(e){
    toast('Ajuste manual: '+e.message,true,6000);
    console.error(e);
  }
}

async function handlePdfPlanUpload(file){
  if(!file||!file.name.toLowerCase().endsWith('.pdf')){toast('Seleccione un archivo PDF',true);return;}
  if(!S.uGJ){toast('Primero cargue el polígono del predio',true,5000);document.getElementById('pdf-fi').value='';return;}
  showProg(true);setProg(15,'Leyendo PDF del plano…');
  try{
    const bounds=getUserLatLngBounds();
    setProg(35,'Renderizando primera página…');
    const rendered=await renderPdfFirstPage(file);
    let detected=null,crop=null,autoErr=null,autoOk=false;
    setProg(60,'Detectando contorno del predio…');
    try{
      detected=detectPdfPredioBox(rendered.canvas,S.uGJ);
      crop=cropPdfToDetectedPredio(rendered.canvas,detected);
      autoOk=true;
    }catch(e){
      autoErr=e;
      crop=rendered.canvas;
      makePdfLineArtTransparent(crop);
    }
    setProg(82,autoOk?'Georreferenciando recorte del plano…':'Cargando plano para ajuste manual…');
    clearPdfPlanLayer();
    const pdfUrl=crop.toDataURL('image/png');
    const data={url:pdfUrl,bounds,name:file.name,imageWidth:crop.width,imageHeight:crop.height,affine:null,allowManual:!autoOk,autoFit:autoOk};
    const fitTxt=(autoOk&&detected.fit)?` · calce ${Math.round(detected.fit.coverage*100)}%`:'';
    const infoText=autoOk?
      `${file.name} · página 1/${rendered.pages} · contorno validado${fitTxt} · fondo transparente`:
      `${file.name} · página 1/${rendered.pages} · carga referencial · active el ajuste manual para georreferenciar`;
    setPdfPlanData(data,infoText);
    map.fitBounds(bounds,{padding:[25,25]});
    setProg(100,'Plano PDF cargado');
    if(autoOk)toast('📄 Plano PDF cargado como capa referencial',false,4500);
    else{
      console.warn('PDF auto-fit fallback:',autoErr);
      toast('PDF cargado sin calce automático. Use Ajuste manual.',true,6500);
    }
    setTimeout(()=>showProg(false),350);
  }catch(e){
    showProg(false);
    toast('PDF: '+e.message,true,6000);
    console.error(e);
  }finally{
    document.getElementById('pdf-fi').value='';
  }
}

function togglePdfPlan(on){
  if(!S.pdfLayer)return;
  if(on){if(!map.hasLayer(S.pdfLayer))S.pdfLayer.addTo(map);}
  else if(map.hasLayer(S.pdfLayer))map.removeLayer(S.pdfLayer);
  if(on)restackLayers();
}

function clearPdfPlanLayer(){
  if(S.pdfLayer){map.removeLayer(S.pdfLayer);S.pdfLayer=null;}
  resetPdfManualControl();
  S.pdfPlanData=null;
  S.pdfName=null;
  showPdfPlanControls(false);
  const info=document.getElementById('pdf-info');if(info){info.style.display='none';info.textContent='';}
  const cb=document.getElementById('cb-pdf-plan');if(cb)cb.checked=false;
}

/* ── MINI-MAPS ── */
function closeMiniMaps(){
  Object.values(miniMaps).forEach(m=>{try{m.remove();}catch(e){}});
  Object.keys(miniMaps).forEach(k=>delete miniMaps[k]);
}

function initMiniMap(key,userGeoJSON,bounds){
  const div=document.getElementById(`mm-${key}`);
  if(!div)return;
  if(miniMaps[key]){try{miniMaps[key].remove();}catch(e){}}
  const m=L.map(div,{zoomControl:false,attributionControl:false,dragging:false,scrollWheelZoom:false,doubleClickZoom:false,touchZoom:false,boxZoom:false,keyboard:false});
  miniMaps[key]=m;
  // Base = ortofoto emparejada cronológicamente; respaldo: imagen Esri actual
  const okey=PAIR[key];
  let baseAdded=false;
  if(okey&&ORTHO[okey]){
    try{ buildOrthoLayer(okey,{opacity:1}).addTo(m); baseAdded=true; }catch(e){}
  }
  if(!baseAdded){
    L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',{maxNativeZoom:19,maxZoom:22}).addTo(m);
  }
  if(S.gjd[key]){
    L.geoJSON(S.gjd[key],{
      style:f=>({color:getColor(key,f.properties.clase),fillColor:getColor(key,f.properties.clase),fillOpacity:0.55,weight:0.5,opacity:0.85})
    }).addTo(m);
  }
  L.geoJSON(userGeoJSON,{
    style:{color:'#f0c040',fillColor:'transparent',fillOpacity:0,weight:2.5,dashArray:'6 3'}
  }).addTo(m);
  try{m.fitBounds(bounds,MM_FIT);}catch(e){}
  m.invalidateSize();
}

/* ── Mini-mapa de imagen aérea (Esri World Imagery) ── */
function initAerialMiniMap(userGeoJSON,bounds){
  const div=document.getElementById('mm-aerial');
  if(!div)return;
  if(miniMaps['__aerial']){try{miniMaps['__aerial'].remove();}catch(e){}}
  const m=L.map(div,{zoomControl:false,attributionControl:false,dragging:false,scrollWheelZoom:false,doubleClickZoom:false,touchZoom:false,boxZoom:false,keyboard:false});
  miniMaps['__aerial']=m;
  // Solo imagen aérea, sin capas de cobertura, para apreciar el terreno real
  L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',{maxNativeZoom:19,maxZoom:22}).addTo(m);
  if(S.pdfPlanData){
    try{
      m.createPane('pdfPlanPane');
      m.getPane('pdfPlanPane').style.zIndex=650;
      createPdfPlanLayer(S.pdfPlanData).addTo(m);
    }catch(e){console.warn('Mini mapa PDF:',e);}
  }
  L.geoJSON(userGeoJSON,{
    style:{color:'#f0c040',fillColor:'transparent',fillOpacity:0,weight:2.5,dashArray:'6 3'}
  }).addTo(m);
  let center;
  try{
    m.fitBounds(bounds,MM_FIT);
    center=m.getCenter();
  }catch(e){center={lat:9.58,lng:-83.85};}
  m.invalidateSize();
  // Consultar la fecha de adquisición de la imagen en el centro del predio
  fetchEsriImageryDate(center.lat,center.lng);
}

/* ── Consulta de fecha de imagen Esri World Imagery (campo SRC_DATE2) ── */
async function getEsriImageryDateText(lat,lon){
  const d=0.0025;
  const url='https://services.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer/identify'+
    '?f=json&geometry='+encodeURIComponent(JSON.stringify({x:lon,y:lat,spatialReference:{wkid:4326}}))+
    '&geometryType=esriGeometryPoint&sr=4326&tolerance=2&returnGeometry=false&layers=all'+
    '&mapExtent='+[lon-d,lat-d,lon+d,lat+d].join(',')+
    '&imageDisplay=600,600,96';
  const resp=await fetch(url);
  if(!resp.ok)throw new Error('HTTP '+resp.status);
  const info=parseEsriImageryResults(await resp.json());
  if(!info)return null;
  let txt='Fuente: Esri World Imagery';
  if(info.dateStr)txt+=' · '+info.dateStr;
  if(info.provider)txt+=' · '+info.provider;
  if(info.res)txt+=' · '+info.res;
  return {text:txt,dateStr:info.dateStr||null};
}

async function fetchEsriImageryDate(lat,lon){
  const el=document.getElementById('mm-aerial-src');
  const titleEl=document.getElementById('mm-aerial-title');
  try{
    const info=await getEsriImageryDateText(lat,lon);
    if(info){
      const txt=info.text;
      el.textContent=txt;
      S.lastAerialDateLabel=info.dateStr||null;
      if(info.dateStr&&titleEl)titleEl.textContent='MAPA 6. Imagen ESRI ('+info.dateStr+') / Dibujo del plano';
      S.lastAerialDate=txt;
    }else{
      el.textContent='Fuente: Esri World Imagery · fecha no disponible para este punto';
      S.lastAerialDate='Fuente: Esri World Imagery';
      S.lastAerialDateLabel=null;
    }
  }catch(e){
    el.textContent='Fuente: Esri World Imagery · fecha no disponible (sin conexión al servicio de metadatos)';
    S.lastAerialDate='Fuente: Esri World Imagery';
    S.lastAerialDateLabel=null;
    console.warn('Esri imagery date:',e);
  }
}

const _MESES=['enero','febrero','marzo','abril','mayo','junio','julio','agosto','septiembre','octubre','noviembre','diciembre'];
function parseEsriImageryResults(data){
  if(!data||!data.results||!data.results.length)return null;
  // Tomar el resultado de mayor resolución disponible (primer registro con SRC_DATE)
  for(const r of data.results){
    const a=r.attributes||{};
    // El campo de fecha puede venir como SRC_DATE2, SRC_DATE o "Source Date"
    let raw=a.SRC_DATE2??a.SRC_DATE??a['Source Date']??a['SRC_DATE2 (YYYYMMDD)']??null;
    const provider=a.SRC_DESC??a.NICE_DESC??a['Source']??null;
    let resRaw=a.SRC_RES??a['Source Resolution']??null;
    let dateStr=formatEsriDate(raw);
    let res=null;
    if(resRaw!=null&&!isNaN(parseFloat(resRaw)))res=parseFloat(resRaw)+' m/px';
    if(dateStr||provider){
      return {dateStr, provider:provider?String(provider).trim():null, res};
    }
  }
  return null;
}
function formatEsriDate(raw){
  if(raw==null)return null;
  const s=String(raw).trim();
  if(!s||s==='0'||s.toLowerCase()==='null')return null;
  // Formato YYYYMMDD (8 dígitos)
  let m=s.match(/^(\d{4})(\d{2})(\d{2})$/);
  if(m){
    const y=+m[1],mo=+m[2];
    if(mo>=1&&mo<=12)return _MESES[mo-1]+' de '+y;
    return String(y);
  }
  // Formato YYYY-MM-DD o YYYY/MM/DD
  m=s.match(/^(\d{4})[-\/](\d{1,2})[-\/](\d{1,2})$/);
  if(m){
    const y=+m[1],mo=+m[2];
    if(mo>=1&&mo<=12)return _MESES[mo-1]+' de '+y;
    return String(y);
  }
  // Epoch en milisegundos (campo numérico tipo date de ArcGIS)
  if(/^\d{12,13}$/.test(s)){
    const dt=new Date(+s);
    if(!isNaN(dt.getTime()))return _MESES[dt.getUTCMonth()]+' de '+dt.getUTCFullYear();
  }
  // Solo año (4 dígitos)
  m=s.match(/^(\d{4})$/);
  if(m)return m[1];
  // Cualquier otra cosa: devolver tal cual recortado
  return s.length<=24?s:null;
}

/* ── ANALYSIS ── */
async function runAnalysis(){
  if(!S.uGJ)return;
  showProg(true);setProg(5,'Preparando análisis…');
  await new Promise(r=>setTimeout(r,50));
  try{
    let uU;
    if(S.uGJ.features.length===1)uU=S.uGJ.features[0];
    else uU=S.uGJ.features.reduce((a,f)=>{try{return turf.union(a,f);}catch(e){return a;}});
    const uHa=areaHa(uU);
    const results={};let p=10;
    for(const k of Object.keys(LM)){
      setProg(p,`Intersectando: ${LM[k].label}…`);
      await new Promise(r=>setTimeout(r,0));
      if(!S.gjd[k]){results[k]={error:'Capa no disponible',uHa};p+=22;continue;}
      const ca={},bb=turf.bbox(uU);
      let proc=0;
      for(const f of S.gjd[k].features){
        const fb=turf.bbox(f);
        if(fb[0]>bb[2]||fb[2]<bb[0]||fb[1]>bb[3]||fb[3]<bb[1])continue;
        let ix;try{ix=turf.intersect(uU,f);}catch(e){continue;}
        if(!ix)continue;
        const ha=areaHa(ix);if(ha<0.001)continue;
        const cls=f.properties.clase||'Sin clase';
        ca[cls]=(ca[cls]||0)+ha;
        proc++;if(proc%50===0)await new Promise(r=>setTimeout(r,0));
      }
      const tot=Object.values(ca).reduce((a,b)=>a+b,0);
      results[k]={ca,tot,void:Math.max(0,uHa-tot),uHa,hasVoids:LM[k].hasVoids};
      p+=22;
    }
    setProg(98,'Construyendo resultados…');
    displayResults(results,S.uGJ,uU);
    setProg(100,'✅ Completado');
    setTimeout(()=>showProg(false),300);
  }catch(e){showProg(false);toast('Error: '+e.message,true,6000);console.error(e);}
}

/* ── DISPLAY RESULTS ── */
function displayResults(results,userGeoJSON,userUnion){
  closeMiniMaps();
  const rb=document.getElementById('rb');
  rb.innerHTML='';
  let ubounds;
  try{ubounds=L.geoJSON(userGeoJSON).getBounds();}catch(e){ubounds=[[9.46,-84.05],[9.78,-83.63]];}
  // Guardar para exportación a Word
  S.lastResults=results;
  S.lastUserGeoJSON=userGeoJSON;
  S.lastBounds=ubounds;
  try{S.lastUserHa=areaHa(userUnion);}catch(e){S.lastUserHa=0;}
  S.lastUserN=(userGeoJSON.features?userGeoJSON.features.length:1);

  // ─── Mini-maps 2×2 (orden cronológico) ──────────────────────────────────
  const grid=document.createElement('div');
  grid.id='minimap-grid';
  Object.entries(LM).forEach(([key,meta])=>{
    const wrap=document.createElement('div');
    wrap.className='mm-wrap';
    const lbl=document.createElement('div');
    lbl.className='mm-title';
    const okey=PAIR[key];
    const oname=(okey&&ORTHO[okey])?ORTHO[okey].short:'';
    lbl.innerHTML=miniMapTitle(key);
    const md=document.createElement('div');
    md.id=`mm-${key}`;
    md.className='mm-div';
    wrap.appendChild(lbl);
    wrap.appendChild(md);
    if(key==='fn2005'){
      const note=document.createElement('div');
      note.style.cssText='font-size:7.5px;color:var(--gold);background:rgba(212,160,42,.08);border:1px solid #4a3a18;border-radius:3px;padding:3px 5px;margin-top:3px;line-height:1.4';
      note.innerHTML='⚙️ '+FN2005_NOTE;
      wrap.appendChild(note);
    }
    grid.appendChild(wrap);
  });
  // Mini-mapa final: imagen aérea (Esri World Imagery), sin capa de cobertura
  {
    const wrap=document.createElement('div');
    wrap.className='mm-wrap';
    const lbl=document.createElement('div');
    lbl.className='mm-title';
    lbl.id='mm-aerial-title';
    lbl.textContent='MAPA 6. Imagen ESRI (fecha por consultar) / Dibujo del plano';
    const md=document.createElement('div');
    md.id='mm-aerial';
    md.className='mm-div';
    const src=document.createElement('div');
    src.id='mm-aerial-src';
    src.style.cssText='font-size:7.5px;color:#5a8a5c;margin-top:2px;line-height:1.3';
    src.textContent='Fuente: Esri World Imagery — consultando fecha…';
    wrap.appendChild(lbl);
    wrap.appendChild(md);
    wrap.appendChild(src);
    grid.appendChild(wrap);
  }
  rb.appendChild(grid);

  // ─── Divider ────────────────────────────────────────────────────────────
  const sep=document.createElement('div');
  sep.style.cssText='font-size:10px;font-weight:700;color:var(--gold);margin-bottom:7px;padding-bottom:4px;border-bottom:1px solid #204522';
  sep.textContent='📊 Cuadro de superficies por tipo de cobertura';
  rb.appendChild(sep);

  // ─── Table ──────────────────────────────────────────────────────────────
  const tbl=document.createElement('table');
  tbl.className='rtbl';
  tbl.innerHTML=`<thead>
    <tr>
      <th rowspan="2">Mapa de cobertura</th>
      <th rowspan="2">Clasificación</th>
      <th colspan="2" style="text-align:center">Superficie del predio</th>
    </tr>
    <tr>
      <th>(ha)</th>
      <th>(%)</th>
    </tr>
  </thead><tbody></tbody>`;
  const tbody=tbl.querySelector('tbody');

  let hasData=false;
  Object.entries(LM).forEach(([key,meta])=>{
    const res=results[key];
    if(!res||res.error)return;
    const{ca,uHa,hasVoids}=res;
    const voidHa=res.void;
    const nonZero=Object.entries(ca).filter(([,h])=>h>0.01).sort((a,b)=>b[1]-a[1]);
    const showVoid=voidHa>0.01;
    if(!nonZero.length&&!showVoid)return;
    hasData=true;
    const totalRows=nonZero.length+(showVoid?1:0)+1;

    nonZero.forEach(([cls,ha],idx)=>{
      const pct=(ha/uHa*100).toFixed(1);
      const color=getColor(key,cls);
      const tr=document.createElement('tr');
      if(idx===0){
        const td=document.createElement('td');
        td.rowSpan=totalRows;
        td.className='td-layer';
        td.textContent=meta.label;
        tr.appendChild(td);
      }
      tr.innerHTML+=`<td><span style="display:inline-block;width:8px;height:8px;background:${color};border-radius:1px;margin-right:3px;vertical-align:middle"></span>${cls}</td>
        <td class="td-num">${ha.toFixed(2)}</td>
        <td class="td-num">${pct}%<div class="bar-wrap"><div class="bar-fill" style="width:${pct}%;background:${color}"></div></div></td>`;
      tbody.appendChild(tr);
    });

    if(showVoid){
      const pct=(voidHa/uHa*100).toFixed(1);
      const vl=hasVoids?'Sin cobertura forestal':'Área sin clasificar';
      const tr=document.createElement('tr');
      tr.innerHTML=`<td class="td-void">⚠️ ${vl}</td>
        <td class="td-num td-void">${voidHa.toFixed(2)}</td>
        <td class="td-num td-void">${pct}%<div class="bar-wrap"><div class="bar-fill" style="width:${pct}%;background:#e17055"></div></div></td>`;
      tbody.appendChild(tr);
    }

    const trT=document.createElement('tr');
    trT.className='td-total';
    trT.innerHTML=`<td><b>TOTAL</b></td><td class="td-num"><b>${uHa.toFixed(2)}</b></td><td class="td-num"><b>100.0%</b></td>`;
    tbody.appendChild(trT);
  });

  if(!hasData){
    const tr=document.createElement('tr');
    tr.innerHTML='<td colspan="4" style="text-align:center;padding:10px;color:var(--warn)">El polígono no intersecta con las capas de cobertura disponibles. Verifique que se ubique en el área de PNLQ/Tapantí–Macizo de la Muerte.</td>';
    tbody.appendChild(tr);
  }

  rb.appendChild(tbl);

  const note=document.createElement('div');
  note.style.cssText='font-size:8.5px;color:#5a8a5c;margin-top:6px;border-top:1px solid #163318;padding-top:5px;line-height:1.4';
  note.innerHTML='<b>Nota metodológica:</b> Solo se muestran clases con superficie &gt; 0.01 ha. Vacíos CF 2021/2023 = área sin bosque dentro del predio. Geometrías a resolución completa (sin simplificar; redondeo de coordenadas 0.11 m). Áreas calculadas en proyección CRTM05/EPSG:5367, coincidentes con QGIS. Cada mini-mapa muestra la cobertura sobre su ortofoto del período correspondiente (SNIT-IGN / Esri).';
  rb.appendChild(note);

  document.getElementById('rp').style.display='block';
  setTimeout(()=>{
    Object.keys(LM).forEach(k=>initMiniMap(k,userGeoJSON,ubounds));
    initAerialMiniMap(userGeoJSON,ubounds);
  },180);
}

function closeResults(){
  document.getElementById('rp').style.display='none';
  closeMiniMaps();
}

/* ════════════════════════════════════════════════════════════════════════
   EXPORTACIÓN A WORD
   Captura cada mapa componiendo las teselas Esri + dibujando los polígonos
   sobre un canvas (sin librerías externas), y arma un documento Word (.doc)
   con imágenes embebidas y las tablas estadísticas.
*/

/* Proyección lng/lat → píxel del canvas usando el mapa temporal */
function _projPt(m,lng,lat,scale){const p=m.latLngToContainerPoint([lat,lng]);return [p.x*scale,p.y*scale];}
function _drawRings(ctx,m,rings,scale){
  ctx.beginPath();
  rings.forEach(ring=>{
    ring.forEach((c,i)=>{const [x,y]=_projPt(m,c[0],c[1],scale);if(i===0)ctx.moveTo(x,y);else ctx.lineTo(x,y);});
    ctx.closePath();
  });
}
function _drawCobertura(ctx,m,geojson,key,scale,alpha){
  if(!geojson)return;
  geojson.features.forEach(f=>{
    const g=f.geometry;if(!g)return;
    const col=getColor(key,f.properties.clase);
    ctx.save();ctx.globalAlpha=alpha;ctx.fillStyle=col;ctx.strokeStyle=col;ctx.lineWidth=Math.max(0.4,0.5*scale);
    if(g.type==='Polygon'){_drawRings(ctx,m,g.coordinates,scale);ctx.fill('evenodd');ctx.stroke();}
    else if(g.type==='MultiPolygon'){g.coordinates.forEach(poly=>{_drawRings(ctx,m,poly,scale);ctx.fill('evenodd');ctx.stroke();});}
    ctx.restore();
  });
}
function _drawUser(ctx,m,geojson,scale){
  if(!geojson)return;
  ctx.save();ctx.strokeStyle='#f0c040';ctx.lineWidth=Math.max(2,2.5*scale);ctx.setLineDash([6*scale,3*scale]);ctx.fillStyle='rgba(240,192,64,0.10)';
  geojson.features.forEach(f=>{
    const g=f.geometry;if(!g)return;
    if(g.type==='Polygon'){_drawRings(ctx,m,g.coordinates,scale);ctx.fill('evenodd');ctx.stroke();}
    else if(g.type==='MultiPolygon'){g.coordinates.forEach(poly=>{_drawRings(ctx,m,poly,scale);ctx.fill('evenodd');ctx.stroke();});}
  });
  ctx.restore();
}

const REPORT_MAPS=[
  {id:'terra1997_fn2000',title:'TERRA 1997 / FONAFIFO 2000',backgroundKey:'terra1997',coverageKey:'fn2000'},
  {id:'orto0507_fn2005',title:'Ortofoto 2005-2007 / FONAFIFO 2005',backgroundKey:'orto0507',coverageKey:'fn2005'},
  {id:'orto1417_tb2012',title:'Ortofoto 2014-2017 / TIPOS DE BOSQUE 2012',backgroundKey:'orto1417',coverageKey:'tb2012'},
  {id:'esri2021_cf2021',title:'Imagen ESRI 2021 / COBERTURA FORESTAL 2021',backgroundKey:'wb2021',coverageKey:'cf2021'},
  {id:'esri2023_cf2023',title:'Imagen ESRI 2023 / COBERTURA FORESTAL 2023',backgroundKey:'wb2023',coverageKey:'cf2023'},
  {id:'esri_current_pdf',title:'Imagen ESRI (la más actualizada disponible) / Dibujo del plano',currentImagery:true,pdfPlan:true}
];

function _bboxIntersects(a,b){return !(a[0]>b[2]||a[2]<b[0]||a[1]>b[3]||a[3]<b[1]);}
function coverageClassesInView(key,bounds){
  const gj=S.gjd[key],seen=new Set();
  if(!gj)return [];
  const bb=[bounds.getWest(),bounds.getSouth(),bounds.getEast(),bounds.getNorth()];
  const viewPoly=(turf.bboxPolygon?turf.bboxPolygon(bb):null);
  gj.features.forEach(f=>{
    if(!f.geometry)return;
    try{
      if(!_bboxIntersects(turf.bbox(f),bb))return;
      if(viewPoly&&turf.booleanIntersects&&!turf.booleanIntersects(f,viewPoly))return;
      seen.add(f.properties.clase||'Sin clase');
    }catch(e){}
  });
  return Array.from(seen).sort((a,b)=>String(a).localeCompare(String(b),'es'));
}

function _drawNorthArrow(ctx,w,h,scale){
  const x=w-58*scale,y=30*scale,s=34*scale;
  ctx.save();
  ctx.fillStyle='rgba(255,255,255,0.86)';
  ctx.strokeStyle='rgba(0,0,0,0.35)';
  ctx.lineWidth=1*scale;
  ctx.beginPath();ctx.arc(x,y+s*0.55,s*0.72,0,Math.PI*2);ctx.fill();ctx.stroke();
  ctx.fillStyle='#111';ctx.strokeStyle='#fff';ctx.lineWidth=2*scale;
  ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x-s*0.34,y+s);ctx.lineTo(x,y+s*0.72);ctx.lineTo(x+s*0.34,y+s);ctx.closePath();ctx.fill();ctx.stroke();
  ctx.fillStyle='#111';ctx.font=`bold ${16*scale}px Arial`;ctx.textAlign='center';ctx.textBaseline='bottom';
  ctx.fillText('N',x,y-3*scale);
  ctx.restore();
}

function _drawLegend(ctx,items,w,h,scale){
  if(!items||!items.length)return;
  ctx.save();
  ctx.font=`${12*scale}px Arial`;
  const pad=8*scale,rowH=18*scale,sw=13*scale;
  const title='Simbología';
  let maxW=ctx.measureText(title).width;
  items.forEach(it=>{maxW=Math.max(maxW,ctx.measureText(it.label).width+sw+7*scale);});
  const boxW=Math.min(w-24*scale,Math.max(150*scale,maxW+pad*2));
  const boxH=pad*2+16*scale+items.length*rowH;
  const x=12*scale,y=h-boxH-12*scale;
  ctx.fillStyle='rgba(255,255,255,0.88)';
  ctx.strokeStyle='rgba(0,0,0,0.30)';
  ctx.lineWidth=1*scale;
  ctx.fillRect(x,y,boxW,boxH);ctx.strokeRect(x,y,boxW,boxH);
  ctx.fillStyle='#111';ctx.font=`bold ${12*scale}px Arial`;ctx.textBaseline='top';
  ctx.fillText(title,x+pad,y+pad);
  ctx.font=`${11*scale}px Arial`;
  items.forEach((it,i)=>{
    const yy=y+pad+18*scale+i*rowH;
    ctx.fillStyle=it.color;ctx.fillRect(x+pad,yy+2*scale,sw,10*scale);
    ctx.strokeStyle='rgba(0,0,0,0.45)';ctx.strokeRect(x+pad,yy+2*scale,sw,10*scale);
    ctx.fillStyle='#111';ctx.fillText(it.label,x+pad+sw+7*scale,yy);
  });
  ctx.restore();
}

function legendItemsForReportMap(cfg,bounds){
  if(cfg.pdfPlan)return [
    {label:'Dibujo del plano (PDF)',color:'#000000'},
    {label:'Predio de análisis',color:'#f0c040'}
  ];
  if(!cfg.coverageKey)return [];
  return coverageClassesInView(cfg.coverageKey,bounds).map(cls=>({label:cls,color:getColor(cfg.coverageKey,cls)}));
}

function orthoDateLabel(key){
  const o=key&&ORTHO[key];
  return o&&(o.dateLabel||o.discover||null);
}

function currentAerialDateLabel(){
  return S.lastAerialDateLabel||null;
}

function reportMapTitle(cfg){
  if(cfg.pdfPlan){
    const d=currentAerialDateLabel();
    return 'Imagen ESRI ('+(d||'fecha no disponible')+') / Dibujo del plano';
  }
  const d=orthoDateLabel(cfg.backgroundKey);
  if(cfg.backgroundKey==='wb2021')return 'Imagen ESRI 2021 ('+(d||'fecha no disponible')+') / COBERTURA FORESTAL 2021';
  if(cfg.backgroundKey==='wb2023')return 'Imagen ESRI 2023 ('+(d||'fecha no disponible')+') / COBERTURA FORESTAL 2023';
  return cfg.title;
}

function miniMapTitle(key){
  const cfg=REPORT_MAPS.find(x=>x.coverageKey===key);
  return cfg?'MAPA '+(REPORT_MAPS.indexOf(cfg)+1)+'. '+reportMapTitle(cfg):key;
}

function reportMapSource(cfg){
  if(cfg.pdfPlan){
    return (S.lastAerialDate||'Fuente: Esri World Imagery · imagen más actual disponible')+' · Dibujo del plano: '+(S.pdfName||'PDF cargado');
  }
  if(cfg.currentImagery)return S.lastAerialDate||'Fuente: Esri World Imagery';
  const bg=cfg.backgroundKey&&ORTHO[cfg.backgroundKey]?ORTHO[cfg.backgroundKey].name:null;
  const d=orthoDateLabel(cfg.backgroundKey);
  const cov=cfg.coverageKey&&LM[cfg.coverageKey]?LM[cfg.coverageKey].label:null;
  return 'Fondo: '+(bg||'Imagen aérea')+(d?' · Fecha: '+d:'')+(cov?' · Cobertura: '+cov:'');
}

function _loadImage(url){
  return new Promise((resolve,reject)=>{
    const img=new Image();
    img.onload=()=>resolve(img);
    img.onerror=reject;
    img.src=url;
  });
}

function normalizeImageryCanvas(ctx,w,h){
  try{
    const img=ctx.getImageData(0,0,w,h),d=img.data;
    const contrast=1.12,sat=1.10,bright=4;
    for(let i=0;i<d.length;i+=4){
      if(d[i+3]<10)continue;
      let r=(d[i]-128)*contrast+128+bright;
      let g=(d[i+1]-128)*contrast+128+bright;
      let b=(d[i+2]-128)*contrast+128+bright;
      const lum=0.299*r+0.587*g+0.114*b;
      r=lum+(r-lum)*sat;g=lum+(g-lum)*sat;b=lum+(b-lum)*sat;
      d[i]=Math.max(0,Math.min(255,r));
      d[i+1]=Math.max(0,Math.min(255,g));
      d[i+2]=Math.max(0,Math.min(255,b));
    }
    ctx.putImageData(img,0,0);
  }catch(e){
    console.warn('Normalización de imagen omitida:',e);
  }
}

async function _drawPdfPlan(ctx,m,pdfData,scale){
  if(!pdfData||!pdfData.url||!pdfData.bounds)return;
  const img=await _loadImage(pdfData.url);
  if(pdfData.affine){
    const w=pdfData.imageWidth,h=pdfData.imageHeight;
    const p0=m.latLngToContainerPoint(pdfAffinePoint(pdfData,0,0));
    const px=m.latLngToContainerPoint(pdfAffinePoint(pdfData,w,0));
    const py=m.latLngToContainerPoint(pdfAffinePoint(pdfData,0,h));
    ctx.save();
    ctx.setTransform((px.x-p0.x)*scale/w,(px.y-p0.y)*scale/w,(py.x-p0.x)*scale/h,(py.y-p0.y)*scale/h,p0.x*scale,p0.y*scale);
    ctx.drawImage(img,0,0);
    ctx.restore();
    return;
  }
  const nw=m.latLngToContainerPoint(pdfData.bounds.getNorthWest());
  const se=m.latLngToContainerPoint(pdfData.bounds.getSouthEast());
  ctx.drawImage(img,nw.x*scale,nw.y*scale,(se.x-nw.x)*scale,(se.y-nw.y)*scale);
}

function _addReportBaseLayer(m,cfg){
  if(cfg.currentImagery){
    return L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',{crossOrigin:'anonymous',maxNativeZoom:19,maxZoom:22});
  }
  if(cfg.backgroundKey&&ORTHO[cfg.backgroundKey])return buildOrthoLayer(cfg.backgroundKey,{opacity:1,crossOrigin:'anonymous',maxZoom:22});
  return L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',{crossOrigin:'anonymous',maxNativeZoom:19,maxZoom:22});
}

/* Captura un mapa combinado imagen/cobertura para el reporte Word */
async function captureMapImage(cfg,userGeoJSON,bounds,w,h){
  if(typeof cfg==='string')cfg={coverageKey:cfg,currentImagery:true,title:LM[cfg]?LM[cfg].label:cfg};
  const tmp=document.createElement('div');
  tmp.style.cssText='position:absolute;left:-10000px;top:0;width:'+w+'px;height:'+h+'px;background:#16281a;';
  document.body.appendChild(tmp);
  const m=L.map(tmp,{zoomControl:false,attributionControl:false,fadeAnimation:false,zoomAnimation:false,markerZoomAnimation:false,inertia:false});
  const imagery=_addReportBaseLayer(m,cfg);
  await new Promise(res=>{
    let done=false;const finish=()=>{if(!done){done=true;res();}};
    imagery.on('load',()=>setTimeout(finish,300));
    imagery.addTo(m);
    try{m.fitBounds(bounds,MM_FIT);}catch(e){}
    m.invalidateSize();
    setTimeout(finish,6000); // respaldo si 'load' no dispara
  });
  await new Promise(r=>setTimeout(r,250));

  const canvas=document.createElement('canvas');
  canvas.width=w;canvas.height=h;
  const ctx=canvas.getContext('2d');
  ctx.fillStyle='#16281a';ctx.fillRect(0,0,w,h);
  const mapRect=tmp.getBoundingClientRect();
  tmp.querySelectorAll('img.leaflet-tile').forEach(img=>{
    if(!img.complete||img.naturalWidth===0)return;
    const r=img.getBoundingClientRect();
    try{ctx.drawImage(img,r.left-mapRect.left,r.top-mapRect.top,r.width,r.height);}catch(e){}
  });
  normalizeImageryCanvas(ctx,w,h);
  // Vectores sobre la imagen
  if(cfg.coverageKey)_drawCobertura(ctx,m,S.gjd[cfg.coverageKey],cfg.coverageKey,1,0.48);
  if(cfg.pdfPlan&&S.pdfPlanData)await _drawPdfPlan(ctx,m,S.pdfPlanData,1);
  _drawUser(ctx,m,userGeoJSON,1);
  const viewBounds=m.getBounds();
  const legendItems=legendItemsForReportMap(cfg,viewBounds);
  _drawNorthArrow(ctx,w,h,1);
  _drawLegend(ctx,legendItems,w,h,1);

  let dataUrl=null;
  try{
    dataUrl=canvas.toDataURL('image/jpeg',0.88);
  }catch(e){
    // Las teselas "contaminaron" el canvas (sin CORS): generar versión solo-vectores
    const c2=document.createElement('canvas');c2.width=w;c2.height=h;
    const x2=c2.getContext('2d');
    x2.fillStyle='#0f2a18';x2.fillRect(0,0,w,h);
    x2.strokeStyle='#24502e';x2.lineWidth=1;
    for(let gx=0;gx<w;gx+=40){x2.beginPath();x2.moveTo(gx,0);x2.lineTo(gx,h);x2.stroke();}
    for(let gy=0;gy<h;gy+=40){x2.beginPath();x2.moveTo(0,gy);x2.lineTo(w,gy);x2.stroke();}
    normalizeImageryCanvas(x2,w,h);
    if(cfg.coverageKey)_drawCobertura(x2,m,S.gjd[cfg.coverageKey],cfg.coverageKey,1,0.65);
    if(cfg.pdfPlan&&S.pdfPlanData)await _drawPdfPlan(x2,m,S.pdfPlanData,1);
    _drawUser(x2,m,userGeoJSON,1);
    _drawNorthArrow(x2,w,h,1);
    _drawLegend(x2,legendItems,w,h,1);
    try{dataUrl=c2.toDataURL('image/jpeg',0.88);}catch(e2){dataUrl=null;}
  }
  m.remove();tmp.remove();
  return {img:dataUrl,legendItems,viewBounds};
}

function _stamp(){
  const d=new Date();
  const p=n=>String(n).padStart(2,'0');
  return d.getFullYear()+p(d.getMonth()+1)+p(d.getDate())+'_'+p(d.getHours())+p(d.getMinutes());
}
function _fechaLarga(){
  const d=new Date();
  return d.getDate()+' de '+_MESES[d.getMonth()]+' de '+d.getFullYear()+', '+
    String(d.getHours()).padStart(2,'0')+':'+String(d.getMinutes()).padStart(2,'0');
}

/* Construye el cuerpo HTML del documento Word */
function _buildDocBody(reportMaps){
  const R=S.lastResults,uHa=S.lastUserHa,uN=S.lastUserN;
  const resultKeys=Object.keys(LM);
  const azul='#1a5e1c';
  let h='';
  // Encabezado institucional
  h+='<div style="text-align:center;border-bottom:2px solid '+azul+';padding-bottom:8px;margin-bottom:14px">';
  h+='<p style="font-size:15pt;font-weight:bold;color:'+azul+';margin:0">Análisis de Cobertura Forestal</p>';
  h+='<p style="font-size:11pt;margin:2px 0">Parque Nacional Los Quetzales (PNLQ)</p>';
  h+='</div>';
  // Datos del predio
  h+='<table style="width:100%;border-collapse:collapse;font-size:9.5pt;margin-bottom:14px">';
  h+='<tr><td style="border:1px solid #999;padding:5px;background:#eef5ee;font-weight:bold;width:40%">Superficie total del predio analizado</td><td style="border:1px solid #999;padding:5px">'+uHa.toFixed(2)+' ha</td></tr>';
  h+='<tr><td style="border:1px solid #999;padding:5px;background:#eef5ee;font-weight:bold">Número de polígonos</td><td style="border:1px solid #999;padding:5px">'+uN+'</td></tr>';
  h+='<tr><td style="border:1px solid #999;padding:5px;background:#eef5ee;font-weight:bold">Fecha de generación</td><td style="border:1px solid #999;padding:5px">'+_fechaLarga()+'</td></tr>';
  h+='</table>';

  // Sección de mapas
  h+='<p style="font-size:12pt;font-weight:bold;color:'+azul+';border-bottom:1px solid '+azul+';margin:14px 0 8px">1. Mapas combinados imagen aérea / cobertura</p>';
  h+='<p style="font-size:8.5pt;color:#555;margin:0 0 8px;line-height:1.35">Cada mapa usa la imagen aérea como fondo y la cobertura semitransparente encima. La simbología incluida corresponde únicamente a clases presentes en la vista del mapa.</p>';
  reportMaps.forEach((entry,i)=>{
    const cfg=entry.cfg,img=entry.img;
    h+='<div style="text-align:center;page-break-inside:avoid;margin:0 0 16px">';
    h+='<p style="font-size:11pt;font-weight:bold;color:'+azul+';margin:0 0 5px">MAPA '+(i+1)+'. '+(entry.title||reportMapTitle(cfg))+'</p>';
    if(img)h+='<img src="'+img+'" width="620" style="border:1px solid #999"/>';
    else h+='<p style="font-size:8pt;color:#a00">[No fue posible capturar este mapa]</p>';
    h+='<p style="font-size:8.5pt;color:#444;margin:4px 0 0;line-height:1.35">'+entry.source+'</p>';
    if(cfg.pdfPlan&&!S.pdfPlanData)h+='<p style="font-size:8pt;color:#a00;margin:2px 0 0">No se incluyó imagen del plano porque no había PDF cargado al exportar.</p>';
    h+='</div>';
  });

  // Cuadro de superficies (consolidado)
  h+='<p style="font-size:12pt;font-weight:bold;color:'+azul+';border-bottom:1px solid '+azul+';margin:16px 0 8px">2. Cuadro de superficies por tipo de cobertura</p>';
  h+='<table style="width:100%;border-collapse:collapse;font-size:9pt">';
  h+='<tr style="background:'+azul+';color:#fff">'+
     '<th style="border:1px solid #999;padding:5px">Mapa de cobertura</th>'+
     '<th style="border:1px solid #999;padding:5px">Clasificación</th>'+
     '<th style="border:1px solid #999;padding:5px">Superficie (ha)</th>'+
     '<th style="border:1px solid #999;padding:5px">Porcentaje (%)</th></tr>';
  resultKeys.forEach(k=>{
    const res=R[k];if(!res||res.error)return;
    const ca=res.ca,vHa=res.void,hasVoids=res.hasVoids;
    const nz=Object.entries(ca).filter(([,x])=>x>0.01).sort((a,b)=>b[1]-a[1]);
    const showVoid=vHa>0.01;
    if(!nz.length&&!showVoid)return;
    const span=nz.length+(showVoid?1:0)+1;
    let first=true;
    nz.forEach(([cls,ha])=>{
      const pct=(ha/uHa*100).toFixed(1);
      h+='<tr>';
      if(first){h+='<td rowspan="'+span+'" style="border:1px solid #999;padding:5px;font-weight:bold;background:#eef5ee;text-align:center;vertical-align:middle">'+LM[k].label+'</td>';first=false;}
      h+='<td style="border:1px solid #999;padding:4px">'+cls+'</td>'+
         '<td style="border:1px solid #999;padding:4px;text-align:right">'+ha.toFixed(2)+'</td>'+
         '<td style="border:1px solid #999;padding:4px;text-align:right">'+pct+'%</td></tr>';
    });
    if(showVoid){
      const pct=(vHa/uHa*100).toFixed(1);
      const vl=hasVoids?'Sin cobertura forestal':'Área sin clasificar';
      h+='<tr>';
      if(first){h+='<td rowspan="'+span+'" style="border:1px solid #999;padding:5px;font-weight:bold;background:#eef5ee;text-align:center;vertical-align:middle">'+LM[k].label+'</td>';first=false;}
      h+='<td style="border:1px solid #999;padding:4px;color:#c0392b;font-style:italic">'+vl+'</td>'+
         '<td style="border:1px solid #999;padding:4px;text-align:right;color:#c0392b">'+vHa.toFixed(2)+'</td>'+
         '<td style="border:1px solid #999;padding:4px;text-align:right;color:#c0392b">'+pct+'%</td></tr>';
    }
    h+='<tr style="background:#dce9dc;font-weight:bold">'+
       '<td style="border:1px solid #999;padding:4px;text-align:right">TOTAL</td>'+
       '<td style="border:1px solid #999;padding:4px;text-align:right">'+uHa.toFixed(2)+'</td>'+
       '<td style="border:1px solid #999;padding:4px;text-align:right">100.0%</td></tr>';
  });
  h+='</table>';

  // Nota metodológica
  h+='<p style="font-size:8pt;color:#555;margin-top:14px;border-top:1px solid #ccc;padding-top:6px;line-height:1.5">';
  h+='<b>Nota metodológica:</b> Solo se reflejan las clases con superficie &gt; 0.01 ha del predio. '+
     'En las capas Cobertura Forestal 2021/2023, los "vacíos" corresponden a áreas sin bosque dentro del predio. '+
     'Las geometrías se procesan a resolución completa (sin simplificación; redondeo de coordenadas a 0.11 m) y las áreas se calculan en proyección CRTM05/EPSG:5367, de modo que coinciden con QGIS sobre los datos originales; '+
     'para fines registrales o de alta precisión deben emplearse las capas originales en CRTM05/EPSG:5367 mediante QGIS. '+
     'Las imágenes aéreas de los mapas provienen de SNIT-IGN y Esri World Imagery/Wayback según el año indicado; la fecha de la imagen actual corresponde a la tesela consultada en el centro del predio. '+
     'Documento generado por el Visor de Cobertura Forestal — PNLQ (SINAC-ACC).</p>';
  return h;
}

/* Membrete institucional SINAC-ACC (plantilla .dotx oficial) embebido en base64.
   Se reutiliza tal cual para conservar encabezado, pie y estilos institucionales;
   el cuerpo del informe se incrusta como altChunk HTML dentro del .docx. */
const MEMBRETE_DOTX_B64="{{MEMBRETE_DOTX_B64}}";

/* Construye un .docx real a partir del membrete oficial, incrustando el cuerpo
   del informe (HTML) como altChunk. El encabezado/pie del membrete se aplican
   automáticamente a todas las páginas. Requiere Microsoft Word para visualizar
   el contenido incrustado. */
async function _buildDocx(bodyHtml){
  if(typeof JSZip==='undefined')throw new Error('JSZip no está disponible');
  const zip=await JSZip.loadAsync(MEMBRETE_DOTX_B64,{base64:true});
  // Registrar el tipo de contenido de la parte HTML incrustada
  let ct=await zip.file('[Content_Types].xml').async('string');
  ct=ct.replace('wordprocessingml.template.main+xml','wordprocessingml.document.main+xml');
  if(ct.indexOf('Extension="htm"')<0){
    ct=ct.replace('</Types>','<Default Extension="htm" ContentType="text/html"/></Types>');
  }
  zip.file('[Content_Types].xml',ct);
  // Parte HTML con el cuerpo del informe (el membrete proviene del .dotx)
  const html='<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:w="urn:schemas-microsoft-com:office:word" xmlns="http://www.w3.org/TR/REC-html40">'+
    '<head><meta charset="utf-8"><title>Análisis de Cobertura Forestal — PNLQ</title>'+
    '<style>body{font-family:Calibri,Arial,sans-serif;color:#222;margin:0}table{border-collapse:collapse;page-break-inside:auto}tr{page-break-inside:avoid}img{max-width:100%}</style>'+
    '</head><body>'+bodyHtml+'</body></html>';
  zip.file('word/afchunk.htm','﻿'+html);
  // Relación altChunk hacia la parte HTML
  const relId='rIdMembreteReport';
  let rels=await zip.file('word/_rels/document.xml.rels').async('string');
  rels=rels.replace('</Relationships>','<Relationship Id="'+relId+'" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/aFChunk" Target="afchunk.htm"/></Relationships>');
  zip.file('word/_rels/document.xml.rels',rels);
  // Insertar el contenido del informe al inicio del cuerpo, conservando el sectPr
  // (y por tanto el encabezado/pie del membrete) de la plantilla.
  let doc=await zip.file('word/document.xml').async('string');
  doc=doc.replace('<w:body>','<w:body><w:altChunk r:id="'+relId+'"/>');
  zip.file('word/document.xml',doc);
  return await zip.generateAsync({type:'blob',mimeType:'application/vnd.openxmlformats-officedocument.wordprocessingml.document'});
}

function _downloadBlob(blob,filename){
  const url=URL.createObjectURL(blob);
  const a=document.createElement('a');
  a.href=url;a.download=filename;document.body.appendChild(a);a.click();
  setTimeout(()=>{document.body.removeChild(a);URL.revokeObjectURL(url);},1500);
}

async function exportWord(){
  if(!S.lastResults||!S.lastUserGeoJSON){toast('Primero calcule una intersección',true);return;}
  const btn=document.getElementById('btn-word');
  if(btn)btn.disabled=true;
  showProg(true);setProg(5,'Preparando documento…');
  await new Promise(r=>setTimeout(r,30));
  try{
    const ug=S.lastUserGeoJSON,bounds=S.lastBounds;
    const W=960,H=640;
    const reportImages=[];
    const center=bounds.getCenter();
    if(!S.lastAerialDate||S.lastAerialDate==='Fuente: Esri World Imagery'){
      try{
        const info=await getEsriImageryDateText(center.lat,center.lng);
        if(info&&info.text){S.lastAerialDate=info.text;S.lastAerialDateLabel=info.dateStr||null;}
      }catch(e){console.warn('current imagery date for report:',e);}
    }
    let p=8;
    const maps=REPORT_MAPS;
    for(const cfg of maps){
      const title=reportMapTitle(cfg);
      setProg(p,'Capturando mapa: '+title+'…');
      await new Promise(r=>setTimeout(r,30));
      let cap={img:null,legendItems:[]};
      try{cap=await captureMapImage(cfg,ug,bounds,W,H);}catch(e){console.warn(cfg.id,e);}
      reportImages.push({cfg,title,img:cap.img,legendItems:cap.legendItems||[],source:reportMapSource(cfg)});
      p+=Math.max(8,Math.floor(72/maps.length));
    }
    setProg(88,'Construyendo documento Word…');
    await new Promise(r=>setTimeout(r,30));
    const body=_buildDocBody(reportImages);
    const blob=await _buildDocx(body);
    _downloadBlob(blob,'Analisis_cobertura_PNLQ_'+_stamp()+'.docx');
    setProg(100,'✅ Documento generado');
    toast('✅ Documento Word generado');
    setTimeout(()=>showProg(false),600);
  }catch(e){
    showProg(false);toast('Error al generar Word: '+e.message,true,6000);console.error(e);
  }finally{
    if(btn)btn.disabled=false;
  }
}

/* ── BOOT ── */
window.addEventListener('load',async()=>{
  setLS('🌿 Cargando capas…');
  // Descubrir configuración de imágenes aéreas en segundo plano (no bloquea)
  discoverImageryConfig().catch(()=>{});
  try{await loadLayers();toast('✅ Capas de cobertura cargadas');}
  catch(e){toast('Error: '+e.message,true,6000);setLS('Error al cargar capas');}
});
</script>
</body>
</html>"""

HTML = HTML.replace("{{CF2021}}", CF2021).replace("{{CF2023}}", CF2023).replace("{{FN2000}}", FN2000).replace("{{FN2005}}", FN2005).replace("{{TB2012}}", TB2012)

# Membrete institucional SINAC-ACC: se embebe la plantilla .dotx en base64 para
# que la exportación a Word genere un .docx con el encabezado/pie oficiales.
import os, base64
_membrete_path = os.environ.get("MEMBRETE_DOTX_PATH") or os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "membrete_sinac.dotx")
with open(_membrete_path, "rb") as _mf:
    MEMBRETE_DOTX_B64 = base64.b64encode(_mf.read()).decode("ascii")
HTML = HTML.replace("{{MEMBRETE_DOTX_B64}}", MEMBRETE_DOTX_B64)

out = "/mnt/user-data/outputs/visor_cobertura_pnlq.html"
with open(out, "w", encoding="utf-8") as f:
    f.write(HTML)

import os
sz = os.path.getsize(out)
print(f"✅ Generado: {sz/1024/1024:.2f} MB")

checks = {
    "Placeholders resueltos": all(p not in HTML for p in ["{{CF2021}}","{{CF2023}}","{{FN2000}}","{{FN2005}}"]),
    "Tabs": HTML.count('class="tab') >= 3,
    "switchTab fn": "function switchTab" in HTML,
    "panel-cobertura": 'id="panel-cobertura"' in HTML,
    "panel-suelos": 'id="panel-suelos"' in HTML,
    "panel-antecedentes": 'id="panel-antecedentes"' in HTML,
    "Subtítulo SINAC–ACC–Tapantí": "Bloque Tapantí Macizo de la Muerte" in HTML,
    "Nombre CF2021 correcto": "Cobertura Forestal 2021</span>" in HTML,
    "Nombre CF2023 correcto": "Cobertura Forestal 2023</span>" in HTML,
    "Nombre FN2000 correcto": "FONAFIFO 2000</span>" in HTML,
    "Nombre FN2005 correcto": "FONAFIFO 2005</span>" in HTML,
    "Sin 'ACC' en nombres de capa": "ACC</span>" not in HTML,
    "LM label CF2021": '"Cobertura Forestal 2021"' in HTML,
    "LM label FN2000": '"FONAFIFO 2000"' in HTML,
    "Mini-maps grid": "minimap-grid" in HTML,
    "initMiniMap fn": "function initMiniMap" in HTML,
    "Tabla rtbl": "rtbl" in HTML,
    "Barras proporcionales": "bar-fill" in HTML,
    "Filtro >0.01ha": "h>0.01" in HTML,
    "Placeholder suelos": "Suelos Forestales" in HTML,
    "Placeholder antecedentes": "Antecedentes y PNE" in HTML,
    "Decreto 41960 ref": "41960" in HTML,
    "Ley Forestal ref": "7575" in HTML,
    "Capa Tipos de Bosque 2012 (checkbox)": 'id="cb-tb2012"' in HTML,
    "Capa Tipos de Bosque 2012 (leyenda)": 'id="lg-tb2012"' in HTML,
    "Capa Tipos de Bosque 2012 (metadata)": '"Tipos de Bosque 2012"' in HTML,
    "Capa Tipos de Bosque 2012 (datos embebidos)": 'tb2012:"' in HTML and '{{TB2012}}' not in HTML,
    "Orden cronológico menú (fn2000 antes de cf2023)": HTML.find('id="cb-fn2000"') < HTML.find('id="cb-cf2023"'),
    "Orden cronológico LM (fn2000 primero)": HTML.find('fn2000:{label:"FONAFIFO 2000"') < HTML.find('cf2023:{label:"Cobertura Forestal 2023"'),
    "Mini-mapa aéreo (div)": "id='mm-aerial'" in HTML or 'id="mm-aerial"' in HTML,
    "Mini-mapa aéreo (init fn)": "function initAerialMiniMap" in HTML,
    "Consulta fecha Esri": "function fetchEsriImageryDate" in HTML,
    "Parser fecha Esri": "function parseEsriImageryResults" in HTML and "function formatEsriDate" in HTML,
    "Endpoint identify Esri": "World_Imagery/MapServer/identify" in HTML,
    "Default activo cf2023": 'id="cb-cf2023" checked' in HTML,
    "Zoom al predio (MM_FIT maxZoom 18)": "MM_FIT={padding:[6,6],maxZoom:18}" in HTML,
    "Mini-mapas usan MM_FIT": HTML.count("fitBounds(bounds,MM_FIT)") >= 2,
    "Botón Word": 'id="btn-word"' in HTML and "exportWord()" in HTML,
    "Función exportWord": "async function exportWord()" in HTML,
    "Captura de mapa (canvas)": "async function captureMapImage" in HTML,
    "Mapas Word combinados": "const REPORT_MAPS=" in HTML and "TERRA 1997 / FONAFIFO 2000" in HTML and "Imagen ESRI (la más actualizada disponible) / Dibujo del plano" in HTML,
    "Secuencia mapas exacta": HTML.find("TERRA 1997 / FONAFIFO 2000") < HTML.find("Ortofoto 2005-2007 / FONAFIFO 2005") < HTML.find("Ortofoto 2014-2017 / TIPOS DE BOSQUE 2012") < HTML.find("Imagen ESRI 2021 / COBERTURA FORESTAL 2021") < HTML.find("Imagen ESRI 2023 / COBERTURA FORESTAL 2023"),
    "Normalizacion visual mapas": "normalizeImageryCanvas" in HTML and ".mm-div .leaflet-tile{filter:" in HTML,
    "Word una columna centrada": 'width="620"' in HTML and "Mapas combinados imagen aérea / cobertura" in HTML and "page-break-inside:avoid" in HTML,
    "Word simbología interna y norte": "function _drawLegend" in HTML and "function _drawNorthArrow" in HTML and "const title='Simbología'" in HTML,
    "Word imagen plano PDF": "pdfPlanData" in HTML and "Dibujo del plano: " in HTML,
    "Composita teselas (drawImage)": "ctx.drawImage(img" in HTML,
    "Dibuja cobertura en canvas": "function _drawCobertura" in HTML,
    "Dibuja predio en canvas": "function _drawUser" in HTML,
    "Genera .docx Word con membrete": "_buildDocx" in HTML and "wordprocessingml.document" in HTML,
    "Membrete .dotx embebido": "MEMBRETE_DOTX_B64" in HTML and "{{MEMBRETE_DOTX_B64}}" not in HTML and "altChunk" in HTML,
    "Tabla consolidada en Word": "_buildDocBody" in HTML,
    "Tarjeta Imágenes aéreas": "Imágenes aéreas" in HTML,
    "Config ORTHO": "const ORTHO=" in HTML,
    "Ortofoto 2005-2007 (Mosaico5000)": "Mosaico5000" in HTML,
    "Ortofoto 2014-2017 (mosaico alta resolucion)": "ortofoto2017_5000_altaresolucion" in HTML,
    "TERRA 1997 WMTS": "Ortofoto_TERRA_1997_40k/wmts" in HTML and "REQUEST=GetTile" in HTML,
    "WMTS proxy para TERRA 1997": "function proxiedTile" in HTML and "ProxiedTileLayer" in HTML,
    "Version cache-buster": "APP_VERSION" in HTML and "version.json" in HTML,
    "Favicon": "favicon.ico" in HTML,
    "Plano PDF referencial": 'id="pdf-fi"' in HTML and "function handlePdfPlanUpload" in HTML and "pdfjsLib" in HTML,
    "Ajuste manual PDF": 'id="btn-pdf-manual"' in HTML and "function applyPdfManualFit" in HTML and "fitAffineFromPairs" in HTML,
    "PDF affine layer": "const PdfAffineLayer" in HTML and "pdfAffinePoint" in HTML,
    "Detector contorno PDF": "function detectPdfPredioBox" in HTML and "cropPdfToDetectedPredio" in HTML and "contorno detectado" in HTML,
    "Control calce PDF": "function pdfBoundaryFit" in HTML and "refinePdfBoxForTarget" in HTML and "contorno validado" in HTML,
    "Line art PDF transparente": "function makePdfLineArtTransparent" in HTML and "pdfPlanPane" in HTML and "fondo transparente" in HTML,
    "Toggle Imagen del plano": 'id="cb-pdf-plan"' in HTML and "Imagen del plano" in HTML and "function togglePdfPlan" in HTML,
    "Coordenadas CRTM05 en barra": "CR05/CRTM05 E:" in HTML and "EPSG:5367" in HTML,
    "Esri Wayback": "wayback.maptiles.arcgis.com" in HTML,
    "Emparejamiento PAIR": "const PAIR=" in HTML,
    "Descubrimiento runtime": "function discoverImageryConfig" in HTML,
    "Area CRTM05 (5367)": "function geomAreaCRTM05" in HTML and "ringAreaCRTM05" in HTML,
    "Minimap usa ortofoto pareada": "const okey=PAIR[key]" in HTML,
    "Toggle ortofotos exclusivo": "function setOrtho" in HTML,
    "Opacidad ortofoto": 'id="ortho-op"' in HTML,
    "Tarjeta Referencias": "🧭 Referencias" in HTML and 'id="cb-ref"' in HTML,
    "Capa base ELIMINADA": 'name="bm"' not in HTML and "🗺️ Capa base" not in HTML,
    "Panes de referencias separados": "createRefPane('refLinePane',610)" in HTML and "createRefPane('refLabelPane',660)" in HTML,
    "Overlay transparente Esri (transporte/lugares)": "World_Hydro_Reference_Overlay" not in HTML and "World_Transportation" in HTML and "World_Boundaries_and_Places" in HTML,
    "Opacidad referencias por capa": 'id="ref-op"' in HTML and "function setRefOpacity" in HTML and "_refBaseOpacity" in HTML,
    "Tile transparente para 404": "TRANSPARENT_TILE" in HTML and "errorTileUrl" in HTML,
    "Datos resolucion completa (cf2021 ~1.1MB)": len(CF2021)//1024 > 900,
    "FONAFIFO 2005 nueva (1344 feats)": len(json.loads(__import__('gzip').decompress(__import__('base64').b64decode(FN2005)).decode())['features'])==1344,
    "Nota ajuste fn2005 (constante)": "const FN2005_NOTE=" in HTML,
    "Nota ajuste en leyenda": "Capa ajustada:" in HTML,
    "Nota ajuste +210": "+210 m en X" in HTML or "+210 m X" in HTML,
    "Wayback over-zoom (maxNativeZoom 19)": "maxNativeZoom:19" in HTML,
    "Mapa maxZoom 22": "zoom:11,maxZoom:22" in HTML,
    "Discovery robusto (leaf layer)": "function firstLeafLayerName" in HTML,
    "Ortofoto 2014-2017 discovery desactivado": "discoverLayer:false" in HTML and "ortofoto2017_5000_altaresolucion" in HTML,
    "Estado por capa (todas)": "st-orto1417" in HTML and "st-wb2021" in HTML,
    "Proxy OGC configurado": "psforgis-ocg.psforestal.workers.dev/ogc?u=" in HTML,
    "ProxiedWMS (teselas via proxy)": "const ProxiedWMS=L.TileLayer.WMS.extend" in HTML,
    "Descubrimiento via proxy": "fetch(viaProxy(c.capsUrl)" in HTML,
    "Wayback config directo (no proxy)": "fetch('https://s3-us-west-2.amazonaws.com" in HTML,
}
for name,result in checks.items():
    print(f"  {'✅' if result else '❌'} {name}")
