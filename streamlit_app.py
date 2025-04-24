import streamlit as st
import pandas as pd#
import os

st.set_option("client.showSidebarNavigation", False)

# -Leere Tabelle für Antworten erstellen, falls keine existiert-
answers_path = "antworten/Antworten.csv"
if os.path.exists(answers_path):
    answers = pd.read_csv("antworten/Antworten.csv")
    new_index = answers.idmax() + 1
else:
    answers = pd.DataFrame()
    new_index = 0

st.switch_page("pages/visualisierung.py")