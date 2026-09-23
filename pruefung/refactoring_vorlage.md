# Prüfung 3

## Teil 1: Aufgabe 1

Codereview (drei Einträge genügen)

| Mangel im neuen Code                                                                     | Massnahme                            | Wirkung auf die Testbarkeit           |
| ---------------------------------------------------------------------------------------- | ------------------------------------ | ------------------------------------- |
| Globaler, veränderlicher Zustand highscores: list[dict] = [] auf Modulebene              | State kapseln, pro Test zurücksetzen | Tests beeinflussen sich gegenseitig   |
| Dateizugriff direkt in lade()/sichere() (open(), os.path.exists(), hartcodierter ORDNER) | Dateizugriff auslagern und mocken    | Tests brauchen echte Dateien, langsam |
| Unklare Namen (m, p, f, d, x in lade, sichere, lade_alle)                                | Sprechende Namen verwenden           | Unklar, was genau getestet wird       |

## Teil 2: Aufgabe 1

Debugging-Protokoll (Mangel M-01)

**Fehlermeldung:**

```text

```

**Fundstelle (Datei, Zeile):** highscore_service.py Zeile 100

**Ursache:** Wenn alle geladen werden sollen wird immer highscores.clear() ausgeführt.

**Korrekturmassnahme:**
