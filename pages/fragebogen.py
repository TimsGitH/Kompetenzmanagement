import streamlit as st
import pandas as pd
import datetime as dt
import pytz
from functions.menu import no_menu

st.set_page_config(page_title="Fragebogen")

no_menu()

# -Mitarbeiterdaten einlesen-
data_mitarbeiter = pd.read_csv("user_management/mitarbeiter.csv", sep=';', index_col=0)

# -Fragebogen einlesen-
fragebogen = pd.read_csv("fragebögen/25-04-25_Itemübersicht_Befragungsinstrument_CSV_UTF8.CSV", sep=';', encoding='utf-8')

# -Funktionen-
def check_none_answers():
    none_counter = 0
    for i in range((st.session_state.page - 1) * amount_questions_per_page, ((st.session_state.page - 1) * amount_questions_per_page) + amount_questions_in_page):
        if st.session_state[fragebogen.loc[i, "Code"]] is None:
            none_counter += 1
    if none_counter == 0:
        if "none_error" in st.session_state:
            del st.session_state.none_error
        return False
    else:
        if "none_error" not in st.session_state:
            st.session_state.none_error = True
        return True

def click_continue():
    if not check_none_answers():
        st.session_state.page += 1

def click_back():
    if "none_error" in st.session_state:
        del st.session_state.none_error
    st.session_state.page -= 1

def submit_form():
    # Tabelle für Antworten verknüpfen
    answers = pd.read_csv("antworten/antworten.csv", sep=';', index_col=0)
    # Tabelle initialisieren
    questionnaire_id = answers.shape[0]
    timezone = pytz.timezone('Europe/Berlin')
    now = dt.datetime.now(timezone)
    formatted_now = now.strftime('%Y-%m-%d %H:%M')
    data_new_answers = {
        "Speicherzeitpunkt": [formatted_now],
        "Mitarbeiter-ID": [st.session_state.id_active_mitarbeiter]
    }
    new_answers = pd.DataFrame(data_new_answers)
    new_answers.index = [questionnaire_id]
    # Antworten eintragen
    for i in range(amount_questions):
        new_answers.loc[questionnaire_id, fragebogen.loc[i, "Code"]] = int(translate_answer_save[st.session_state[fragebogen.loc[i, "Code"]]])
    # Tabellen kombinieren und Antworten als int speichern
    combined_answers = pd.concat([answers, new_answers], axis=0)
    question_codes = fragebogen["Code"].tolist()
    for code in question_codes:
        combined_answers[code] = combined_answers[code].astype(int)
    combined_answers.to_csv("antworten/antworten.csv", sep=';', index_label="Antwort-ID")
    # Session States aufräumen
    del st.session_state.page
    del st.session_state.id_active_mitarbeiter
    del st.session_state.name_active_mitarbeiter


# -Mögliche Antworten für die Fragen (trifft zu entspricht 1, trifft nicht zu entspricht 5)
options_form= ("trifft nicht zu", "trifft eher nicht zu", "teils-teils", "trifft eher zu", "trifft zu")

# -Übersetzungstabelle-
translate_answer_save = {
    "trifft nicht zu": 5, 
    "trifft eher nicht zu": 4, 
    "teils-teils": 3, 
    "trifft eher zu": 2, 
    "trifft zu": 1,
    None: 0
}
translate_answer_index = {
    "trifft nicht zu": 0, 
    "trifft eher nicht zu": 1, 
    "teils-teils": 2, 
    "trifft eher zu": 3, 
    "trifft zu": 4,
    None: None
}

# -Anzahl der Fragen auslesen-
amount_questions = fragebogen.shape[0]

# -Anpassbare Variable zur Einstellung der maximalen Fragen pro Seite-
amount_questions_per_page = 6

# -Titel-
st.title("Fragebogen")
st.write(f"Mitarbeiter: {st.session_state.name_active_mitarbeiter}")
st.write(f"Mitarbeiter-ID: {st.session_state.id_active_mitarbeiter}")
st.write(f"Anzahl Fragen: {amount_questions}")

# -Anzahl der Seiten berechnen-
if amount_questions == 0:
    st.write("Es wurde kein Fragebogen hinterlegt.")
else:
    amount_pages = - ( - amount_questions // amount_questions_per_page ) #Aufgerundete, ganzzahlige Division
    st.write(f"Anzahl Seiten des Fragebogens: {amount_pages}")

# -Forschrittsanzeigen-
if 'page' not in st.session_state:
    st.session_state.page = 1
st.progress((st.session_state.page - 1) / amount_pages, text="Fortschritt Fragebogen")

# -Fragebogen-
with st.form("Fragebogen"):
    if st.session_state.page < amount_pages:
        amount_questions_in_page = amount_questions_per_page
    else:
        amount_questions_in_page = amount_questions - ((st.session_state.page - 1) * amount_questions_per_page)
    st.header("Formular")
    st.write(f"Anzahl Fragen auf dieser Seite: {amount_questions_in_page}")
    for i in range((st.session_state.page - 1) * amount_questions_per_page, ((st.session_state.page - 1) * amount_questions_per_page) + amount_questions_in_page):
        st.markdown("")
        st.markdown(body=fragebogen.loc[i, "Itemformulierung"])
        if fragebogen.loc[i, "Code"] in st.session_state:
            radio_button = st.radio(label=fragebogen.loc[i, "Itemformulierung"], options=options_form, index=translate_answer_index[st.session_state[fragebogen.loc[i, "Code"]]], key=fragebogen.loc[i, "Code"], horizontal=True, label_visibility="collapsed")
        else:
            radio_button = st.radio(label=fragebogen.loc[i, "Itemformulierung"], options=options_form, index=None, key=fragebogen.loc[i, "Code"], horizontal=True, label_visibility="collapsed")
    st.write(f"Seite {st.session_state.page} von {amount_pages}")
    left, right = st.columns(2)
    if st.session_state.page < amount_pages:
        continue_button = right.form_submit_button(label="Weiter", on_click=click_continue)
    else:
        submit_button = right.form_submit_button(label="Fragebogen abschließen")
        if submit_button:
            if not check_none_answers():
                submit_form()
                if st.session_state.role == "Admin":
                    st.switch_page("pages/kompetenzbeurteilung.py")
                elif st.session_state.role == "Mitarbeiter":
                    st.switch_page("pages/fragebogen_start.py")
                else:
                    raise Exception("session_state.role not valid")
    if st.session_state.page > 1:
        back_button = left.form_submit_button(label="Zurück", on_click=click_back)
    if "none_error" in st.session_state and st.session_state.none_error:
        st.warning("Bitte beantworten Sie alle Fragen.")
