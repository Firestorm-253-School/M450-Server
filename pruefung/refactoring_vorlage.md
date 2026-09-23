# Prüfung 3

## Teil 1: Aufgabe 1

Codereview (drei Einträge genügen)


| Mangel im neuen Code                              | Massnahme                                                                      | Wirkung auf die Testbarkeit       |
| ------------------------------------------------- | ------------------------------------------------------------------------------ | --------------------------------- |
| Variabeln sind nur buchstaben                     | variabeln richtig bennenen                                                     | Einfachere erkennung              |
| Fehler Werden nicht gehändelt gerät stürtzt ab    | Botentielle Fehler vorher schon entgegen nehmen und Fehlermeldung zurück geben | Besser erkennen was abgedeckt ist |
| Das zugreifen auf die daten nicht funktion selber | In eine eigene Klasse packen und funktionen nur noch auf daten schicken                                                                              | Test sind Konsistenter und kann andere test schreiben                                  |


## Teil 2: Aufgabe 1

Debugging-Protokoll (Mangel M-01)

**Fehlermeldung:**

```text
Keiner zumindest in der Konsole
```

**Fundstelle (Datei, Zeile):** Z.39 Highscore_Service

**Ursache:** Die funktion lade alle wurde nicht gecallt und die funktion lade alle hat nichts returned

**Korrekturmassnahme:** return eingefügt und lade_alle.