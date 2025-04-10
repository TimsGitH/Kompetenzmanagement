import streamlit as st
import pandas as pd
from menu import default_menu

default_menu()

data_mitarbeiter = pd.read_csv("user_management/mitarbeiter.csv", index_col=0)

def selectbox():
    st.session_state.id_active_mitarbeiter = data_mitarbeiter.index[data_mitarbeiter["Name"] == st.session_state.name_active_mitarbeiter][0]

st.title("Kompetenzbeurteilung")

st.selectbox(label="Welcher MA soll beurteilt werden?", options=data_mitarbeiter[["Name"]], index=None, key="name_active_mitarbeiter", on_change=selectbox, placeholder="Bitte Mitarbeiter auswählen")

if "id_active_mitarbeiter" in st.session_state:
    if data_mitarbeiter.loc[st.session_state.id_active_mitarbeiter, "Initialisiert"]:
        st.write("Für den Mitarbeiter wurde bereits eine initiale Bewertung erstellt.")
    else:
        st.write("Für den Mitarbeiter wurde noch keine initiale Bewertung erstellt.")

    st.write("\n")

    st.write("Wie möchten Sie Daten aufnehmen?")

    left, right = st.columns(2)
    with left:
        if st.button(label="Fragebogen ausfüllen"):
            st.switch_page("pages/fragebogen.py")
    with right:
        if st.button(label="Kompetenzen manuell festlegen"):
            st.switch_page("pages/kompetenzen_festlegen.py")
