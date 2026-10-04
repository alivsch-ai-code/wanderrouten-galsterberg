# Wanderrouten Galsterberg & Ennstal

Dashboard für die Samstags-Wanderung beim Chalet-Wochenende in Pruggern (Steiermark): 6 Touren mit Höhenmetern, Gehzeit, Anfahrt, Gesamtdauer ab Chalet, Wetter-Check und Checklisten.

## Live-Version (GitHub Pages)

https://alivsch-ai-code.github.io/wanderrouten-galsterberg/

Statische Seite aus `docs/index.html`, läuft ohne Server.

## Streamlit-Version lokal

```bash
pip install -r requirements.txt
streamlit run app.py
```

Die Google-Maps-Routen starten am Chalet. Auf der Seite lässt sich auf „Mein Standort“ umschalten. Anderer Startpunkt: Umgebungsvariable `CHALET_ADRESSE` setzen.

## Statische Seite neu bauen

```bash
python build_static.py   # schreibt docs/index.html
```

## Eigene Fotos

Fotos als `docs/img/tour-1.jpg` … `tour-6.jpg` ablegen (Querformat). Die Seite zeigt sie automatisch statt der Illustration.

## Dateien

- `routes.py`: Daten zu den Touren (hier ändern)
- `app.py`: Streamlit-Dashboard
- `build_static.py`: erzeugt die GitHub-Pages-Seite

Hinweis: Anfahrt, Pausen und Gesamtdauer sind Schätzungen. Vor Ort Wetter und Hüttenöffnungszeiten prüfen.
