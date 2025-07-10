import streamlit as st
import gspread
import pandas as pd
from google.oauth2.service_account import Credentials
from config import GSHEET_SERVICE_ACCOUNT_FILENAME, SHEET_NAME

def get_spreadsheet(file_name, spreadsheet_name):
    """
    TODO: Beschreibung der Funktion
    TODO: Schlüssel korrekt in Secrets speichern und laden.
    """
    scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    ]
    credentials_dict = st.secrets["service_account"]
    credentials = Credentials.from_service_account_info(credentials_dict, scopes=scopes)
    spreadsheet = gspread.authorize(credentials)
    return spreadsheet.open(spreadsheet_name)

def get_dataframe(worksheet_name):
    """
    TODO: Beschreibung der Funktion
    """
    spreadsheet = get_spreadsheet(GSHEET_SERVICE_ACCOUNT_FILENAME, SHEET_NAME)
    worksheet = spreadsheet.worksheet(worksheet_name)
    records = worksheet.get_all_records()
    if records and list(records[0].keys()):
        dataframe = pd.DataFrame(records).set_index(list(records[0].keys())[0])
    else:
        dataframe = pd.DataFrame()
    return dataframe
