import streamlit as st
import pandas as pd
from functions.menu import default_menu
from functions.user_management import create_mitarbeiter

st.set_page_config(page_title="Fragebogen")

default_menu()

# -Mitarbeiterdaten einlesen-
data_mitarbeiter = pd.read_csv("user_management/mitarbeiter.csv", sep=';', index_col=0)

# -Titel-
st.title("Fragebogen")

set_id_active_mitarbeiter = st.number_input(label="Mitarbeiter-ID (zwischen 101 und 999):", min_value=101, max_value=999, value=None)
st.button(label="Bestätigen")
if set_id_active_mitarbeiter is not None:
    set_id_active_mitarbeiter = int(set_id_active_mitarbeiter)
    if set_id_active_mitarbeiter in data_mitarbeiter.index:
        set_name_active_mitarbeiter = data_mitarbeiter.loc[set_id_active_mitarbeiter, "Name"]
        st.write(f"Mitarbeiter mit der ID {set_id_active_mitarbeiter}: {set_name_active_mitarbeiter}")
        begin_fragebogen = st.button(label="Fragebogen starten")
        if begin_fragebogen:
            st.session_state.id_active_mitarbeiter = set_id_active_mitarbeiter
            st.session_state.name_active_mitarbeiter = set_name_active_mitarbeiter
            st.switch_page("pages/fragebogen.py")
    else:
        st.write(f"Kein Mitarbeiter mit der ID {set_id_active_mitarbeiter} gefunden.")
        set_name_active_mitarbeiter = st.text_input(label="Mitarbeiter Name")
        confirm_new_mitarbeiter = st.button(label="Mitarbeiter anlegen")
        if confirm_new_mitarbeiter:
            create_mitarbeiter(id=set_id_active_mitarbeiter, name=set_name_active_mitarbeiter)
            st.rerun(scope="app")
