import streamlit as st
import pandas as pd
from config import PATH_PROFILES

def create_profile(id, name):
    # Funktion zur Erstellung eines neuen Profils.
    data_profiles = pd.read_csv(PATH_PROFILES, sep=';', index_col=0)
    data_profiles.loc[id, "Name"] = name
    data_profiles.to_csv(PATH_PROFILES, sep=';', index_label="Profil-ID")
