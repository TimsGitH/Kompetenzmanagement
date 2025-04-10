import streamlit as st

# -Button Funktionen-
def click_back_button_1():
    st.session_state.warning = True

def click_cancel_button():
    del st.session_state.warning

# -Menüs / Seitenleisten-
def debug_menu():
    st.sidebar.header("Debug")
    st.sidebar.write("Session State:")
    st.sidebar.write(st.session_state)
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
            for key in st.session_state.keys():
                del st.session_state[key]
            st.switch_page("pages/kompetenzbeurteilung.py")
    else:
        st.sidebar.error("Error")
    debug_menu()
