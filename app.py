"""Wanderrouten Galsterberg & Ennstal: Streamlit-Dashboard.

Start:  pip install -r requirements.txt
        streamlit run app.py
"""
import math

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Wanderrouten Galsterberg", page_icon="⛰️", layout="wide")

from routes import CHALET, MAUT_PKW, PLAENE, ROUTES, WETTER, fmt_h, fmt_m, make_df, maps_url

df = make_df()

# ----------------------------------------------------------------------------
# Farben: validierte Kategorien-Slots (blau, orange), je Hell/Dunkel
# ----------------------------------------------------------------------------
try:
    DARK = st.context.theme.type == "dark"
except Exception:
    DARK = False
COL = {"leicht": "#3987e5" if DARK else "#2a78d6", "mittel": "#d95926" if DARK else "#eb6834"}
SURFACE = "#1a1a19" if DARK else "#fcfcfb"
INK2 = "#c3c2b7" if DARK else "#52514e"
GRID = "rgba(150,150,150,0.25)"


def style(fig, height=380, legend=True):
    fig.update_layout(height=height, margin=dict(l=10, r=10, t=30, b=10), showlegend=legend,
                      legend=dict(orientation="h", y=1.1, x=0), font=dict(color=INK2),
                      paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", hoverlabel=dict(font_size=13))
    fig.update_xaxes(gridcolor=GRID, zeroline=False)
    fig.update_yaxes(gridcolor=GRID, zeroline=False)
    return fig


# ----------------------------------------------------------------------------
# Sidebar-Filter
# ----------------------------------------------------------------------------
st.sidebar.header("Filter")
niveaus = st.sidebar.multiselect("Niveau", ["leicht", "mittel"], default=["leicht", "mittel"])
max_geh = st.sidebar.slider("Max. Gehzeit (Std.)", 1.0, 3.0, 3.0, 0.25)
max_hm = st.sidebar.slider("Max. Aufstieg (Hm)", 0, 500, 500, 5)
nur_auto_frei = st.sidebar.checkbox("Nur Touren ohne Mautstraße", value=False)
st.sidebar.divider()
st.sidebar.caption("Anfahrt, Pausen und Gesamtdauer sind Schätzungen für eine Unterkunft am Pruggererberg. "
                   "Die genaue Fahrzeit zeigt der Maps-Link bei jeder Tour.")

mask = df["niveau"].isin(niveaus) & (df["geh"] <= max_geh * 60) & (df["hm"] <= max_hm)
if nur_auto_frei:
    mask &= ~df["maut"]
f = df[mask].copy()

# ----------------------------------------------------------------------------
# Kopf
# ----------------------------------------------------------------------------
st.title("⛰️ Wanderrouten Galsterberg & Ennstal")
st.caption("Chalet-Wochenende · Pruggern, Steiermark · Samstag im Oktober 2026 · Verantwortlich: Eugen (Женя)")

if f.empty:
    st.warning("Keine Tour passt zu den Filtern. Bitte in der Seitenleiste lockern.")
    st.stop()

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Touren", f"{len(f)} von {len(df)}")
k2.metric("Max. Aufstieg", f"{int(f['hm'].max())} Hm")
k3.metric("Höchster Punkt", fmt_m(f["top"].max()))
k4.metric("Max. Gehzeit", fmt_h(f["geh"].max()))
k5.metric("Längster Tag ab Chalet", fmt_h(f["gesamt"].max()))

tab_plan, tab_ueber, tab_hoehe, tab_anreise, tab_detail, tab_wetter, tab_check = st.tabs(
    ["Tagespläne", "Überblick", "Höhenmeter", "Anreise & Gesamtzeit", "Tourdetails", "Wetter-Check", "Checklisten"])

# ----------------------------------------------------------------------------
# Tagespläne
# ----------------------------------------------------------------------------
with tab_plan:
    st.subheader("Tagespläne für Samstag")
    wahl = st.radio("Plan", [p["id"] for p in PLAENE], horizontal=True,
                    format_func=lambda i: next(f"{p['id']} · {p['titel']}" for p in PLAENE if p["id"] == i))
    p = next(x for x in PLAENE if x["id"] == wahl)
    st.markdown(f"**{p['tipp']}** · Wetter: {p['wetter']}  \n{p['kurz']}")
    st.caption(" · ".join(p["plus"]))
    for zeit, was in p["plan"]:
        st.markdown(f"**{zeit}** &nbsp; {was}")
    st.dataframe(df[df["nr"].isin(p["touren"])].assign(Tour=lambda d: d["nr"].astype(str) + "  " + d["name"], Gehzeit=lambda d: d["geh"].map(fmt_h),
                 Aufstieg=lambda d: d["hm"].astype(str) + " Hm")[["Tour", "Gehzeit", "Aufstieg", "auto"]].rename(columns={"auto": "Auto"}),
                 hide_index=True, width="stretch")

# ----------------------------------------------------------------------------
# Überblick
# ----------------------------------------------------------------------------
with tab_ueber:
    c1, c2 = st.columns([3, 2])
    with c1:
        st.subheader("Aufwand: Gehzeit gegen Aufstieg")
        fig = go.Figure()
        for niv in ["leicht", "mittel"]:
            d = f[f["niveau"] == niv]
            if d.empty:
                continue
            fig.add_trace(go.Scatter(
                x=d["geh"] / 60, y=d["hm"], mode="markers+text", name=niv.capitalize(),
                text=d["nr"].astype(str), textposition="middle center", textfont=dict(color="white", size=12),
                marker=dict(size=d["km"] * 9 + 14, color=COL[niv], line=dict(color=SURFACE, width=2)),
                customdata=d[["kurz", "km", "top"]].values,
                hovertemplate="<b>%{customdata[0]}</b><br>Gehzeit %{x:.2f} h<br>Aufstieg %{y} Hm<br>"
                              "Länge %{customdata[1]} km<br>Höchster Punkt %{customdata[2]} m<extra></extra>"))
        fig.update_xaxes(title="Gehzeit (Stunden)", range=[0.5, 3])
        fig.update_yaxes(title="Aufstieg (Höhenmeter)", range=[-40, 560])
        st.plotly_chart(style(fig, 400), width="stretch")
        st.caption("Blasengröße = Länge in km. Die Zahl im Kreis ist die Tour-Nummer.")
    with c2:
        st.subheader("Aufstieg je Tour")
        s = f.sort_values("hm")
        fig = go.Figure(go.Bar(
            x=s["hm"], y=s["label"], orientation="h", marker=dict(color=[COL[n] for n in s["niveau"]], cornerradius=4),
            text=s["hm"].astype(str) + " Hm", textposition="outside", cliponaxis=False,
            hovertemplate="<b>%{y}</b><br>%{x} Hm<extra></extra>"))
        fig.update_xaxes(range=[0, 600], title=None)
        fig.update_yaxes(title=None)
        st.plotly_chart(style(fig, 400, legend=False), width="stretch")
        st.caption("Blau = leicht, orange = mittel.")

    st.subheader("Alle Touren im Überblick")
    show = f.assign(Tour=f["nr"].astype(str) + "  " + f["name"], Niveau=f["niveau"].str.capitalize(),
                    Gehzeit=f["geh"].map(fmt_h), Gesamt=f["gesamt"].map(fmt_h),
                    Karte=f["url"], Maps=f["dest"].map(maps_url))
    st.dataframe(
        show[["Tour", "Niveau", "km", "Gehzeit", "hm", "start_hoehe", "top", "Gesamt", "Karte", "Maps"]],
        hide_index=True, width="stretch",
        column_config={"km": st.column_config.NumberColumn("Länge (km)", format="%.1f"),
                       "hm": st.column_config.NumberColumn("Aufstieg (Hm)"),
                       "start_hoehe": st.column_config.NumberColumn("Start ca. (m)", format="%d"),
                       "top": st.column_config.NumberColumn("Höchster Punkt (m)", format="%d"),
                       "Gesamt": st.column_config.TextColumn("Gesamt ab Chalet"),
                       "Karte": st.column_config.LinkColumn("Tourenseite", display_text="öffnen"),
                       "Maps": st.column_config.LinkColumn("Route", display_text="Google Maps")})

# ----------------------------------------------------------------------------
# Höhenmeter
# ----------------------------------------------------------------------------
with tab_hoehe:
    st.subheader("Höhenbereich je Tour")
    fig = go.Figure()
    for niv in ["leicht", "mittel"]:
        d = f[f["niveau"] == niv].sort_values("top")
        if d.empty:
            continue
        fig.add_trace(go.Bar(
            y=d["label"], x=d["hm"], base=d["start_hoehe"], orientation="h", name=niv.capitalize(),
            marker=dict(color=COL[niv], cornerradius=4, line=dict(color=SURFACE, width=2)),
            text=[f"{a:,} – {b:,} m".replace(",", ".") for a, b in zip(d["start_hoehe"], d["top"])],
            textposition="outside", cliponaxis=False, customdata=d[["hm"]].values,
            hovertemplate="<b>%{y}</b><br>Start ca. %{base} m<br>Aufstieg %{customdata[0]} Hm<extra></extra>"))
    fig.update_xaxes(title="Höhe über dem Meer (m)", range=[500, 2450])
    fig.update_yaxes(title=None, autorange="reversed")
    st.plotly_chart(style(fig, 360), width="stretch")
    st.caption("Balken von der Starthöhe bis zum höchsten Punkt. Starthöhe = höchster Punkt minus Aufstieg (abgeleitet, daher ca.). "
               "Die Talrunden liegen bei rund 670 bis 720 m, die Bergtouren zwischen 1.600 und 2.100 m.")

    st.subheader("Vereinfachtes Höhenprofil")
    wahl = st.selectbox("Tour", f["label"].tolist(), key="profil")
    r = f[f["label"] == wahl].iloc[0]
    if r["top"] < 1000:
        xs = [0, 0.25, 0.5, 0.75, 1.0]
        ys = [r["start_hoehe"], r["start_hoehe"] + r["hm"] * 0.5, r["top"], r["start_hoehe"] + r["hm"] * 0.4, r["start_hoehe"]]
    else:
        xs = [0, 0.5, 1.0]
        ys = [r["start_hoehe"], r["top"], r["start_hoehe"]]
    fig = go.Figure(go.Scatter(x=[x * r["km"] for x in xs], y=ys, mode="lines+markers", line=dict(color=COL[r["niveau"]], width=3),
                               marker=dict(size=9, color=COL[r["niveau"]], line=dict(color=SURFACE, width=2)),
                               fill="tozeroy", fillcolor="rgba(120,140,170,0.12)",
                               hovertemplate="km %{x:.1f}<br>%{y:.0f} m<extra></extra>"))
    if r.get("huette") == r.get("huette") and pd.notna(r.get("huette")):
        frac = (r["huette"] - r["start_hoehe"]) / r["hm"] * 0.5
        fig.add_trace(go.Scatter(x=[frac * r["km"]], y=[r["huette"]], mode="markers+text", text=["Pleschnitzzinken Hütte (1.911 m)"],
                                 textposition="top left", marker=dict(size=11, color=COL[r["niveau"]], symbol="diamond",
                                                                     line=dict(color=SURFACE, width=2)), showlegend=False,
                                 hovertemplate="Hütte 1.911 m<extra></extra>"))
    fig.add_annotation(x=r["km"] * xs[ys.index(max(ys))], y=max(ys), text=f"Höchster Punkt {fmt_m(r['top'])}", showarrow=True, arrowhead=0, ay=-30,
                       font=dict(color=INK2))
    fig.update_xaxes(title="Strecke (km, grob)")
    fig.update_yaxes(title="Höhe (m)", range=[max(0, r["start_hoehe"] - 120), r["top"] + 120])
    st.plotly_chart(style(fig, 340, legend=False), width="stretch")
    st.caption("Schematisch: nur Start und höchster Punkt sind belegt, der Verlauf dazwischen ist vereinfacht und nicht maßstabsgetreu. "
               f"Gesamter Aufstieg: {r['hm']} Hm auf {r['km']} km.")

# ----------------------------------------------------------------------------
# Anreise & Gesamtzeit
# ----------------------------------------------------------------------------
with tab_anreise:
    st.subheader("Gesamtdauer ab Chalet")
    s = f.sort_values("gesamt")
    fig = go.Figure()
    teile = [("Fahrt (hin und zurück)", 2 * s["fahrt"], "#8c8b85" if not DARK else "#7a7972"),
             ("Gehzeit", s["geh"], COL["leicht"]), ("Pause / Einkehr", s["pause"], "#c3c2b7" if not DARK else "#5c5b56")]
    for name, vals, color in teile:
        fig.add_trace(go.Bar(y=s["label"], x=vals / 60, orientation="h", name=name,
                             marker=dict(color=color, line=dict(color=SURFACE, width=2)),
                             hovertemplate="<b>%{y}</b><br>" + name + ": %{x:.2f} h<extra></extra>"))
    fig.update_layout(barmode="stack")
    fig.update_xaxes(title="Stunden")
    fig.update_yaxes(title=None, autorange="reversed")
    st.plotly_chart(style(fig, 360), width="stretch")
    st.caption("Fahrzeiten und Pausen sind Schätzungen. Für die genaue Fahrzeit den Maps-Link bei den Tourdetails nutzen.")

    st.subheader("Auto & Maut")
    a, b, c = st.columns(3)
    personen = a.number_input("Personen", 1, 20, 9)
    plaetze = b.number_input("Plätze pro Auto", 2, 9, 5)
    autos = math.ceil(personen / plaetze)
    c.metric("Autos nötig", autos)
    touren_maut = f[f["maut"]]
    if touren_maut.empty:
        st.info("Keine der gefilterten Touren nutzt die Mautstraße.")
    else:
        kosten = autos * MAUT_PKW
        st.metric("Maut Stoderzinken (Tour 3, 4, 7)", f"{kosten} €", f"{kosten / personen:.2f} € pro Person".replace(".", ","), delta_color="off")
        st.caption("20 € pro Pkw. Laut Tourismusseite ist die Maut zwischen 14.09. und 01.11.2026 mit der Schladming-Dachstein Card inklusive.")
    st.dataframe(f.assign(Tour=f["nr"].astype(str) + "  " + f["kurz"], Anfahrt=f["fahrt"].astype(str) + " Min",
                          Auto=f["auto"], Gesamt=f["gesamt"].map(fmt_h))[["Tour", "Anfahrt", "Auto", "Gesamt"]],
                 hide_index=True, width="stretch")

# ----------------------------------------------------------------------------
# Tourdetails
# ----------------------------------------------------------------------------
with tab_detail:
    wahl = st.selectbox("Tour wählen", f["label"].tolist(), key="detail")
    r = f[f["label"] == wahl].iloc[0]
    st.header(f"{r['nr']} · {r['name']}")
    st.markdown(f"**Niveau:** :{'green' if r['niveau'] == 'leicht' else 'orange'}[{r['niveau'].capitalize()}] · {r['kondition']}")
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Länge", f"{r['km']:.1f} km".replace(".", ","))
    m2.metric("Gehzeit", fmt_h(r["geh"]))
    m3.metric("Aufstieg", f"{r['hm']} Hm")
    m4.metric("Start ca.", fmt_m(r["start_hoehe"]))
    m5.metric("Höchster Punkt", fmt_m(r["top"]))
    left, right = st.columns([3, 2])
    with left:
        st.markdown(f"**Start:** {r['start_ort']}")
        st.markdown(f"**Route:** {r['weg']}")
        st.markdown("**Highlights**")
        for p in r["plus"]:
            st.markdown(f"- {p}")
        st.markdown(f"**Gut zu wissen:** {r['info']}")
    with right:
        st.markdown("**Ab Chalet**")
        st.markdown(f"- Anfahrt ca. {r['fahrt']} Min (einfach, Schätzung)\n- Gesamtdauer {fmt_h(r['gesamt'])}\n- Auto: {r['auto']}")
        st.link_button("Tourenseite mit Karte öffnen", r["url"], width="stretch")
        st.link_button("Route in Google Maps", maps_url(r["dest"]), width="stretch")

# ----------------------------------------------------------------------------
# Wetter-Check
# ----------------------------------------------------------------------------
with tab_wetter:
    st.subheader("Welche Tour passt zum Wetter?")
    lage = st.radio("Wetterlage", list(WETTER), horizontal=True)
    st.success(WETTER[lage])
    passend = df[df["wetter"].map(lambda w: lage in w)]
    st.dataframe(passend.assign(Tour=passend["nr"].astype(str) + "  " + passend["name"], Niveau=passend["niveau"].str.capitalize(),
                                Aufstieg=passend["hm"].astype(str) + " Hm", Gehzeit=passend["geh"].map(fmt_h))
                 [["Tour", "Niveau", "Aufstieg", "Gehzeit"]], hide_index=True, width="stretch")
    st.info("Mitte Oktober ist in den Höhenlagen Schnee möglich. Sonnenuntergang ungefähr gegen 18 Uhr (am Tag selbst prüfen). "
            "Die Galsterbergalmhütte hat im Herbst Fr–So 9–18 Uhr geöffnet, die Pleschnitzzinken Hütte ist unbewirtschaftet. "
            "Die Galsterbergbahn fährt nur im Winter.")

# ----------------------------------------------------------------------------
# Checklisten
# ----------------------------------------------------------------------------
with tab_check:
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Checkliste für Eugen")
        for i, t in enumerate(["Wetter und Schneelage am Vorabend prüfen", "Plan nach Wetter wählen und Gruppen einteilen (Gipfel / Hütte)",
                               "Galsterbergalm: Tisch für 9 reservieren (+43 676 951 8228)", "Fahrgemeinschaften und Abfahrtszeit festlegen",
                               "Plan B: Maut 20 € pro Auto, Öffnung Steinerhaus/Rosemi Alm prüfen", "Notruf und Treffpunkt im Chat teilen"]):
            st.checkbox(t, key=f"e{i}")
    with c2:
        st.subheader("Ausrüstung")
        for i, t in enumerate(["Wanderschuhe mit Profil", "Warme Schichten, Mütze", "Regen- und Windjacke", "Trinkflasche (1 l)",
                               "Gipfel-Brotzeit", "Stirnlampe", "Powerbank, Offline-Karte", "Erste-Hilfe-Set", "Sonnenbrille"]):
            st.checkbox(t, key=f"g{i}")
    st.error("Notruf: Bergrettung 140 · Euro-Notruf 112. Bei Unfall oder Wetterumschwung früh umkehren, Gruppe zusammenhalten.")

st.divider()
st.caption("Quellen: schladming-dachstein.at, steiermark.com, hauser-kaibling.at, tourispo.de. Alle Angaben sind Richtwerte, "
           "aktuelle Bedingungen vor Ort prüfen.")
