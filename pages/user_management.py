import streamlit as st
import pandas as pd
from menu import default_menu

st.set_page_config(page_title="User Management")

default_menu()

# -Tabelle für Mitarbeiter verknüpfen-
data_mitarbeiter = pd.read_csv("user_management/mitarbeiter.csv", sep=';', index_col=0)

# -Tabelle für Antworten verknüpfen-
answers = pd.read_csv("antworten/antworten.csv", sep=';', index_col=0)

st.title("User Management")

st.write("Vorhandene Nutzer:")
st.write(data_mitarbeiter)

st.write("Ausgefüllte Fragebögen:")
st.write(answers)