import streamlit as st
import pandas as pd

st.set_option("client.showSidebarNavigation", False)

#from menu import default_menu

#data_mitarbeiter = pd.read_csv("user_management/mitarbeiter.csv", index_col=0)

# -Page Setup-
#visualisierung_page = st.Page(
#    page="pages/visualisierung.py", 
#    title="Visualisierung", 
#    default=True
#)
#user_management_page = st.Page(
#    "pages/user_management.py", 
#    title="User Management"
#)

# -Navigation Setup-
#pg = st.navigation([
#    visualisierung_page,
#    st.Page("pages/user_management.py", title="User Management"),
#    st.Page("pages/kompetenzbeurteilung.py", title="Kompetenzbeurteilung"),
#    st.Page("pages/admin.py", title="Admin"),
#    st.Page("pages/debug.py", title="Debug"),
#    st.Page("pages/fragebogen.py", title="Fragebogen"),
#    st.Page("pages/kompetenzen_festlegen.py", title="Kompetenzen festlegen")
#], position="hidden")

# -Run Navigation-
#pg.run()

st.switch_page("pages/visualisierung.py")