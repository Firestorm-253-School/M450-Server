import json
import os
from pathlib import Path

MODI = ("classic", "medium", "pro")
NAME_MAX = 12
LEADERBOARD_SIZE = 10
HINWEIS_LEER = "Noch keine Spiele gespielt"
HINWEIS_LEER_MODUS = "Noch keine Spiele im Modus {modus}"
ORDNER = Path("daten")

highscores: list[dict] = []

def normalisiere(modus: object) -> str:
    if not isinstance(modus, str):
        raise TypeError(f"'{modus}' muss ein String sein")
    normalisiert = modus.lower()
    if normalisiert not in MODI:
        raise ValueError(f"'{modus}' ist ein unbekannter Spielmodus")
    return normalisiert

def topten(modus: object | None = None) -> list[dict]:
    eintraege = highscores
    if modus is not None:
        gesucht = normalisiere(modus)
        eintraege = []

        for eintrag in highscores:
            if eintrag["modus"] == gesucht:
                eintraege.append(eintrag)

    return sorted(eintraege, key=lambda eintrag: eintrag["score"], reverse=True)[:LEADERBOARD_SIZE]

def uebersicht (modus: object | None = None) -> dict:
    eintraege = topten(modus)

    if eintraege:
        hinweis = ""
    elif modus is None:
        hinweis = HINWEIS_LEER
    else:
        hinweis = HINWEIS_LEER_MODUS.format(modus=normalisiere(modus))

    return {"highscore": eintraege, "hinweis": hinweis}


def speichere(name: object, score: object, modus: object) -> dict:
    if not isinstance(name, str):
        raise TypeError("name muss ein Text sein")
    if not 1 <= len(name) <= NAME_MAX:
        raise ValueError(f"name muss 1 bis {NAME_MAX} Zeichen lang sein")
    if not name.isascii() or not name.isalnum():
        raise ValueError("name darf nur Buchstaben und Ziffern enthalten")
    if isinstance(score, bool) or not isinstance(score, int):
        raise TypeError("score muss eine ganze Zahl sein")
    if score < 0:
        raise ValueError("score darf nicht negativ sein")

    eintrag = {"name": name, "score": score, "modus": normalisiere(modus)}
    highscores.append(eintrag)
    return eintrag


class HighscoreDatei:
    def __init__(self, ordner: Path = ORDNER):
        self.ordner = Path(ordner)

    def lade(self, modus: str) -> list[dict]:
        pfad1 = self.ordner / (modus + ".json")

        if not pfad1.exists():
            return []

        text = pfad1.read_text(encoding="utf-8")
        eintreage = json.loads(text)

        print("pfad")
        return eintreage

    
def lade(modus ):
    pfad = ORDNER + "/" + modus + ".json"
    if not os.path.exists(pfad):
        return []
    formatierung = open(pfad, encoding="utf-8")
    eintreage = json.load(formatierung)
    formatierung.close()
    print("pfad")
    return eintreage


def sichere(modus: str, datei:HighscoreDatei):
    os.makedirs(ORDNER, exist_ok=True)
    formatierung = open(ORDNER + "/" + modus + ".json", "w", encoding="utf-8")
    json.dump(highscores, formatierung)
    formatierung.close()


def lade_alle():
    highscores.clear()
    for modus in MODI:
        for x in lade(modus):
            highscores.append(x)


def speichere_dauerhaft(name, score, modus):
    eintrag = speichere(name, score, modus)
    sichere(eintrag["modus"])
    return eintrag
