"""Daten und Hilfsfunktionen für die Wanderrouten (gemeinsam für Streamlit-App und statische Seite).

Quellen: schladming-dachstein.at, steiermark.com, hauser-kaibling.at, tourispo.de (geprüft am 04.10.2026).
Start-Höhe = höchster Punkt minus Aufstieg (abgeleitet, daher "ca.").
Anfahrt, Pause und Gesamtdauer ab Chalet sind Schätzungen.
"""
import os
from urllib.parse import quote_plus

import pandas as pd

# Optional: Adresse der Unterkunft als Umgebungsvariable setzen, dann enthalten die Maps-Links den Startpunkt.
# Ohne Angabe plant Google Maps die Route ab dem aktuellen Standort.
CHALET = os.environ.get("CHALET_ADRESSE", "")
MAUT_PKW = 20  # Euro pro Pkw, Stoderzinken-Mautstraße


def maps_url(dest: str) -> str:
    url = "https://www.google.com/maps/dir/?api=1"
    if CHALET:
        url += "&origin=" + quote_plus(CHALET, safe=",")
    return url + "&destination=" + quote_plus(dest, safe=",")


def fmt_h(m):
    return f"{int(m) // 60}:{int(m) % 60:02d} h"


def fmt_m(v):
    return f"{int(v):,}".replace(",", ".") + " m"


ROUTES = [
    dict(nr=1, name="Galsterbergalmhütte-Runde", kurz="Galsterbergalm", niveau="leicht", km=2.0, geh=60, hm=135, top=1800,
         start_ort="Parkplatz Bottinghaus", kondition="Kondition 2/6 · Technik 2/6", fahrt=10, pause=45,
         auto="Ja, empfohlen (am Start keine öffentliche Anbindung)", maut=False, bus=False, dest="Bottinghaus, 8965 Pruggern",
         weg="Forstweg zum Wegkreuz, dann links talwärts am Speicherteich vorbei zur Hütte. Zurück über einen Wald- und Wurzelsteig hinter der Hütte.",
         plus=["Sonnenterrasse der Galsterbergalmhütte", "Murmeltiere rund um die Hütte", "Kurz und gut als Aufwärmrunde"],
         info="Zufahrt über den Pruggererbergweg ab Pruggern (Serpentinen), nicht an der Talstation parken. Hütte im Herbst Fr–So 9–18 Uhr geöffnet, Küche 10:30–17 Uhr (Tel. +43 676 951 8228). Die Galsterbergbahn fährt nur im Winter.",
         url="https://www.schladming-dachstein.at/de/aktivitaeten/touren/Wanderung-zur-Galsterbergalmh-C3-BCtte_tour_6190",
         wetter={"Klar und stabil", "Wolken oder Neuschnee in der Höhe"}),
    dict(nr=2, name="Pleschnitzzinken (2.112 m)", kurz="Pleschnitzzinken", niveau="mittel", km=5.5, geh=150, hm=490, top=2112,
         start_ort="Parkplatz Bottinghaus", kondition="Kondition 4/6", fahrt=10, pause=45,
         auto="Ja, empfohlen (am Start keine öffentliche Anbindung)", maut=False, bus=False, dest="Bottinghaus, 8965 Pruggern",
         weg="Forststraße, dann Waldsteig durch Fichten, Lärchen und Zirben. Über der Baumgrenze durch Latschen und Almrosen zur unbewirtschafteten "
             "Pleschnitzzinken Hütte, dann über den Grasrücken zum Gipfelkreuz. Abstieg über die andere Rückenseite und die Galsterbergalm.",
         plus=["Gipfelkreuz auf 2.112 m", "Blick auf Hochwildstelle und Dachstein", "Einkehr auf dem Rückweg an der Galsterbergalm (Sa geöffnet)"],
         info="Große Variante ab Hüttendorf Pruggern: ca. 11 km, 1.057 Hm, nach Quelle 7:30 h. Erweiterungen: Ochsenkarhöhe (ca. +1 h), Schober (ca. 5 h). "
              "Wetterumschwung, Wind und Schnee einplanen.",
         url="https://www.schladming-dachstein.at/de/aktivitaeten/touren/Pleschnitzzinken_tour_6191",
         wetter={"Klar und stabil"}, huette=1911),
    dict(nr=3, name="Stoderzinken-Gipfelrundweg (2.048 m)", kurz="Stoderzinken-Gipfel", niveau="mittel", km=4.9, geh=150, hm=400, top=2048,
         start_ort="Parkplatz Roßfeld (Wanderportal Rosemi Alm)", kondition="Kondition 3/6 · Technik 3/6", fahrt=40, pause=60,
         auto="Ja, Mautstraße (Shuttle fährt im Oktober nicht)", maut=True, bus=False, dest="Rosemi Alm, Stoderzinken, 8962 Gröbming",
         weg="Von der Rosemi Alm durch Lärchen-, Zirben- und Latschenwald über die Baumgrenze. Stationen: AV-Weg 675, Stoderhütte, "
             "Peter-Rosegger-Denkmal, Gipfel, Brünnerhütte, Steinerhaus.",
         plus=["360-Grad-Panorama mit Dachstein-Gletscher", "Blick auf das Gröbminger Becken", "Mehrere Hütten entlang der Runde"],
         info="Trittsicherheit und Schwindelfreiheit nötig. Maut 20 € pro Pkw (14.09.–01.11.2026, mit Schladming-Dachstein Card frei). Öffnung von Steinerhaus und Rosemi Alm vorab prüfen. Lässt sich mit dem Friedenskircherl (7) kombinieren.",
         url="https://www.schladming-dachstein.at/de/schladming-dachstein-entdecken/winterberge/galsterberg/touren/Stoderzinken-Gipfelrundweg_tour_6139",
         wetter={"Klar und stabil", "Klar, aber gemütlich"}),
    dict(nr=4, name="Stoderalm-Rundweg zum Gröbminger Blick", kurz="Stoderalm-Rundweg", niveau="leicht", km=4.9, geh=105, hm=230, top=1829,
         start_ort="Parkplatz Roßfeld oder Christophorus", kondition="leichte Runde", fahrt=40, pause=45,
         auto="Ja, Mautstraße (Shuttle fährt im Oktober nicht)", maut=True, bus=False, dest="Rosemi Alm, Stoderzinken, 8962 Gröbming",
         weg="Rundweg über die Stoderalm-Weiden mit Rosemi Alm, AV-Weg 675, Stoderhütte, Brünner Hütte und Steinerhaus. "
             "Höhepunkt ist die Aussichtsbank „Gröbminger Blick“.",
         plus=["Aussichtsbank Gröbminger Blick", "Wenig Höhenmeter", "Lässt sich mit Tour 3 kombinieren"],
         info="Mautstraße beachten. Mit Tour 3 kombiniert dauert der Tag ab Chalet etwa 7 h.",
         url="https://www.steiermark.com/de/Urlaub-planen/Tourenportal/Stoderalm-Rundweg-zum-Groebminger-Blick_tour_28199775",
         wetter={"Klar, aber gemütlich"}),
    dict(nr=5, name="Pruggern–Assach-Runde (P2)", kurz="Pruggern–Assach", niveau="leicht", km=5.4, geh=90, hm=45, top=719,
         start_ort="Panoramatafel am Dorfplatz Pruggern", kondition="Kondition 2/6 · Technik 2/6", fahrt=10, pause=45,
         auto="Auto oder Bus 900/901 ab Pruggern Ort", maut=False, bus=True, dest="Dorfplatz, 8965 Pruggern",
         weg="Wiesen- und Asphaltwege entlang des Enns-Radwegs. Stationen: Gasthaus Bierfriedl, Dunner Reitanlage, Ennsweg, Assach, zurück über die Ennstalstraße.",
         plus=["Am Fluss entlang", "Ganzjährig begehbar", "Ideal bei Regen oder Neuschnee in der Höhe"],
         info="Direkt im Ort startbar.",
         url="https://www.hauser-kaibling.at/en/activities/hiking/Pruggern-Assach-Runde_tour_5968",
         wetter={"Regen oder Nebel", "Wolken oder Neuschnee in der Höhe"}),
    dict(nr=6, name="Pruggern–Moosheim-Runde (P4)", kurz="Pruggern–Moosheim", niveau="leicht", km=5.7, geh=90, hm=15, top=685,
         start_ort="B320-Abzweigung Pruggern Ort", kondition="leichte Runde", fahrt=10, pause=30,
         auto="Auto oder Bus 900/901 ab Pruggern Ort", maut=False, bus=True, dest="Regional Regal Pruggern, 8965 Pruggern",
         weg="Durch Wiesen und an Bauernhöfen vorbei nach Moosheim. Die Enns liegt rechts, links der Blick auf Stoderzinken und Kammspitze.",
         plus=["Blick auf Stoderzinken und Kammspitze", "Fast eben", "Mit Bus erreichbar"],
         info="Parkplatz gegenüber Regional Regal Pruggern (nahe Bahnsteig). Busse 900 (ab Schladming) und 901 (ab Stainach).",
         url="https://www.steiermark.com/de/Schladming-Dachstein/Urlaub-planen/Tourenportal/Pruggern-Moosheim-Runde-P4_tour_54673603",
         wetter={"Regen oder Nebel", "Wolken oder Neuschnee in der Höhe"}),
    dict(nr=7, name="Friedenskircherl am Stoderzinken", kurz="Friedenskircherl", niveau="leicht", km=3.0, geh=75, hm=160, top=1903,
         start_ort="Parkplatz Roßfeld (Rosemi Alm) oder Christophorus", kondition="leicht, aber kurze ausgesetzte Stellen", fahrt=40, pause=45,
         auto="Ja, Mautstraße (Shuttle fährt im Oktober nicht)", maut=True, bus=False, dest="Rosemi Alm, Stoderzinken, 8962 Gröbming",
         weg="Von der Rosemi Alm leicht ansteigend zum Rosegger-Denkmal. Danach ein flacher, schmaler und gesicherter Steig dicht an der Felswand "
             "zur Kapelle (ca. 40 Min). Das letzte Stück führt über Kalkschutt und ist etwas ausgesetzt.",
         plus=["Kapelle von 1902 direkt an der Felswand", "2022 im ORF zum schönsten Platz Österreichs gewählt", "Kurz, ideal mit dem Gipfelrundweg (3)"],
         info="Gute Schuhe und Stöcke. Die Geländer an den steilen Stellen sind laut Quelle nur im Sommer montiert, bei Schnee oder Eis nicht gehen.",
         url="https://www.steiermark.com/de/Schladming-Dachstein/Urlaub-planen/Tourenportal/Friedenskircherl-am-Stoderzinken_tour_1198170",
         wetter={"Klar und stabil", "Klar, aber gemütlich"}),
]

WETTER = {
    "Klar und stabil": "Plan A: Gruppe teilen. Die Fitten gehen auf den Pleschnitzzinken (2), die anderen direkt zur Galsterbergalm (1). Mittagessen gemeinsam an der Hütte. Alternative: Plan B am Stoderzinken (3 + 7).",
    "Klar, aber gemütlich": "Plan B: Stoderzinken. Friedenskircherl (7) und Stoderalm-Runde (4) mit Einkehr, wer mag nimmt den Gipfel (3) mit. Alles ab demselben Parkplatz.",
    "Wolken oder Neuschnee in der Höhe": "Plan C: Galsterbergalm-Runde (1) mit langer Einkehr, nur 10 Min vom Chalet. Kein Friedenskircherl und kein Gipfel bei Schnee.",
    "Regen oder Nebel": "Plan D: Talrunde Pruggern–Assach (5) mit Einkehr im Landgasthof Bierfriedl, danach früh in die Banja.",
}

# Fertige Tagespläne. Zeiten sind Vorschläge (Gehzeiten laut Quelle, Rest geschätzt).
PLAENE = [
    dict(id="A", titel="Gruppe teilen am Galsterberg", wetter="Klar und stabil", touren=[2, 1], tipp="Empfehlung",
         kurz="Fitte auf den Pleschnitzzinken, alle anderen gemütlich zur Hütte. Mittag gemeinsam an der Galsterbergalm.",
         plan=[("09:30", "Gruppe Gipfel: Abfahrt am Chalet zum Parkplatz Bottinghaus (Auto 1, ca. 10 Min)"),
               ("09:45", "Gruppe Gipfel: Start auf Forststraße und Waldsteig"),
               ("10:45", "Gruppe Gipfel an der Pleschnitzzinken Hütte (1.911 m)"),
               ("11:00", "Gruppe Hütte: Abfahrt am Chalet (Auto 2)"),
               ("11:15", "Gruppe Gipfel am Gipfelkreuz (2.112 m) · Gruppe Hütte startet die Galsterbergalm-Runde"),
               ("12:15", "Alle treffen sich an der Galsterbergalmhütte, Küche ab 10:30"),
               ("13:45", "Gemeinsam zurück zum Parkplatz (ca. 15 Min)"),
               ("14:15", "Zurück am Chalet, Zeit für die Banja")],
         plus=["Nur 10 Min Anfahrt, keine Maut", "Jeder findet sein Tempo", "Hütte ist samstags geöffnet"]),
    dict(id="B", titel="Stoderzinken mit Friedenskircherl", wetter="Klar, aber gemütlich", touren=[7, 4, 3], tipp="Fotospot",
         kurz="Das bekannteste Ausflugsziel der Gegend. Friedenskircherl und Stoderalm-Runde, der Gipfel ist optional.",
         plan=[("09:00", "Abfahrt am Chalet, Mautstraße ab Gröbming (ca. 40 Min, 20 € pro Auto)"),
               ("09:45", "Parkplatz Roßfeld an der Rosemi Alm"),
               ("10:00", "Friedenskircherl über Rosegger-Denkmal (hin und zurück 1:15 h)"),
               ("11:20", "Stoderalm-Runde zum Gröbminger Blick (1:45 h), Fitte über den Gipfel (3)"),
               ("13:15", "Einkehr am Stoderzinken (Öffnung vorab prüfen)"),
               ("14:30", "Rückfahrt"),
               ("15:15", "Zurück am Chalet")],
         plus=["Kapelle an der Felswand", "Dachstein-Panorama", "Alles ab einem Parkplatz"]),
    dict(id="C", titel="Kurz & gemütlich", wetter="Wolken oder Neuschnee in der Höhe", touren=[1], tipp="Schlechtwetter oben",
         kurz="Eine Stunde Runde mit Murmeltieren und langer Einkehr. Sicher auch bei Neuschnee weiter oben.",
         plan=[("10:30", "Abfahrt am Chalet zum Bottinghaus"),
               ("10:45", "Galsterbergalm-Runde (1 h)"),
               ("11:45", "Einkehr an der Galsterbergalmhütte"),
               ("13:30", "Zurück am Chalet")],
         plus=["Ausschlafen möglich", "Kaum Risiko", "Viel Zeit für Banja"]),
    dict(id="D", titel="Talrunde bei Regen", wetter="Regen oder Nebel", touren=[5], tipp="Regen",
         kurz="Fast eben an der Enns entlang, mit Einkehr im Landgasthof Bierfriedl (täglich 9–23 Uhr).",
         plan=[("10:30", "Abfahrt am Chalet ins Tal (ca. 10 Min)"),
               ("10:45", "Pruggern–Assach-Runde ab Dorfplatz (1:30 h)"),
               ("12:15", "Mittag im Landgasthof Bierfriedl"),
               ("13:45", "Zurück am Chalet")],
         plus=["Ganzjährig begehbar", "Kein Auto nötig ab Ort", "Wetterunabhängig"]),
]


def make_df() -> pd.DataFrame:
    df = pd.DataFrame(ROUTES)
    df["start_hoehe"] = df["top"] - df["hm"]
    df["gesamt"] = 2 * df["fahrt"] + df["geh"] + df["pause"]
    df["label"] = df["nr"].astype(str) + "  " + df["kurz"]
    return df
