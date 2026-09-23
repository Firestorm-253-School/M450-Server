# Prüfung 3 

## Teil 1: Aufgabe 1
Codereview (drei Einträge genügen)

| Mangel im neuen Code | Massnahme | Wirkung auf die Testbarkeit |
|----------------------| --------- | --------------------------- |
| bad variable naming | nützliche und akkurate variabel namen geben. | erleichtert lesbarkeit, auch wenn nicht direkt testing. |
| open() sollte "with open(file, 'r') as infile: ..." | (siehe mangel) | - |
| copy paste path definition | file_path auslagern in extra funktion | HighscoreRepository._get_file_path_from_modus() kann separat getestet werden. |

## Teil 2: Aufgabe 1 
Debugging-Protokoll (Mangel M-01)

**Fehlermeldung:**

```text
Beim neustart werden keine Daten geladen.
```

**Fundstelle (Datei, Zeile):**
api/highscores.py:11
services/highscore_services.py:60
ganzer trace-stack

**Ursache:**
api-get wird aufgerufen, ohne das jemals davor highscore_service.lade_alle() aufgerufen wird.

**Korrekturmassnahme:**
highscore_service.lade_alle() zb global von highscore_service aufrufen, oder bei api-get (obwohl sub optimal, siehe performance).