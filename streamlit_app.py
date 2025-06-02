import streamlit as st
from functions.initialize import create_empty_answers_dataframe
from functions.session_state import clear_session_states_except_role_and_debug_mode
from functions.menu import debug_menu

debug_menu()

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
    if st.session_state.selected_role == "Mitarbeiter":
        st.session_state.role = st.session_state.selected_role
        st.session_state.debug_mode = st.session_state.selected_debug_mode
        clear_session_states_except_role_and_debug_mode()
        st.switch_page("pages/fragebogen_start.py")
    elif st.session_state.selected_role == "Admin":
        st.session_state.role = st.session_state.selected_role
        st.session_state.debug_mode = st.session_state.selected_debug_mode
        clear_session_states_except_role_and_debug_mode()
        st.switch_page("pages/visualisierung.py")
    else:
        st.warning("Bitte wählen Sie eine Rolle aus")
