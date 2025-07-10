import streamlit as st
import pandas as pd
import plotly.express as px
from functions.menu import default_menu


# -Seitenkonfiguration-
st.set_page_config(page_title="Diagnose", layout="wide")
default_menu()

st.title("Diagnose")

# -Tabelle für Profile verknüpfen-
data_profiles = pd.read_csv("user_management/profiles.csv", sep=';', index_col=0)

set_name_active_profile = st.selectbox("Profil auswählen:", data_profiles[["Name"]])
set_id_active_profile = data_profiles.index[data_profiles["Name"] == set_name_active_profile][0]
