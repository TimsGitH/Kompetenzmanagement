import streamlit as st
from functions import data

def initialize_fragebogen_start():
    # Funktion zum Initialisieren der Session States für den Fragebogen Start.
    if "page" not in st.session_state:
        st.session_state.page = 1

def initialize_fragebogen():
    # Funktion zum Initialisieren der Session States für den Fragebogen.
    if "page" not in st.session_state:
        st.session_state.page = 1
    
    # current_answers initialisieren falls nicht vorhanden
    if "current_answers" not in st.session_state:
        st.session_state.current_answers = {}
    
    # Nur Fragebogen-Antworten initialisieren, demographische Antworten beibehalten
    question_ids = data.get_question_ids()
    for frage_id in question_ids:
        if frage_id not in st.session_state.current_answers:
            st.session_state.current_answers[frage_id] = None
