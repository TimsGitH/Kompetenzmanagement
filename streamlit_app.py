import streamlit as st
import pandas as pd
from initialize import create_empty_answers_dataframe

st.set_option("client.showSidebarNavigation", False)

# -Leere Tabelle für Antworten erstellen, falls keine existiert-
create_empty_answers_dataframe()

# -Rolle ausgewählt-
def confirm():
    st.session_state.role = st.session_state.selected_role

# -Titel-
st.title("Kompetenzmanagment")
st.selectbox(label="Bitte wählen Sie ihre Rolle aus:", options=["Mitarbeiter", "Admin"], index=None, key="selected_role", placeholder="Rolle")
st.checkbox(label="Debug Modus", key="selected_debug_mode")
confirm_button = st.button(label="Bestätigen & Weiter")
if confirm_button:
    st.session_state.role = st.session_state.selected_role
    st.session_state.debug_mode = st.session_state.selected_debug_mode
    if st.session_state.role == "Mitarbeiter":
        st.switch_page("pages/fragebogen_start.py")
    else:
        st.switch_page("pages/visualisierung.py")
