import streamlit as st
import pandas as pd
import datetime as dt
from menu import no_menu

st.set_page_config(page_title="Fragebogen")

no_menu()

# -Mitarbeiterdaten einlesen-
data_mitarbeiter = pd.read_csv("user_management/mitarbeiter.csv", index_col=0)

# -Fragebogen einlesen-
fragebogen = pd.read_csv("fragebögen/Messinstrument_V01_aufbereitet.CSV", sep=';', encoding='utf-8')

# -Tabelle für Antworten verknüpfen-
answers = pd.read_csv("antworten/Antworten.csv")

# -Funktionen-
def click_continue():
    st.session_state.page += 1

def click_back():
    st.session_state.page -= 1

def submit_form():
    datetime = dt.datetime.now()
    data_new_answers = {
        "Datum": [datetime.strftime("%x %X")],
        "Mitarbeiter-ID": [st.session_state.id_active_mitarbeiter]
    }
    new_answers = pd.DataFrame(data_new_answers)
    for i in range(amount_questions):
        if fragebogen.loc[i, "invertiert"] is True:
            new_answers.loc[0, fragebogen.loc[i, "Code"]] = translate_answer_inverted[st.session_state[fragebogen.loc[i, "Code"]]]
        else:
            new_answers.loc[0, fragebogen.loc[i, "Code"]] = translate_answer[st.session_state[fragebogen.loc[i, "Code"]]]
    combined_answers = pd.concat([answers, new_answers], ignore_index=True)
    combined_answers.to_csv("antworten/Antworten.csv")
    del st.session_state.page
    del st.session_state.id_active_mitarbeiter
    del st.session_state.name_active_mitarbeiter

# -Mögliche Antworten für die Fragen (trifft zu entspricht 1, trifft nicht zu entspricht 5)
options_form= ("trifft nicht zu", "trifft eher nicht zu", "teils-teils", "trifft eher zu", "trifft zu")

# -Übersetzungstabellen-
translate_answer = {
    "trifft nicht zu": 5, 
    "trifft eher nicht zu": 4, 
    "teils-teils": 3, 
    "trifft eher zu": 2, 
    "trifft zu": 1,
    None: 0
}
translate_answer_inverted = {
    "trifft nicht zu": 1, 
    "trifft eher nicht zu": 2, 
    "teils-teils": 3, 
    "trifft eher zu": 4, 
    "trifft zu": 5,
    None: 0
}

# -Anzahl der Fragen auslesen-
amount_questions = fragebogen.shape[0]

# -Anpassbare Variable zur Einstellung der maximalen Fragen pro Seite
amount_questions_per_page = 6

# -Titel-
st.title("Fragebogen")
st.write(f"Für {st.session_state.name_active_mitarbeiter}")
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

# -Fragen ausgeben-
st.header("Fragen:")
st.write(fragebogen)

# -Fragebogen-
with st.form("Fragebogen"):
    if st.session_state.page < amount_pages:
        amount_questions_in_page = amount_questions_per_page
    else:
        amount_questions_in_page = amount_questions - ((st.session_state.page - 1) * amount_questions_per_page)
    st.header("Formular")
    st.write(f"Anzahl Fragen auf dieser Seite: {amount_questions_in_page}")
    for i in range((st.session_state.page - 1) * amount_questions_per_page, ((st.session_state.page - 1) * amount_questions_per_page) + amount_questions_in_page):
        radio_button = st.radio(label=fragebogen.loc[i, "Items"], options=options_form, index=None, key=fragebogen.loc[i, "Code"], horizontal=True)
    st.write(f"Seite {st.session_state.page} von {amount_pages}")
    left, right = st.columns(2)
    if st.session_state.page < amount_pages:
        continue_button = left.form_submit_button(label="Weiter", on_click=click_continue)
    else:
        submit_button = left.form_submit_button(label="Fragebogen abschließen")
        if submit_button:
            submit_form()
            st.switch_page("pages/kompetenzbeurteilung.py")
    if st.session_state.page > 1:
        back_button = right.form_submit_button(label="Zurück", on_click=click_back)
