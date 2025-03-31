import streamlit as st
import pandas as pd

data_mitarbeiter = pd.read_csv("user_management/mitarbeiter.csv", index_col=0)

name_active_mitarbeiter = st.selectbox("Welcher MA soll beurteilt werden?", data_mitarbeiter[["Name"]])
st.write(name_active_mitarbeiter)

id_active_mitarbeiter = data_mitarbeiter.index[data_mitarbeiter["Name"] == name_active_mitarbeiter][0]
st.write(id_active_mitarbeiter)

if data_mitarbeiter.loc[id_active_mitarbeiter, "Initialisiert"]:
    st.write("Für den Mitarbeiter wurde bereits eine initiale Bewertung erstellt. Möchten Sie diese aktualisieren?")
    if st.button("Ja"):
        st.switch_page("pages/fragebogen.py")
        
    st.button("Nein")



st.title("Fragebogen")
st.write("Seite 1/X")
options_umfrage= ("sehr schlecht", "eher schlecht", "neutral", "eher gut", "sehr gut")

antworten = st.select_slider(label="Wie finden Sie Grünkohl?", options=options_umfrage)
st.radio(label="Wie steht es um Ihre Intelligenz?", options=options_umfrage, index=2, horizontal=True)