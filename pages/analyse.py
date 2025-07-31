import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from functions.menu import default_menu
from functions.data import get_cluster_names, get_selected_cluster_values, get_latest_update_time, \
    get_cluster_values_over_time, calculate_cluster_differences, create_gap_analysis_chart, get_gap_analysis_legend, \
    get_bedarfe_for_profile
from config import GOOGLE_SHEET_ANSWERS, COLUMN_TIMESTAMP, GOOGLE_SHEET_PROFILES, COLUMN_PROFILE_ID, GOOGLE_SHEET_BEDARFE
from functions.database import get_dataframe_from_gsheet

# -Seitenkonfiguration-
st.set_page_config(page_title="Analyse", layout="wide")
default_menu()

st.title("Visualisierung")

# -Tabelle für Profile verknüpfen-
data_profiles = get_dataframe_from_gsheet(GOOGLE_SHEET_PROFILES, index_col=COLUMN_PROFILE_ID)
data_answers = get_dataframe_from_gsheet(GOOGLE_SHEET_ANSWERS, index_col=COLUMN_TIMESTAMP)
data_bedarfe = get_dataframe_from_gsheet(GOOGLE_SHEET_BEDARFE, index_col=COLUMN_TIMESTAMP)

col1, col2 = st.columns(2)

with col1:
    # Profil auswählen
    st.subheader("Profil Auswahl:")
    set_name_active_profile = st.selectbox("Profil auswählen:", data_profiles[["Name"]], key="analyse_profil_auswahl_1")
    set_id_active_profile = data_profiles.index[data_profiles["Name"] == set_name_active_profile][0]

    # Zeitpunkt auswählen
    filtered_update_time = data_answers.index[data_answers["Profil-ID"] == set_id_active_profile]
    set_update_time_active_profile = st.selectbox("Zeitpunkt auswählen:", filtered_update_time, key="analyse_zeitpunkt_1")

with col2:
    st.subheader("Bedarf Auswahl:")

    # Bedarf auswählen #format_func=lambda x: f"Profil {x}"
    unique_bedarf_ids = data_bedarfe["Profil-ID"].unique().tolist()
    set_bedarf_id = st.selectbox("Bedarf auswählen:", unique_bedarf_ids, key="bedarf_auswahl_1")

    # Zeitpunkt auswählen
    filtered_timestamps_bedarf = data_bedarfe.index[data_bedarfe["Profil-ID"] == set_bedarf_id]
    set_timestamp_bedarf = st.selectbox("Zeitpunkt auswählen:", filtered_timestamps_bedarf,
                                              key="analyse_zeitpunkt_2")

with st.container():
    cols = st.columns(2)
    # -Netzdiagramm Kompetenzen-
    with cols[0]:
        with st.container(border=False):
            st.header("Netzdiagramm Kompetenzen & Bedarfe")
            # Cluster-Werte für aktives Profil und Bedarf abrufen
            cluster_values_profil = get_selected_cluster_values(set_id_active_profile, set_update_time_active_profile)
            cluster_values_bedarf = get_bedarfe_for_profile(set_bedarf_id, set_timestamp_bedarf)

            kategorien = get_cluster_names()
            kategorien_list = kategorien.tolist()

            fig = go.Figure()
            # Fläche Bedarf
            fig.add_trace(go.Scatterpolar(
                r=cluster_values_bedarf + [cluster_values_bedarf[0]],
                theta=kategorien_list + [kategorien_list[0]],
                fill='toself',
                name='Bedarfs Profil',
                line=dict(color='red'),
                fillcolor='rgba(255, 0, 0, 0.3)',  # Rot mit Transparenz
            ))


            # Fläche Profil
            fig.add_trace(go.Scatterpolar(
                r=cluster_values_profil + [cluster_values_profil[0]],
                theta=kategorien_list + [kategorien_list[0]],
                fill='toself',
                name='Aktives Profil',
                line=dict(color='blue'),
                fillcolor='rgba(0, 0, 255, 0.6)',  # Blau mit Transparenz
            ))

            fig.update_layout(
                polar=dict(
                    radialaxis=dict(range=[0, 5], visible=True)
                ),
                showlegend=True,
                title="Netzdiagramm Kompetenzen & Bedarfe"
            )

            st.plotly_chart(fig)

    # -Profilentwicklung Diagramm-
    with cols[1]:
        with st.container(border=False):
            st.header("Profilentwicklung")
            set_category = st.selectbox("Kategorie:", kategorien, key="analyse_kategorien_1")
            
            # Zeitreihen-Daten für die ausgewählte Kategorie laden
            time_series_data = get_cluster_values_over_time(set_id_active_profile, set_category)
            
            if not time_series_data.empty:
                # Zeitpunkt in Jahr konvertieren
                time_series_data['Jahr'] = pd.to_datetime(time_series_data['Zeitpunkt'], format='%d.%m.%Y %H:%M').dt.year
                
                # Plotly Liniendiagramm erstellen
                fig = px.line(
                    time_series_data, 
                    x='Jahr', 
                    y='Wert',
                    title=f'Entwicklung: {set_category}',
                    labels={'Jahr': 'Jahr', 'Wert': 'Wert (1-5)'},
                    markers=True
                )
                
                # y-Achse auf 1-5 begrenzen
                fig.update_layout(
                    yaxis=dict(range=[1, 5]),
                    xaxis=dict(type='linear'),
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.write("Keine Daten für die Profilentwicklung verfügbar.")

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

    # GAP-Analyse
    with cols[1]:
        with st.container(border=False):
            st.header("GAP-Analyse")

            if not data_bedarfe.empty:
                # Differenzen berechnen mit modularer Funktion
                differences_df = calculate_cluster_differences(set_id_active_profile, set_bedarf_id, set_update_time_active_profile, set_timestamp_bedarf)
            else:
                differences_df = pd.DataFrame()

            if not differences_df.empty:
                # GAP-Diagramm
                title = f'Differenz: Ist (Profil {set_id_active_profile}) - Bedarf (Profil {set_bedarf_id})'
                fig = create_gap_analysis_chart(
                    differences_df,
                    title,
                    'Differenz (Ist - Bedarf)',
                    show_legend=False
                )

                if fig:
                    # Höhe für dieses Diagramm anpassen
                    fig.update_layout(height=500)
                    st.plotly_chart(fig, use_container_width=True)
                    st.markdown(get_gap_analysis_legend("bedarf"))

            else:
                st.warning("Keine Daten für die Differenzberechnung verfügbar.")