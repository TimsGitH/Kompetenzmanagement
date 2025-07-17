import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from functions.menu import default_menu
from functions.data import get_cluster_names, get_latest_cluster_values, get_selected_cluster_values, get_latest_update_time, get_cluster_values_over_time, get_available_bedarfe_profiles, calculate_cluster_differences
from config import PATH_PROFILES, PATH_ANSWERS

# -Seitenkonfiguration-
st.set_page_config(page_title="Visualisierung", layout="wide")
default_menu()

# -Tabelle für Profile verknüpfen-
data_profiles = pd.read_csv(PATH_PROFILES, sep=';', index_col=0)
data_answers = pd.read_csv(PATH_ANSWERS, sep=';', index_col=1)

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
                
                # Y-Achse auf 1-5 begrenzen
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

    # -Analysehilfe-
    with cols[1]:
        with st.container(border=False):
            st.header("Analysehilfe")
            
            # Verfügbare Bedarfe-Profile laden
            available_bedarfe_profiles = get_available_bedarfe_profiles()
            
            if available_bedarfe_profiles:
                # Dropdown für Bedarfe-Profil
                selected_bedarfe_profile = st.selectbox(
                    "Bedarfe-Profil auswählen:", 
                    available_bedarfe_profiles,
                    format_func=lambda x: f"Profil {x}"
                )
                
                # Differenzen berechnen
                differences_df = calculate_cluster_differences(set_id_active_profile, selected_bedarfe_profile, set_update_time_active_profile)
                
                if not differences_df.empty:
                    # Farben für positive/negative Abweichungen
                    colors = ['red' if x < 0 else 'green' for x in differences_df['Differenz']]
                    
                    # Horizontales Barchart erstellen
                    fig = go.Figure()
                    
                    # Balken hinzufügen
                    fig.add_trace(go.Bar(
                        y=differences_df['Cluster'],
                        x=differences_df['Differenz'],
                        orientation='h',
                        marker_color=colors,
                        text=[f'{x:.1f}' for x in differences_df['Differenz']],
                        textposition='auto',
                        textangle=0,
                        name='Differenz'
                    ))
                    
                    # Layout anpassen
                    fig.update_layout(
                        title=f'Differenz: Ist (Profil {set_id_active_profile}) - Bedarf (Profil {selected_bedarfe_profile})',
                        xaxis_title='Differenz (Ist - Bedarf)',
                        yaxis_title='Cluster',
                        xaxis=dict(
                            zeroline=True,
                            zerolinecolor='black',
                            zerolinewidth=2,
                            range=[differences_df['Differenz'].min() - 0.5, differences_df['Differenz'].max() + 0.5]
                        ),
                        yaxis=dict(
                            autorange='reversed'  # Größte negative Abweichung oben
                        ),
                        height=500,
                        showlegend=False
                    )
                    
                    # Hinzufügen einer vertikalen Linie bei 0
                    fig.add_vline(x=0, line_width=2, line_color="black", line_dash="solid")
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Legende
                    st.markdown("""
                    **Legende:**
                    - 🔴 **Rot**: Negative Abweichung (Ist < Bedarf) - Verbesserungspotential
                    - 🟢 **Grün**: Positive Abweichung (Ist > Bedarf) - Stärke
                    """)
                    
                else:
                    st.warning("Keine Daten für die Differenzberechnung verfügbar.")
            else:
                st.info("Keine Bedarfe-Daten verfügbar. Bitte stellen Sie sicher, dass die Bedarfe-Tabelle verfügbar ist.")
