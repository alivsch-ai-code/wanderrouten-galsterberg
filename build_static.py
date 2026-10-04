"""Erzeugt die statische Seite docs/index.html für GitHub Pages.

    python build_static.py

Die Seite ist eigenständig (Plotly ist eingebettet) und braucht keinen Server.
"""
import json
from pathlib import Path

from plotly.offline import get_plotlyjs

from routes import CHALET, MAUT_PKW, PLAENE, ROUTES, WETTER, make_df, maps_url

df = make_df()
routes = []
for r in df.to_dict("records"):
    r["maps"] = maps_url(r["dest"])
    r["wetter"] = sorted(r["wetter"])
    r["huette"] = None if r.get("huette") != r.get("huette") else r.get("huette")
    routes.append({k: (v.item() if hasattr(v, "item") else v) for k, v in r.items()})

DATA = {"routes": routes, "wetter": WETTER, "maut": MAUT_PKW, "plaene": PLAENE, "chalet": CHALET}
data_json = json.dumps(DATA, ensure_ascii=False).replace("</", "<\\/")

HTML = r"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Wanderrouten Galsterberg</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{color-scheme:light dark;--bg:#fcfcfb;--card:#f3f6fa;--ink:#0b0b0b;--muted:#52514e;--line:#d5dce6;--blue:#2a78d6;--orange:#eb6834;--accent:#1b3a66}
@media (prefers-color-scheme:dark){:root{--bg:#1a1a19;--card:#242423;--ink:#fff;--muted:#c3c2b7;--line:#3a3a38;--blue:#3987e5;--orange:#d95926;--accent:#9db8e8}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 Inter,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
.hero{position:relative;color:#fff;overflow:hidden;min-height:clamp(300px,46vw,470px);display:flex;align-items:flex-end}
.hero svg.art{position:absolute;inset:0;width:100%;height:100%}
.hero::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,20,40,0) 35%,rgba(10,20,40,.72) 100%)}
.hero .in{position:relative;z-index:1;max-width:1100px;margin:0 auto;padding:0 16px 26px;width:100%}
.eyebrow{display:inline-block;font-size:12px;letter-spacing:.14em;text-transform:uppercase;font-weight:600;background:rgba(255,255,255,.16);backdrop-filter:blur(6px);padding:4px 10px;border-radius:999px;margin-bottom:10px}
h1{margin:0 0 6px;font-size:clamp(28px,5.4vw,52px);line-height:1.05;font-weight:800;letter-spacing:-.02em;text-shadow:0 2px 18px rgba(0,0,0,.35)}
.sub{font-size:clamp(13px,1.8vw,16px);opacity:.92}
.hstats{display:flex;flex-wrap:wrap;gap:8px;margin-top:14px}
.hstats span{background:rgba(255,255,255,.14);backdrop-filter:blur(6px);border:1px solid rgba(255,255,255,.22);border-radius:10px;padding:6px 12px;font-size:13px}
.hstats b{font-size:16px;margin-right:4px}
main{padding-top:18px!important}
.cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:16px;margin:8px 0 20px}
.card{background:var(--card);border-radius:16px;overflow:hidden;box-shadow:0 1px 2px rgba(0,0,0,.06),0 8px 24px rgba(20,40,80,.08);display:flex;flex-direction:column;transition:transform .15s,box-shadow .15s}
.card:hover{transform:translateY(-2px);box-shadow:0 2px 4px rgba(0,0,0,.08),0 14px 32px rgba(20,40,80,.14)}
.cover{position:relative;aspect-ratio:16/9;background:#c9d6e6}
.cover svg,.cover img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:block}
.cover .nr{position:absolute;left:12px;top:12px;width:30px;height:30px;border-radius:50%;background:rgba(10,20,40,.55);backdrop-filter:blur(4px);color:#fff;font-weight:700;display:grid;place-items:center;font-size:14px}
.cover .pill{position:absolute;right:12px;top:14px;box-shadow:0 2px 8px rgba(0,0,0,.25)}
.cover .alt{position:absolute;right:12px;bottom:10px;color:#fff;font-weight:700;font-size:13px;text-shadow:0 1px 6px rgba(0,0,0,.6)}
.cbody{padding:14px 16px 16px;display:flex;flex-direction:column;gap:10px;flex:1}
.cbody h3{margin:0;font-size:17px;line-height:1.25}
.cbody p{margin:0;color:var(--muted);font-size:13.5px}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:6px}
.stats div{background:var(--bg);border-radius:10px;padding:7px 6px;text-align:center}
.stats svg{width:16px;height:16px;color:var(--muted);display:block;margin:0 auto 2px}
.stats b{display:block;font-size:13.5px}.stats span{font-size:10.5px;color:var(--muted)}
.cact{display:flex;gap:8px;margin-top:auto}
.cact .btn{margin:0;flex:1;text-align:center}
.btn.ghost{background:transparent;color:var(--accent);border:1px solid var(--line)}
.dcover{position:relative;aspect-ratio:21/8;border-radius:14px;overflow:hidden;margin:-2px 0 14px;background:#c9d6e6}
.dcover svg,.dcover img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
@media(max-width:640px){.dcover{aspect-ratio:16/9}}
.plans{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px;margin:8px 0 22px}
.plan{background:var(--card);border-radius:16px;padding:16px;display:flex;flex-direction:column;gap:10px;border:2px solid transparent;cursor:pointer;transition:border-color .15s}
.plan.on{border-color:var(--accent)}
.plan .hd{display:flex;align-items:center;gap:10px}
.plan .lt{width:36px;height:36px;border-radius:10px;background:var(--accent);color:var(--bg);display:grid;place-items:center;font-weight:800;font-size:18px;flex:0 0 auto}
.plan h3{margin:0;font-size:16px;line-height:1.2}
.plan .tag{font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:var(--orange);font-weight:700}
.plan p{margin:0;font-size:13.5px;color:var(--muted)}
.plan .tl{display:flex;gap:6px;flex-wrap:wrap}
.plan .tl span{font-size:12px;background:var(--bg);border-radius:999px;padding:3px 9px}
.tline{scroll-margin-top:60px;background:var(--card);border-radius:16px;padding:16px 18px;margin:-8px 0 22px}
.tline h3{margin:0 0 4px}
.tline ol{list-style:none;margin:10px 0 0;padding:0;position:relative}
.tline ol::before{content:"";position:absolute;left:52px;top:6px;bottom:6px;width:2px;background:var(--line)}
.tline li{display:grid;grid-template-columns:44px 1fr;gap:22px;padding:6px 0;position:relative;font-size:14px}
.tline li b{font-variant-numeric:tabular-nums;color:var(--accent)}
.tline li::before{content:"";position:absolute;left:47px;top:12px;width:12px;height:12px;border-radius:50%;background:var(--orange);border:2px solid var(--card)}
.tline .tchips{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}
.tline .tchips a{font-size:13px;text-decoration:none;border:1px solid var(--line);border-radius:999px;padding:4px 10px;color:var(--ink)}
.sec-title{display:flex;align-items:baseline;justify-content:space-between;gap:10px;flex-wrap:wrap}
main{max-width:1100px;margin:0 auto;padding:0 16px 40px}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:14px 0}
.kpi{background:var(--card);border-radius:10px;padding:10px 14px}
.kpi b{display:block;font-size:22px}.kpi span{color:var(--muted);font-size:12px}
.filters{display:flex;flex-wrap:wrap;gap:16px;align-items:center;background:var(--card);border-radius:10px;padding:10px 14px;margin-bottom:10px}
.abwahl{font-size:13px;color:var(--muted);display:flex;gap:6px;align-items:center}
.filters label{font-size:13px;color:var(--muted);display:flex;gap:8px;align-items:center}
.chip{border:1px solid var(--line);border-radius:999px;padding:3px 12px;cursor:pointer;background:transparent;color:var(--ink);font:inherit;font-size:13px}
.chip[aria-pressed=true]{background:var(--accent);color:var(--bg);border-color:var(--accent)}
nav{display:flex;gap:4px;flex-wrap:nowrap;overflow-x:auto;scrollbar-width:none;border-bottom:1px solid var(--line);margin:8px 0 14px;position:sticky;top:0;z-index:5;background:var(--bg)}nav::-webkit-scrollbar{display:none}
nav button{white-space:nowrap;flex:0 0 auto;background:none;border:0;border-bottom:3px solid transparent;padding:9px 12px;font:inherit;color:var(--muted);cursor:pointer}
nav button[aria-selected=true]{color:var(--ink);border-bottom-color:var(--orange);font-weight:600}
section.tab{display:none}section.tab.on{display:block}
h2{font-size:18px;margin:18px 0 6px;color:var(--accent)}
.grid2{display:grid;grid-template-columns:3fr 2fr;gap:18px}
@media(max-width:800px){.grid2{grid-template-columns:1fr}}
.chart{width:100%;min-height:340px}
.note{color:var(--muted);font-size:12.5px;margin:4px 0 10px}
table{width:100%;border-collapse:collapse;font-size:13.5px}
th,td{text-align:left;padding:7px 8px;border-bottom:1px solid var(--line)}th{color:var(--muted);font-weight:600;background:var(--card)}
td.n,th.n{text-align:right;white-space:nowrap}
.tw{overflow-x:auto;-webkit-overflow-scrolling:touch}
.tw table th:first-child,.tw table td:first-child{position:sticky;left:0;background:var(--bg);z-index:1}
@media (max-width:640px){
 .kpis{grid-template-columns:repeat(3,1fr);gap:8px}
 .kpis>*{padding:10px!important}
 .kpis b,.kpis strong{font-size:18px!important}
 .filters{gap:10px;padding:10px 12px}
 .filters label{width:100%;justify-content:space-between}
 .filters input[type=range]{flex:1}
 .filters label:has(input[type=checkbox]){justify-content:flex-start}
 .tw table td:first-child{min-width:150px;max-width:170px}
 .tw::after{content:"← wischen für mehr Spalten →";display:block;font-size:11.5px;color:var(--muted);text-align:center;margin-top:4px}
}
a{color:var(--blue)}
.pill{display:inline-block;padding:1px 9px;border-radius:999px;font-size:12px;color:#fff}
.pill.leicht{background:var(--blue)}.pill.mittel{background:var(--orange)}
select,input[type=number]{font:inherit;padding:6px 8px;border-radius:8px;border:1px solid var(--line);background:var(--bg);color:var(--ink)}
.detail{background:var(--card);border-radius:10px;padding:14px 16px;margin-top:10px}
.detail .m{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:8px;margin:10px 0}
.detail .m div{background:var(--bg);border-radius:8px;padding:6px 10px}.detail .m b{display:block;font-size:17px}.detail .m span{font-size:12px;color:var(--muted)}
.btn{display:inline-block;margin:4px 8px 0 0;padding:8px 14px;border-radius:10px;font-weight:600;background:var(--accent);color:var(--bg);text-decoration:none;font-size:14px}
.msg{background:var(--card);border-left:4px solid var(--blue);padding:10px 14px;border-radius:6px;margin:10px 0}
.warn{border-left-color:var(--orange)}.err{border-left-color:#c0392b}
ul.chk{list-style:none;padding:0}ul.chk li{padding:3px 0}
footer{max-width:1100px;margin:0 auto;padding:0 16px 30px;color:var(--muted);font-size:12.5px}
</style>
</head>
<body>
<header class="hero">
<svg class="art" id="hero-art" viewBox="0 0 1600 600" preserveAspectRatio="xMidYMid slice" aria-hidden="true"></svg>
<div class="in">
<span class="eyebrow">Chalet-Wochenende · Oktober 2026</span>
<h1>Wanderrouten Galsterberg &amp; Ennstal</h1>
<div class="sub">Pruggern, Steiermark · Samstagstour · Verantwortlich: Eugen (Женя)</div>
<div class="hstats" id="hstats"></div>
</div>
</header>
<main>
<div class="filters" role="group" aria-label="Filter">
  <span>Niveau:</span>
  <button class="chip" id="f-leicht" aria-pressed="true">Leicht</button>
  <button class="chip" id="f-mittel" aria-pressed="true">Mittel</button>
  <label>Max. Gehzeit <input type="range" id="f-geh" min="60" max="180" step="15" value="180"> <b id="v-geh">3:00 h</b></label>
  <label>Max. Aufstieg <input type="range" id="f-hm" min="0" max="500" step="5" value="500"> <b id="v-hm">500 Hm</b></label>
  <label><input type="checkbox" id="f-maut"> ohne Mautstraße</label>
  <span class="abwahl">Route ab: <button class="chip" id="ab-chalet" aria-pressed="true">Chalet</button> <button class="chip" id="ab-hier" aria-pressed="false">Mein Standort</button></span>
</div>
<div class="kpis" id="kpis"></div>
<nav role="tablist" id="tabs">
  <button role="tab" data-t="ueber" aria-selected="true">Überblick</button>
  <button role="tab" data-t="hoehe" aria-selected="false">Höhenmeter</button>
  <button role="tab" data-t="anreise" aria-selected="false">Anreise &amp; Gesamtzeit</button>
  <button role="tab" data-t="detail" aria-selected="false">Tourdetails</button>
  <button role="tab" data-t="wetter" aria-selected="false">Wetter-Check</button>
  <button role="tab" data-t="check" aria-selected="false">Checklisten</button>
</nav>
<div id="empty" class="msg warn" hidden>Keine Tour passt zu den Filtern. Bitte oben lockern.</div>

<section class="tab on" id="t-ueber">
  <div class="sec-title"><h2>Tagespläne für Samstag</h2><span class="note">Nach Wetter wählen, Zeiten sind Vorschläge</span></div>
  <div class="plans" id="plans"></div>
  <div class="tline" id="tline"></div>
  <div class="sec-title"><h2>Die Touren</h2><span class="note">Karte antippen für alle Details</span></div>
  <div class="cards" id="cards"></div>
  <div class="grid2">
    <div><h2>Aufwand: Gehzeit gegen Aufstieg</h2><div id="c-bubble" class="chart"></div><div class="note">Blasengröße = Länge in km. Die Zahl im Kreis ist die Tour-Nummer.</div></div>
    <div><h2>Aufstieg je Tour</h2><div id="c-bar" class="chart"></div><div class="note">Blau = leicht, orange = mittel.</div></div>
  </div>
  <h2>Alle Touren im Überblick</h2>
  <div class="tw"><table id="tbl"></table></div>
</section>

<section class="tab" id="t-hoehe">
  <h2>Höhenbereich je Tour</h2><div id="c-band" class="chart"></div>
  <div class="note">Balken von der Starthöhe bis zum höchsten Punkt. Starthöhe = höchster Punkt minus Aufstieg (abgeleitet, daher ca.).</div>
  <h2>Vereinfachtes Höhenprofil</h2>
  <select id="sel-profil" aria-label="Tour für Höhenprofil"></select>
  <div id="c-profil" class="chart"></div>
  <div class="note" id="n-profil"></div>
</section>

<section class="tab" id="t-anreise">
  <h2>Gesamtdauer ab Chalet</h2><div id="c-stack" class="chart"></div>
  <div class="note">Fahrzeiten und Pausen sind Schätzungen. Die genaue Fahrzeit zeigt der Maps-Link bei den Tourdetails.</div>
  <h2>Auto &amp; Maut</h2>
  <p>Personen <input type="number" id="in-pers" min="1" max="20" value="9" style="width:70px"> &nbsp; Plätze pro Auto <input type="number" id="in-pl" min="2" max="9" value="5" style="width:70px"> &nbsp; <b id="out-autos"></b></p>
  <div id="out-maut"></div>
  <div class="tw"><table id="tbl-anreise"></table></div>
</section>

<section class="tab" id="t-detail">
  <select id="sel-detail" aria-label="Tour wählen"></select>
  <div id="detail"></div>
</section>

<section class="tab" id="t-wetter">
  <h2>Welche Tour passt zum Wetter?</h2>
  <div id="wetter-btns" role="group"></div>
  <div class="msg" id="wetter-txt"></div>
  <div class="tw"><table id="tbl-wetter"></table></div>
  <div class="msg warn">Mitte Oktober ist in den Höhenlagen Schnee möglich. Sonnenuntergang ungefähr gegen 18 Uhr (am Tag selbst prüfen). Die Galsterbergalmhütte hat im Herbst Fr–So 9–18 Uhr geöffnet, die Pleschnitzzinken Hütte ist unbewirtschaftet. Die Galsterbergbahn fährt nur im Winter.</div>
</section>

<section class="tab" id="t-check">
  <div class="grid2">
    <div><h2>Checkliste für Eugen</h2><ul class="chk" id="chk-e"></ul></div>
    <div><h2>Ausrüstung</h2><ul class="chk" id="chk-g"></ul></div>
  </div>
  <div class="msg err">Notruf: Bergrettung 140 · Euro-Notruf 112. Bei Unfall oder Wetterumschwung früh umkehren, Gruppe zusammenhalten.</div>
</section>
</main>
<footer>Quellen: schladming-dachstein.at, steiermark.com, hauser-kaibling.at, tourispo.de (geprüft am 04.10.2026). Alle Angaben sind Richtwerte, aktuelle Bedingungen vor Ort prüfen. Anfahrt, Pausen und Gesamtdauer sind Schätzungen.</footer>

<script id="data" type="application/json">__DATA__</script>
<script>__PLOTLY__</script>
<script>
const D = JSON.parse(document.getElementById('data').textContent);
const ALL = D.routes;
const $ = id => document.getElementById(id);
const fmtH = m => Math.floor(m/60) + ':' + String(m%60).padStart(2,'0') + ' h';
const fmtM = v => Math.round(v).toLocaleString('de-DE') + ' m';
const de1 = v => v.toFixed(1).replace('.', ',');
const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
const state = {niv:{leicht:true, mittel:true}, geh:180, hm:500, ohneMaut:false, tab:'ueber', lage:Object.keys(D.wetter)[0]};

function filtered(){
  return ALL.filter(r => state.niv[r.niveau] && r.geh <= state.geh && r.hm <= state.hm && !(state.ohneMaut && r.maut));
}
function col(n){ return n === 'leicht' ? css('--blue') : css('--orange'); }
function layout(extra){
  return Object.assign({margin:{l:10,r:10,t:30,b:40}, paper_bgcolor:'rgba(0,0,0,0)', plot_bgcolor:'rgba(0,0,0,0)',
    font:{color:css('--muted'), size:12}, legend:{orientation:'h', y:1.12, x:0}, hoverlabel:{font:{size:13}}}, extra);
}
const CFG = {responsive:true, displayModeBar:false};
const grid = 'rgba(150,150,150,0.25)';
function plot(id, traces, lay){ Plotly.react(id, traces, lay, CFG); }


// ---------- Illustrationen ----------
function rng(seed){ let x = seed*9301 + 49297; return () => (x = (x*9301 + 49297) % 233280) / 233280; }
const SKIES = [['#7fb3e6','#cfe3f5','#f6e7cf'],['#5d93d1','#a9cdee','#f3d9b5'],['#8db7e0','#dcebf7','#fbe9d0'],['#4f86c6','#9fc6ea','#f1d3a8'],['#76a9dd','#c7def3','#f7e3c6'],['#6c9fd6','#bcd7f1','#f5ddb9']];
function ridge(r, w, base, amp, n, rough){
  const pts = []; for (let i = 0; i <= n; i++){ const x = i/n*w; pts.push([x, base - amp*(0.45 + 0.55*Math.sin(i*1.7 + r()*2))*(0.6 + r()*rough)]); }
  return 'M0,' + base + ' ' + pts.map(p => 'L' + p[0].toFixed(1) + ',' + p[1].toFixed(1)).join(' ') + ' L' + w + ',' + base + ' L' + w + ',1000 L0,1000 Z';
}
function trees(r, w, y0, y1, n, palette, scale){
  let o = ''; for (let i = 0; i < n; i++){ const x = r()*w, y = y0 + r()*(y1 - y0), h = (14 + r()*16)*scale*(0.6 + (y - y0)/(y1 - y0 + 1)*0.8), c = palette[Math.floor(r()*palette.length)];
    o += '<path d="M'+x.toFixed(1)+','+(y-h).toFixed(1)+' L'+(x-h*0.32).toFixed(1)+','+y.toFixed(1)+' L'+(x+h*0.32).toFixed(1)+','+y.toFixed(1)+' Z" fill="'+c+'"/>'; }
  return o;
}
const AUTUMN = ['#2f5a3a','#3b6b45','#c9762d','#d9902f','#9c4a22','#284d33','#e2a43b'];
function tourArt(t, W, H){
  W = W || 640; H = H || 360;
  const r = rng(t.nr*7 + 3), sky = SKIES[(t.nr - 1) % SKIES.length], id = 'g' + t.nr + '_' + W;
  const hi = Math.min(1, Math.max(0.12, (t.top - 600)/1600));
  let peakX = W*(0.48 + r()*0.16), peakY = H*(0.70 - hi*0.52), baseY = H*0.80;
  const lw = W*(0.42 + r()*0.08), rw = W*(0.40 + r()*0.08);
  const valley = t.top < 1000;
  const j = () => (r() - 0.5);
  let mPts, mPath, snow = '', route, sx, sy, fx, fy;
  if (!valley){
    mPts = [[peakX - lw, baseY],[peakX - lw*(0.62 + j()*0.2), baseY - (baseY - peakY)*(0.35 + j()*0.2)],[peakX - lw*(0.33 + j()*0.15), baseY - (baseY - peakY)*(0.66 + j()*0.15)],[peakX - lw*0.12, peakY + (baseY - peakY)*(0.08 + r()*0.08)],[peakX, peakY],[peakX + rw*(0.12 + r()*0.08), peakY + (baseY - peakY)*(0.12 + r()*0.1)],[peakX + rw*(0.36 + j()*0.15), baseY - (baseY - peakY)*(0.6 + j()*0.2)],[peakX + rw*(0.68 + j()*0.15), baseY - (baseY - peakY)*(0.3 + j()*0.15)],[peakX + rw, baseY]];
    if (r() > 0.4){ const k = 0.32 + r()*0.2; mPts.splice(7, 0, [peakX + rw*(0.5 + j()*0.1), baseY - (baseY - peakY)*k]); }
    mPath = 'M' + mPts.map(p => p[0].toFixed(1) + ',' + p[1].toFixed(1)).join(' L') + ' Z';
    if (t.top > 1700) snow = '<path d="M'+(peakX - lw*0.13).toFixed(1)+','+(peakY + (baseY-peakY)*0.12).toFixed(1)+' L'+peakX.toFixed(1)+','+peakY.toFixed(1)+' L'+(peakX + rw*0.15).toFixed(1)+','+(peakY + (baseY-peakY)*0.17).toFixed(1)+' L'+(peakX+rw*0.05).toFixed(1)+','+(peakY+(baseY-peakY)*0.13).toFixed(1)+' L'+(peakX-lw*0.03).toFixed(1)+','+(peakY+(baseY-peakY)*0.19).toFixed(1)+' Z" fill="#fff" opacity=".92"/>';
    sx = peakX - lw*0.78; sy = baseY - 6; fx = peakX; fy = peakY;
    route = 'M'+sx.toFixed(1)+','+sy.toFixed(1)+' C'+(sx + (peakX - sx)*0.35).toFixed(1)+','+(sy - 4).toFixed(1)+' '+(peakX - lw*0.45).toFixed(1)+','+(peakY + (baseY-peakY)*0.55).toFixed(1)+' '+(peakX - lw*0.25).toFixed(1)+','+(peakY + (baseY-peakY)*0.42).toFixed(1)+' S'+(peakX - lw*0.05).toFixed(1)+','+(peakY + (baseY-peakY)*0.08).toFixed(1)+' '+peakX.toFixed(1)+','+(peakY + 2).toFixed(1);
  } else {
    // Talrunde: hohe Kulisse hinten, Weg durch Wiesen vorne
    const peaks = [[W*(0.2 + j()*0.1), H*0.22],[W*(0.55 + j()*0.1), H*0.14],[W*(0.85 + j()*0.08), H*0.26]];
    mPath = peaks.map(([x, y]) => { const w = W*0.26; return 'M'+(x-w).toFixed(1)+','+(H*0.66).toFixed(1)+' L'+(x-w*0.35).toFixed(1)+','+(y+H*0.14).toFixed(1)+' L'+x.toFixed(1)+','+y.toFixed(1)+' L'+(x+w*0.3).toFixed(1)+','+(y+H*0.12).toFixed(1)+' L'+(x+w).toFixed(1)+','+(H*0.66).toFixed(1)+' Z'; }).join(' ');
    snow = peaks.map(([x, y]) => { const w = W*0.26; return '<path d="M'+(x-w*0.1).toFixed(1)+','+(y+H*0.04).toFixed(1)+' L'+x.toFixed(1)+','+y.toFixed(1)+' L'+(x+w*0.1).toFixed(1)+','+(y+H*0.04).toFixed(1)+' L'+(x+w*0.02).toFixed(1)+','+(y+H*0.06).toFixed(1)+' Z" fill="#fff" opacity=".9"/>'; }).join('');
    sx = W*0.08; sy = H*0.90; fx = W*0.86; fy = H*0.80;
    route = 'M'+sx.toFixed(1)+','+sy.toFixed(1)+' C'+(W*0.3).toFixed(1)+','+(H*0.80).toFixed(1)+' '+(W*0.42).toFixed(1)+','+(H*0.95).toFixed(1)+' '+(W*0.6).toFixed(1)+','+(H*0.86).toFixed(1)+' S'+(W*0.78).toFixed(1)+','+(H*0.78).toFixed(1)+' '+fx.toFixed(1)+','+fy.toFixed(1);
    baseY = H*0.70;
  }
  const sun = '<circle cx="'+(W*(0.15 + r()*0.2)).toFixed(1)+'" cy="'+(H*(0.18 + r()*0.08)).toFixed(1)+'" r="'+(H*0.07).toFixed(1)+'" fill="#fff6dc" opacity=".9"/>';
  const clouds = [0,1].map(i => { const cx = r()*W, cy = H*(0.12 + r()*0.18), s = 0.6 + r()*0.7; return '<g opacity=".75" fill="#fff"><ellipse cx="'+cx.toFixed(1)+'" cy="'+cy.toFixed(1)+'" rx="'+(46*s).toFixed(1)+'" ry="'+(11*s).toFixed(1)+'"/><ellipse cx="'+(cx+18*s).toFixed(1)+'" cy="'+(cy-8*s).toFixed(1)+'" rx="'+(26*s).toFixed(1)+'" ry="'+(12*s).toFixed(1)+'"/></g>'; }).join('');
  const water = valley ? '<path d="M0,'+(H*0.93).toFixed(1)+' C'+(W*0.3).toFixed(1)+','+(H*0.88).toFixed(1)+' '+(W*0.6).toFixed(1)+','+(H*0.98).toFixed(1)+' '+W+','+(H*0.91).toFixed(1)+' L'+W+','+(H*0.96).toFixed(1)+' C'+(W*0.6).toFixed(1)+','+(H*1.02).toFixed(1)+' '+(W*0.3).toFixed(1)+','+(H*0.93).toFixed(1)+' 0,'+(H*0.98).toFixed(1)+' Z" fill="#7fb0d8" opacity=".85"/>' : '';
  const flag = '<g transform="translate('+fx.toFixed(1)+','+fy.toFixed(1)+')"><line x1="0" y1="0" x2="0" y2="-22" stroke="#1b2a40" stroke-width="2"/><path d="M0,-22 L15,-17 L0,-12 Z" fill="#eb6834"/></g>';
  return '<svg viewBox="0 0 '+W+' '+H+'" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="Illustration '+t.kurz+'">'+
    '<defs><linearGradient id="s'+id+'" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="'+sky[0]+'"/><stop offset=".6" stop-color="'+sky[1]+'"/><stop offset="1" stop-color="'+sky[2]+'"/></linearGradient>'+
    '<linearGradient id="m'+id+'" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#8f9bab"/><stop offset=".55" stop-color="#6c7a8c"/><stop offset="1" stop-color="#4c596b"/></linearGradient>'+
    '<linearGradient id="v'+id+'" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#7f9a52"/><stop offset="1" stop-color="#55703a"/></linearGradient></defs>'+
    '<rect width="'+W+'" height="'+H+'" fill="url(#s'+id+')"/>'+sun+clouds+
    '<path d="'+ridge(r, W, H*0.66, H*0.22, 9, 0.6)+'" fill="#a9b9cf" opacity=".75"/>'+
    '<path d="'+ridge(r, W, H*0.72, H*0.14, 12, 0.5)+'" fill="#8ea2bb" opacity=".8"/>'+
    '<path d="'+mPath+'" fill="url(#m'+id+')"/>'+snow+
    '<path d="'+mPath+'" fill="none"/>'+
    '<path d="'+ridge(r, W, valley ? H*0.74 : H*0.86, H*0.08, 14, 0.4)+'" fill="url(#v'+id+')"/>'+
    (valley ? trees(r, W, H*0.70, H*0.78, Math.round(W/12), AUTUMN, H/360*0.8) + '<rect x="0" y="'+(H*0.78).toFixed(1)+'" width="'+W+'" height="'+(H*0.22).toFixed(1)+'" fill="#8aa55a"/>' + water : trees(r, W, H*0.80, H*0.97, Math.round(W/9), AUTUMN, H/360))+
    '<path d="'+route+'" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" opacity=".55"/>'+
    '<path d="'+route+'" fill="none" stroke="#eb6834" stroke-width="2.6" stroke-dasharray="7 6" stroke-linecap="round"/>'+
    '<circle cx="'+sx.toFixed(1)+'" cy="'+sy.toFixed(1)+'" r="5" fill="#fff" stroke="#eb6834" stroke-width="2.5"/>'+flag+'</svg>';
}
function heroArt(){
  const W = 1600, H = 600, r = rng(42);
  const far = ridge(r, W, H*0.58, H*0.26, 16, 0.7), mid = ridge(r, W, H*0.68, H*0.22, 20, 0.6), near = ridge(r, W, H*0.80, H*0.14, 24, 0.5);
  let peaks = ''; [[0.18,0.30],[0.47,0.22],[0.74,0.27]].forEach(([px, py]) => { const x = W*px, y = H*py, w = W*0.17;
    peaks += '<path d="M'+(x-w)+','+(H*0.62)+' L'+(x-w*0.4)+','+(y+H*0.15)+' L'+(x-w*0.1)+','+(y+H*0.03)+' L'+x+','+y+' L'+(x+w*0.2)+','+(y+H*0.06)+' L'+(x+w*0.5)+','+(y+H*0.18)+' L'+(x+w)+','+(H*0.62)+' Z" fill="url(#hm)"/>'+
             '<path d="M'+(x-w*0.12)+','+(y+H*0.04)+' L'+x+','+y+' L'+(x+w*0.22)+','+(y+H*0.07)+' L'+(x+w*0.08)+','+(y+H*0.06)+' L'+(x-w*0.02)+','+(y+H*0.09)+' Z" fill="#fff" opacity=".9"/>'; });
  const chalet = '<g transform="translate('+(W*0.62)+','+(H*0.80)+')"><rect x="-34" y="-30" width="68" height="34" fill="#7a4a2a"/><path d="M-44,-28 L0,-62 L44,-28 Z" fill="#4a2c1a"/><rect x="-10" y="-14" width="14" height="18" fill="#f4c46a"/><rect x="12" y="-22" width="12" height="10" fill="#f4c46a"/><rect x="18" y="-58" width="7" height="16" fill="#4a2c1a"/></g>';
  $('hero-art').innerHTML = '<defs><linearGradient id="hs" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3f6fae"/><stop offset=".55" stop-color="#9cc0e4"/><stop offset="1" stop-color="#f3cf9c"/></linearGradient>'+
    '<linearGradient id="hm" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#9aa6b6"/><stop offset="1" stop-color="#55627a"/></linearGradient>'+
    '<radialGradient id="hsun"><stop offset="0" stop-color="#fff4d6"/><stop offset="1" stop-color="#fff4d6" stop-opacity="0"/></radialGradient></defs>'+
    '<rect width="'+W+'" height="'+H+'" fill="url(#hs)"/><circle cx="'+(W*0.86)+'" cy="'+(H*0.30)+'" r="160" fill="url(#hsun)"/><circle cx="'+(W*0.86)+'" cy="'+(H*0.30)+'" r="34" fill="#fff6df"/>'+
    '<path d="'+far+'" fill="#b4c2d6" opacity=".7"/>'+peaks+'<path d="'+mid+'" fill="#6f8aa6" opacity=".85"/>'+
    '<path d="'+near+'" fill="#58703f"/>'+trees(r, W, H*0.76, H*1.0, 150, AUTUMN, 1.6)+chalet;
}
const ICO = {
  km:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M4 18c4 0 4-12 8-12s4 12 8 12"/><circle cx="4" cy="18" r="1.5"/><circle cx="20" cy="18" r="1.5"/></svg>',
  geh:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
  hm:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 18l6-7 4 4 8-9"/><path d="M15 6h6v6"/></svg>',
  top:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M2 20l7-12 4 6 3-4 6 10z"/></svg>'
};
const photo = t => '<img src="img/tour-'+t.nr+'.jpg" alt="'+t.kurz+'" loading="lazy" onerror="this.remove()">';
function renderCards(f){
  $('cards').innerHTML = f.map(t => '<article class="card"><div class="cover">'+tourArt(t)+photo(t)+'<span class="nr">'+t.nr+'</span><span class="pill '+t.niveau+'">'+t.niveau+'</span><span class="alt">▲ '+fmtM(t.top)+'</span></div>'+
    '<div class="cbody"><h3>'+t.name+'</h3><p>'+t.plus[0]+'</p>'+
    '<div class="stats"><div>'+ICO.km+'<b>'+de1(t.km)+' km</b><span>Länge</span></div><div>'+ICO.geh+'<b>'+fmtH(t.geh)+'</b><span>Gehzeit</span></div><div>'+ICO.hm+'<b>'+t.hm+'</b><span>Hm</span></div><div>'+ICO.top+'<b>'+fmtH(t.gesamt)+'</b><span>ab Chalet</span></div></div>'+
    '<div class="cact"><a class="btn" href="#" data-open="'+t.nr+'">Details</a><a class="btn ghost" href="'+mapsUrl(t)+'" target="_blank" rel="noopener">Maps</a></div></div></article>').join('');
}


state.plan = 'A';
state.ab = 'chalet';
function mapsUrl(r){
  let u = 'https://www.google.com/maps/dir/?api=1';
  if (state.ab === 'chalet' && D.chalet) u += '&origin=' + encodeURIComponent(D.chalet);
  return u + '&destination=' + encodeURIComponent(r.dest) + '&travelmode=driving';
}
function renderPlans(){
  $('plans').innerHTML = D.plaene.map(p => '<div class="plan'+(p.id===state.plan?' on':'')+'" data-plan="'+p.id+'" role="button" tabindex="0"><div class="hd"><span class="lt">'+p.id+'</span><div><div class="tag">'+p.tipp+'</div><h3>'+p.titel+'</h3></div></div><p>'+p.kurz+'</p>'+
    '<div class="tl"><span>☁ '+p.wetter+'</span>'+p.touren.map(n => '<span>Tour '+n+'</span>').join('')+'</div></div>').join('');
  const p = D.plaene.find(x => x.id === state.plan);
  const ts = p.touren.map(n => ALL.find(r => r.nr === n));
  $('tline').innerHTML = '<h3>Plan '+p.id+': '+p.titel+'</h3><div class="note">'+p.plus.join(' · ')+'</div><ol>'+p.plan.map(([t, x]) => '<li><b>'+t+'</b><span>'+x+'</span></li>').join('')+'</ol>'+
    '<div class="tchips">'+ts.map(r => '<a href="#" data-open="'+r.nr+'">'+r.nr+' · '+r.kurz+' · '+fmtH(r.geh)+' · '+r.hm+' Hm →</a>').join('')+'</div>';
}
document.addEventListener('click', e => { const g = e.target.closest('[data-goplan]'); if (g){ e.preventDefault(); state.plan = g.dataset.goplan; setTab('ueber'); $('plans').scrollIntoView({behavior:'smooth'}); } });
document.addEventListener('click', e => { const c = e.target.closest('[data-plan]'); if (c){ state.plan = c.dataset.plan; renderPlans(); if (innerWidth < 800) $('tline').scrollIntoView({behavior:'smooth', block:'start'}); } });

function renderKpis(f){
  const mx = k => Math.max(...f.map(r => r[k]));
  $('kpis').innerHTML = [
    ['Touren', f.length + ' von ' + ALL.length], ['Max. Aufstieg', mx('hm') + ' Hm'], ['Höchster Punkt', fmtM(mx('top'))],
    ['Max. Gehzeit', fmtH(mx('geh'))], ['Längster Tag ab Chalet', fmtH(mx('gesamt'))]
  ].map(([l,v]) => '<div class="kpi"><b>'+v+'</b><span>'+l+'</span></div>').join('');
}

function renderOver(f){
  const traces = ['leicht','mittel'].map(n => {
    const d = f.filter(r => r.niveau === n);
    return {type:'scatter', mode:'markers+text', name:n[0].toUpperCase()+n.slice(1), x:d.map(r => r.geh/60), y:d.map(r => r.hm),
      text:d.map(r => String(r.nr)), textfont:{color:'#fff', size:12}, textposition:'middle center',
      marker:{size:d.map(r => r.km*9+14), color:col(n), line:{color:css('--bg'), width:2}},
      customdata:d.map(r => [r.kurz, r.km, r.top]),
      hovertemplate:'<b>%{customdata[0]}</b><br>Gehzeit %{x:.2f} h<br>Aufstieg %{y} Hm<br>Länge %{customdata[1]} km<br>Höchster Punkt %{customdata[2]} m<extra></extra>'};
  });
  plot('c-bubble', traces, layout({height:400, xaxis:{title:'Gehzeit (Stunden)', range:[0.6,2.9], gridcolor:grid, zeroline:false},
    yaxis:{title:'Aufstieg (Höhenmeter)', automargin:true, range:[-90,590], gridcolor:grid, zeroline:false}}));
  const s = f.slice().sort((a,b) => a.hm - b.hm);
  plot('c-bar', [{type:'bar', orientation:'h', x:s.map(r => r.hm), y:s.map(r => r.nr + '  ' + r.kurz),
    marker:{color:s.map(r => col(r.niveau)), cornerradius:4}, text:s.map(r => r.hm + ' Hm'), textposition:'outside', cliponaxis:false,
    hovertemplate:'<b>%{y}</b><br>%{x} Hm<extra></extra>'}],
    layout({height:400, showlegend:false, xaxis:{range:[0,620], gridcolor:grid, zeroline:false}, yaxis:{automargin:true}}));
  $('tbl').innerHTML = '<tr><th>Tour</th><th>Niveau</th><th class="n">Länge</th><th class="n">Gehzeit</th><th class="n">Aufstieg</th><th class="n">Start ca.</th><th class="n">Höchster Punkt</th><th class="n">Gesamt ab Chalet</th><th>Links</th></tr>' +
    f.map(r => '<tr><td>'+r.nr+' · '+r.name+'</td><td><span class="pill '+r.niveau+'">'+r.niveau+'</span></td><td class="n">'+de1(r.km)+' km</td><td class="n">'+fmtH(r.geh)+
      '</td><td class="n">'+r.hm+' Hm</td><td class="n">'+fmtM(r.start_hoehe)+'</td><td class="n">'+fmtM(r.top)+'</td><td class="n">'+fmtH(r.gesamt)+
      '</td><td><a href="'+r.url+'" target="_blank" rel="noopener">Tour</a> · <a href="'+mapsUrl(r)+'" target="_blank" rel="noopener">Maps</a></td></tr>').join('');
}

function profileXY(r){
  if (r.top < 1000) return [[0,.25,.5,.75,1], [r.start_hoehe, r.start_hoehe + r.hm*.5, r.top, r.start_hoehe + r.hm*.4, r.start_hoehe]];
  return [[0,.5,1], [r.start_hoehe, r.top, r.start_hoehe]];
}
function renderHoehe(f){
  const traces = ['leicht','mittel'].map(n => {
    const d = f.filter(r => r.niveau === n).sort((a,b) => a.top - b.top);
    return {type:'bar', orientation:'h', name:n[0].toUpperCase()+n.slice(1), y:d.map(r => r.nr + '  ' + r.kurz), x:d.map(r => r.hm), base:d.map(r => r.start_hoehe),
      marker:{color:col(n), cornerradius:4, line:{color:css('--bg'), width:2}},
      text:d.map(r => Math.round(r.start_hoehe).toLocaleString('de-DE') + ' – ' + Math.round(r.top).toLocaleString('de-DE') + ' m'), textposition:'outside', cliponaxis:false,
      customdata:d.map(r => [r.hm, r.start_hoehe]), hovertemplate:'<b>%{y}</b><br>Start ca. %{customdata[1]} m<br>Aufstieg %{customdata[0]} Hm<extra></extra>'};
  });
  plot('c-band', traces, layout({height:360, xaxis:{title:'Höhe über dem Meer (m)', range:[500,2450], gridcolor:grid, zeroline:false}, yaxis:{autorange:'reversed', automargin:true}}));
  const sel = $('sel-profil'), cur = sel.value;
  sel.innerHTML = f.map(r => '<option value="'+r.nr+'">'+r.nr+'  '+r.kurz+'</option>').join('');
  if (f.some(r => String(r.nr) === cur)) sel.value = cur;
  const r = f.find(x => String(x.nr) === sel.value) || f[0];
  const [xs, ys] = profileXY(r);
  const tr = [{type:'scatter', mode:'lines+markers', x:xs.map(x => x*r.km), y:ys, line:{color:col(r.niveau), width:3}, marker:{size:9, color:col(r.niveau), line:{color:css('--bg'), width:2}},
    fill:'tozeroy', fillcolor:'rgba(120,140,170,0.12)', hovertemplate:'km %{x:.1f}<br>%{y:.0f} m<extra></extra>'}];
  const lay = layout({height:340, showlegend:false, xaxis:{title:'Strecke (km, grob)', gridcolor:grid, zeroline:false},
    yaxis:{title:'Höhe (m)', range:[Math.max(0, r.start_hoehe-120), r.top+120], gridcolor:grid, zeroline:false}});
  const ann = [];
  const im = ys.indexOf(Math.max(...ys));
  ann.push({x:xs[im]*r.km, y:ys[im], text:'Höchster Punkt ' + fmtM(r.top), showarrow:true, arrowhead:0, ay:-30, font:{color:css('--muted')}});
  if (r.huette){
    const frac = (r.huette - r.start_hoehe)/r.hm*.5;
    tr.push({type:'scatter', mode:'markers', x:[frac*r.km], y:[r.huette], marker:{size:11, symbol:'diamond', color:col(r.niveau), line:{color:css('--bg'), width:2}}, hovertemplate:'Pleschnitzzinken Hütte 1.911 m<extra></extra>'});
    ann.push({x:frac*r.km, y:r.huette, text:'Hütte 1.911 m', showarrow:false, xanchor:'right', yanchor:'bottom', font:{color:css('--muted')}});
  }
  lay.annotations = ann;
  plot('c-profil', tr, lay);
  $('n-profil').textContent = 'Schematisch: nur Start und höchster Punkt sind belegt, der Verlauf dazwischen ist vereinfacht. Gesamter Aufstieg: ' + r.hm + ' Hm auf ' + de1(r.km) + ' km.';
}

function renderAnreise(f){
  const s = f.slice().sort((a,b) => a.gesamt - b.gesamt), y = s.map(r => r.nr + '  ' + r.kurz);
  const part = (name, key, color, fn) => ({type:'bar', orientation:'h', name, y, x:s.map(r => fn(r)/60), marker:{color, line:{color:css('--bg'), width:2}}, hovertemplate:'<b>%{y}</b><br>'+name+': %{x:.2f} h<extra></extra>'});
  plot('c-stack', [part('Fahrt (hin und zurück)','', '#8c8b85', r => 2*r.fahrt), part('Gehzeit','', css('--blue'), r => r.geh), part('Pause / Einkehr','', '#b5b4ac', r => r.pause)],
    layout({height:360, barmode:'stack', xaxis:{title:'Stunden', gridcolor:grid, zeroline:false}, yaxis:{autorange:'reversed', automargin:true}}));
  const pers = Math.max(1, +$('in-pers').value || 1), pl = Math.max(2, +$('in-pl').value || 5), autos = Math.ceil(pers/pl);
  $('out-autos').textContent = 'Autos nötig: ' + autos;
  const hasMaut = f.some(r => r.maut), kosten = autos*D.maut;
  $('out-maut').innerHTML = hasMaut
    ? '<div class="msg"><b>Maut Stoderzinken (Tour 3, 4, 7): '+kosten+' €</b> ('+(kosten/pers).toFixed(2).replace('.',',')+' € pro Person). 20 € pro Pkw. Laut Tourismusseite ist die Maut zwischen 14.09. und 01.11.2026 mit der Schladming-Dachstein Card inklusive.</div>'
    : '<div class="msg">Keine der gefilterten Touren nutzt die Mautstraße.</div>';
  $('tbl-anreise').innerHTML = '<tr><th>Tour</th><th class="n">Anfahrt</th><th>Auto</th><th class="n">Gesamt</th></tr>' +
    f.map(r => '<tr><td>'+r.nr+'  '+r.kurz+'</td><td class="n">'+r.fahrt+' Min</td><td>'+r.auto+'</td><td class="n">'+fmtH(r.gesamt)+'</td></tr>').join('');
}

function renderDetail(f){
  const sel = $('sel-detail'), cur = sel.value;
  sel.innerHTML = f.map(r => '<option value="'+r.nr+'">'+r.nr+'  '+r.name+'</option>').join('');
  if (f.some(r => String(r.nr) === cur)) sel.value = cur;
  const r = f.find(x => String(x.nr) === sel.value) || f[0];
  $('detail').innerHTML = '<div class="detail"><div class="dcover">'+tourArt(r, 1050, 400)+photo(r)+'</div><h2 style="margin-top:0">'+r.nr+' · '+r.name+'</h2><span class="pill '+r.niveau+'">'+r.niveau+'</span> '+r.kondition+
    '<div class="m"><div><b>'+de1(r.km)+' km</b><span>Länge</span></div><div><b>'+fmtH(r.geh)+'</b><span>Gehzeit</span></div><div><b>'+r.hm+' Hm</b><span>Aufstieg</span></div><div><b>'+fmtM(r.start_hoehe)+'</b><span>Start ca.</span></div><div><b>'+fmtM(r.top)+'</b><span>Höchster Punkt</span></div></div>'+
    '<p><b>Start:</b> '+r.start_ort+'</p><p><b>Route:</b> '+r.weg+'</p><p><b>Highlights</b></p><ul>'+r.plus.map(p => '<li>'+p+'</li>').join('')+'</ul><p><b>Gut zu wissen:</b> '+r.info+'</p>'+
    '<p><b>Ab Chalet:</b> Anfahrt ca. '+r.fahrt+' Min (einfach, Schätzung) · Gesamtdauer '+fmtH(r.gesamt)+' · Auto: '+r.auto+'</p>'+
    '<a class="btn" href="'+r.url+'" target="_blank" rel="noopener">Tourenseite mit Karte</a><a class="btn" href="'+mapsUrl(r)+'" target="_blank" rel="noopener">Route in Google Maps</a></div>';
}

function renderWetter(){
  $('wetter-btns').innerHTML = Object.keys(D.wetter).map(k => '<button class="chip" data-l="'+k+'" aria-pressed="'+(k===state.lage)+'">'+k+'</button>').join(' ');
  $('wetter-txt').textContent = D.wetter[state.lage];
  const wp = D.plaene.find(p => p.wetter === state.lage); if (wp) $('wetter-txt').innerHTML += ' <a href="#" data-goplan="'+wp.id+'">Zeitplan ansehen →</a>';
  const p = ALL.filter(r => r.wetter.includes(state.lage));
  $('tbl-wetter').innerHTML = '<tr><th>Tour</th><th>Niveau</th><th class="n">Aufstieg</th><th class="n">Gehzeit</th></tr>' +
    p.map(r => '<tr><td>'+r.nr+' · '+r.name+'</td><td><span class="pill '+r.niveau+'">'+r.niveau+'</span></td><td class="n">'+r.hm+' Hm</td><td class="n">'+fmtH(r.geh)+'</td></tr>').join('');
}

const CHK_E = ['Wetter und Schneelage am Vorabend prüfen','Plan nach Wetter wählen und Gruppen einteilen (Gipfel / Hütte)','Galsterbergalm: Tisch für 9 reservieren (+43 676 951 8228)','Fahrgemeinschaften und Abfahrtszeit festlegen','Plan B: Maut 20 € pro Auto, Öffnung Steinerhaus/Rosemi Alm prüfen','Notruf und Treffpunkt im Chat teilen'];
const CHK_G = ['Wanderschuhe mit Profil','Warme Schichten, Mütze','Regen- und Windjacke','Trinkflasche (1 l)','Gipfel-Brotzeit','Stirnlampe','Powerbank, Offline-Karte','Erste-Hilfe-Set','Sonnenbrille'];
function lsGet(k){ try { return localStorage.getItem(k) === '1'; } catch(e){ return false; } }
function lsSet(k,v){ try { localStorage.setItem(k, v ? '1' : '0'); } catch(e){} }
function renderChecks(){
  const mk = (id, arr, p) => { $(id).innerHTML = arr.map((t,i) => '<li><label><input type="checkbox" data-k="'+p+i+'" '+(lsGet(p+i)?'checked':'')+'> '+t+'</label></li>').join(''); };
  mk('chk-e', CHK_E, 'e'); mk('chk-g', CHK_G, 'g');
}

function render(){
  const f = filtered();
  $('empty').hidden = f.length > 0;
  document.querySelectorAll('section.tab').forEach(s => s.style.visibility = f.length ? 'visible' : 'hidden');
  if (!f.length){ $('kpis').innerHTML = ''; return; }
  renderKpis(f);
  const t = state.tab;
  if (t === 'ueber'){ renderPlans(); renderCards(f); renderOver(f); }
  if (t === 'hoehe') renderHoehe(f);
  if (t === 'anreise') renderAnreise(f);
  if (t === 'detail') renderDetail(f);
  if (t === 'wetter') renderWetter();
  if (t === 'check') renderChecks();
}

function setTab(t){
  state.tab = t;
  document.querySelectorAll('#tabs button').forEach(b => b.setAttribute('aria-selected', b.dataset.t === t));
  document.querySelectorAll('section.tab').forEach(s => s.classList.toggle('on', s.id === 't-' + t));
  render();
}
$('tabs').addEventListener('click', e => { const b = e.target.closest('button'); if (b) setTab(b.dataset.t); });
['leicht','mittel'].forEach(n => $('f-'+n).addEventListener('click', e => { state.niv[n] = !state.niv[n]; e.currentTarget.setAttribute('aria-pressed', state.niv[n]); render(); }));
$('f-geh').addEventListener('input', e => { state.geh = +e.target.value; $('v-geh').textContent = fmtH(state.geh); render(); });
$('f-hm').addEventListener('input', e => { state.hm = +e.target.value; $('v-hm').textContent = state.hm + ' Hm'; render(); });
['chalet','hier'].forEach(k => $('ab-'+k).addEventListener('click', () => { state.ab = k === 'chalet' ? 'chalet' : 'hier';
  $('ab-chalet').setAttribute('aria-pressed', state.ab === 'chalet'); $('ab-hier').setAttribute('aria-pressed', state.ab !== 'chalet'); render(); }));
$('f-maut').addEventListener('change', e => { state.ohneMaut = e.target.checked; render(); });
$('sel-profil').addEventListener('change', render);
$('sel-detail').addEventListener('change', render);
$('in-pers').addEventListener('input', render);
$('in-pl').addEventListener('input', render);
$('wetter-btns').addEventListener('click', e => { const b = e.target.closest('button'); if (b){ state.lage = b.dataset.l; render(); } });
document.addEventListener('change', e => { const k = e.target.dataset && e.target.dataset.k; if (k) lsSet(k, e.target.checked); });
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', render);
heroArt();
(function(){ const mx = k => Math.max(...ALL.map(r => r[k])), mn = k => Math.min(...ALL.map(r => r[k]));
  $('hstats').innerHTML = '<span><b>'+ALL.length+'</b>Touren</span><span><b>'+mn('hm')+'–'+mx('hm')+'</b>Hm</span><span><b>'+fmtH(mn('geh')).replace(' h','')+'–'+fmtH(mx('geh'))+'</b>Gehzeit</span><span><b>'+fmtM(mx('top'))+'</b>höchster Punkt</span>'; })();
document.addEventListener('click', e => { const a = e.target.closest('[data-open]'); if (!a) return; e.preventDefault();
  $('sel-detail').innerHTML = '<option value="'+a.dataset.open+'"></option>'; setTab('detail'); $('sel-detail').value = a.dataset.open; render(); $('tabs').scrollIntoView({behavior:'smooth'}); });
render();
</script>
</body>
</html>
"""

out = Path(__file__).parent / "docs"
out.mkdir(exist_ok=True)
html = HTML.replace("__DATA__", data_json).replace("__PLOTLY__", get_plotlyjs())
(out / "index.html").write_text(html, encoding="utf-8")
(out / ".nojekyll").write_text("", encoding="utf-8")
print("docs/index.html:", round(len(html) / 1e6, 1), "MB")
