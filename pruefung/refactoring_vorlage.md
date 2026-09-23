# Prüfung 3

## Teil 1: Aufgabe 1

Codereview (drei Einträge genügen)

| Mangel im neuen Code                                                                                                 | Massnahme                                                                      | Wirkung auf die Testbarkeit             |
| -------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ | --------------------------------------- |
| in sichere() werden alle highscores in der fatei für den entsprechenden modus gespeichert, auch aus den anderen modi | nur highscores aus dem entsprechenden modi in der entsprechenden datei sichern |                                         |
| Dateizugriff und Logik sind vermischt                                                                                | lesen von Daten auslagern                                                      | Dateizugriff kann besser gemockt werden |
| Code ist schlecht leserlich (unverständliche variablennamen)                                                         | variablennamen besser wählen                                                   |                                         |

## Teil 2: Aufgabe 1

### Debugging-Protokoll (Mangel M-01)

**Fehlermeldung:**

Es gibt keine Fehlermeldung (es fehlen einfach Daten)

```text

```

**Fundstelle (Datei, Zeile):**
highscore_service.py - load_all()

**Ursache:**
load_all() wird zum start des Services nicht aufgerufen und somit werden die gespeicherten highscores nicht geladen

**Korrekturmassnahme:**

### Debugging-Protokoll (Mangel M-02)

**Fehlermeldung:**

Es gibt keine Fehlermeldung (Einträge sind doppelt)

```text

```

**Fundstelle (Datei, Zeile):**
highscore_service.py - load_all()

**Ursache:**
es werden alle highscores in allen modi abgespeichert, pro modus werden alle highscores in der datei geladen, somit werden alle highscored dreifach geladen

**Korrekturmassnahme:**
nur die highscores aus der datei lesen, welche den entsprechenden modus haben
und beim abspeichern, für jeden modi nur die highscores mit diesem modi sichern
