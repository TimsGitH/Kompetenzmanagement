import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

def connect_to_gsheet():
    return st.connection("gsheets", type=GSheetsConnection)

def get_dataframe_from_gsheet(worksheet_name):
    """
    TODO: Übersetzen
    Retrieves a DataFrame from a specified Google Sheets worksheet.
    
    Args:
        worksheet_name (str): The name of the worksheet to retrieve data from.
    
    Returns:
        pd.DataFrame: A DataFrame containing the data from the specified worksheet.
    """
    conn = connect_to_gsheet()
    import_dataframe = conn.read(worksheet=worksheet_name)
    dataframe = pd.DataFrame(import_dataframe)
    dataframe = dataframe.set_index(dataframe.columns[0])
    return dataframe

def update_dataframe_to_gsheet(worksheet_name, dataframe):
    """
    TODO: Beschreibung hinzufügen
    """
    conn = connect_to_gsheet()
    dataframe_without_index = dataframe.reset_index()
    conn.update(worksheet=worksheet_name, data=dataframe_without_index)

def create_worksheet(worksheet_name):
    conn = connect_to_gsheet()
    conn.create(worksheet=worksheet_name)
