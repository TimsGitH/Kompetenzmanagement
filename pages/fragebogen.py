import streamlit as st
import pandas as pd
import datetime as dt
import pytz
from functions.data import get_cluster_numbers
from functions.menu import no_menu

st.set_page_config(page_title="Fragebogen")

no_menu()

# -Mitarbeiterdaten einlesen-
data_mitarbeiter = pd.read_csv("user_management/mitarbeiter.csv", sep=';', index_col=0)

# -Fragebogen einlesen-
fragebogen = pd.read_csv("fragebögen/2025-06-25_Finalversion_Fragebogen_pro-kom_aufbereitet_UTF-8.csv", sep=';', encoding='utf-8')

# -Funktionen-
def check_none_answers():
    none_counter = 0
    for i in range((st.session_state.page - 1) * amount_questions_per_page, ((st.session_state.page - 1) * amount_questions_per_page) + amount_questions_in_page):
        if st.session_state[fragebogen.loc[i, "Frage-ID"]] is None:
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
        new_answers.loc[questionnaire_id, fragebogen.loc[i, "Frage-ID"]] = int(translate_answer_save[st.session_state[fragebogen.loc[i, "Frage-ID"]]])
    # Tabellen kombinieren und Antworten als int speichern
    combined_answers = pd.concat([answers, new_answers], axis=0)
    question_ids = fragebogen["Frage-ID"].tolist()
    for id in question_ids:
        combined_answers[id] = combined_answers[id].astype(int)
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

# -Anzahl der Seiten berechnen und ausgeben-
if amount_questions == 0:
    st.write("Es wurde kein passender Fragebogen hinterlegt.")
else:
    amount_selected_clusters = st.session_state.selected_clusters["Selected"].sum()
    st.write(f"Anzahl ausgewählter Cluster: {amount_selected_clusters}")

# -Forschrittsanzeigen-
first_selected_cluster = st.session_state.selected_clusters[st.session_state.selected_clusters["Selected"]].index[0]
if "current_cluster" not in st.session_state:
    st.session_state.current_cluster = first_selected_cluster

# -Fragebogen-
with st.form("Fragebogen"):
    st.header("Formular")
    questions_for_current_cluster = fragebogen[fragebogen["Cluster-Nummer"] == st.session_state.current_cluster]
    amount_questions_in_page = len(questions_for_current_cluster)
    st.write(f"Anzahl Fragen auf dieser Seite: {amount_questions_in_page}")
    st.write(f"Cluster-Name: {st.session_state.selected_clusters.loc[st.session_state.current_cluster, 'Cluster-Name']}")
    for i in range(amount_questions_in_page):
        st.markdown("")
        st.markdown(body=fragebogen.loc[i, "Frage"])
        if fragebogen.loc[i, "Frage-ID"] in st.session_state:
            radio_button = st.radio(label=fragebogen.loc[i, "Frage"], options=options_form, index=translate_answer_index[st.session_state[fragebogen.loc[i, "Frage-ID"]]], key=fragebogen.loc[i, "Frage-ID"], horizontal=True, label_visibility="collapsed")
        else:
            radio_button = st.radio(label=fragebogen.loc[i, "Frage"], options=options_form, index=None, key=fragebogen.loc[i, "Frage-ID"], horizontal=True, label_visibility="collapsed")
    st.write(f"Cluster {st.session_state.current_cluster} von {amount_selected_clusters}")
    left, right = st.columns(2)
    if st.session_state.current_cluster < amount_selected_clusters:
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
    # Prüfen, ob current_cluster der erste ausgewählte Cluster ist
    if st.session_state.current_cluster != first_selected_cluster:
        back_button = left.form_submit_button(label="Zurück", on_click=click_back)
    if "none_error" in st.session_state and st.session_state.none_error:
        st.warning("Bitte beantworten Sie alle Fragen.")
