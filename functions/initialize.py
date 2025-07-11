import streamlit as st
import pandas as pd
import os
from functions import data
from config import PATH_ANSWERS

def create_empty_answers_dataframe():
    # Leere Tabelle für Antworten erstellen, falls keine existiert
    if not os.path.exists(PATH_ANSWERS):
        column_names = ["Speicherzeitpunkt", "Profil-ID"]
        answers = pd.DataFrame(columns=column_names)
        answers.to_csv(PATH_ANSWERS, sep=';', index_label="Antwort-ID")

def initialize_fragebogen():
    # Funktion zum Initialisieren der Session States für den Fragebogen.
    if "page" not in st.session_state:
        st.session_state.page = 1
    if "current_answers" not in st.session_state:
        st.session_state.current_answers = {frage_id: None for frage_id in data.get_question_ids()}
