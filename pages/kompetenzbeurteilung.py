import streamlit as st
import pandas as pd
from menu import default_menu

default_menu()

# -Tabelle für Mitarbeiter verknüpfen-
data_mitarbeiter = pd.read_csv("user_management/mitarbeiter.csv", index_col=0)

# -Tabelle für Antworten verknüpfen-
answers = pd.read_csv("antworten/Antworten.csv")

# -Mitarbeiter auswählen-
def selectbox():
    st.session_state.id_active_mitarbeiter = data_mitarbeiter.index[data_mitarbeiter["Name"] == st.session_state.selected_mitarbeiter][0]
    st.session_state.name_active_mitarbeiter = st.session_state.selected_mitarbeiter

st.title("Kompetenzbeurteilung")

selectbox_mitarbeiter = st.selectbox(label="Welcher MA soll beurteilt werden?", options=data_mitarbeiter[["Name"]], index=None, key="selected_mitarbeiter", on_change=selectbox, placeholder="Bitte Mitarbeiter auswählen")

if "id_active_mitarbeiter" in st.session_state:
    amount_answered_forms = len(answers.loc[answers["Mitarbeiter-ID"] == st.session_state.id_active_mitarbeiter])
    if amount_answered_forms == 1:
    #if data_mitarbeiter.loc[st.session_state.id_active_mitarbeiter, "Initialisiert"]:
        st.write("Für den Mitarbeiter wurde bereits ein Fragebogen ausgefüllt.")
    elif amount_answered_forms > 1:
        st.write(f"Für den Mitarbeiter wurden bereits {amount_answered_forms} Fragebögen ausgefüllt.")
    else:
        st.write("Für den Mitarbeiter wurde noch kein Fragebogen ausgefüllt.")

    st.write("\n")

    st.write("Wie möchten Sie Daten aufnehmen?")

    left, right = st.columns(2)
    with left:
        if st.button(label="Fragebogen ausfüllen"):
            st.switch_page("pages/fragebogen.py")
    with right:
        if st.button(label="Kompetenzen manuell festlegen"):
            st.switch_page("pages/kompetenzen_festlegen.py")
