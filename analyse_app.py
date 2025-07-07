import streamlit as st
from functions.initialize import create_empty_answers_dataframe

st.session_state.mode = "analyse"
st.session_state.debug_mode = True

# -Leere Tabelle für Antworten erstellen, falls keine existiert-
create_empty_answers_dataframe()

# -Startseite öffnen-
st.switch_page("pages/visualisierung.py")
