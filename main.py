import streamlit as st
import pandas as pd

from menu import default_menu

data_mitarbeiter = pd.read_csv("user_management/mitarbeiter.csv", index_col=0)

pg = st.navigation([
    st.Page("pages/visualisierung.py", title="Visualisierung", default=True),
    st.Page("pages/user_management.py", title="User Management"),
    st.Page("pages/kompetenzbeurteilung.py", title="Kompetenzbeurteilung"),
    st.Page("pages/admin.py", title="Admin"),
    st.Page("pages/debug.py", title="Debug"),
    st.Page("pages/fragebogen.py", title="Fragebogen"),
    st.Page("pages/kompetenzen_festlegen.py", title="Kompetenzen festlegen")
], position="hidden")

pg.run()

default_menu()
