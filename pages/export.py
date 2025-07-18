import streamlit as st
import pandas as pd
from functions.menu import default_menu
from functions.database import get_dataframe_from_gsheet
from config import GOOGLE_SHEET_ANSWERS, COLUMN_INDEX

st.set_page_config(page_title="Export")

default_menu()

st.title("Export")

def convert_for_download(df):
    return df.to_csv(sep=';')



# -Tabelle für Antworten verknüpfen-
answers = get_dataframe_from_gsheet(GOOGLE_SHEET_ANSWERS, index_col=COLUMN_INDEX, refresh_time_in_minutes=0)
answers_csv = convert_for_download(answers)

# -Download Buttons-
# st.download_button(label="Export Profildaten", data=data_profiles_csv, file_name="user_management/profiles.csv")
st.download_button(label="Export Antworten", data=answers_csv, file_name="antworten.csv")

