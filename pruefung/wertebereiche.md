# Prüfung 2 – Wertebereiche

Klasse: gültig, Grenzwert, ungültig (Negativfall), Spezialfall

## Funktion 1: `normalisiere_modus(modus)`

| ID  | Parameter | Klasse                 | Bereich / Beschreibung                           | Vertreter | Erwartetes Ergebnis |
| --- | --------- | ---------------------- | ------------------------------------------------ | --------- | ------------------- |
| 1.1 | modus     | gültig                 | String, der (klein geschrieben) in MODI vorkommt | "classic" | Rückgabe "classic"  |
| 1.2 | modus     | Spezialfall            | Gross- / Kleinschreibung wir ignoriert           | "PRO"     | Rückgabe "pro"      |
| 1.3 | modus     | ungültig (Negativfall) | String, aber nicht in MODI enthalten             | "Extrem"  | ValueError          |
| 1.4 | modus     | ungültig (Negativfall) | kein String (falscher Typ)                       | 42        | TypError            |

## Funktion 2: `speichere(name, score, modus)`

| ID  | Parameter | Klasse                 | Bereich / Beschreibung                                               | Vertreter      | Erwartetes Ergebnis   |
| --- | --------- | ---------------------- | -------------------------------------------------------------------- | -------------- | --------------------- |
| 2.1 | name      | gültig                 | String, Name bestent aus Buchstaben und Zahlen                       | "Sam10"        | wird gespeichert      |
| 2.2 | name      | ungültg (Negativfall)  | leerer String                                                        | ""             | ValueError            |
| 2.3 | name      | Grenzwert              | String, enthält genau 12 Zeichen                                     | "asedfrgwnghr" | wird gespeichert      |
| 2.4 | name      | Spezialfall            | kein String / Sonderzeichen oder Umlaute (isascii()/isalnum() false) | 123 bzw "Ännä" | TypError / ValueError |
| 2.5 | score     | gültig                 | positive ganze Zahl                                                  | 200            | wird gespeichert      |
| 2.6 | score     | ungültig (Negativfall) | Negative Zahl                                                        | -10            | ValueError            |
| 2.7 | score     | Grenzwert              | ist direkt 0                                                         | 0              | wird gespeichert      |
