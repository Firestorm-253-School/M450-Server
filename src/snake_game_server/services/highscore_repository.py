import os
import json

class HighscoreRepository:
  def __init__(self, directory):
    self.directory = directory

  def load(self, mode: str):
    path = self.directory + "/" + mode + ".json"

    if not os.path.exists(path):
        return []
    
    file = open(path, encoding="utf-8")
    data = json.load(file)
    file.close()
    return data

  def save(self, mode, highscores):
    os.makedirs(self.directory, exist_ok=True)
    file = open(self.directory + "/" + mode + ".json", "w", encoding="utf-8")
    json.dump(highscores, file)
    file.close()