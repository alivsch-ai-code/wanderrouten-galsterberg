"""Erzeugt die statische Seite docs/index.html für GitHub Pages.

    python build_static.py

Die Seite ist eigenständig (Plotly ist eingebettet) und braucht keinen Server.
"""
import json
from pathlib import Path

from plotly.offline import get_plotlyjs

from routes import MAUT_PKW, ROUTES, WETTER, make_df, maps_url

df = make_df()
routes = []
for r in df.to_dict("records"):
    r["maps"] = maps_url(r["dest"])
    r["wetter"] = sorted(r["wetter"])
    r["huette"] = None if r.get("huette") != r.get("huette") else r.get("huette")
    routes.append({k: (v.item() if hasattr(v, "item") else v) for k, v in r.items()})

DATA = {"routes": routes, "wetter": WETTER, "maut": MAUT_PKW}
data_json = json.dumps(DATA, ensure_ascii=False).replace("</", "<\\/")

HTML = r"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Wanderrouten Galsterberg</title>
<style>
:root{color-scheme:light dark;--bg:#fcfcfb;--card:#f3f6fa;--ink:#0b0b0b;--muted:#52514e;--line:#d5dce6;--blue:#2a78d6;--orange:#eb6834;--accent:#1b3a66}
@media (prefers-color-scheme:dark){:root{--bg:#1a1a19;--card:#242423;--ink:#fff;--muted:#c3c2b7;--line:#3a3a38;--blue:#3987e5;--orange:#d95926;--accent:#9db8e8}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
header{padding:22px 16px 8px;max-width:1100px;margin:0 auto}
h1{margin:0 0 4px;font-size:clamp(22px,4vw,32px);color:var(--accent)}
.sub{color:var(--muted);font-size:13px}
main{max-width:1100px;margin:0 auto;padding:0 16px 40px}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:10px;margin:14px 0}
.kpi{background:var(--card);border-radius:10px;padding:10px 14px}
.kpi b{display:block;font-size:22px}.kpi span{color:var(--muted);font-size:12px}
.filters{display:flex;flex-wrap:wrap;gap:16px;align-items:center;background:var(--card);border-radius:10px;padding:10px 14px;margin-bottom:10px}
.filters label{font-size:13px;color:var(--muted);display:flex;gap:8px;align-items:center}
.chip{border:1px solid var(--line);border-radius:999px;padding:3px 12px;cursor:pointer;background:transparent;color:var(--ink);font:inherit;font-size:13px}
.chip[aria-pressed=true]{background:var(--accent);color:var(--bg);border-color:var(--accent)}
nav{display:flex;gap:4px;flex-wrap:wrap;border-bottom:1px solid var(--line);margin:8px 0 14px}
nav button{background:none;border:0;border-bottom:3px solid transparent;padding:9px 12px;font:inherit;color:var(--muted);cursor:pointer}
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
.tw{overflow-x:auto}
a{color:var(--blue)}
.pill{display:inline-block;padding:1px 9px;border-radius:999px;font-size:12px;color:#fff}
.pill.leicht{background:var(--blue)}.pill.mittel{background:var(--orange)}
select,input[type=number]{font:inherit;padding:6px 8px;border-radius:8px;border:1px solid var(--line);background:var(--bg);color:var(--ink)}
.detail{background:var(--card);border-radius:10px;padding:14px 16px;margin-top:10px}
.detail .m{display:grid;grid-template-columns:repeat(auto-fit,minmax(110px,1fr));gap:8px;margin:10px 0}
.detail .m div{background:var(--bg);border-radius:8px;padding:6px 10px}.detail .m b{display:block;font-size:17px}.detail .m span{font-size:12px;color:var(--muted)}
.btn{display:inline-block;margin:4px 8px 0 0;padding:7px 14px;border-radius:8px;background:var(--accent);color:var(--bg);text-decoration:none;font-size:14px}
.msg{background:var(--card);border-left:4px solid var(--blue);padding:10px 14px;border-radius:6px;margin:10px 0}
.warn{border-left-color:var(--orange)}.err{border-left-color:#c0392b}
ul.chk{list-style:none;padding:0}ul.chk li{padding:3px 0}
footer{max-width:1100px;margin:0 auto;padding:0 16px 30px;color:var(--muted);font-size:12.5px}
</style>
</head>
<body>
<header>
<h1>⛰️ Wanderrouten Galsterberg &amp; Ennstal</h1>
<div class="sub">Chalet-Wochenende · Pruggern, Steiermark · Samstag im Oktober 2026 · Verantwortlich: Eugen (Женя)</div>
</header>
<main>
<div class="filters" role="group" aria-label="Filter">
  <span>Niveau:</span>
  <button class="chip" id="f-leicht" aria-pressed="true">Leicht</button>
  <button class="chip" id="f-mittel" aria-pressed="true">Mittel</button>
  <label>Max. Gehzeit <input type="range" id="f-geh" min="60" max="180" step="15" value="180"> <b id="v-geh">3:00 h</b></label>
  <label>Max. Aufstieg <input type="range" id="f-hm" min="0" max="500" step="5" value="500"> <b id="v-hm">500 Hm</b></label>
  <label><input type="checkbox" id="f-maut"> ohne Mautstraße</label>
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
  <div class="msg warn">Mitte Oktober ist in den Höhenlagen Schnee möglich. Sonnenuntergang ungefähr gegen 18 Uhr (am Tag selbst prüfen). Hüttenöffnungszeiten vorab klären, die Pleschnitzzinken Hütte ist unbewirtschaftet.</div>
</section>

<section class="tab" id="t-check">
  <div class="grid2">
    <div><h2>Checkliste für Eugen</h2><ul class="chk" id="chk-e"></ul></div>
    <div><h2>Ausrüstung</h2><ul class="chk" id="chk-g"></ul></div>
  </div>
  <div class="msg err">Notruf: Bergrettung 140 · Euro-Notruf 112. Bei Unfall oder Wetterumschwung früh umkehren, Gruppe zusammenhalten.</div>
</section>
</main>
<footer>Quellen: schladming-dachstein.at, steiermark.com, hauser-kaibling.at, tourispo.de. Alle Angaben sind Richtwerte, aktuelle Bedingungen vor Ort prüfen. Anfahrt, Pausen und Gesamtdauer sind Schätzungen.</footer>

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
  plot('c-bubble', traces, layout({height:400, xaxis:{title:'Gehzeit (Stunden)', range:[0.5,3], gridcolor:grid, zeroline:false},
    yaxis:{title:'Aufstieg (Höhenmeter)', automargin:true, range:[-40,560], gridcolor:grid, zeroline:false}}));
  const s = f.slice().sort((a,b) => a.hm - b.hm);
  plot('c-bar', [{type:'bar', orientation:'h', x:s.map(r => r.hm), y:s.map(r => r.nr + '  ' + r.kurz),
    marker:{color:s.map(r => col(r.niveau)), cornerradius:4}, text:s.map(r => r.hm + ' Hm'), textposition:'outside', cliponaxis:false,
    hovertemplate:'<b>%{y}</b><br>%{x} Hm<extra></extra>'}],
    layout({height:400, showlegend:false, xaxis:{range:[0,620], gridcolor:grid, zeroline:false}, yaxis:{automargin:true}}));
  $('tbl').innerHTML = '<tr><th>Tour</th><th>Niveau</th><th class="n">Länge</th><th class="n">Gehzeit</th><th class="n">Aufstieg</th><th class="n">Start ca.</th><th class="n">Höchster Punkt</th><th class="n">Gesamt ab Chalet</th><th>Links</th></tr>' +
    f.map(r => '<tr><td>'+r.nr+' · '+r.name+'</td><td><span class="pill '+r.niveau+'">'+r.niveau+'</span></td><td class="n">'+de1(r.km)+' km</td><td class="n">'+fmtH(r.geh)+
      '</td><td class="n">'+r.hm+' Hm</td><td class="n">'+fmtM(r.start_hoehe)+'</td><td class="n">'+fmtM(r.top)+'</td><td class="n">'+fmtH(r.gesamt)+
      '</td><td><a href="'+r.url+'" target="_blank" rel="noopener">Tour</a> · <a href="'+r.maps+'" target="_blank" rel="noopener">Maps</a></td></tr>').join('');
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
    ? '<div class="msg"><b>Maut Stoderzinken (Tour 3/4): '+kosten+' €</b> ('+(kosten/pers).toFixed(2).replace('.',',')+' € pro Person). 20 € pro Pkw. Laut Tourismusseite ist die Maut zwischen 14.09. und 01.11.2026 mit der Schladming-Dachstein Card inklusive.</div>'
    : '<div class="msg">Keine der gefilterten Touren nutzt die Mautstraße.</div>';
  $('tbl-anreise').innerHTML = '<tr><th>Tour</th><th class="n">Anfahrt</th><th>Auto</th><th class="n">Gesamt</th></tr>' +
    f.map(r => '<tr><td>'+r.nr+'  '+r.kurz+'</td><td class="n">'+r.fahrt+' Min</td><td>'+r.auto+'</td><td class="n">'+fmtH(r.gesamt)+'</td></tr>').join('');
}

function renderDetail(f){
  const sel = $('sel-detail'), cur = sel.value;
  sel.innerHTML = f.map(r => '<option value="'+r.nr+'">'+r.nr+'  '+r.name+'</option>').join('');
  if (f.some(r => String(r.nr) === cur)) sel.value = cur;
  const r = f.find(x => String(x.nr) === sel.value) || f[0];
  $('detail').innerHTML = '<div class="detail"><h2 style="margin-top:0">'+r.nr+' · '+r.name+'</h2><span class="pill '+r.niveau+'">'+r.niveau+'</span> '+r.kondition+
    '<div class="m"><div><b>'+de1(r.km)+' km</b><span>Länge</span></div><div><b>'+fmtH(r.geh)+'</b><span>Gehzeit</span></div><div><b>'+r.hm+' Hm</b><span>Aufstieg</span></div><div><b>'+fmtM(r.start_hoehe)+'</b><span>Start ca.</span></div><div><b>'+fmtM(r.top)+'</b><span>Höchster Punkt</span></div></div>'+
    '<p><b>Start:</b> '+r.start_ort+'</p><p><b>Route:</b> '+r.weg+'</p><p><b>Highlights</b></p><ul>'+r.plus.map(p => '<li>'+p+'</li>').join('')+'</ul><p><b>Gut zu wissen:</b> '+r.info+'</p>'+
    '<p><b>Ab Chalet:</b> Anfahrt ca. '+r.fahrt+' Min (einfach, Schätzung) · Gesamtdauer '+fmtH(r.gesamt)+' · Auto: '+r.auto+'</p>'+
    '<a class="btn" href="'+r.url+'" target="_blank" rel="noopener">Tourenseite mit Karte</a><a class="btn" href="'+r.maps+'" target="_blank" rel="noopener">Route in Google Maps</a></div>';
}

function renderWetter(){
  $('wetter-btns').innerHTML = Object.keys(D.wetter).map(k => '<button class="chip" data-l="'+k+'" aria-pressed="'+(k===state.lage)+'">'+k+'</button>').join(' ');
  $('wetter-txt').textContent = D.wetter[state.lage];
  const p = ALL.filter(r => r.wetter.includes(state.lage));
  $('tbl-wetter').innerHTML = '<tr><th>Tour</th><th>Niveau</th><th class="n">Aufstieg</th><th class="n">Gehzeit</th></tr>' +
    p.map(r => '<tr><td>'+r.nr+' · '+r.name+'</td><td><span class="pill '+r.niveau+'">'+r.niveau+'</span></td><td class="n">'+r.hm+' Hm</td><td class="n">'+fmtH(r.geh)+'</td></tr>').join('');
}

const CHK_E = ['Wetter und Schneelage am Vorabend prüfen','Tour mit der Gruppe abstimmen (Niveau, Dauer)','Hüttenöffnung telefonisch klären','Fahrgemeinschaften und Abfahrtszeit festlegen','Mautstraße und Parkplatz klären (Tour 3 und 4)','Notruf und Treffpunkt im Chat teilen'];
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
  if (t === 'ueber') renderOver(f);
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
$('f-maut').addEventListener('change', e => { state.ohneMaut = e.target.checked; render(); });
$('sel-profil').addEventListener('change', render);
$('sel-detail').addEventListener('change', render);
$('in-pers').addEventListener('input', render);
$('in-pl').addEventListener('input', render);
$('wetter-btns').addEventListener('click', e => { const b = e.target.closest('button'); if (b){ state.lage = b.dataset.l; render(); } });
document.addEventListener('change', e => { const k = e.target.dataset && e.target.dataset.k; if (k) lsSet(k, e.target.checked); });
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', render);
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
