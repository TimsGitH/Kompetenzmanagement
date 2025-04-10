import streamlit as st
import pandas as pd
from menu import default_menu

st.set_page_config(page_title="User Management")

default_menu()

data_mitarbeiter = pd.read_csv("user_management/mitarbeiter.csv", index_col=0)

st.title("User Management")

st.write("Vorhandene Nutzer:")
st.write(data_mitarbeiter)