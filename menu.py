import streamlit as st
from initialize import create_empty_answers_dataframe
from session_state import clear_session_states, clear_session_states_except_role_and_debug_mode

# -Button Funktionen-
def click_back_button_1():
    st.session_state.warning = True

def click_cancel_button():
    del st.session_state.warning

# -Menüs / Seitenleisten-
def debug_menu():
    if st.session_state.debug_mode:
        for i in range(5):
            st.sidebar.write("\n")
        st.sidebar.header("Debug")
        st.sidebar.write("Session State:")
        st.sidebar.write(st.session_state)
        st.sidebar.button(label="Session State löschen (Außer Rolle & Debug Modus)", on_click=clear_session_states_except_role_and_debug_mode)
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
    if st.session_state.role == "Admin":
        if "warning" not in st.session_state:
            st.sidebar.button(label="Zurück", use_container_width=True, on_click=click_back_button_1)
        elif st.session_state.warning:
            st.sidebar.warning("Änderungen werden nicht gespeichert!")
            st.sidebar.button(label="Abbrechen", on_click=click_cancel_button)
            if st.sidebar.button(label="Trotzdem Zurück"):
                clear_session_states_except_role_and_debug_mode()
                st.switch_page("pages/kompetenzbeurteilung.py")
        else:
            st.sidebar.error("Error")
    debug_menu()
