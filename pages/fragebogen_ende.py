import streamlit as st
from functions.menu import default_menu
from functions.session_state import clear_session_states_except_mode_and_debug_mode

st.set_page_config(page_title="Fragebogen")

default_menu()

st.title("Vielen Dank für Ihre Teilnahme!")

st.markdown("""
Herzlichen Dank, dass Sie den Fragebogen ausgefüllt haben.

Ihre Antworten wurden erfolgreich übermittelt.
""")

end_button = st.button("Fragebogen beenden", on_click=clear_session_states_except_mode_and_debug_mode)
if end_button:
    st.switch_page("pages/fragebogen_start.py")