import streamlit as st
import pandas as pd
from functions.menu import default_menu
from functions.user_management import create_profile

st.set_page_config(page_title="User Management")

default_menu()

# -Submenus-
def submenu_data():
    st.write("Vorhandene Profile:")
    st.write(data_profiles)

    st.write("Ausgefüllte Fragebögen:")
    st.write(answers)

def submenu_add():
    set_id_active_profile = st.number_input(label="Profil-ID (zwischen 101 und 999):", min_value=101, max_value=999, value=None)
    if set_id_active_profile is not None and set_id_active_profile in data_profiles.index:
        name = data_profiles.loc[set_id_active_profile, "Name"]
        st.warning(f"ID bereits vergeben. Profil mit der ID {set_id_active_profile}: {name}.")
        id_taken = True
    else:
        id_taken = False
    set_name_active_profile = st.text_input(label="Profil Name")
    confirm_new_profile = st.button(label="Profil anlegen", disabled=id_taken)
    if confirm_new_profile and set_id_active_profile not in data_profiles.index:
        create_profile(id=set_id_active_profile, name=set_name_active_profile)
        st.rerun(scope="app")

def submenu_edit():
    pass

# -Tabelle für Profile verknüpfen-
data_profiles = pd.read_csv("user_management/profiles.csv", sep=';', index_col=0)

# -Tabelle für Antworten verknüpfen-
answers = pd.read_csv("antworten/antworten.csv", sep=';', index_col=0)

# -Seiteninhalt-
st.title("User Management")

submenu_options = ["Daten", "Hinzufügen", "Bearbeiten"]

submenu_functions = {
    "Daten": submenu_data,
    "Hinzufügen": submenu_add,
    "Bearbeiten": submenu_edit
}

selected_submenu = st.segmented_control(label="submenu", options=submenu_options, default=submenu_options[0], label_visibility="collapsed")

submenu_functions[selected_submenu]()
