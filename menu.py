import streamlit as st
import pandas as pd
import os

# -Button Funktionen-
def click_back_button_1():
    st.session_state.warning = True

def click_cancel_button():
    del st.session_state.warning

def delete_session_state():
    for key in st.session_state.keys():
        del st.session_state[key]

# -Leere Tabelle für Antworten erstellen, falls keine existiert-
def create_empty_answers_dataframe():
    answers_path = "antworten/Antworten.csv"
    if not os.path.exists(answers_path):
        column_names = ["Speicherzeitpunkt", "Mitarbeiter-ID"]
        answers = pd.DataFrame(columns=column_names)
        answers.to_csv(answers_path, index_label="Fragebogen-ID")

# -Menüs / Seitenleisten-
def debug_menu():
    for i in range(5):
        st.sidebar.write("\n")
    st.sidebar.header("Debug")
    st.sidebar.write("Session State:")
    st.sidebar.write(st.session_state)
    st.sidebar.button(label="Session State löschen", on_click=delete_session_state)
    st.sidebar.button(label="Leere Tabelle für Antworten erstellen", on_click=create_empty_answers_dataframe)
    st.sidebar.page_link("pages/visualisierung.py", label="Zurück zu Visualisierung")

def default_menu():
    st.set_option("client.showSidebarNavigation", False)
    st.sidebar.header("Navigation")
    st.sidebar.page_link("pages/visualisierung.py", label="Visualisierung")
    st.sidebar.page_link("pages/user_management.py", label="User Management")
    st.sidebar.page_link("pages/kompetenzbeurteilung.py", label="Kompetenzbeurteilung")
    st.sidebar.page_link("pages/admin.py", label="Admin")
    debug_menu()

def no_menu():
    st.set_option("client.showSidebarNavigation", False)
    if "warning" not in st.session_state:
        st.sidebar.button(label="Zurück", use_container_width=True, on_click=click_back_button_1)
    elif st.session_state.warning:
        st.sidebar.warning("Änderungen werden nicht gespeichert!")
        st.sidebar.button(label="Abbrechen", on_click=click_cancel_button)
        if st.sidebar.button(label="Trotzdem Zurück"):
            delete_session_state()
            st.switch_page("pages/kompetenzbeurteilung.py")
    else:
        st.sidebar.error("Error")
    debug_menu()
