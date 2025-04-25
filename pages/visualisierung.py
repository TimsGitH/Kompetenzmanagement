import streamlit as st
import pandas as pd
from menu import default_menu

st.set_page_config(page_title="Visualisierung")

default_menu()

def update(user_id):
    st.write("User-ID: " + str(user_id))
    st.area_chart(data=data_peter, x_label="Kompetenz", y_label="Wert")

data_mitarbeiter = pd.read_csv("user_management/mitarbeiter.csv", sep=';', index_col=0)

data_peter = pd.read_csv("kompetenzen/kompetenzen_peter.csv", index_col=0)




st.title("Visualisierung")
name_active_mitarbeiter = st.selectbox("Mitarbeiter auswählen:", data_mitarbeiter[["Name"]])
id_active_mitarbeiter = data_mitarbeiter.index[data_mitarbeiter["Name"] == name_active_mitarbeiter][0]
update(id_active_mitarbeiter)
