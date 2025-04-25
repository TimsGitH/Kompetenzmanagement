import streamlit as st
import pandas as pd
from menu import default_menu

st.set_page_config(page_title="Debug")

default_menu()

data_mitarbeiter = pd.read_csv("user_management/mitarbeiter.csv", sep=';', index_col=0)

st.title("debug")
st.write(data_mitarbeiter)