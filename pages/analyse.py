import streamlit as st
import pandas as pd
import plotly.express as px
from functions.menu import default_menu
from functions.data import get_cluster_names, get_selected_cluster_values, get_latest_update_time, get_cluster_values_over_time, get_available_bedarfe_profiles, calculate_cluster_differences, create_gap_analysis_chart, get_gap_analysis_legend
from config import GOOGLE_SHEET_ANSWERS, COLUMN_TIMESTAMP, GOOGLE_SHEET_PROFILES, COLUMN_PROFILE_ID
from functions.database import get_dataframe_from_gsheet

# -Seitenkonfiguration-
st.set_page_config(page_title="Visualisierung", layout="wide")
default_menu()

# -Tabelle für Profile verknüpfen-
data_profiles = get_dataframe_from_gsheet(GOOGLE_SHEET_PROFILES, index_col=COLUMN_PROFILE_ID)
data_answers = get_dataframe_from_gsheet(GOOGLE_SHEET_ANSWERS, index_col=COLUMN_TIMESTAMP)


# -Profilauswahl (oben)-

st.title("Visualisierung")

set_name_active_profile = st.selectbox("Profil auswählen:", data_profiles[["Name"]])
set_id_active_profile = data_profiles.index[data_profiles["Name"] == set_name_active_profile][0]

filtered_update_time = data_answers.index[data_answers["Profil-ID"] == set_id_active_profile]
set_update_time_active_profile = st.selectbox("Zeitpunkt auswählen:", filtered_update_time)

with st.container():
    cols = st.columns(2)
    # -Netzdiagramm Kompetenzen-
    with cols[0]:
        with st.container(border=False):

            
            st.header("Kompetenzen")
            df_radar = dict(
                Wert=get_selected_cluster_values(set_id_active_profile, set_update_time_active_profile),
                Kategorie=get_cluster_names()
            )
            radar_chart = px.line_polar(df_radar, r="Wert", theta="Kategorie", range_r=[0,5], line_close=True)
            st.plotly_chart(figure_or_data=radar_chart)

    # -Profilentwicklung Diagramm-
    with cols[1]:
        with st.container(border=False):
            st.header("Profilentwicklung")
            set_category = st.selectbox("Kategorie:", get_cluster_names())
            
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
            
            # Verfügbare Bedarfe-Profile laden
            available_bedarfe_profiles = get_available_bedarfe_profiles()
            
            if available_bedarfe_profiles:
                # Dropdown für Bedarfe-Profil
                selected_bedarfe_profile = st.selectbox(
                    "Bedarfe-Profil auswählen:", 
                    available_bedarfe_profiles,
                    format_func=lambda x: f"Profil {x}"
                )
                
                # Differenzen berechnen mit modularer Funktion
                differences_df = calculate_cluster_differences(set_id_active_profile, selected_bedarfe_profile, set_update_time_active_profile)
                
                if not differences_df.empty:
                    # Diagramm mit modularer Funktion erstellen
                    title = f'Differenz: Ist (Profil {set_id_active_profile}) - Bedarf (Profil {selected_bedarfe_profile})'
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
            else:
                st.info("Keine Bedarfe-Daten verfügbar. Bitte stellen Sie sicher, dass die Bedarfe-Tabelle verfügbar ist.")
