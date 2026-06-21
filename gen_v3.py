import json

with open("/home/claude/cobertura_fo/layers_b64.json") as f:
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
<link rel="icon" href="favicon.ico?v=2026-06-21-pdf-plan-v1">
<link rel="shortcut icon" href="favicon.ico?v=2026-06-21-pdf-plan-v1">
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
        <div style="display:flex;gap:5px;align-items:center">
          <select id="pdf-buffer" title="Buffer para colocar el plano PDF" style="width:66px;background:#08200b;color:var(--txt);border:1px solid #28562b;border-radius:4px;padding:5px;font-size:10px">
            <option value="5">5 m</option>
            <option value="20" selected>20 m</option>
            <option value="50">50 m</option>
            <option value="100">100 m</option>
          </select>
          <button class="btn bp" id="btn-pdf-load" type="button" style="flex:1;width:auto;margin-top:0" onclick="document.getElementById('pdf-fi').click()">📄 Cargar PDF</button>
        </div>
        <input type="file" id="pdf-fi" accept=".pdf" style="display:none">
        <label class="ltog" id="pdf-toggle-row" style="display:none;margin-top:5px">
          <input type="checkbox" id="cb-pdf-plan" checked><span style="flex:1">Mostrar plano PDF</span><span class="lbadge">ref</span>
        </label>
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
  <span id="ci" class="coo">Lat: -- | Lon: --</span>
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
const APP_VERSION='2026-06-21-pdf-plan-v1';
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
  pdfLayer:null,pdfBufferLayer:null,pdfName:null,pdfOpacity:0.72};
const miniMaps={};
// Encuadre ajustado al predio para todos los mini-mapas (zoom al predio)
const MM_FIT={padding:[12,12],maxZoom:17};

/* ── MAP SETUP ── */
const map=L.map('mc',{center:[9.58,-83.85],zoom:11,maxZoom:20});

function createRefPane(name,zIndex){
  map.createPane(name);
  const pane=map.getPane(name);
  pane.style.zIndex=zIndex;
  pane.style.pointerEvents='none';
}
createRefPane('refLinePane',610);
createRefPane('refLabelPane',660);

/* ── CAPA DE REFERENCIAS (superposición transparente) ──
   Los servicios de Esri son tiles ya renderizados. Para evitar franjas y
   líneas encima del texto, se usan solo overlays con alfa limpio: caminos en
   un pane inferior y topónimos/límites en un pane superior. */
const TRANSPARENT_TILE='data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR4nGNgYGBgAAAABQABpfZFQAAAAABJRU5ErkJggg==';
let refOpacity=0.85;
const refTileDefaults={maxZoom:19,updateWhenIdle:true,keepBuffer:2,errorTileUrl:TRANSPARENT_TILE};
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

map.on('mousemove',e=>{document.getElementById('ci').textContent=`Lat: ${e.latlng.lat.toFixed(6)} | Lon: ${e.latlng.lng.toFixed(6)}`;});
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
  wb2021:{name:'Imagen aérea 2021 (Esri)',short:'Imagen aérea 2021 (Esri)',type:'xyz',
    rel:'13851',rel_fallback:'13851',discover:'2021',
    attribution:'Esri World Imagery (Wayback 2021)'},
  wb2023:{name:'Imagen aérea 2023 (Esri)',short:'Imagen aérea 2023 (Esri)',type:'xyz',
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
  } else { // xyz (Esri Wayback) — over-zoom para permitir acercamiento igual al 2023
    const url=WB_BASE.replace('{rel}', c.rel);
    lyr=L.tileLayer(url,{opacity:op, crossOrigin:opts.crossOrigin||null,
      maxNativeZoom:19, maxZoom:opts.maxZoom||20, attribution:c.attribution});
  }
  return lyr;
}

/* Mantiene el orden correcto: ortofoto debajo de las capas de cobertura */
function restackLayers(){
  // las ortofotos al fondo
  Object.values(orthoLayers).forEach(l=>{if(l&&l.bringToBack)l.bringToBack();});
  // luego las capas de cobertura por encima
  Object.keys(LM).forEach(k=>{if(S.lfl[k]&&map.hasLayer(S.lfl[k])&&S.lfl[k].bringToFront)S.lfl[k].bringToFront();});
  // el plano PDF queda como referencia sobre la cobertura, sin alterar el predio
  if(S.pdfLayer&&map.hasLayer(S.pdfLayer)&&S.pdfLayer.bringToFront)S.pdfLayer.bringToFront();
  if(S.pdfBufferLayer&&map.hasLayer(S.pdfBufferLayer)&&S.pdfBufferLayer.bringToFront)S.pdfBufferLayer.bringToFront();
  // el polígono del usuario siempre arriba
  if(S.uLfl&&S.uLfl.bringToFront)S.uLfl.bringToFront();
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
      const items=Object.values(cfg).map(v=>({rel:String(v.releaseNum||'').trim(),label:v.releaseDateLabel||v.itemTitle||'',d:v.releaseDatetime||0}));
      const pick=(year)=>{
        const cand=items.filter(it=>String(it.label).includes(String(year))&&it.rel);
        if(!cand.length)return null;
        cand.sort((a,b)=>b.d-a.d);
        return cand[0];
      };
      const p21=pick(2021), p23=pick(2023);
      if(p21){ORTHO.wb2021.rel=p21.rel;ORTHO.wb2021.attribution='Esri World Imagery (Wayback '+p21.label+')';ORTHO.wb2021.dateLabel=p21.label;}
      if(p23){ORTHO.wb2023.rel=p23.rel;ORTHO.wb2023.attribution='Esri World Imagery (Wayback '+p23.label+')';ORTHO.wb2023.dateLabel=p23.label;}
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

function getPdfBufferMeters(){
  const el=document.getElementById('pdf-buffer');
  const v=Number(el&&el.value)||20;
  return [5,20,50,100].includes(v)?v:20;
}

function getBufferedUserBounds(meters){
  if(!S.uGJ)throw new Error('Primero cargue el polígono del predio');
  const buffered=turf.buffer(S.uGJ,meters,{units:'meters'});
  if(!buffered)throw new Error('No se pudo calcular el buffer del predio');
  const bbox=turf.bbox(buffered);
  return {buffered,bounds:L.latLngBounds([bbox[1],bbox[0]],[bbox[3],bbox[2]])};
}

function makeWhiteTransparent(canvas,threshold=246){
  const ctx=canvas.getContext('2d',{willReadFrequently:true});
  const img=ctx.getImageData(0,0,canvas.width,canvas.height);
  const d=img.data;
  for(let i=0;i<d.length;i+=4){
    if(d[i]>=threshold&&d[i+1]>=threshold&&d[i+2]>=threshold)d[i+3]=0;
    else if(d[i]>225&&d[i+1]>225&&d[i+2]>225)d[i+3]=Math.min(d[i+3],95);
  }
  ctx.putImageData(img,0,0);
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
  const scale=Math.min(2.2,Math.max(1.2,1400/Math.max(vp0.width,vp0.height)));
  const viewport=page.getViewport({scale});
  const canvas=document.createElement('canvas');
  canvas.width=Math.ceil(viewport.width);
  canvas.height=Math.ceil(viewport.height);
  const ctx=canvas.getContext('2d',{willReadFrequently:true});
  await page.render({canvasContext:ctx,viewport}).promise;
  makeWhiteTransparent(canvas);
  const result={url:canvas.toDataURL('image/png'),pages:pdf.numPages,width:canvas.width,height:canvas.height};
  try{await pdf.destroy();}catch(e){}
  return result;
}

async function handlePdfPlanUpload(file){
  if(!file||!file.name.toLowerCase().endsWith('.pdf')){toast('Seleccione un archivo PDF',true);return;}
  if(!S.uGJ){toast('Primero cargue el polígono del predio',true,5000);document.getElementById('pdf-fi').value='';return;}
  showProg(true);setProg(15,'Leyendo PDF del plano…');
  try{
    const meters=getPdfBufferMeters();
    const {buffered,bounds}=getBufferedUserBounds(meters);
    setProg(45,'Renderizando primera página…');
    const rendered=await renderPdfFirstPage(file);
    setProg(75,'Colocando plano sobre el mapa…');
    clearPdfPlanLayer();
    S.pdfLayer=L.imageOverlay(rendered.url,bounds,{opacity:S.pdfOpacity,interactive:false}).addTo(map);
    S.pdfBufferLayer=L.geoJSON(buffered,{style:{color:'#e74c3c',weight:2,dashArray:'6 4',fill:false,opacity:0.9},interactive:false}).addTo(map);
    S.pdfName=file.name;
    document.getElementById('pdf-toggle-row').style.display='flex';
    document.getElementById('btn-pdf-clear').style.display='block';
    document.getElementById('cb-pdf-plan').checked=true;
    const info=document.getElementById('pdf-info');
    info.style.display='block';
    info.textContent=`${file.name} · página 1/${rendered.pages} · buffer ${meters} m · capa referencial`;
    map.fitBounds(bounds,{padding:[25,25]});
    restackLayers();
    setProg(100,'Plano PDF cargado');
    toast('📄 Plano PDF cargado como capa referencial',false,4500);
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
  [S.pdfLayer,S.pdfBufferLayer].forEach(l=>{
    if(!l)return;
    if(on){if(!map.hasLayer(l))l.addTo(map);}
    else if(map.hasLayer(l))map.removeLayer(l);
  });
  if(on)restackLayers();
}

function clearPdfPlanLayer(){
  if(S.pdfLayer){map.removeLayer(S.pdfLayer);S.pdfLayer=null;}
  if(S.pdfBufferLayer){map.removeLayer(S.pdfBufferLayer);S.pdfBufferLayer=null;}
  S.pdfName=null;
  const row=document.getElementById('pdf-toggle-row');if(row)row.style.display='none';
  const btn=document.getElementById('btn-pdf-clear');if(btn)btn.style.display='none';
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
    L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',{maxZoom:18}).addTo(m);
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
  L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',{maxZoom:19}).addTo(m);
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
async function fetchEsriImageryDate(lat,lon){
  const el=document.getElementById('mm-aerial-src');
  const titleEl=document.getElementById('mm-aerial-title');
  // Extensión pequeña alrededor del punto, a escala de zoom ~16-17 (la metadata
  // de Esri se sirve a zoom >=12). imageDisplay y mapExtent deben ser coherentes.
  const d=0.0025;
  const url='https://services.arcgisonline.com/arcgis/rest/services/World_Imagery/MapServer/identify'+
    '?f=json&geometry='+encodeURIComponent(JSON.stringify({x:lon,y:lat,spatialReference:{wkid:4326}}))+
    '&geometryType=esriGeometryPoint&sr=4326&tolerance=2&returnGeometry=false&layers=all'+
    '&mapExtent='+[lon-d,lat-d,lon+d,lat+d].join(',')+
    '&imageDisplay=600,600,96';
  try{
    const resp=await fetch(url);
    if(!resp.ok)throw new Error('HTTP '+resp.status);
    const data=await resp.json();
    const info=parseEsriImageryResults(data);
    if(info){
      let txt='Fuente: Esri World Imagery';
      if(info.dateStr)txt+=' · '+info.dateStr;
      if(info.provider)txt+=' · '+info.provider;
      if(info.res)txt+=' · '+info.res;
      el.textContent=txt;
      if(info.dateStr&&titleEl)titleEl.textContent='Imagen aérea (Esri · '+info.dateStr+')';
      S.lastAerialDate=txt;
    }else{
      el.textContent='Fuente: Esri World Imagery · fecha no disponible para este punto';
      S.lastAerialDate='Fuente: Esri World Imagery';
    }
  }catch(e){
    el.textContent='Fuente: Esri World Imagery · fecha no disponible (sin conexión al servicio de metadatos)';
    S.lastAerialDate='Fuente: Esri World Imagery';
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
    lbl.innerHTML=meta.label+(oname?'<span style="color:#9bc99a;font-weight:400"> · sobre '+oname+'</span>':'');
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
    lbl.textContent='Imagen aérea (Esri)';
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

/* Captura un mapa (cobertura opcional) a imagen base64 JPEG */
async function captureMapImage(coberturaKey,userGeoJSON,bounds,w,h){
  const tmp=document.createElement('div');
  tmp.style.cssText='position:absolute;left:-10000px;top:0;width:'+w+'px;height:'+h+'px;background:#16281a;';
  document.body.appendChild(tmp);
  const m=L.map(tmp,{zoomControl:false,attributionControl:false,fadeAnimation:false,zoomAnimation:false,markerZoomAnimation:false,inertia:false});
  const imagery=L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',{crossOrigin:'anonymous',maxZoom:19});
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
  // Vectores sobre la imagen
  if(coberturaKey)_drawCobertura(ctx,m,S.gjd[coberturaKey],coberturaKey,1,0.6);
  _drawUser(ctx,m,userGeoJSON,1);

  let dataUrl=null;
  try{
    dataUrl=canvas.toDataURL('image/jpeg',0.85);
  }catch(e){
    // Las teselas "contaminaron" el canvas (sin CORS): generar versión solo-vectores
    const c2=document.createElement('canvas');c2.width=w;c2.height=h;
    const x2=c2.getContext('2d');
    x2.fillStyle='#0f2a18';x2.fillRect(0,0,w,h);
    x2.strokeStyle='#24502e';x2.lineWidth=1;
    for(let gx=0;gx<w;gx+=40){x2.beginPath();x2.moveTo(gx,0);x2.lineTo(gx,h);x2.stroke();}
    for(let gy=0;gy<h;gy+=40){x2.beginPath();x2.moveTo(0,gy);x2.lineTo(w,gy);x2.stroke();}
    if(coberturaKey)_drawCobertura(x2,m,S.gjd[coberturaKey],coberturaKey,1,0.75);
    _drawUser(x2,m,userGeoJSON,1);
    try{dataUrl=c2.toDataURL('image/jpeg',0.85);}catch(e2){dataUrl=null;}
  }
  m.remove();tmp.remove();
  return dataUrl;
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
function _buildDocBody(images,aerialImg){
  const R=S.lastResults,uHa=S.lastUserHa,uN=S.lastUserN;
  const azul='#1a5e1c';
  let h='';
  // Encabezado institucional
  h+='<div style="text-align:center;border-bottom:2px solid '+azul+';padding-bottom:8px;margin-bottom:14px">';
  h+='<p style="font-size:15pt;font-weight:bold;color:'+azul+';margin:0">Análisis de Cobertura Forestal</p>';
  h+='<p style="font-size:11pt;margin:2px 0">Parque Nacional Los Quetzales (PNLQ)</p>';
  h+='<p style="font-size:9pt;color:#444;margin:0">SINAC — Área de Conservación Central — Bloque Tapantí Macizo de la Muerte</p>';
  h+='</div>';
  // Datos del predio
  h+='<table style="width:100%;border-collapse:collapse;font-size:9.5pt;margin-bottom:14px">';
  h+='<tr><td style="border:1px solid #999;padding:5px;background:#eef5ee;font-weight:bold;width:40%">Superficie total del predio analizado</td><td style="border:1px solid #999;padding:5px">'+uHa.toFixed(2)+' ha</td></tr>';
  h+='<tr><td style="border:1px solid #999;padding:5px;background:#eef5ee;font-weight:bold">Número de polígonos</td><td style="border:1px solid #999;padding:5px">'+uN+'</td></tr>';
  h+='<tr><td style="border:1px solid #999;padding:5px;background:#eef5ee;font-weight:bold">Fecha de generación</td><td style="border:1px solid #999;padding:5px">'+_fechaLarga()+'</td></tr>';
  h+='<tr><td style="border:1px solid #999;padding:5px;background:#eef5ee;font-weight:bold">Sistema de referencia</td><td style="border:1px solid #999;padding:5px">Análisis en WGS84 (EPSG:4326). Datos originales CRTM05 / EPSG:5367.</td></tr>';
  h+='</table>';

  // Sección de mapas
  h+='<p style="font-size:12pt;font-weight:bold;color:'+azul+';border-bottom:1px solid '+azul+';margin:14px 0 8px">1. Mapas de análisis por capa</p>';
  h+='<table style="width:100%;border-collapse:collapse">';
  const keys=Object.keys(LM);
  for(let i=0;i<keys.length;i+=2){
    h+='<tr>';
    for(let j=i;j<i+2;j++){
      if(j<keys.length){
        const k=keys[j];const img=images[k];
        h+='<td style="width:50%;border:1px solid #ccc;padding:6px;vertical-align:top;text-align:center">';
        h+='<p style="font-size:9.5pt;font-weight:bold;color:'+azul+';margin:0 0 4px">'+LM[k].label+'</p>';
        if(img)h+='<img src="'+img+'" width="320" style="border:1px solid #999"/>';
        else h+='<p style="font-size:8pt;color:#a00">[No fue posible capturar este mapa]</p>';
        if(k==='fn2005')h+='<p style="font-size:7pt;color:#7a5c10;text-align:left;margin:4px 0 0;line-height:1.35">⚙️ '+FN2005_NOTE+'</p>';
        h+='</td>';
      } else {
        h+='<td style="width:50%;border:none"></td>';
      }
    }
    h+='</tr>';
  }
  h+='</table>';

  // Imagen aérea
  h+='<p style="font-size:12pt;font-weight:bold;color:'+azul+';border-bottom:1px solid '+azul+';margin:16px 0 8px">2. Imagen aérea de referencia</p>';
  h+='<div style="text-align:center">';
  if(aerialImg)h+='<img src="'+aerialImg+'" width="430" style="border:1px solid #999"/>';
  else h+='<p style="font-size:8pt;color:#a00">[No fue posible capturar la imagen aérea]</p>';
  h+='<p style="font-size:8.5pt;color:#444;margin:4px 0 0">'+(S.lastAerialDate||'Fuente: Esri World Imagery')+'</p>';
  h+='</div>';

  // Cuadro de superficies (consolidado)
  h+='<p style="font-size:12pt;font-weight:bold;color:'+azul+';border-bottom:1px solid '+azul+';margin:16px 0 8px">3. Cuadro de superficies por tipo de cobertura</p>';
  h+='<table style="width:100%;border-collapse:collapse;font-size:9pt">';
  h+='<tr style="background:'+azul+';color:#fff">'+
     '<th style="border:1px solid #999;padding:5px">Mapa de cobertura</th>'+
     '<th style="border:1px solid #999;padding:5px">Clasificación</th>'+
     '<th style="border:1px solid #999;padding:5px">Superficie (ha)</th>'+
     '<th style="border:1px solid #999;padding:5px">Porcentaje (%)</th></tr>';
  keys.forEach(k=>{
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
     'Las imágenes aéreas provienen de Esri World Imagery; la fecha indicada corresponde a la tesela consultada en el centro del predio. '+
     'Documento generado por el Visor de Cobertura Forestal — PNLQ (SINAC-ACC).</p>';
  return h;
}

function _downloadDoc(bodyHtml,filename){
  const head='<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:w="urn:schemas-microsoft-com:office:word" xmlns="http://www.w3.org/TR/REC-html40">'+
    '<head><meta charset="utf-8"><title>Análisis de Cobertura Forestal — PNLQ</title>'+
    '<!--[if gte mso 9]><xml><w:WordDocument><w:View>Print</w:View><w:Zoom>100</w:Zoom></w:WordDocument></xml><![endif]-->'+
    '<style>@page{size:21.59cm 27.94cm;margin:2cm}body{font-family:Calibri,Arial,sans-serif;color:#222}table{page-break-inside:auto}tr{page-break-inside:avoid}img{max-width:100%}</style>'+
    '</head><body>';
  const tail='</body></html>';
  const blob=new Blob(['\ufeff'+head+bodyHtml+tail],{type:'application/msword'});
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
    const W=720,H=500;
    const images={};
    const keys=Object.keys(LM);
    let p=8;
    for(const k of keys){
      setProg(p,'Capturando mapa: '+LM[k].label+'…');
      await new Promise(r=>setTimeout(r,30));
      try{images[k]=await captureMapImage(k,ug,bounds,W,H);}catch(e){images[k]=null;console.warn(k,e);}
      p+=12;
    }
    setProg(p,'Capturando imagen aérea…');
    await new Promise(r=>setTimeout(r,30));
    let aerial=null;
    try{aerial=await captureMapImage(null,ug,bounds,W,H);}catch(e){console.warn('aerial',e);}
    setProg(88,'Construyendo documento Word…');
    await new Promise(r=>setTimeout(r,30));
    const body=_buildDocBody(images,aerial);
    _downloadDoc(body,'Analisis_cobertura_PNLQ_'+_stamp()+'.doc');
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
    "Zoom al predio (MM_FIT maxZoom 17)": "MM_FIT={padding:[12,12],maxZoom:17}" in HTML,
    "Mini-mapas usan MM_FIT": HTML.count("fitBounds(bounds,MM_FIT)") >= 2,
    "Botón Word": 'id="btn-word"' in HTML and "exportWord()" in HTML,
    "Función exportWord": "async function exportWord()" in HTML,
    "Captura de mapa (canvas)": "async function captureMapImage" in HTML,
    "Composita teselas (drawImage)": "ctx.drawImage(img" in HTML,
    "Dibuja cobertura en canvas": "function _drawCobertura" in HTML,
    "Dibuja predio en canvas": "function _drawUser" in HTML,
    "Genera .doc Word": "application/msword" in HTML,
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
    "Buffer PDF configurable": 'id="pdf-buffer"' in HTML and "getBufferedUserBounds" in HTML and "turf.buffer" in HTML,
    "Toggle Plano PDF": 'id="cb-pdf-plan"' in HTML and "function togglePdfPlan" in HTML,
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
    "Mapa maxZoom 20": "zoom:11,maxZoom:20" in HTML,
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
