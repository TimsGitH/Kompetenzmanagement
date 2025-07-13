import pandas as pd
from config import PATH_ANSWERS, PATH_QUESTIONNAIRE

def get_amount_questions():
    """
    Ruft die Anzahl der Fragen im Fragebogen ab.
    
    Returns:
        int: Anzahl der Fragen im Fragebogen
    """
    # Funktion zum Abrufen der Anzahl der Fragen im Fragebogen.
    fragebogen = pd.read_csv(PATH_QUESTIONNAIRE, sep=';', encoding='utf-8')
    return fragebogen.shape[0]

def invert_corresponding_answers(df):
    """
    Invertiert die Antworten, die im Fragebogen als invertiert markiert sind.
    
    Args:
        df (pandas.DataFrame): DataFrame mit den Antworten
        
    Returns:
        pandas.DataFrame: DataFrame mit invertierten Antworten für entsprechend markierte Fragen
    """
    # Funktion zum invertieren der im Fragebogen entsprechend markierten Antworten.
    invert_dict = {1: 5, 2:4, 3:3, 4:2, 5:1}
    fragebogen = pd.read_csv(PATH_QUESTIONNAIRE, sep=';', encoding='utf-8')
    df_with_inverted_answers = df
    for index in df_with_inverted_answers.index:
        if index in fragebogen["Frage-ID"].values and fragebogen.loc[fragebogen['Frage-ID'] == index, "invertiert"].values[0] is True:
            df_with_inverted_answers.loc[index] = invert_dict[df_with_inverted_answers.loc[index]]
    return df_with_inverted_answers

def calculate_cluster_values(df):
    """
    Berechnet die Cluster-Werte für die gegebenen Antworten.
    
    Args:
        df (pandas.DataFrame): DataFrame mit den Antworten
        
    Returns:
        list: Liste der berechneten Cluster-Werte
    """
    df_with_inverted_answers = invert_corresponding_answers(df)
    cluster_values = []
    for i in range(len(get_cluster_names())):
        mask = df_with_inverted_answers.index.str.match(fr'^{i + 1}[A-Z]')
        cluster_answers = df_with_inverted_answers[mask]
        cluster_value = round(cluster_answers.sum() / len(cluster_answers), 1)
        cluster_values.append(cluster_value)
    return cluster_values

def get_cluster_names():
    """
    Ruft die Namen der Cluster aus dem Fragebogen ab.
    
    Returns:
        numpy.ndarray: Array mit den eindeutigen Cluster-Namen
    """
    # Funktion zum Abrufen der Cluster-Namen des hinterlegten Fragebogens.
    fragebogen = pd.read_csv(PATH_QUESTIONNAIRE, sep=';', encoding='utf-8')
    return fragebogen["Cluster-Name"].unique()

def get_cluster_numbers():
    """
    Ruft die Nummern der Cluster aus dem Fragebogen ab.
    
    Returns:
        numpy.ndarray: Array mit den eindeutigen Cluster-Nummern
    """
    # Funktion zum Abrufen der Cluster-Nummern des hinterlegten Fragebogens.
    fragebogen = pd.read_csv(PATH_QUESTIONNAIRE, sep=';', encoding='utf-8')
    return fragebogen["Cluster-Nummer"].unique()

def get_cluster_table():
    """
    Erstellt eine Tabelle mit Cluster-Nummern und zugehörigen Namen.
    
    Returns:
        pandas.DataFrame: DataFrame mit Cluster-Nummern als Index und Cluster-Namen als Spalte
    """
    # Funktion zum Abrufen der Cluster-Nummern des hinterlegten Fragebogens.
    fragebogen = pd.read_csv(PATH_QUESTIONNAIRE, sep=';', encoding='utf-8')
    cluster_data = fragebogen[["Cluster-Nummer", "Cluster-Name"]].drop_duplicates()
    cluster_data.set_index("Cluster-Nummer", inplace=True)
    return cluster_data

def get_cluster_values_with_times(id):
    """
    Ruft die Cluster-Werte mit entsprechenden Zeitpunkten für eine bestimmte Profil-ID ab.
    
    Args:
        id: Profil-ID für die die Cluster-Werte abgerufen werden sollen
        
    Returns:
        pandas.DataFrame: DataFrame mit Cluster-Werten und Zeitpunkten für die gegebene Profil-ID
    """
    # Funktion zum Abrufen der Cluster-Werte mit entsprechenden Zeitpunkten.
    answers = pd.read_csv(PATH_ANSWERS, sep=';', index_col=0)
    return answers[answers["Profil-ID"] == id]

def get_question_ids():
    """
    Ruft alle Frage-IDs aus dem Fragebogen als Liste ab.
    
    Returns:
        list: Liste aller Frage-IDs
    """
    # Funktion zum Abrufen der Frage-IDs als Liste.
    fragebogen = pd.read_csv(PATH_QUESTIONNAIRE, sep=';', encoding='utf-8')
    return fragebogen["Frage-ID"].tolist()

def get_latest_update_time(id):
    """
    Ruft den Zeitpunkt des letzten Eintrags für eine bestimmte Profil-ID ab.
    
    Args:
        id: Profil-ID für die der letzte Eintrag gesucht wird
        
    Returns:
        str or None: Zeitpunkt des letzten Eintrags oder None falls keine Einträge vorhanden
    """
    # Funktion zum Abrufen des letzten Eintrags für die gegebene ID.
    answers = pd.read_csv(PATH_ANSWERS, sep=';', index_col=0)
    filtered_answers = answers[answers["Profil-ID"] == id]
    if len(filtered_answers) == 0:
        return None
    sorted_answers = filtered_answers.sort_values(by="Speicherzeitpunkt", ascending=False)
    return sorted_answers["Speicherzeitpunkt"].values[0]

def get_latest_cluster_values(id):
    """
    Berechnet die Cluster-Werte aus dem aktuellsten Fragebogen für eine bestimmte Profil-ID.
    
    Args:
        id: Profil-ID für die die Cluster-Werte berechnet werden sollen
        
    Returns:
        list or None: Liste der Cluster-Werte oder None falls keine Antworten vorhanden
    """
    answers = pd.read_csv(PATH_ANSWERS, sep=';', index_col=0)
    filtered_answers = answers[answers["Profil-ID"] == id]
    if len(filtered_answers) == 0:
        return None
    sorted_answers = filtered_answers.sort_values(by="Speicherzeitpunkt", ascending=False)
    latest_answer = sorted_answers.iloc[0]
    return calculate_cluster_values(latest_answer)

def load_profiles_with_ids(csv_path: str) -> list[str]:
    """
    Liest eine CSV-Datei mit Profilen und gibt eine Liste von Strings im Format "ID, Name" zurück.
    TODO: An google Sheet anpassen; unter config.py Pfad anpassen.

    Args:
        csv_path (str): Pfad zur CSV-Datei (Semikolon-getrennt)

    Returns:
        list[str]: Eine Liste wie ["101, Fritz", "102, Peter", ...]
    """
    try:
        df = pd.read_csv(csv_path, sep=';')
        profiles = df.apply(lambda row: f"{row['Profil-ID']}, {row['Name']}", axis=1).tolist()
        return profiles
    except Exception as e:
        print(f"Error while loading the file: {e}")
        return []

def get_cluster_values_over_time(id, cluster_name):
    """
    Berechnet die Cluster-Werte für eine bestimmte Kategorie über die Zeit.
    
    Args:
        id: Profil-ID für die die Cluster-Werte berechnet werden sollen
        cluster_name (str): Name der Kategorie/des Clusters
        
    Returns:
        pandas.DataFrame: DataFrame mit Zeitpunkten und Cluster-Werten für die gegebene Kategorie
    """
    # Alle Antworten für die Profil-ID laden
    answers = pd.read_csv(PATH_ANSWERS, sep=';', index_col=0)
    filtered_answers = answers[answers["Profil-ID"] == id]
    
    if len(filtered_answers) == 0:
        return pd.DataFrame()
    
    # Nach Zeitpunkt sortieren
    sorted_answers = filtered_answers.sort_values(by="Speicherzeitpunkt", ascending=True)
    
    # Cluster-Nummer für die gegebene Kategorie finden
    fragebogen = pd.read_csv(PATH_QUESTIONNAIRE, sep=';', encoding='utf-8')
    cluster_data = fragebogen[fragebogen["Cluster-Name"] == cluster_name]
    cluster_number = int(cluster_data["Cluster-Nummer"].iloc[0])
    
    # Zeitpunkte und Cluster-Werte sammeln
    time_data = []
    cluster_values = []
    
    for _, row in sorted_answers.iterrows():
        # Cluster-Werte für diesen Zeitpunkt berechnen
        cluster_value = calculate_cluster_values(row)[cluster_number - 1]  # -1 weil Index bei 0 beginnt
        time_data.append(row["Speicherzeitpunkt"])
        cluster_values.append(cluster_value)
    
    # DataFrame erstellen
    result_df = pd.DataFrame({
        "Zeitpunkt": time_data,
        "Wert": cluster_values
    })
    
    return result_df

def load_bedarfe_from_google():
    """
    Lädt die Bedarfe aus der Google Tabelle.
    
    Returns:
        pandas.DataFrame: DataFrame mit den Bedarfen für alle Profile
    """
    # TODO: Implementierung für Google Sheets API
    # Für jetzt verwenden wir eine lokale CSV-Datei als Platzhalter
    try:
        # Platzhalter - später durch Google Sheets API ersetzen
        bedarfe_df = pd.read_csv("bedarfe/bedarfe.csv", sep=';', index_col=0)
        return bedarfe_df
    except FileNotFoundError:
        # Fallback: Erstelle leeren DataFrame mit korrekter Struktur
        columns = ['Speicherzeitpunkt', 'Profil-ID'] + [f'cluster{i}' for i in range(1, 12)]
        return pd.DataFrame(columns=columns, data=[])

def get_bedarfe_for_profile(profile_id):
    """
    Ruft die Bedarfe für eine bestimmte Profil-ID ab.
    
    Args:
        profile_id: Profil-ID für die die Bedarfe abgerufen werden sollen
        
    Returns:
        list or None: Liste der Bedarfe für alle 11 Cluster oder None falls nicht gefunden
    """
    bedarfe_df = load_bedarfe_from_google()
    
    # Suche nach der Profil-ID
    profile_bedarfe = bedarfe_df[bedarfe_df['Profil-ID'] == profile_id]
    
    if len(profile_bedarfe) == 0:
        return None
    
    # Nehme den neuesten Eintrag (falls mehrere vorhanden)
    sorted_bedarfe = profile_bedarfe.sort_values(by='Speicherzeitpunkt', ascending=False)
    latest_bedarfe = sorted_bedarfe.iloc[0]
    
    # Extrahiere die Cluster-Bedarfe (cluster1 bis cluster11)
    cluster_bedarfe = []
    for i in range(1, 12):
        cluster_bedarfe.append(latest_bedarfe[f'cluster{i}'])
    
    return cluster_bedarfe

def get_available_bedarfe_profiles():
    """
    Ruft alle verfügbaren Profil-IDs aus der Bedarfe-Tabelle ab.
    
    Returns:
        list: Liste der verfügbaren Profil-IDs
    """
    bedarfe_df = load_bedarfe_from_google()
    
    if bedarfe_df.empty:
        return []
    
    # Extrahiere eindeutige Profil-IDs
    available_profiles = bedarfe_df['Profil-ID'].unique().tolist()
    return sorted(available_profiles)

def calculate_cluster_differences(actual_profile_id, bedarfe_profile_id):
    """
    Berechnet die Differenzen zwischen tatsächlichen Cluster-Werten und Bedarfen.
    
    Args:
        actual_profile_id: Profil-ID für die tatsächlichen Werte
        bedarfe_profile_id: Profil-ID für die Bedarfe
        
    Returns:
        pandas.DataFrame: DataFrame mit Cluster-Namen und Differenzen
    """
    # Aktuelle Cluster-Werte laden
    actual_values = get_latest_cluster_values(actual_profile_id)
    if actual_values is None:
        return pd.DataFrame()
    
    # Bedarfe laden
    bedarfe_values = get_bedarfe_for_profile(bedarfe_profile_id)
    if bedarfe_values is None:
        return pd.DataFrame()
    
    # Cluster-Namen laden
    cluster_names = get_cluster_names()
    
    # Differenzen berechnen (Ist - Bedarf)
    differences = []
    for i in range(len(cluster_names)):
        diff = actual_values[i] - bedarfe_values[i]
        differences.append(diff)
    
    # DataFrame erstellen
    result_df = pd.DataFrame({
        'Cluster': cluster_names,
        'Differenz': differences
    })
    
    # Nach Differenz sortieren (größte negative zuerst)
    result_df = result_df.sort_values('Differenz', ascending=True)
    
    return result_df