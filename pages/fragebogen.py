import streamlit as st
import pandas as pd

st.title("Fragebogen")
st.write("Seite 1/X")
options_umfrage= ("sehr schlecht", "eher schlecht", "neutral", "eher gut", "sehr gut")

antworten = st.select_slider(label="Wie finden Sie Grünkohl?", options=options_umfrage)
st.radio(label="Wie steht es um Ihre Intelligenz?", options=options_umfrage, index=2, horizontal=True)
