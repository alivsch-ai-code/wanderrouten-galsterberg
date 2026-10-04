"""Daten und Hilfsfunktionen für die Wanderrouten (gemeinsam für Streamlit-App und statische Seite).

Quellen: schladming-dachstein.at, steiermark.com, hauser-kaibling.at, tourispo.de.
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
         info="Zufahrt über den Pruggererbergweg ab Pruggern (Serpentinen). Öffnungszeiten der Hütte vorab klären.",
         url="https://www.schladming-dachstein.at/de/aktivitaeten/touren/Wanderung-zur-Galsterbergalmh-C3-BCtte_tour_6190",
         wetter={"Klar und stabil", "Wolken oder Neuschnee in der Höhe"}),
    dict(nr=2, name="Pleschnitzzinken (2.112 m)", kurz="Pleschnitzzinken", niveau="mittel", km=5.5, geh=150, hm=490, top=2112,
         start_ort="Parkplatz Bottinghaus", kondition="Kondition 4/6", fahrt=10, pause=45,
         auto="Ja, empfohlen (am Start keine öffentliche Anbindung)", maut=False, bus=False, dest="Bottinghaus, 8965 Pruggern",
         weg="Forststraße, dann Waldsteig durch Fichten, Lärchen und Zirben. Über der Baumgrenze durch Latschen und Almrosen zur unbewirtschafteten "
             "Pleschnitzzinken Hütte, dann über den Grasrücken zum Gipfelkreuz. Abstieg über die andere Rückenseite und die Galsterbergalm.",
         plus=["Gipfelkreuz auf 2.112 m", "Blick ins Ennstal", "Einkehr auf dem Rückweg an der Galsterbergalm"],
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
         info="Trittsicherheit und Schwindelfreiheit nötig. Der Weg zum Friedenskircherl ist bei Schnee ungeeignet.",
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
]

WETTER = {
    "Klar und stabil": "Gipfeltag: Pleschnitzzinken (2) oder Stoderzinken (3). Mit Zeitreserve zusätzlich die Galsterbergalm-Runde (1).",
    "Klar, aber gemütlich": "Stoderzinken-Gipfelrundweg (3), danach die Stoderalm-Runde (4). Beide starten am gleichen Parkplatz.",
    "Wolken oder Neuschnee in der Höhe": "Kurz und mit Hütte als Ziel: Galsterbergalm-Runde (1). Alternativ die Talrunden (5, 6).",
    "Regen oder Nebel": "Talrunden Pruggern–Assach (5) oder Pruggern–Moosheim (6): fast eben, ganzjährig begehbar, direkt im Ort.",
}



def make_df() -> pd.DataFrame:
    df = pd.DataFrame(ROUTES)
    df["start_hoehe"] = df["top"] - df["hm"]
    df["gesamt"] = 2 * df["fahrt"] + df["geh"] + df["pause"]
    df["label"] = df["nr"].astype(str) + "  " + df["kurz"]
    return df
