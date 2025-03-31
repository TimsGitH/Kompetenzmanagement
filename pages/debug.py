import streamlit as st
import pandas as pd

data_mitarbeiter = pd.read_csv("user_management/mitarbeiter.csv", index_col=0)

st.title("debug")
st.write(data_mitarbeiter)