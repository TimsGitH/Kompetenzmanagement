import streamlit as st
import pandas as pd

st.title("Kompetenzbeurteilung")

data_mitarbeiter = pd.read_csv("user_management/mitarbeiter.csv", index_col=0)

name_active_mitarbeiter = st.selectbox("Welcher MA soll beurteilt werden?", data_mitarbeiter[["Name"]])
id_active_mitarbeiter = data_mitarbeiter.index[data_mitarbeiter["Name"] == name_active_mitarbeiter][0]

if data_mitarbeiter.loc[id_active_mitarbeiter, "Initialisiert"]:
    st.write("Für den Mitarbeiter wurde bereits eine initiale Bewertung erstellt.")
else:
    st.write("Für den Mitarbeiter wurde noch keine initiale Bewertung erstellt.")

st.write("\n")

st.write("Wie möchten Sie Daten aufnehmen?")

links, rechts = st.columns(2)
with links:
    if st.button("Fragebogen ausfüllen"):
        st.switch_page("pages/fragebogen.py")
with rechts:
    if st.button("Kompetenzen manuell festlegen"):
        st.switch_page("pages/kompetenzen_festlegen.py")