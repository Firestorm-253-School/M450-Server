import os
import json

class HighscoreRepository:
  def __init__(self, directory):
    self.directory = directory

  def load(self, mode: str):
    p = self.directory + "/" + mode + ".json"

    if not os.path.exists(p):
        return []
    
    f = open(p, encoding="utf-8")
    d = json.load(f)
    f.close()
    return d

  def save(self, mode, highscores):
    os.makedirs(self.directory, exist_ok=True)
    f = open(self.directory + "/" + mode + ".json", "w", encoding="utf-8")
    json.dump(highscores, f)
    f.close()