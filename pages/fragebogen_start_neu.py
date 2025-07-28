import streamlit as st
import pandas as pd
import datetime as dt
import pytz
from config import INTRODUCTION_TEXT, CONSENT_TEXT, DEMOGRAPHY_TEXT, OPTIONS_INDUSTRY, INTRODUCTION_QUERRY, ADDITIONAL_INFORMATION_IDS
from functions.menu import no_menu
from functions.data import get_amount_questions, get_question_ids
from functions.session_state import clear_session_states_except_mode_and_debug_mode
from functions.database import get_dataframe_from_gsheet, update_dataframe_to_gsheet

st.set_page_config(page_title="Fragebogen")

no_menu()

# Funktion zum Initialisieren der Session States für den Fragebogen Start.
# TODO: Löschen, wenn nicht mehr benötigt
if "page_einleitung" not in st.session_state:
    st.session_state.page_einleitung = 1

# -Funktionen-
def check_errors():
    if check_no_consent():
        return True
    # Prüfe, ob wir auf Seite 3 (Demographie) sind
    if st.session_state.get("page_einleitung") == 3:
        fehlende = check_demography_complete()
        if fehlende:
            st.session_state.none_error = True
            st.session_state.fehlende_felder = fehlende
            return True
        else:
            if "fehlende_felder" in st.session_state:
                del st.session_state.fehlende_felder
    return False

def check_no_consent():
    if "answer_consent" in st.session_state and not st.session_state.answer_consent:
        st.session_state.consent_error = True
        return True
    else:
        return False

def update_answers():
    """
    Zusätzliche Informationen in Session State speichern
    """
    # Demographische Antworten in current_answers speichern
    demographic_answers = {
        id: st.session_state.get(f"answer_{id}") # entspricht den Keys der Fragen
        for id in ADDITIONAL_INFORMATION_IDS
    }
    
    # current_answers initialisieren falls nicht vorhanden
    if "current_answers" not in st.session_state:
        st.session_state.current_answers = {}
    
    # Demographische Antworten hinzufügen
    for key, value in demographic_answers.items():
        if value is not None:
            st.session_state.current_answers[key] = value

def delete_errors():
    if "none_error" in st.session_state:
        del st.session_state.none_error
    if "consent_error" in st.session_state:
        del st.session_state.consent_error
    if "answer_consent" in st.session_state:
        del st.session_state.answer_consent

def click_continue():
    if not check_errors():
        delete_errors()
        update_answers()
        st.session_state.page_einleitung += 1

def click_back():
    delete_errors()
    update_answers()
    st.session_state.page_einleitung -= 1

def check_demography_complete():
    fehlende_felder = []
    branche = st.session_state.get("answer_0SD01")
    branche_sonstige = st.session_state.get("answer_0SD01B", "")
    if branche is None:
        fehlende_felder.append("Branche")
    if branche == "Sonstige":
        if branche_sonstige is None or str(branche_sonstige).strip() == "":
            fehlende_felder.append("Branche (Wenn Sonstige)")
    else:
        if branche_sonstige is not None and str(branche_sonstige).strip() != "":
            fehlende_felder.append("'Branche (Wenn Sonstige)' darf nur bei Auswahl von 'Sonstige' befüllt sein)")
    abteilung = st.session_state.get("answer_0SD02", "")
    if abteilung is None or str(abteilung).strip() == "":
        fehlende_felder.append("Abteilung/Bereich")
    team_jahre = st.session_state.get("answer_0SD03")
    if team_jahre is None or team_jahre == 0:
        fehlende_felder.append("Teamzugehörigkeit")
    unternehmen_jahre = st.session_state.get("answer_0SD04")
    if unternehmen_jahre is None or unternehmen_jahre == 0:
        fehlende_felder.append("Unternehmenszugehörigkeit")
    personalverantwortung = st.session_state.get("answer_0SD05")
    if personalverantwortung not in ["Ja", "Nein"]:
        fehlende_felder.append("Personalverantwortung")
    alter = st.session_state.get("answer_0SD06")
    if alter is None or alter == 0:
        fehlende_felder.append("Alter")
    return fehlende_felder

# -Titel-
st.title("Fragebogen - Zusätzliche Informationen")

# -Inhalt der Formulare-
def page_1():
    st.header("Einleitung")
    st.markdown(INTRODUCTION_TEXT)

def page_2():
    st.header("Zustimmung Datenschutz")
    st.markdown(CONSENT_TEXT)
    st.markdown("")
    st.checkbox("Ich stimme zu", key="answer_consent", value=False)

def page_3():
    st.header("Demographie")
    st.markdown(DEMOGRAPHY_TEXT)
    st.markdown("")
    st.radio(label="Branche", options=OPTIONS_INDUSTRY + ["Sonstige"], key="answer_0SD01", index=None)
    st.text_input(label="Branche (Wenn Sonstige)", key="answer_0SD01B", value=None)
    st.text_input(label="In welcher Abteilung oder in welchem Bereich sind Sie zurzeit tätig?", key="answer_0SD02", value=None)
    st.number_input(label="Wie lange gehören Sie bereits Ihrem aktuellen Team an? (Bitte geben Sie die Anzahl der Jahre an.)", min_value=0.0, max_value=99.0, step=0.5, key="answer_0SD03")
    st.number_input(label="Wie lange arbeiten Sie bereits in Ihrem aktuellen Unternehmen?", min_value=0.0, max_value=99.0, step=0.5, key="answer_0SD04")
    st.radio(label="Haben Sie derzeit Personalverantwortung?", key="answer_0SD05", options=["Ja", "Nein"], index=None)
    st.number_input(label="Wie alt sind Sie? (1 eingeben falls Sie nicht antworten möchten)", min_value=0, max_value=99, key="answer_0SD06") # TODO: Möglichkeit nicht zu beantworten?
    # Zeige Warnung, falls Felder fehlen
    if "fehlende_felder" in st.session_state and st.session_state.fehlende_felder:
        st.warning(f"Bitte beantworten Sie alle Felder: {', '.join(st.session_state.fehlende_felder)}")

def page_4():
    st.header("Einleitung Kompetenzabfrage")
    st.markdown(INTRODUCTION_QUERRY)

# Zuweisung der Seiten
pages_dict = {
    1: page_1,
    2: page_2,
    3: page_3,
    4: page_4
}

# -Aufrufen der Seiten-
with st.form("form_page", enter_to_submit=False):
    if st.session_state.page_einleitung in pages_dict:
        pages_dict[st.session_state.page_einleitung]()
    left, right = st.columns(2)
    if st.session_state.page_einleitung < len(pages_dict):
        continue_button = right.form_submit_button(label="Weiter", on_click=click_continue)
    else:
        submit_button = right.form_submit_button(label="Fragebogen beginnen")
        if submit_button:
            if not check_errors():
                update_answers()
                st.switch_page("pages/fragebogen.py")
    if st.session_state.page_einleitung > 1:
        back_button = left.form_submit_button(label="Zurück", on_click=click_back)
    if "none_error" in st.session_state and st.session_state.none_error:
        st.warning("Bitte beantworten Sie alle Fragen.")
    if "consent_error" in st.session_state and st.session_state.consent_error:
        st.warning("Bitte stimmen Sie der Datenschutzerklärung zu.")