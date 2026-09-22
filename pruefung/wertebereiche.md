# Prüfung 2 – Wertebereiche

Klasse: gültig, Grenzwert, ungültig (Negativfall), Spezialfall

## Funktion 1: `normalisiere_modus(modus)`

| ANF-ID | Parameter | Klasse                 | Bereich / Beschreibung                                  | Vertreter | Erwartetes Ergebnis |
| ------ | --------- | ---------------------- | ------------------------------------------------------- | --------- | ------------------- |
| ANF-02 | modus     | ungültig (Negativfall) | nicht "classic", "medium", "pro"                        | "ultra"   | ValueError          |
| ANF-01 | modus     | gültig                 | "classic", "medium", "pro"                              | "classic" | "classic"           |
| ANF-02 | modus     | ungültig (Negativfall) | kein string                                             | None      | TypeError           |
| ANF-01 | modus     | Spezialfall            | "classic", "medium", "pro" Gross / Kleinschreibung egal | "MedIuM"  | "medium"            |

## Funktion 2: `speichere(name, score, modus)`

| ANF-ID | Parameter | Klasse                 | Bereich / Beschreibung                                                                 | Vertreter       | Erwartetes Ergebnis                                     |
| ------ | --------- | ---------------------- | -------------------------------------------------------------------------------------- | --------------- | ------------------------------------------------------- |
| ANF-05 | name      | ungültig (Negativfall) | kein string                                                                            | None            | TypeError                                               |
| ANF-05 | name      | ungültig (Negativfall) | leerer string                                                                          | ""              | ValueError                                              |
| ANF-05 | name      | gültig                 | string von buchstaben und zahlen mit 1 - 12 Zeichen                                    | "H4llo"         | highscores hat ein neues element {"name": "H4llo", ...} |
| ANF-05 | name      | ungültig (Negativfall) | string von buchstaben und zahlen ab 13 Zeichen                                         | "HelloWorld123" | ValueError                                              |
| ANF-05 | name      | ungültig (Negativfall) | string mit 1 - 12 Zeichen (enthält mindestens ein (nicht buchstabe oder zahl)-Zeichen) | ",.=?"          | ValueError                                              |
| ANF-05 | score     | ungültig (Negativfall) | kein string                                                                            | None            | TypeError                                               |
| ANF-05 | score     | gültig (Grenzwert)     | positive Zahl                                                                          | 0               | ValueError                                              |
| ANF-05 | score     | gültig (Grenzwert)     | positive Zahl                                                                          | 10              | highscores hat ein neues element {"score": 10, ...}     |
| ANF-05 | score     | Spezialfall (ungültig) | bool                                                                                   | True            | Type Error                                              |
