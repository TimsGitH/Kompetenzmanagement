import streamlit as st
from functions.menu import default_menu

st.set_page_config(page_title="Fragebogen")

default_menu()

st.title("Vielen Dank für Ihre Teilnahme!")

st.markdown("""
Herzlichen Dank, dass Sie den Fragebogen ausgefüllt haben.

Ihre Antworten wurden erfolgreich übermittelt.
""")
