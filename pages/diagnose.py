import streamlit as st
import pandas as pd
import plotly.express as px
from functions.menu import default_menu
from config import GOOGLE_SHEET_PROFILES, COLUMN_PROFILE_ID
from functions.database import get_dataframe_from_gsheet

# -Seitenkonfiguration-
st.set_page_config(page_title="Diagnose", layout="wide")
default_menu()

st.title("Diagnose")

# -Tabelle für Profile verknüpfen-
data_profiles = get_dataframe_from_gsheet(GOOGLE_SHEET_PROFILES, index_col=COLUMN_PROFILE_ID)

set_name_active_profile = st.selectbox("Profil auswählen:", data_profiles[["Name"]])
set_id_active_profile = data_profiles.index[data_profiles["Name"] == set_name_active_profile][0]
