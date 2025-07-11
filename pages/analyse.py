import streamlit as st
import pandas as pd
import plotly.express as px
from functions.menu import default_menu
from functions.data import get_cluster_names, get_latest_cluster_values, get_latest_update_time
from config import PATH_PROFILES

# -Seitenkonfiguration-
st.set_page_config(page_title="Visualisierung", layout="wide")
default_menu()

# -Tabelle für Profile verknüpfen-
data_profiles = pd.read_csv(PATH_PROFILES, sep=';', index_col=0)

# -Profilauswahl (oben)-

st.title("Visualisierung")

set_name_active_profile = st.selectbox("Profil auswählen:", data_profiles[["Name"]])
set_id_active_profile = data_profiles.index[data_profiles["Name"] == set_name_active_profile][0]

with st.container():
    cols = st.columns(2)
    # -Netzdiagramm Kompetenzen-
    with cols[0]:
        with st.container(border=False):

            
            st.header("Kompetenzen")
            df_radar = dict(
                Wert=get_latest_cluster_values(set_id_active_profile),
                Kategorie=get_cluster_names()
            )
            radar_chart = px.line_polar(df_radar, r="Wert", theta="Kategorie", range_r=[0,5], line_close=True)
            st.plotly_chart(figure_or_data=radar_chart)

    # -Profilentwicklung Diagramm-
    with cols[1]:
        with st.container(border=False):
            st.header("Profilentwicklung")
            set_category = st.selectbox("Kategorie:", get_cluster_names())
            df_line_chart = pd.DataFrame({
                "Kategorie": get_cluster_names(),
                "Wert": get_latest_cluster_values(set_id_active_profile)
            })
            st.line_chart(df_line_chart, x="Kategorie", y="Wert")

with st.container():
    cols = st.columns(2)
    # -Meta-Daten-
    with cols[0]:
        with st.container(border=False):
            st.header("Meta-Daten")
            st.write(f"Profil-ID: {set_id_active_profile}")
            st.write(f"Name: {set_name_active_profile}")
            st.write("Rolle: ...")
            st.write("Geburtsdatum: ...")
            st.write(f"Letzte Aktualisierung: {get_latest_update_time(set_id_active_profile)}")

    # -Analysehilfe-
    with cols[1]:
        with st.container(border=False):
            st.header("Analysehilfe")
