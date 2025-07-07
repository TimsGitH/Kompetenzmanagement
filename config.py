# Datei zur Konfiguration von Variablen, die in mehreren Dateien verwendet werden können.

# -Fragebogen-
# Mögliche Antworten für die Fragen
OPTIONS_FORM = ("trifft nicht zu", "trifft eher nicht zu", "teils-teils", "trifft eher zu", "trifft zu")

# Anzahl Fragen pro Seite im Fragebogen
AMOUNT_QUESTIONS_PER_PAGE = 12

# Übersetzungstabellen
TRANSLATE_ANSWER_SAVE = {
    "trifft nicht zu": 1, 
    "trifft eher nicht zu": 2, 
    "teils-teils": 3, 
    "trifft eher zu": 4, 
    "trifft zu": 5,
    None: 0
}
TRANSLATE_ANSWER_INDEX = {
    "trifft nicht zu": 0, 
    "trifft eher nicht zu": 1, 
    "teils-teils": 2, 
    "trifft eher zu": 3, 
    "trifft zu": 4,
    None: None
}

