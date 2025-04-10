import streamlit as st
import pandas as pd
from menu import no_menu

st.set_page_config(page_title="Fragebogen")

no_menu()

data_mitarbeiter = pd.read_csv("user_management/mitarbeiter.csv", index_col=0)

name_active_mitarbeiter = data_mitarbeiter.loc[st.session_state.id_active_mitarbeiter, "Name"]

st.title("Fragebogen")
st.write(f"Für {name_active_mitarbeiter}")
st.write("Seite 1/X")

progress = 0
progress_bar = st.progress(progress, text="Fortschritt")

options_umfrage= ("sehr schlecht", "eher schlecht", "neutral", "eher gut", "sehr gut")

fragen = pd.read_csv("fragebögen/fragebogen.csv", index_col=0, sep=';')
amount_questions = fragen.shape[0]
st.write(fragen)
st.write(f"Anzahl Fragen: {amount_questions}")

antworten = list()

amount_questions_per_page = 6

if amount_questions == 0:
    st.write("Es wurde kein Fragebogen hinterlegt.")
else:
    amount_pages = - ( - amount_questions // amount_questions_per_page ) #Aufgerundete, ganzzahlige Division
    st.write(f"Anzahl Seiten des Fragebogens: {amount_pages}")

with st.form("Fragebogen"):
    if 'page' not in st.session_state:
        st.session_state.page = 1
    page = st.session_state.page
    st.write(f"Seite {page} von {amount_pages}")
    if page < amount_pages:
        amount_questions_in_page = amount_questions_per_page
    else:
        amount_questions_in_page = amount_questions - ((page - 1) * amount_questions_per_page)
    st.write(f"Anzahl Fragen auf dieser Seite: {amount_questions_in_page}")
    for i in range((page - 1) * amount_questions_per_page, ((page - 1) * amount_questions_per_page) + amount_questions_in_page):
        antworten.append(st.radio(label=fragen.loc[i+1, "Frage"], options=options_umfrage, index=2, horizontal=True))
    if page < amount_pages:
        if st.form_submit_button("Weiter"):
            st.session_state.page += 1
    else:
        if st.form_submit_button("Fragebogen abschließen"):
            del st.session_state.page
            del st.session_state.id_active_mitarbeiter
            st.switch_page("pages/kompetenzbeurteilung.py")

#for page in range(amount_pages):
#    with st.form("Fragebogen"):
#        st.write(f"Seite {page+1} von {amount_pages}")
#        if page + 1 < amount_pages:
#            amount_questions_in_page = amount_questions_per_page
#        else:
#            amount_questions_in_page = amount_questions - ( page * amount_questions_per_page)
#        st.write(f"Anzahl Fragen auf dieser Seite: {amount_questions_in_page}")
#        for i in range(page*amount_questions_per_page, (page*amount_questions_per_page)+amount_questions_in_page):
#            antworten.append(st.radio(label=fragen.loc[i+1, "Frage"], options=options_umfrage, index=2, horizontal=True))
#
#        if st.form_submit_button("Weiter"):
#            st.write(antworten)
#        if st.button(label = f"Weiter (Seite {page})"):
#            st.write(antworten)


#st.radio(label="Wie steht es um Ihre Intelligenz?", options=options_umfrage, index=2, horizontal=True)

#if page < amount_pages:
#    amount_questions_in_page = amount_questions_per_page
#else:
#    amount_questions_in_page = amount_questions - ( page * amount_questions_per_page)
