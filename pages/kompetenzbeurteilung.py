import streamlit as st
import pandas as pd
from menu import default_menu

default_menu()

# -Tabelle für Mitarbeiter verknüpfen-
data_mitarbeiter = pd.read_csv("user_management/mitarbeiter.csv", sep=';', index_col=0)

# -Tabelle für Antworten verknüpfen-
answers = pd.read_csv("antworten/antworten.csv", sep=';', index_col=0)

# -Titel-
st.title("Kompetenzbeurteilung")

# -Mitarbeiterauswahl-
selected_id_active_mitarbeiter = st.selectbox(label="Welcher MA soll beurteilt werden?", options=data_mitarbeiter.index, index=None, placeholder="Bitte Mitarbeiter auswählen")

if selected_id_active_mitarbeiter is not None:
    selected_name_active_mitarbeiter = data_mitarbeiter.loc[selected_id_active_mitarbeiter, "Name"]
    amount_answered_forms = len(answers.loc[answers["Mitarbeiter-ID"] == selected_id_active_mitarbeiter])
    st.write(f"Ausgewählter Mitarbeiter: {selected_name_active_mitarbeiter}")
    if amount_answered_forms == 1:
        st.write(f"Für den Mitarbeiter wurde bereits ein Fragebogen ausgefüllt.")
    elif amount_answered_forms > 1:
        st.write(f"Für den Mitarbeiter wurden bereits {amount_answered_forms} Fragebögen ausgefüllt.")
    else:
        st.write("Für den Mitarbeiter wurde noch kein Fragebogen ausgefüllt.")

    st.markdown('#')

    st.write("Wie möchten Sie Daten aufnehmen?")

    left, right = st.columns(2)
    with left:
        if st.button(label="Fragebogen ausfüllen"):
            st.session_state.id_active_mitarbeiter = selected_id_active_mitarbeiter
            st.session_state.name_active_mitarbeiter = selected_name_active_mitarbeiter
            st.switch_page("pages/fragebogen.py")
    with right:
        if st.button(label="Kompetenzen manuell festlegen"):
            st.session_state.id_active_mitarbeiter = selected_id_active_mitarbeiter
            st.session_state.name_active_mitarbeiter = selected_name_active_mitarbeiter
            st.switch_page("pages/kompetenzen_festlegen.py")
