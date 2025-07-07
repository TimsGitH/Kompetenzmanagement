import pandas as pd

def get_amount_questions():
    # Funktion zum Abrufen der Anzahl der Fragen im Fragebogen.
    fragebogen = pd.read_csv("fragebögen/2025-06-25_Finalversion_Fragebogen_pro-kom_aufbereitet_UTF-8.csv", sep=';', encoding='utf-8')
    return fragebogen.shape[0]

def invert_corresponding_answers(df):
    # Funktion zum invertieren der im Fragebogen entsprechend markierten Antworten.
    invert_dict = {1: 5, 2:4, 3:3, 4:2, 5:1}
    fragebogen = pd.read_csv("fragebögen/2025-06-25_Finalversion_Fragebogen_pro-kom_aufbereitet_UTF-8.csv", sep=';', encoding='utf-8')
    df_with_inverted_answers = df
    for index in df_with_inverted_answers.index:
        if index in fragebogen["Frage-ID"].values and fragebogen.loc[fragebogen['Frage-ID'] == index, "invertiert"].values[0] is True:
            df_with_inverted_answers.loc[index] = invert_dict[df_with_inverted_answers.loc[index]]
    return df_with_inverted_answers

def calculate_cluster_values(df):
    # Funktion zum Berechnen der Cluster-Werte für Tabellen.
    df_with_inverted_answers = invert_corresponding_answers(df)
    cluster_values = []
    for i in range(len(get_cluster_names())):
        mask = df_with_inverted_answers.index.str.match(fr'^{i + 1}[A-Z]')
        cluster_answers = df_with_inverted_answers[mask]
        cluster_value = round(cluster_answers.sum() / len(cluster_answers), 1)
        cluster_values.append(cluster_value)
    return cluster_values

def get_cluster_names():
    # Funktion zum Abrufen der Cluster-Namen des hinterlegten Fragebogens.
    fragebogen = pd.read_csv("fragebögen/2025-06-25_Finalversion_Fragebogen_pro-kom_aufbereitet_UTF-8.csv", sep=';', encoding='utf-8')
    return fragebogen["Cluster-Name"].unique()

def get_cluster_numbers():
    # Funktion zum Abrufen der Cluster-Nummern des hinterlegten Fragebogens.
    fragebogen = pd.read_csv("fragebögen/2025-06-25_Finalversion_Fragebogen_pro-kom_aufbereitet_UTF-8.csv", sep=';', encoding='utf-8')
    return fragebogen["Cluster-Nummer"].unique()

def get_cluster_table():
    # Funktion zum Abrufen der Cluster-Nummern des hinterlegten Fragebogens.
    fragebogen = pd.read_csv("fragebögen/2025-06-25_Finalversion_Fragebogen_pro-kom_aufbereitet_UTF-8.csv", sep=';', encoding='utf-8')
    cluster_data = fragebogen[["Cluster-Nummer", "Cluster-Name"]].drop_duplicates()
    cluster_data.set_index("Cluster-Nummer", inplace=True)
    return cluster_data

def get_cluster_values_with_times(id):
    # Funktion zum Abrufen der Cluster-Werte mit entsprechenden Zeitpunkten.
    answers = pd.read_csv("antworten/antworten.csv", sep=';', index_col=0)
    return answers[answers["Profil-ID"] == id]

def get_question_ids():
    # Funktion zum Abrufen der Frage-IDs als Liste.
    fragebogen = pd.read_csv("fragebögen/2025-06-25_Finalversion_Fragebogen_pro-kom_aufbereitet_UTF-8.csv", sep=';', encoding='utf-8')
    return fragebogen["Frage-ID"].tolist()

def get_latest_update_time(id):
    # Funktion zum Abrufen des letzten Eintrags für die gegebene ID.
    answers = pd.read_csv("antworten/antworten.csv", sep=';', index_col=0)
    filtered_answers = answers[answers["Profil-ID"] == id]
    if len(filtered_answers) == 0:
        return None
    sorted_answers = filtered_answers.sort_values(by="Speicherzeitpunkt", ascending=False)
    return sorted_answers["Speicherzeitpunkt"].values[0]

def get_latest_cluster_values(id):
    # Funktion zum Berechnen der Cluster-Werte aus dem aktuellsten Fragebogen.
    answers = pd.read_csv("antworten/antworten.csv", sep=';', index_col=0)
    filtered_answers = answers[answers["Profil-ID"] == id]
    if len(filtered_answers) == 0:
        return None
    sorted_answers = filtered_answers.sort_values(by="Speicherzeitpunkt", ascending=False)
    latest_answer = sorted_answers.iloc[0]
    return calculate_cluster_values(latest_answer)
