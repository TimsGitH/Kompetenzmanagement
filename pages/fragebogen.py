import streamlit as st
import pandas as pd
from menu import no_menu

st.set_page_config(page_title="Fragebogen")

no_menu()

data_mitarbeiter = pd.read_csv("user_management/mitarbeiter.csv", index_col=0)

def click_continue():
    st.session_state.page += 1
    st.session_state.total_progress += len(antworten)

name_active_mitarbeiter = data_mitarbeiter.loc[st.session_state.id_active_mitarbeiter, "Name"]

# -Titel-
st.title("Fragebogen")
st.write(f"Für {name_active_mitarbeiter}")

# -Forschrittsanzeigen-
if "total_progress" not in st.session_state:
    st.session_state.total_progress = 0
if "cluster_progress" not in st.session_state:
    st.session_state.cluster_progress = 0
st.progress(st.session_state.total_progress, text="Fortschritt Fragebogen")
st.progress(st.session_state.cluster_progress, text="Fortschritt Cluster")

# -Mögliche Antworten für die Fragen (trifft zu entspricht 1, trifft nicht zu entspricht 5)
options_umfrage= ("trifft zu", "trifft eher zu", "teils-teils", "trifft eher nicht zu", "trifft nicht zu")

# -Daten einlesen-
fragebogen = pd.read_csv("fragebögen/Messinstrument_V01_aufbereitet.CSV", sep=';', encoding='latin-1')

# -Fragen ausgeben-
st.header("Fragen:")
st.write(fragebogen)

# -Anzahl der Fragen auslesen-
amount_questions = fragebogen.shape[0]
st.write(f"Anzahl Fragen: {amount_questions}")

# -Anpassbare Variable zur Einstellung der maximalen Fragen pro Seite
amount_questions_per_page = 6

# -Anzahl der Seiten berechnen-
if amount_questions == 0:
    st.write("Es wurde kein Fragebogen hinterlegt.")
else:
    amount_pages = - ( - amount_questions // amount_questions_per_page ) #Aufgerundete, ganzzahlige Division
    st.write(f"Anzahl Seiten des Fragebogens: {amount_pages}")

# -Fragebogen-
with st.form("Fragebogen"):
    st.header("Formular")
    antworten = list()
    if 'page' not in st.session_state:
        st.session_state.page = 1
    page = st.session_state.page
    if page < amount_pages:
        amount_questions_in_page = amount_questions_per_page
    else:
        amount_questions_in_page = amount_questions - ((page - 1) * amount_questions_per_page)
    st.write(f"Anzahl Fragen auf dieser Seite: {amount_questions_in_page}")
    for i in range((page - 1) * amount_questions_per_page, ((page - 1) * amount_questions_per_page) + amount_questions_in_page):
        antworten.append(st.radio(label=fragebogen.loc[i, "Items"], options=options_umfrage, index=None, horizontal=True))
    left, right = st.columns(2)
    if page < amount_pages:
        submit_button = left.form_submit_button(label="Weiter", on_click=click_continue)
    else:
        submit_button = left.form_submit_button("Fragebogen abschließen")
        if submit_button:
            del st.session_state.page
            del st.session_state.id_active_mitarbeiter
            st.switch_page("pages/kompetenzbeurteilung.py")
    right.write(f"Seite {page} von {amount_pages}")
