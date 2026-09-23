import os
import json

class HighscoreRepository:
    def __init__(self, folder: str):
        self.folder = folder

    def _get_file_path_from_modus(self, modus: str):
        return f"{self.folder}/{modus}.json"
        
    def lade(self, modus):
        file_path = self._get_file_path_from_modus(modus)
        if not os.path.exists(file_path):
            return []
        
        with open(file_path, encoding="utf-8") as file:
            data = json.load(file)
        return data

    def sichere(self, modus, highscores):
        os.makedirs(self.folder, exist_ok=True)

        file_path = self._get_file_path_from_modus(modus)

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(highscores, file)
