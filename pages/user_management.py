import streamlit as st
import pandas as pd
from functions.menu import default_menu
from functions.user_management import create_profile

st.set_page_config(page_title="User Management")

default_menu()

# -Submenus-
def submenu_data():
    st.write("Vorhandene Mitarbeiterinnen und Mitarbeiter:")
    st.write(data_mitarbeiter)

    st.write("Ausgefüllte Fragebögen:")
    st.write(answers)

def submenu_add():
    set_id_active_mitarbeiter = st.number_input(label="Mitarbeiter-ID (zwischen 101 und 999):", min_value=101, max_value=999, value=None)
    if set_id_active_mitarbeiter is not None and set_id_active_mitarbeiter in data_mitarbeiter.index:
        name = data_mitarbeiter.loc[set_id_active_mitarbeiter, "Name"]
        st.warning(f"ID bereits vergeben. Mitarbeiter mit der ID {set_id_active_mitarbeiter}: {name}.")
        id_taken = True
    else:
        id_taken = False
    set_name_active_mitarbeiter = st.text_input(label="Mitarbeiter Name")
    confirm_new_mitarbeiter = st.button(label="Mitarbeiter anlegen", disabled=id_taken)
    if confirm_new_mitarbeiter and set_id_active_mitarbeiter not in data_mitarbeiter.index:
        create_profile(id=set_id_active_mitarbeiter, name=set_name_active_mitarbeiter)
        st.rerun(scope="app")

def submenu_edit():
    pass

# -Tabelle für Mitarbeiter verknüpfen-
data_mitarbeiter = pd.read_csv("user_management/mitarbeiter.csv", sep=';', index_col=0)

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
