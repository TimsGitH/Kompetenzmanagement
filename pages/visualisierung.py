import streamlit as st
import pandas as pd
import plotly.express as px
from functions.menu import default_menu
from functions.data import get_cluster_names, get_latest_cluster_values, get_latest_update_time

# -Seitenkonfiguration-
st.set_page_config(page_title="Visualisierung", layout="wide")
default_menu()
top = st.container()
left, right = st.columns(2)


# -Tabelle für Mitarbeiter verknüpfen-
data_mitarbeiter = pd.read_csv("user_management/mitarbeiter.csv", sep=';', index_col=0)

# -Tabelle für Antworten verknüpfen-
answers = pd.read_csv("antworten/antworten.csv", sep=';', index_col=0)


# -Inhalt-

# -Mitarbeiter Auswahl (oben)-
with top:
    st.title("Visualisierung")
    set_name_active_mitarbeiter = st.selectbox("Mitarbeiter auswählen:", data_mitarbeiter[["Name"]])
    set_id_active_mitarbeiter = data_mitarbeiter.index[data_mitarbeiter["Name"] == set_name_active_mitarbeiter][0]

# -Linke Seite-
with left:

    # -Netzdiagramm-
    st.header("Kompetenzen")
    df_radar = dict(
        Wert=get_latest_cluster_values(set_id_active_mitarbeiter),
        Kategorie=get_cluster_names()
    )
    radar_chart = px.line_polar(df_radar, r="Wert", theta="Kategorie", range_r=[5,0], line_close=True)
    st.plotly_chart(figure_or_data=radar_chart)

    # -Meta-Daten-
    st.header("Meta-Daten")
    st.write(f"Mitarbeiter-ID: {set_id_active_mitarbeiter}")
    st.write(f"Name: {set_name_active_mitarbeiter}")
    st.write("Rolle: ...")
    st.write("Geburtsdatum: ...")
    st.write(f"Letzte Aktualisierung: {get_latest_update_time(set_id_active_mitarbeiter)}")

# -Rechte Seite-
with right:

    # -Profilentwicklung Diagramm-
    st.header("Profilentwicklung")
    set_category = st.selectbox("Kategorie:", get_cluster_names())
    df_line_chart = pd.DataFrame({
        "Kategorie": get_cluster_names(),
        "Wert": get_latest_cluster_values(set_id_active_mitarbeiter)
    })
    st.line_chart(df_line_chart, x="Kategorie", y="Wert")

    # -Analyse-
    st.header("Analysehilfe")
