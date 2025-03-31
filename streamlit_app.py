import streamlit as st
from menu import default_menu

pg = st.navigation([
    st.Page("pages/visualisierung.py", default=True),
    st.Page("pages/user_management.py"),
    st.Page("pages/kompetenzbeurteilung.py"),
    st.Page("pages/admin.py"),
    st.Page("pages/debug.py"),
    st.Page("pages/fragebogen.py")
], position="hidden")

pg.run()

default_menu()

#with st.sidebar:
#    st.title("Fenster:")
#    if st.button("Visualisierung"):
#        st.switch_page(st.Page(visualisierung))
#    if st.button("User Management"):
#        st.switch_page(st.Page(user_management))
#    if st.button("Kompetenzbeurteilung"):
#        st.switch_page(st.Page("kompetenzbeurteilung.py"))
#    if st.button("Admin"):
#        st.switch_page(st.Page(admin))
#    if st.button("Debug"):
#        st.switch_page(st.Page(debug))
