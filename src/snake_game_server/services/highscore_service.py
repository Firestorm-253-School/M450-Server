from .highscore_repository import HighscoreRepository

MODI = ("classic", "medium", "pro")
NAME_MAX = 12
LEADERBOARD_SIZE = 10
HINWEIS_LEER = "Noch keine Spiele gespielt"
HINWEIS_LEER_MODUS = "Noch keine Spiele im Modus {modus}"
ORDNER = "daten"

class HighscoreService:
    highscores: list[dict] = []
    highscore_repository: HighscoreRepository

    def __init__(self, highscore_repository: HighscoreRepository):
        self.highscore_repository = highscore_repository
        self.load_all()

    def normalisiere(self, modus: object) -> str:
        if not isinstance(modus, str):
            raise TypeError(f"'{modus}' muss ein String sein")
        normalisiert = modus.lower()
        if normalisiert not in MODI:
            raise ValueError(f"'{modus}' ist ein unbekannter Spielmodus")
        return normalisiert

    def topten(self, modus: object | None = None) -> list[dict]:
        eintraege = self.highscores
        if modus is not None:
            gesucht = self.normalisiere(modus)
            eintraege = []

            for eintrag in self.highscores:
                if eintrag["modus"] == gesucht:
                    eintraege.append(eintrag)

        return sorted(eintraege, key=lambda eintrag: eintrag["score"], reverse=True)[:LEADERBOARD_SIZE]

    def uebersicht (self, modus: object | None = None) -> dict:
        eintraege = self.topten(modus)

        if eintraege:
            hinweis = ""
        elif modus is None:
            hinweis = HINWEIS_LEER
        else:
            hinweis = HINWEIS_LEER_MODUS.format(modus=self.normalisiere(modus))

        return {"highscore": eintraege, "hinweis": hinweis}


    def speichere(self, name: object, score: object, modus: object) -> dict:
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

        eintrag = {"name": name, "score": score, "modus": self.normalisiere(modus)}
        self.highscores.append(eintrag)
        return eintrag



    def save_mode(self, highscore_repository: HighscoreRepository, mode: str):
        mode_highscores = list(filter(lambda highscore: highscore["modus"] == mode, self.highscores))
        highscore_repository.save(mode, mode_highscores)


    def load_all(self):
        self.highscores.clear()
        for mode in MODI:
            mode_highscores = self.highscore_repository.load(mode)
            for highscore in mode_highscores:
                if(highscore["modus"] == mode):
                    self.highscores.append(highscore)


    def save_permanently(self, name, score, modus):
        highscore_entry = self.speichere(name, score, modus)
        self.save_mode(self.highscore_repository, highscore_entry["modus"])
        return highscore_entry


