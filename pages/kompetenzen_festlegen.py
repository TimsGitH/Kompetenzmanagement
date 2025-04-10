import streamlit as st
import pandas as pd
from menu import no_menu

st.set_page_config(page_title="Kompetenzen festlegen")

no_menu()

st.title("Kompetenzen festlegen")

level_kompetenzen= (0, 1, 2, 3, 4)

antworten = st.select_slider(label="Kompetenz 1", options=level_kompetenzen)
st.radio(label="Kompetenz 2", options=level_kompetenzen, horizontal=True)
