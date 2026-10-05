"""Erzeugt docs/plan-a.html: ausführliche Seite für Plan A (große Pleschnitzzinken-Runde, Favorit von Vadim und Eugen).

    python build_plan_a.py      (wird auch von build_static.py aufgerufen)
"""
import json
from pathlib import Path

from routes import CHALET, PLAENE, ROUTES

T8 = next(r for r in ROUTES if r["nr"] == 8)
T1 = next(r for r in ROUTES if r["nr"] == 1)
T2 = next(r for r in ROUTES if r["nr"] == 2)
PLAN = next(p for p in PLAENE if p["id"] == "A")
SONNE = {"auf": "07:25", "unter": "18:14"}  # Pruggern, Sa 17.10.2026 (berechnet)

# Schematisches Profil: Wegpunkte (km, Höhe, Name). Hütte und Gipfel nach Komoot, Galsterbergalm geschätzt.
PROFIL = [
    (0.0, 1108, "Talstation"),
    (5.5, 1911, "Pleschnitzzinken Hütte"),
    (8.4, 2112, "Gipfel"),
    (9.5, 1800, "Galsterbergalm"),
    (12.5, 1108, "Talstation"),
]

ETAPPEN = [
    dict(zeit="08:30", titel="Start an der Galsterberg-Talstation", hoehe="1.108 m", km="km 0",
         text="Treffpunkt für Team Gipfel. Am besten zu Fuß vom Chalet, die Entfernung am Freitag kurz prüfen. Rucksack-Check: Wasser, Jacke, Handy geladen.",
         tipp="Langsam loslegen. Der Tag ist lang, das Tempo gibt der Langsamste vor."),
    dict(zeit="ca. 09:30", titel="Aufstieg über den Pruggererberg", hoehe="Aussichtspunkt", km="bis ca. km 3",
         text="Forst- und Wanderwege mit losem Untergrund. Oben laut Komoot „eine herrliche Aussicht auf die Tauern und in das Ennstal“.",
         tipp="Erste Trinkpause und Gruppenfoto mit Ennstal-Blick."),
    dict(zeit="ca. 10:45", titel="Pleschnitzzinken Hütte", hoehe="1.911 m", km="ca. km 5–6",
         text="Unbewirtschaftete Hütte über der Baumgrenze, hier gibt es nichts zu kaufen. Gute Stelle für eine Pause im Windschatten.",
         tipp="Checkpoint: Bis 11:00 hier? Dann weiter zum Gipfel. Sonst umkehren und direkt zur Galsterbergalm."),
    dict(zeit="ca. 12:00", titel="Gipfel Pleschnitzzinken", hoehe="2.112 m", km="ca. km 8,4",
         text="Über den Grasrücken zum Gipfelkreuz. Rundumblick auf Hochwildstelle, Dachstein und ins Ennstal. Hier oben kann es windig und kalt sein, im Oktober auch um 0 °C.",
         tipp="Gipfelfoto, warme Schicht anziehen, nicht zu lange auskühlen. Spätestens 12:30 Abstieg."),
    dict(zeit="12:45", titel="Galsterbergalmhütte: alle treffen sich", hoehe="ca. 1.800 m", km="ca. km 9,5",
         text="Team Hütte und Team Chalet sind schon da. Gemeinsames Mittagessen, Küche 10:30–17 Uhr, Murmeltiere vor der Hütte. Im Herbst Fr–So 9–18 Uhr geöffnet.",
         tipp="Tisch für 9 vorher reservieren: +43 676 951 8228."),
    dict(zeit="14:15", titel="Abstieg zur Talstation", hoehe="1.108 m", km="km 9,5 bis 12,5",
         text="Rund 700 Höhenmeter bergab auf ca. 3 km. Das geht in die Knie, Stöcke helfen. Die anderen Teams fahren mit dem Auto zurück.",
         tipp="Konzentriert bleiben, auf nassem Gras und Wurzeln rutscht man leicht."),
    dict(zeit="15:30", titel="Zurück am Chalet", hoehe="", km="Ziel",
         text="Team Chalet hat die Banja angeheizt. Duschen, aufwärmen, anstoßen.",
         tipp="Genug trinken vor dem ersten Saunagang."),
]

REGELN = [
    ("11:00", "Noch nicht an der Pleschnitzzinken Hütte?", "Kein Gipfel. Auf dem Aufstiegsweg zurück und zur Galsterbergalm, dort mit den anderen essen."),
    ("12:30", "Spätester Gipfelzeitpunkt", "Wer bis dahin nicht oben ist, kehrt um. Der Abstieg braucht mindestens 2 Stunden."),
    ("15:00", "Spätester Aufbruch an der Galsterbergalm", "Damit alle lange vor Sonnenuntergang (" + SONNE["unter"] + " Uhr) unten sind."),
    ("Wetter", "Gewitter, dichter Nebel, Neuschnee oder Eis am Grat", "Gipfel streichen und auf Plan C wechseln: Galsterbergalm-Runde mit langer Einkehr."),
]

PACK = [
    ("Am Körper", "Zwiebelprinzip, keine Baumwolle", [
        ("Wanderschuhe mit gutem Profil, am besten wasserabweisend. Keine normalen Sneaker, Wald- und Wiesenwege können nass und rutschig sein.", True),
        ("Lange Wanderhose", True),
        ("Warme Wandersocken", True),
        ("Funktionsshirt", False),
        ("Fleece oder warme dünne Jacke", True),
        ("Dünne Mütze oder Stirnband, wenn ihr schnell friert", True),
    ]),
    ("Im Rucksack", "Tagesrucksack mit 20–30 Litern", [
        ("Regen- und Windjacke", False),
        ("Handschuhe, am Gipfel wird es kalt", False),
        ("Trockenes Wechselshirt für den Gipfel", False),
        ("1,5 l Wasser oder heißer Tee in der Thermoskanne", False),
        ("Brotzeit und Snacks für unterwegs (Riegel, Nüsse, Obst)", False),
        ("Wanderstöcke, sehr hilfreich beim langen Abstieg", False),
        ("Sonnenbrille und Sonnencreme", False),
        ("Etwas Bargeld für die Galsterbergalm (Kartenzahlung nicht sicher)", False),
    ]),
    ("Sicherheit & Technik", "Für den Notfall", [
        ("Handy voll geladen, dazu eine Powerbank", False),
        ("Komoot-Tour offline gespeichert", False),
        ("Stirnlampe, Sonnenuntergang um " + SONNE["unter"] + " Uhr", False),
        ("Erste-Hilfe-Set mit Blasenpflastern", False),
        ("Rettungsdecke", False),
        ("Ausweis und Krankenversicherungskarte", False),
    ]),
    ("Team Chalet & Team Hütte", "Wer nicht auf den Gipfel geht", [
        ("Festes Schuhwerk und Jacke für die Galsterbergalm", False),
        ("Autoschlüssel und Fahrer für die Fahrt zum Bottinghaus", False),
        ("Banja: Holz und Anzünder, Handtücher, Banja-Hüte", False),
        ("Wein und Getränke kalt stellen für die Rückkehr", False),
    ]),
]

DATA = dict(t8=T8 | {"wetter": sorted(T8["wetter"])}, plan=PLAN, profil=PROFIL, etappen=ETAPPEN, regeln=REGELN, pack=PACK,
            sonne=SONNE, chalet=CHALET, t1=dict(nr=1, kurz=T1["kurz"], geh=T1["geh"], hm=T1["hm"]),
            t2=dict(nr=2, kurz=T2["kurz"], geh=T2["geh"], hm=T2["hm"]))
data_json = json.dumps(DATA, ensure_ascii=False).replace("</", "<\\/")

HTML = r"""<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Plan A: Pleschnitzzinken</title>
<meta name="description" content="Plan A für Samstag: große Pleschnitzzinken-Runde ab Galsterberg-Talstation, mit Zeitplan, Route, Umkehrregeln und Packliste.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
:root{color-scheme:light dark;--bg:#fcfcfb;--card:#f3f6fa;--ink:#0b0b0b;--muted:#52514e;--line:#d5dce6;--blue:#2a78d6;--orange:#eb6834;--red:#b4232f;--green:#2f7d4a;--accent:#1b3a66}
@media (prefers-color-scheme:dark){:root{--bg:#1a1a19;--card:#242423;--ink:#fff;--muted:#c3c2b7;--line:#3a3a38;--blue:#3987e5;--orange:#d95926;--red:#e0525c;--green:#5cb77a;--accent:#9db8e8}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 Inter,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif}
a{color:var(--blue)}
.wrap{max-width:980px;margin:0 auto;padding:0 16px}
.topbar{position:sticky;top:0;z-index:10;background:color-mix(in srgb,var(--bg) 88%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.topbar .wrap{display:flex;align-items:center;gap:12px;height:52px;overflow-x:auto;scrollbar-width:none}
.topbar .wrap::-webkit-scrollbar{display:none}
.topbar a{white-space:nowrap;text-decoration:none;color:var(--muted);font-size:14px;font-weight:500}
.topbar a.back{color:var(--accent);font-weight:700;margin-right:6px}
.hero{position:relative;color:#fff;min-height:clamp(340px,52vw,520px);display:flex;align-items:flex-end;overflow:hidden}
.hero svg{position:absolute;inset:0;width:100%;height:100%}
.hero::after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,20,40,0) 30%,rgba(10,20,40,.78) 100%)}
.hero .wrap{position:relative;z-index:1;padding-bottom:28px;width:100%}
.fav{display:inline-flex;align-items:center;gap:8px;background:#eb6834;color:#fff;font-weight:700;font-size:13px;border-radius:999px;padding:5px 12px;box-shadow:0 4px 14px rgba(0,0,0,.25)}
h1{font-size:clamp(30px,6vw,56px);line-height:1.04;margin:12px 0 8px;font-weight:800;letter-spacing:-.02em;text-shadow:0 2px 18px rgba(0,0,0,.35)}
.lead{font-size:clamp(15px,2vw,18px);max-width:640px;opacity:.95;margin:0}
.facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px;margin:-34px 0 0;position:relative;z-index:2}
.fact{background:var(--bg);border:1px solid var(--line);border-radius:14px;padding:12px 14px;box-shadow:0 8px 24px rgba(20,40,80,.08)}
.fact b{display:block;font-size:22px;font-weight:800}.fact span{font-size:12.5px;color:var(--muted)}
section{padding:34px 0 6px}
h2{font-size:clamp(22px,3.4vw,30px);margin:0 0 6px;color:var(--accent);letter-spacing:-.01em}
.sub{color:var(--muted);margin:0 0 16px}
.why{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:12px}
.why div{background:var(--card);border-radius:14px;padding:14px 16px}
.why b{display:block;margin-bottom:2px}
.teams{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:14px}
.team{background:var(--card);border-radius:16px;padding:16px;border-top:5px solid var(--red)}
.team.h{border-top-color:var(--blue)}.team.c{border-top-color:var(--green)}
.team h3{margin:0 0 4px}.team .m{font-size:13px;color:var(--muted);margin-bottom:8px}
.team p{margin:0;font-size:14.5px}
.profile{background:var(--card);border-radius:16px;padding:12px 12px 4px}
.profile svg{width:100%;height:auto;display:block}
.note{font-size:12.5px;color:var(--muted);margin:6px 2px 0}
.steps{list-style:none;margin:0;padding:0;position:relative}
.steps::before{content:"";position:absolute;left:19px;top:10px;bottom:10px;width:3px;background:var(--line);border-radius:3px}
.step{position:relative;padding:0 0 18px 54px}
.step .dot{position:absolute;left:6px;top:4px;width:29px;height:29px;border-radius:50%;background:var(--accent);color:var(--bg);font-weight:800;font-size:13px;display:grid;place-items:center;box-shadow:0 0 0 4px var(--bg)}
.step .card{background:var(--card);border-radius:14px;padding:12px 16px}
.step .hd{display:flex;flex-wrap:wrap;gap:6px 12px;align-items:baseline}
.step .t{font-weight:800;color:var(--orange);font-variant-numeric:tabular-nums}
.step h3{margin:0;font-size:17px}
.step .meta{font-size:12.5px;color:var(--muted)}
.step p{margin:6px 0 0;font-size:14.5px}
.step .tip{margin-top:8px;font-size:13.5px;background:var(--bg);border-left:3px solid var(--orange);padding:6px 10px;border-radius:6px}
.timeline{background:var(--card);border-radius:16px;padding:6px 16px}
.timeline div{display:grid;grid-template-columns:56px 1fr;gap:12px;padding:9px 0;border-bottom:1px solid var(--line);font-size:14.5px}
.timeline div:last-child{border-bottom:0}
.timeline b{color:var(--accent);font-variant-numeric:tabular-nums}
.rules{display:grid;gap:10px}
.rule{display:grid;grid-template-columns:78px 1fr;gap:14px;align-items:start;background:var(--card);border-radius:14px;padding:12px 14px;border-left:5px solid var(--orange)}
.rule .k{font-weight:800;font-size:18px;color:var(--orange)}
.rule b{display:block}.rule span{font-size:14px;color:var(--muted)}
.sos{display:flex;flex-wrap:wrap;gap:10px;margin-top:12px}
.sos a{flex:1 1 200px;text-align:center;text-decoration:none;background:var(--red);color:#fff;font-weight:800;border-radius:12px;padding:12px;font-size:16px}
.sos a.alt{background:var(--accent);color:var(--bg)}
.packbar{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin-bottom:12px}
.progress{flex:1 1 200px;height:10px;background:var(--card);border-radius:999px;overflow:hidden;border:1px solid var(--line)}
.progress i{display:block;height:100%;width:0;background:var(--green);transition:width .2s}
.btn{display:inline-block;padding:9px 14px;border-radius:10px;background:var(--accent);color:var(--bg);text-decoration:none;font-weight:600;font-size:14px;border:0;cursor:pointer;font-family:inherit}
.btn.ghost{background:transparent;color:var(--accent);border:1px solid var(--line)}
.packs{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:14px}
.pack{background:var(--card);border-radius:16px;padding:14px 16px}
.pack h3{margin:0}.pack .m{font-size:13px;color:var(--muted);margin-bottom:6px}
.pack label{display:flex;gap:10px;align-items:flex-start;padding:7px 0;border-bottom:1px solid var(--line);font-size:14.5px;cursor:pointer}
.pack label:last-child{border-bottom:0}
.pack input{width:20px;height:20px;margin-top:1px;accent-color:var(--green);flex:0 0 auto}
.pack label.done span{text-decoration:line-through;color:var(--muted)}
.eu{font-size:11px;font-weight:700;color:var(--green);border:1px solid var(--green);border-radius:999px;padding:0 6px;margin-left:4px;white-space:nowrap}
.links{display:flex;flex-wrap:wrap;gap:10px}
footer{color:var(--muted);font-size:12.5px;padding:30px 0 40px}
.toast{position:fixed;left:50%;bottom:20px;transform:translateX(-50%);background:var(--accent);color:var(--bg);padding:10px 16px;border-radius:10px;font-weight:600;opacity:0;transition:opacity .2s;pointer-events:none}
.toast.on{opacity:1}
@media(max-width:600px){.facts{margin-top:-24px;grid-template-columns:repeat(3,1fr);gap:8px}.fact{padding:10px}.fact b{font-size:16px}.fact span{font-size:11.5px}.rule{grid-template-columns:62px 1fr}.rule .k{font-size:16px}}
@media print{.topbar,.hero::after,.sos,.packbar .btn,.links{display:none}.hero{min-height:200px;color:#000}.hero svg{display:none}h1{text-shadow:none}}
</style>
</head>
<body>
<nav class="topbar"><div class="wrap">
  <a class="back" href="./">← Alle Touren</a>
  <a href="#teams">Teams</a><a href="#zeitplan">Zeitplan</a><a href="#route">Route</a><a href="#sicherheit">Sicherheit</a><a href="#packliste">Packliste</a>
</div></nav>

<header class="hero">
  <svg id="hero8" viewBox="0 0 1200 520" preserveAspectRatio="xMidYMid slice" aria-hidden="true"></svg>
  <div class="wrap">
    <span class="fav">★ Favorit von Vadim &amp; Eugen</span>
    <h1>Plan A: Die große Pleschnitzzinken-Runde</h1>
    <p class="lead">Samstag, 17. Oktober. Ein ganzer Bergtag ab der Galsterberg-Talstation bis aufs Gipfelkreuz auf 2.112 m, danach gemeinsames Mittagessen mit allen an der Galsterbergalm.</p>
  </div>
</header>

<main class="wrap">
  <div class="facts" id="facts"></div>

  <section>
    <h2>Warum diese Tour?</h2>
    <p class="sub">Kurz erklärt für alle, die nicht jede Route im Detail lesen wollen.</p>
    <div class="why">
      <div><b>⛰️ Richtiger Gipfel</b>Höchster Punkt aller Touren, Rundumblick auf Dachstein und Hochwildstelle.</div>
      <div><b>🚶 Ohne Auto</b>Start an der Talstation, also direkt in der Nähe des Chalets. Keine Maut, kein Parkplatzstress.</div>
      <div><b>🍲 Mittag mit allen</b>Der Abstieg führt an der Galsterbergalm vorbei, dort treffen sich alle drei Teams.</div>
      <div><b>🔥 Banja danach</b>Um 15:30 zurück. Bis dahin hat Team Chalet die Banja angeheizt.</div>
    </div>
  </section>

  <section id="teams">
    <h2>Drei Teams, ein Mittagessen</h2>
    <p class="sub">Niemand muss den Gipfel machen. Jeder sucht sich sein Team aus.</p>
    <div class="teams" id="teamcards"></div>
  </section>

  <section id="zeitplan">
    <h2>Zeitplan</h2>
    <p class="sub">Richtwerte. Sonnenaufgang __AUF__ Uhr, Sonnenuntergang __UNTER__ Uhr.</p>
    <div class="timeline" id="timeline"></div>
  </section>

  <section id="route">
    <h2>Höhenprofil</h2>
    <p class="sub">940 Höhenmeter hoch und wieder runter auf 12,5 km.</p>
    <div class="profile"><svg id="profil" viewBox="0 0 900 300" role="img" aria-label="Höhenprofil der großen Pleschnitzzinken-Runde"></svg></div>
    <p class="note">Schematisch: Start, Hütte und Gipfel nach Komoot, die Lage der Galsterbergalm ist geschätzt. Der echte Weg hat mehr Auf und Ab.</p>
  </section>

  <section>
    <h2>Die Route Schritt für Schritt</h2>
    <p class="sub">Was euch unterwegs erwartet und worauf ihr achten solltet.</p>
    <ol class="steps" id="steps"></ol>
  </section>

  <section id="sicherheit">
    <h2>Sicherheit &amp; Umkehrregeln</h2>
    <p class="sub">Vorher vereinbart, damit unterwegs keiner diskutieren muss. Komoot stuft die Tour als schwer ein: 3,2 km alpines Gelände, 8 km loser Untergrund.</p>
    <div class="rules" id="rules"></div>
    <div class="sos">
      <a href="tel:140">🚑 Bergrettung 140</a>
      <a href="tel:112">🆘 Euro-Notruf 112</a>
      <a class="alt" href="tel:+436769518228">📞 Galsterbergalm</a>
    </div>
    <p class="note">Gruppe bleibt zusammen, der Langsamste gibt das Tempo vor. Im Gruppenchat den Live-Standort teilen.</p>
  </section>

  <section id="packliste">
    <h2>Packliste</h2>
    <p class="sub">Abhaken geht direkt hier, der Stand bleibt auf deinem Handy gespeichert. Punkte mit <span class="eu">Eugen</span> stammen aus seiner Liste im Chat.</p>
    <div class="packbar">
      <div class="progress" aria-hidden="true"><i id="pbar"></i></div>
      <b id="pcount"></b>
      <button class="btn" id="copy">Packliste für WhatsApp kopieren</button>
      <button class="btn ghost" id="reset">Zurücksetzen</button>
    </div>
    <div class="packs" id="packs"></div>
  </section>

  <section>
    <h2>Links</h2>
    <div class="links" id="links"></div>
  </section>

  <footer>Quellen: Komoot (Pruggererberg – Pleschnitzzinken-Gipfel Runde), steiermark.com (Galsterbergalm Hütte, Öffnungszeiten Herbst 2026), schladming-dachstein.at (Pleschnitzzinken). Sonnenzeiten für Pruggern berechnet. Alle Zeiten sind Richtwerte, Bedingungen am Tag selbst prüfen.</footer>
</main>
<div class="toast" id="toast">Kopiert ✓</div>

<script id="data" type="application/json">__DATA__</script>
<script>
const D = JSON.parse(document.getElementById('data').textContent);
const $ = id => document.getElementById(id);
const fmtH = m => Math.floor(m/60) + ':' + String(m%60).padStart(2,'0') + ' h';
const fmtM = v => Math.round(v).toLocaleString('de-DE') + ' m';
const de1 = v => v.toFixed(1).replace('.', ',');
__ART__
const t = D.t8;
// Hero
(function(){ const s = tourArt(t, 1200, 520); $('hero8').innerHTML = s.replace(/^<svg[^>]*>/, '').replace(/<\/svg>$/, ''); })();
// Facts
$('facts').innerHTML = [[de1(t.km)+' km','Strecke'],[t.hm+' Hm','hoch & runter'],[fmtH(t.geh),'reine Gehzeit'],['2.112 m','Gipfel'],['1.108 m','Start Talstation'],['schwer','laut Komoot']]
  .map(([b,s]) => '<div class="fact"><b>'+b+'</b><span>'+s+'</span></div>').join('');
// Teams
const TM = {'Team Gipfel':['','Eugen führt, Vadim ist dabei, dazu jeder, der Lust hat','Große Runde (8), Start 08:30. Wer es kürzer mag: Pleschnitzzinken ab Bottinghaus (2), '+fmtH(D.t2.geh)+' und '+D.t2.hm+' Hm, Start 10:30.'],
            'Team Hütte':['h','Für müde Beine oder einen schmerzenden Fuß','Galsterbergalm-Runde (1): '+fmtH(D.t1.geh)+', nur '+D.t1.hm+' Hm. Abfahrt 11:30 am Chalet, Start 11:45 am Bottinghaus.'],
            'Team Chalet':['c','Für alle, die zum Geburtstag feiern gekommen sind und nicht zum Ironman','Ausschlafen, Banja anheizen, Essen vorbereiten, Wein kalt stellen. Zum Mittag mit dem Auto zur Galsterbergalm dazustoßen.']};
$('teamcards').innerHTML = D.plan.teams.map(([n]) => { const [c, m, p] = TM[n]; return '<div class="team '+c+'"><h3>'+n+'</h3><div class="m">'+m+'</div><p>'+p+'</p></div>'; }).join('');
// Zeitplan
$('timeline').innerHTML = D.plan.plan.map(([z, x]) => '<div><b>'+z+'</b><span>'+x+'</span></div>').join('');
// Etappen
$('steps').innerHTML = D.etappen.map((e, i) => '<li class="step"><span class="dot">'+(i+1)+'</span><div class="card"><div class="hd"><span class="t">'+e.zeit+'</span><h3>'+e.titel+'</h3></div>'+
  '<div class="meta">'+[e.hoehe, e.km].filter(Boolean).join(' · ')+'</div><p>'+e.text+'</p><div class="tip">💡 '+e.tipp+'</div></div></li>').join('');
// Regeln
$('rules').innerHTML = D.regeln.map(([k, b, s]) => '<div class="rule"><div class="k">'+k+'</div><div><b>'+b+'</b><span>'+s+'</span></div></div>').join('');
// Profil (SVG)
function drawProfile(){
  const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
  const nar = innerWidth < 640, W = nar ? 460 : 900, H = nar ? 330 : 300, L = nar ? 44 : 54, R = nar ? 14 : 20, T = 40, B = 40, fs = nar ? 13 : 13, maxKm = 12.5, lo = 1000, hi = 2250;
  const x = k => L + k/maxKm*(W - L - R), y = h => T + (hi - h)/(hi - lo)*(H - T - B);
  const P = D.profil, ink = css('--muted'), line = css('--line'), red = css('--red');
  let g = '';
  [1000,1250,1500,1750,2000,2250].forEach(h => { g += '<line x1="'+L+'" x2="'+(W-R)+'" y1="'+y(h)+'" y2="'+y(h)+'" stroke="'+line+'" stroke-width="1"/><text x="'+(L-8)+'" y="'+(y(h)+4)+'" text-anchor="end" font-size="12" fill="'+ink+'">'+h.toLocaleString('de-DE')+'</text>'; });
  (nar ? [0,4,8,12] : [0,2,4,6,8,10,12]).forEach(k => { g += '<text x="'+x(k)+'" y="'+(H-B+20)+'" text-anchor="middle" font-size="12" fill="'+ink+'">'+k+' km</text>'; });
  const pts = P.map(p => x(p[0]).toFixed(1)+','+y(p[1]).toFixed(1)).join(' ');
  g += '<polygon points="'+x(0)+','+y(lo)+' '+pts+' '+x(maxKm)+','+y(lo)+'" fill="'+red+'" opacity=".12"/>';
  g += '<polyline points="'+pts+'" fill="none" stroke="'+red+'" stroke-width="3.5" stroke-linejoin="round"/>';
  P.forEach((p, i) => { const up = i !== 3;
    g += '<circle cx="'+x(p[0])+'" cy="'+y(p[1])+'" r="6" fill="'+red+'" stroke="'+css('--card')+'" stroke-width="2.5"/>';
    if (i === 4) return;
    const anchor = i === 0 ? 'start' : (nar && i === 3) ? 'start' : 'middle';
    const lbl = nar && i === 1 ? 'Hütte' : p[2];
    g += '<text x="'+x(p[0])+'" y="'+(y(p[1]) + (up ? -14 : 22))+'" text-anchor="'+anchor+'" font-size="13" font-weight="700" fill="'+css('--ink')+'">'+lbl+'</text>'+
         '<text x="'+x(p[0])+'" y="'+(y(p[1]) + (up ? -30 : 38))+'" text-anchor="'+anchor+'" font-size="12" fill="'+ink+'">'+p[1].toLocaleString('de-DE')+' m</text>';
  });
  $('profil').setAttribute('viewBox', '0 0 '+W+' '+H); $('profil').innerHTML = g;
}
drawProfile();
matchMedia('(prefers-color-scheme: dark)').addEventListener('change', drawProfile);
addEventListener('resize', drawProfile);
// Packliste
const ls = { get: k => { try { return localStorage.getItem(k) === '1'; } catch(e){ return false; } }, set: (k, v) => { try { localStorage.setItem(k, v ? '1' : '0'); } catch(e){} } };
function renderPack(){
  let n = 0, done = 0;
  $('packs').innerHTML = D.pack.map(([titel, sub, items], gi) => '<div class="pack"><h3>'+titel+'</h3><div class="m">'+sub+'</div>'+items.map(([txt, eu], ii) => {
    const k = 'pa_'+gi+'_'+ii, c = ls.get(k); n++; if (c) done++;
    return '<label class="'+(c?'done':'')+'"><input type="checkbox" data-k="'+k+'" '+(c?'checked':'')+'><span>'+txt+(eu?' <span class="eu">Eugen</span>':'')+'</span></label>'; }).join('')+'</div>').join('');
  $('pbar').style.width = (done/n*100)+'%'; $('pcount').textContent = done+' von '+n+' gepackt';
}
renderPack();
$('packs').addEventListener('change', e => { const k = e.target.dataset.k; if (k){ ls.set(k, e.target.checked); renderPack(); } });
$('reset').addEventListener('click', () => { D.pack.forEach(([,,items], gi) => items.forEach((_, ii) => ls.set('pa_'+gi+'_'+ii, false))); renderPack(); });
$('copy').addEventListener('click', () => {
  const txt = '🎒 Packliste Plan A (Pleschnitzzinken, Sa 17.10.)\n\n' + D.pack.map(([titel,, items]) => '*'+titel+'*\n'+items.map(([x]) => '▫️ '+x).join('\n')).join('\n\n') + '\n\nAlle Infos: ' + location.href.split('#')[0];
  const ok = () => { $('toast').classList.add('on'); setTimeout(() => $('toast').classList.remove('on'), 1600); };
  if (navigator.clipboard) navigator.clipboard.writeText(txt).then(ok, () => prompt('Kopieren:', txt)); else prompt('Kopieren:', txt);
});
// Links
const maps = 'https://www.google.com/maps/dir/?api=1' + (D.chalet ? '&origin=' + encodeURIComponent(D.chalet) : '') + '&destination=' + encodeURIComponent(t.dest) + '&travelmode=walking';
$('links').innerHTML = '<a class="btn" href="'+t.url+'" target="_blank" rel="noopener">Tour in Komoot öffnen</a><a class="btn ghost" href="'+maps+'" target="_blank" rel="noopener">Weg Chalet → Talstation</a><a class="btn ghost" href="./">Alle Touren &amp; Pläne</a>';
</script>
</body>
</html>
"""

html = (HTML.replace("__ART__", (Path(__file__).parent / "art.js").read_text(encoding="utf-8"))
        .replace("__AUF__", SONNE["auf"]).replace("__UNTER__", SONNE["unter"]).replace("__DATA__", data_json))
out = Path(__file__).parent / "docs"
out.mkdir(exist_ok=True)
(out / "plan-a.html").write_text(html, encoding="utf-8")
print("docs/plan-a.html:", round(len(html) / 1e3), "kB")
