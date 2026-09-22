# Prüfung 2 – Wertebereiche

Klasse: gültig, Grenzwert, ungültig (Negativfall), Spezialfall

## Funktion 1: `normalisiere(modus)`

| ID  | Parameter | Klasse                | Bereich / Beschreibung                                                     | Vertreter    | Erwartetes Ergebnis                                     |
| --- | --------- | --------------------- | -------------------------------------------------------------------------- | ------------ | ------------------------------------------------------- |
|     | modus     | gültig                | "classic", "medium", oder "pro"                                            | "CLASSIC"    | returned "classic"                                      |
|     | modus     | Sepzialfall ungültig  | empty string "", oder " "                                                  | " "          | raise ValueError(f"' ' ist ein unbekannter Spielmodus") |
|     | modus     | ungültig              | irgend ein anderes non string object                                       | 4.21 (float) | raise TypeError(f"'4.21' muss ein String sein")         |
|     | modus     | Spezialfall/Grenzwert | "classic", "medium", oder "pro", aber jegliche buchstaben gross oder klein | "cLASSiC     | returned "classic"                                      |

Hier gibt es nicht wirklich klassische Grenzwerte wie bei Zahlen. (Aufgabe 2)

## Funktion 2: `speichere(name, score, modus)`

| ID  | Parameter | Klasse              | Bereich / Beschreibung                                  | Vertreter       | Erwartetes Ergebnis                                                |
| --- | --------- | ------------------- | ------------------------------------------------------- | --------------- | ------------------------------------------------------------------ |
|     | name      | Sonderfall ungültig | empty string "" or " "                                  | ""              | raise ValueError("name darf nur Buchstaben und Ziffern enthalten") |
|     | name      | Sonderfall ungültig | jegliche non string objects                             | 239 (int)       | raise TypeError("name muss ein Text sein")                         |
|     | name      | gültig              | string aus buchstaben & zahlen und kleiner als NAME_MAX | "Laurin"        | returned {"name": "Laurin", ...}                                   |
|     | name      | Grenzwert gültig    | string mit länge NAME_MAX (12)                          | "IchBinLaurin"  | returned {"name": "IchBinLaurin", ...}                             |
|     | name      | Grenzwert ungültig  | string mit länge 13                                     | "IchBinLaurin2" | raise ValueError(f"name muss 1 bis {NAME_MAX} Zeichen lang sein")  |
