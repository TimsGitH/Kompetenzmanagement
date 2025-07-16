import streamlit as st
import pandas as pd
from functions.menu import no_menu
from functions.user_management import create_profile
from functions.initialize import initialize_fragebogen

st.set_page_config(page_title="Fragebogen")

no_menu()

# -Profildaten einlesen-
data_profiles = pd.read_csv("user_management/profiles.csv", sep=';', index_col=0)

# -Titel-
st.title("Fragebogen")

set_id_active_profile = st.number_input(label="Profil-ID (zwischen 101 und 999):", min_value=101, max_value=999, value=None)
st.button(label="Bestätigen")
if set_id_active_profile is not None:
    set_id_active_profile = int(set_id_active_profile)
    if set_id_active_profile in data_profiles.index:
        set_name_active_profile = data_profiles.loc[set_id_active_profile, "Name"]
        st.write(f"Profil mit der ID {set_id_active_profile}: {set_name_active_profile}")
        begin_fragebogen = st.button(label="Fragebogen starten")
        if begin_fragebogen:
            st.session_state.id_active_profile = set_id_active_profile
            st.session_state.name_active_profile = set_name_active_profile
            initialize_fragebogen()
            st.switch_page("pages/fragebogen.py")
    else:
        st.write(f"Kein Profil mit der ID {set_id_active_profile} gefunden.")
        set_name_active_profile = st.text_input(label="Profil Name")
        confirm_new_profile = st.button(label="Profil anlegen")
        if confirm_new_profile and set_name_active_profile:
            create_profile(id=set_id_active_profile, name=set_name_active_profile)
            st.rerun(scope="app")
