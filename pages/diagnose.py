import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from functions.menu import default_menu
from config import GOOGLE_SHEET_PROFILES, COLUMN_PROFILE_ID, GOOGLE_SHEET_ANSWERS, COLUMN_TIMESTAMP
from functions.database import get_dataframe_from_gsheet
from functions.data import get_cluster_names, get_selected_cluster_values, calculate_time_differences, create_gap_analysis_chart, get_gap_analysis_legend

# -Seitenkonfiguration-
st.set_page_config(page_title="Diagnose", layout="wide")
default_menu()

st.title("Diagnose")

# Daten laden
data_profiles = get_dataframe_from_gsheet(GOOGLE_SHEET_PROFILES, index_col=COLUMN_PROFILE_ID)
data_answers = get_dataframe_from_gsheet(GOOGLE_SHEET_ANSWERS, index_col=COLUMN_TIMESTAMP)

# Profil auswählen
set_name_active_profile = st.selectbox("Profil auswählen:", data_profiles[["Name"]])
set_id_active_profile = data_profiles.index[data_profiles["Name"] == set_name_active_profile][0]

# Zeitpunkt auswählen
filtered_update_time = data_answers.index[data_answers["Profil-ID"] == set_id_active_profile]
set_first_timestamp_active_profile = st.selectbox("Ersten Zeitpunkt auswählen:", filtered_update_time)
set_second_timestamp_active_profile = st.selectbox("Zweiten Zeitpunkt auswählen:", filtered_update_time[-1])

# Platzhalter-Daten für die Diagramme
placeholder_data = pd.DataFrame({
    'Kategorie': ['A', 'B', 'C', 'D'],
    'Wert': [25, 30, 20, 25]
})

# Erste Zeile mit zwei Diagrammen
col1, col2 = st.columns(2)

with col1:
    st.subheader("IST Entwicklung")
    
    # Differenzen berechnen mit modularer Funktion
    differences_df = calculate_time_differences(
        set_id_active_profile, 
        set_first_timestamp_active_profile, 
        set_second_timestamp_active_profile
    )
    
    if not differences_df.empty:
        # Diagramm mit modularer Funktion erstellen
        title = f'Entwicklung: {set_second_timestamp_active_profile} - {set_first_timestamp_active_profile}'
        fig = create_gap_analysis_chart(
            differences_df, 
            title, 
            'Differenz (Später - Früher)'
        )
        
        if fig:
            st.plotly_chart(fig, use_container_width=True)
            st.markdown(get_gap_analysis_legend("zeitvergleich"))
    else:
        st.warning("Keine Werte für die ausgewählten Zeitpunkte verfügbar.")

with col2:
    st.subheader("Diagramm 2")
    fig2 = px.pie(placeholder_data, values='Wert', names='Kategorie', title="Platzhalter Diagramm 2")
    st.plotly_chart(fig2, use_container_width=True)

# Zweite Zeile mit zwei Diagrammen
col3, col4 = st.columns(2)

with col3:
    st.subheader("Diagramm 3")
    fig3 = px.line(placeholder_data, x='Kategorie', y='Wert', title="Platzhalter Diagramm 3")
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.subheader("Diagramm 4")
    fig4 = px.scatter(placeholder_data, x='Kategorie', y='Wert', title="Platzhalter Diagramm 4")
    st.plotly_chart(fig4, use_container_width=True)










