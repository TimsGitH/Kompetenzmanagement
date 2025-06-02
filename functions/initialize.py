import pandas as pd
import os

# -Leere Tabelle für Antworten erstellen, falls keine existiert-
def create_empty_answers_dataframe():
    answers_path = "antworten/antworten.csv"
    if not os.path.exists(answers_path):
        column_names = ["Speicherzeitpunkt", "Mitarbeiter-ID"]
        answers = pd.DataFrame(columns=column_names)
        answers.to_csv(answers_path, sep=';', index_label="Antwort-ID")