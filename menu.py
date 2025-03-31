import streamlit as st

def default_menu():
    st.sidebar.page_link("pages/visualisierung.py", label="Visualisierung"),
    st.sidebar.page_link("pages/user_management.py", label="User Management"),
    st.sidebar.page_link("pages/kompetenzbeurteilung.py", label="Kompetenzbeurteilung")
    st.sidebar.page_link("pages/admin.py", label="Admin"),
    st.sidebar.page_link("pages/debug.py", label="Debug")

def menu_mit_fragebogen():
    st.sidebar.page_link("pages/fragebogen.py", label="Fragebogen")