import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

def connect_to_gsheet():
    """
    Verbindet mit der Google Tabelle.
    """
    return st.connection("gsheets", type=GSheetsConnection)

def get_dataframe_from_gsheet(worksheet_name):
    """
    Lädt einen DataFrame aus der Google Tabelle.
    
    Args:
        worksheet_name (str): Der Name des Arbeitsblatts.
    
    Returns:
        pd.DataFrame: Ein DataFrame, der die Daten aus dem angegebenen Arbeitsblatt enthält.
    """
    conn = connect_to_gsheet()
    import_dataframe = conn.read(worksheet=worksheet_name)
    dataframe = pd.DataFrame(import_dataframe)
    dataframe = dataframe.set_index(dataframe.columns[0])
    return dataframe

def update_dataframe_to_gsheet(worksheet_name, dataframe):
    """
    Lädt einen DataFrame in die Google Tabelle.
    Args:
        worksheet_name (str): Der Name des Arbeitsblatts.
        dataframe (pd.DataFrame): Der DataFrame, der in die Google Tabelle geladen werden soll.
    """
    conn = connect_to_gsheet()
    dataframe_without_index = dataframe.reset_index()
    conn.update(worksheet=worksheet_name, data=dataframe_without_index)

def create_worksheet(worksheet_name):
    conn = connect_to_gsheet()
    conn.create(worksheet=worksheet_name)

