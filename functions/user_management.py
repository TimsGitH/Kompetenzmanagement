import streamlit as st
import pandas as pd

def create_profile(id, name):
    # Funktion zur Erstellung eines neuen Profils.
    data_profiles = pd.read_csv("user_management/profiles.csv", sep=';', index_col=0)
    data_profiles.loc[id, "Name"] = name
    data_profiles.to_csv("user_management/profiles.csv", sep=';', index_label="Profil-ID")
