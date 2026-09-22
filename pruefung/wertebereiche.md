# Prüfung 2 – Wertebereiche

Klasse: gültig, Grenzwert, ungültig (Negativfall), Spezialfall

## Funktion 1: `normalisiere_modus(modus)`

| ID | Parameter | Klasse | Bereich / Beschreibung | Vertreter | Erwartetes Ergebnis |
| -- | --------- | ------ | ---------------------- | --------- | ------------------- |
|ANF-01|   modus |gültig| classic oder medium oder pro|   pro| ok                  |
|ANF-03| modus   |grenzfall(gültig)|str: kann gross oder keline sein (ClaSsic oder Medium oder) pro                     |    pRo       |        OK             |
|ANF-02|   modus |ungütlig|alles ausser die 3      |  test     |Value Error (ist ein unbekannter Spielmodus)  |

## Funktion 2: `speichere(name, score, modus)`

| ID | Parameter | Klasse | Bereich / Beschreibung | Vertreter | Erwartetes Ergebnis |
| -- | --------- | ------ | ---------------------- | --------- | ------------------- |
|ANF-05|name  | Gültig | str and int: betwen 1<= x >=12 zeichen|  max1        |      OK ("name": max1)|
|ANF-05|score    | Gütlig | 0<= Score             |  10         |    OK("score": 10)                 |
|ANF-05|modus    | Gütlig  |   classic oder medium oder pro     | pro          | OK("modus":"pro")                    |
|ANF-05|name     | grenzfall(gültig)       | 12                       | 12          |OK                     |
|ANF-05|score |grenzfall(gültig) |0 |0 |ok |
|ANF-03| modus   |grenzfall(gültig)|str: kann gross oder keline sein (ClaSsic oder Medium oder) pro                     |    pRo       |        OK             |
|ANF-05|name |ungültig(zulang) |str and int: x < 12 zeichen | maxmustemann12 |fehlermeldung |
|ANF-02 |   modus |ungütlig|alles ausser die 3      |  test     |Value Error (ist ein unbekannter Spielmodus) 
|ANF-05 |score |ungültig |x<0 |-1 |Fehlermeldung |
