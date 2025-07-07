import streamlit as st
import pandas as pd

def create_profile(id, name):
    # Funktion zur Erstellung einer neuen Mitarbeiterin oder eines neuen Mitarbeiters.
    data_mitarbeiter = pd.read_csv("user_management/mitarbeiter.csv", sep=';', index_col=0)
    data_mitarbeiter.loc[id, "Name"] = name
    data_mitarbeiter.to_csv("user_management/mitarbeiter.csv", sep=';', index_label="Mitarbeiter-ID")
