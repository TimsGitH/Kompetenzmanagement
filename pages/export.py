import streamlit as st
import pandas as pd
from menu import default_menu

st.set_page_config(page_title="Export")

default_menu()

st.title("Export")

# -Funktion zum Konvertieren der Datei-
@st.cache_data
def convert_for_download(df):
    return df.to_csv(sep=';')

# -Tabelle für Mitarbeiter verknüpfen-
data_mitarbeiter = pd.read_csv("user_management/mitarbeiter.csv", sep=';', index_col=0)
data_mitarbeiter_csv = convert_for_download(data_mitarbeiter)

# -Tabelle für Antworten verknüpfen-
answers = pd.read_csv("antworten/antworten.csv", sep=';', index_col=0)
answers_csv = convert_for_download(answers)

# -Download Buttons-
st.download_button(label="Export Mitarbeiterdaten", data=data_mitarbeiter_csv, file_name="user_management/mitarbeiter.csv")
st.download_button(label="Export Antworten", data=answers_csv, file_name="antworten/antworten.csv")