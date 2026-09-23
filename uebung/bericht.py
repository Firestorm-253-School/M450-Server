import json
from datetime import date
from pathlib import Path

ORDNER = Path("uebung/daten")
ANZAHL_BESTE = 3
HINWEIS_LEER = "Noch keine Spiele in diesem Modus"


class HighscoreDatei:
    def __init__(self, ordner: Path = ORDNER):
        self.ordner = Path(ordner)

    def lade(self, modus: str) -> list[dict]:
        pfad = self.ordner / (modus + ".json")

        if not pfad.exists():
            return []

        text = pfad.read_text(encoding="utf-8")
        eintraege = json.loads(text)

        return eintraege


def beste(eintraege: list[dict], anzahl: int = ANZAHL_BESTE) -> list[dict]:
    sortierte_eintraege = sorted(eintraege, key=lambda eintrag: eintrag["score"], reverse=True)
    return sortierte_eintraege[:anzahl]


def durchschnitt(eintraege: list[dict]) -> float:
    if not eintraege:
        return 0.0

    scores = []

    for eintrag in eintraege:
        scores.append(eintrag["score"])

    ergebnis = sum(scores) / len(scores)
    return round(ergebnis, 1)


def formatiere(modus: str, eintraege: list[dict], datum: date) -> str:
    zeilen = []

    datum_text = datum.strftime("%d.%m.%Y")
    erste_zeile = "Bericht " + modus + " vom " + datum_text

    zeilen.append(erste_zeile)

    if not eintraege:
        zeilen.append(HINWEIS_LEER)
    else:
        beste_eintraege = beste(eintraege)
        rang = 1
        for eintrag in beste_eintraege:
            name = eintrag["name"]
            score = eintrag["score"]
            zeile = str(rang) + ". " + name + " " + str(score)
            zeilen.append(zeile)
            rang = rang + 1

        mittelwert = durchschnitt(eintraege)

        zeilen.append("Durchschnitt: " + str(mittelwert))

    text = "\n".join(zeilen)

    return text + "\n"


def erstelle_bericht(modus: str, datei: HighscoreDatei, heute: date) -> str:
    eintraege = datei.lade(modus)

    bericht = formatiere(modus, eintraege, heute)

    return bericht


if __name__ == "__main__":
    import sys
    modus = sys.argv[1]
    datei = HighscoreDatei()
    heute = date.today()
    bericht = erstelle_bericht(modus, datei, heute)
    print(bericht)