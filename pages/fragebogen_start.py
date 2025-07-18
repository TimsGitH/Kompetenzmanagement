import streamlit as st
import pandas as pd
from functions.menu import default_menu
from functions.user_management import create_profile
from functions.initialize import initialize_fragebogen
from config import GOOGLE_SHEET_PROFILES, COLUMN_PROFILE_ID
from functions.database import get_dataframe_from_gsheet

st.set_page_config(page_title="Fragebogen")

default_menu()

# -Profildaten einlesen-
data_profiles = get_dataframe_from_gsheet(GOOGLE_SHEET_PROFILES, index_col=COLUMN_PROFILE_ID)

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
            st.switch_page("pages/fragebogen_start_neu.py")
    else:
        st.write(f"Kein Profil mit der ID {set_id_active_profile} gefunden.")
        set_name_active_profile = st.text_input(label="Profil Name")
        confirm_new_profile = st.button(label="Profil anlegen")
        if confirm_new_profile and set_name_active_profile:
            create_profile(id=set_id_active_profile, name=set_name_active_profile) 
            st.cache_data.clear()           
            st.rerun(scope="app")
