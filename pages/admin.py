import streamlit as st
from functions.menu import default_menu

st.set_page_config(page_title="Admin")

default_menu()

st.title("Admin")