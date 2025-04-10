import streamlit as st

def default_menu():
    st.set_option("client.showSidebarNavigation", False)
    st.sidebar.page_link("pages/visualisierung.py", label="Visualisierung")
    st.sidebar.page_link("pages/user_management.py", label="User Management")
    st.sidebar.page_link("pages/kompetenzbeurteilung.py", label="Kompetenzbeurteilung")
    st.sidebar.page_link("pages/admin.py", label="Admin")

def no_menu():
    st.sidebar.page_link("pages/visualisierung.py", label="Debug: Zurück")
    if "warning" in st.session_state:
        st.write(st.session_state.warning)
    else:
        st.write("Leer")
    st.set_option("client.showSidebarNavigation", False)
    if "warning" not in st.session_state:
        st.session_state.warning = False
    if not st.session_state.warning:
        back_button = st.sidebar.button(label="Zurück", use_container_width=True)
        if back_button:
            st.session_state.warning = True
    elif st.session_state.warning:
        st.sidebar.warning("Änderungen werden nicht gespeichert!")
        cancel_button = st.sidebar.button("Abbrechen")
        back_button_2 = st.sidebar.button("Trotzdem Zurück")
        if cancel_button:
            st.session_state.warning = False
        elif back_button_2:
            st.session_state.warning = False
            st.switch_page("pages/kompetenzbeurteilung.py")
    else:
        st.sidebar.error("Error")
