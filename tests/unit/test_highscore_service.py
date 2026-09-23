from snake_game_server.services.highscore_service import HighscoreService, HighscoreRepository
from unittest.mock import Mock

import pytest

@pytest.fixture
def highscore_repository():
  highscore_repository = Mock(HighscoreRepository)

  highscore_repository.load.return_value = []
  highscore_repository.save.return_value = None

  return highscore_repository


# Mängel 2
def test_highscores_load_only_from_same_mode(highscore_repository: Mock):

  def data(mode):
    match mode:
      case 'classic':
        return [{"name": "Janick", "modus": "medium", "score": 100}]
      case 'medium':
        return [{"name": "Janick", "modus": "medium", "score": 100}]
      case 'pro':
        return [{"name": "Janick", "modus": "pro", "score": 100}]
    

  highscore_repository.load.side_effect = data
  highscore_service = HighscoreService(highscore_repository)

  assert len(highscore_service.highscores) == 2

# T01
def test_add_first_highscore_persists(highscore_repository: Mock):

  highscore_repository.load.return_value = [{"name": "Janick", "modus": "pro", "score": 100}]
  highscore_service = HighscoreService(highscore_repository)

  entry = {"name": "Peter", "modus": "pro", "score": 50}

  highscore_service.save_permanently(highscore_repository, entry["name"], entry["score"], entry["modus"])

  highscore_repository.save.assert_called_once()

  assert len(highscore_service.highscores) == 2


# T02
def test_loads_all_highscores(highscore_repository: Mock):

  def data(mode):
    match mode:
      case 'classic':
        return [{"name": "Janick", "modus": "classic", "score": 100}]
      case 'medium':
        return [{"name": "Janick", "modus": "medium", "score": 100}]
      case 'pro':
        return [{"name": "Janick", "modus": "pro", "score": 100}]
    

  highscore_repository.load.side_effect = data
  highscore_service = HighscoreService(highscore_repository)

  assert len(highscore_service.highscores) == 3

# T03
def test_mode_invalid(highscore_repository: Mock):
  highscore_service = HighscoreService(highscore_repository)

  with pytest.raises(ValueError):
    highscore_service.save_permanently("janick", 20, "ultra")

# T04
def test_mode_letterspace_save(highscore_repository: Mock):
  highscore_service = HighscoreService(highscore_repository)

  highscore_service.save_permanently("janick", 20, "PRO")

  highscore_repository.save.assert_called_with("pro", [{"name": "janick", "score": 20, "modus": "pro"}])

