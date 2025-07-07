import streamlit as st
import pandas as pd
import datetime as dt
import pytz
from config import AMOUNT_QUESTIONS_PER_PAGE, OPTIONS_FORM, TRANSLATE_ANSWER_SAVE, TRANSLATE_ANSWER_INDEX
from functions.menu import no_menu
from functions.data import get_amount_questions, get_question_ids
from functions.session_state import clear_session_states_except_mode_and_debug_mode

st.set_page_config(page_title="Fragebogen")

no_menu()

# -Profildaten einlesen-
data_profiles = pd.read_csv("user_management/profiles.csv", sep=';', index_col=0)

# -Fragebogen einlesen-
fragebogen = pd.read_csv("fragebögen/2025-06-25_Finalversion_Fragebogen_pro-kom_aufbereitet_UTF-8.csv", sep=';', encoding='utf-8')

# -Funktionen-
def check_none_answers():
    none_counter = 0
    for question_id in question_ids_current_page:
        if st.session_state[f"answer_{question_id}"] is None:
            none_counter += 1
            question_text = fragebogen.loc[fragebogen["Frage-ID"] == current_question_id, "Frage"].values[0]
            st.write(f"Frage {question_id} ({question_text}) wurde nicht beantwortet.")
    if none_counter == 0:
        if "none_error" in st.session_state:
            del st.session_state.none_error
        return False
    else:
        if "none_error" not in st.session_state:
            st.session_state.none_error = True
        st.write(f"Es fehlen {none_counter} Antworten.")
        return True

def update_answers():
    for current_question_id in question_ids_current_page:
        st.session_state.current_answers[current_question_id] = st.session_state[f"answer_{current_question_id}"]
        del st.session_state[f"answer_{current_question_id}"]

def click_continue():
    if not check_none_answers():
        update_answers()
        st.session_state.page += 1

def click_back():
    if "none_error" in st.session_state:
        del st.session_state.none_error
    update_answers()
    st.session_state.page -= 1

def submit_form():
    # Tabelle für Antworten verknüpfen
    answers = pd.read_csv("antworten/antworten.csv", sep=';', index_col=0)
    # Tabelle initialisieren
    questionnaire_id = answers.shape[0]
    timezone = pytz.timezone('Europe/Berlin')
    timestamp = dt.datetime.now(timezone)
    formatted_timestamp = timestamp.strftime('%Y-%m-%d %H:%M')
    data_new_answers = {
        "Speicherzeitpunkt": [formatted_timestamp],
        "Profil-ID": [st.session_state.id_active_profile]
    }
    # Antworten aus current_answers übernehmen
    for frage_id, antwort in st.session_state.current_answers.items():
        data_new_answers[frage_id] = [int(TRANSLATE_ANSWER_SAVE[antwort])]
    new_answers = pd.DataFrame(data_new_answers)
    new_answers.index = [questionnaire_id]
    # Tabellen kombinieren und Antworten als int speichern
    combined_answers = pd.concat([answers, new_answers], axis=0)
    #for question_id in question_ids:
    #    if question_id in combined_answers.columns:
    #        combined_answers[question_id] = combined_answers[question_id].astype(int)
    combined_answers.to_csv("antworten/antworten.csv", sep=';', index_label="Antwort-ID")
    # Session States aufräumen
    clear_session_states_except_mode_and_debug_mode()


# -Werte und Listen laden-
amount_questions = get_amount_questions()
question_ids = get_question_ids()

# -Titel-
st.title("Fragebogen")
st.write(f"Profil: {st.session_state.name_active_profile}")
st.write(f"Profil-ID: {st.session_state.id_active_profile}")
st.write(f"Anzahl Fragen: {amount_questions}")

# -Anzahl der Seiten berechnen-
if amount_questions == 0:
    st.write("Es wurde kein Fragebogen hinterlegt.")
else:
    amount_pages = - ( - amount_questions // AMOUNT_QUESTIONS_PER_PAGE) # Aufgerundete, ganzzahlige Division
    st.write(f"Anzahl Seiten des Fragebogens: {amount_pages}")

# -Forschrittsanzeigen-
if 'page' not in st.session_state:
    st.session_state.page = 1
st.progress((st.session_state.page - 1) / amount_pages, text="Fortschritt Fragebogen")

# -Fragebogen-
with st.form("Fragebogen"):
    if st.session_state.page < amount_pages:
        amount_questions_in_page = AMOUNT_QUESTIONS_PER_PAGE
    else:
        amount_questions_in_page = amount_questions - ((st.session_state.page - 1) * AMOUNT_QUESTIONS_PER_PAGE)
    st.header("Formular")
    st.write(f"Anzahl Fragen auf dieser Seite: {amount_questions_in_page}")
    question_ids_current_page = question_ids[(st.session_state.page - 1) * AMOUNT_QUESTIONS_PER_PAGE: ((st.session_state.page - 1) * AMOUNT_QUESTIONS_PER_PAGE) + amount_questions_in_page]
    for current_question_id in question_ids_current_page:
        st.markdown("")
        current_question_text = fragebogen.loc[fragebogen["Frage-ID"] == current_question_id, "Frage"].values[0]
        st.markdown(body = current_question_text)
        current_answer = st.session_state.current_answers[current_question_id]
        radio_button = st.radio(label="", options=OPTIONS_FORM, index=TRANSLATE_ANSWER_INDEX[current_answer], key=f"answer_{current_question_id}", horizontal=True, label_visibility="collapsed")
    st.write(f"Seite {st.session_state.page} von {amount_pages}")
    left, right = st.columns(2)
    if st.session_state.page < amount_pages:
        continue_button = right.form_submit_button(label="Weiter", on_click=click_continue)
    else:
        submit_button = right.form_submit_button(label="Fragebogen abschließen")
        if submit_button:
            if not check_none_answers():
                update_answers()
                submit_form()
                if st.session_state.mode == "analyse":
                    st.switch_page("pages/kompetenzbeurteilung.py")
                elif st.session_state.mode == "fragebogen":
                    st.switch_page("pages/fragebogen_start.py")
                else:
                    raise Exception("session_state.mode not valid")
    if st.session_state.page > 1:
        back_button = left.form_submit_button(label="Zurück", on_click=click_back)
    if "none_error" in st.session_state and st.session_state.none_error:
        st.warning("Bitte beantworten Sie alle Fragen.")
