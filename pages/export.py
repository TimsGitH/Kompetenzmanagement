import streamlit as st
import pandas as pd
from functions.menu import default_menu

st.set_page_config(page_title="Export")

default_menu()

st.title("Export")

# -Funktion zum Konvertieren der Datei-
@st.cache_data
def convert_for_download(df):
    return df.to_csv(sep=';')

# -Tabelle für Profile verknüpfen-
data_profiles = pd.read_csv("user_management/profiles.csv", sep=';', index_col=0)
data_profiles_csv = convert_for_download(data_profiles)

# -Tabelle für Antworten verknüpfen-
answers = pd.read_csv("antworten/antworten.csv", sep=';', index_col=0)
answers_csv = convert_for_download(answers)

# -Download Buttons-
st.download_button(label="Export Profildaten", data=data_profiles_csv, file_name="user_management/profiles.csv")
st.download_button(label="Export Antworten", data=answers_csv, file_name="antworten/antworten.csv")