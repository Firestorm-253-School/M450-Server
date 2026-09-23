import json
import os

MODI = ("classic", "medium", "pro")
NAME_MAX = 12
LEADERBOARD_SIZE = 10
HINWEIS_LEER = "Noch keine Spiele gespielt"
HINWEIS_LEER_MODUS = "Noch keine Spiele im Modus {modus}"
ORDNER = "daten"

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


def lade(m):
    p = ORDNER + "/" + m + ".json"
    if not os.path.exists(p):
        return []
    f = open(p, encoding="utf-8")
    d = json.load(f)
    f.close()
    return d


def sichere(m):
    os.makedirs(ORDNER, exist_ok=True)
    f = open(ORDNER + "/" + m + ".json", "w", encoding="utf-8")
    json.dump(highscores, f)
    f.close()


def lade_alle():
    highscores.clear()
    for m in MODI:
        for x in lade(m):
            highscores.append(x)


def speichere_dauerhaft(name, score, modus):
    eintrag = speichere(name, score, modus)
    sichere(eintrag["modus"])
    return eintrag
