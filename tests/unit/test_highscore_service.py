from unittest import mock
from snake_game_server.services.highscore_service import uebersicht, speichere_dauerhaft, lade_alle, highscores
from snake_game_server.pruefung3.highscore_repository import HighscoreRepository


def test_uebersicht():
    mock_repository = mock.Mock(spec=HighscoreRepository)

    speichere_dauerhaft(name="Moritz", score=10, modus="classic", highscore_repository=mock_repository)
    speichere_dauerhaft(name="Mia", score=120, modus="pro", highscore_repository=mock_repository)
    speichere_dauerhaft(name="Max", score=130, modus="medium", highscore_repository=mock_repository)

    result = uebersicht()
    result_classic = uebersicht("classic")

    assert len(result.get("highscore")) == 3
    assert len(result_classic.get("highscore")) == 1


def test_T02():
    mock_repository = mock.Mock(spec=HighscoreRepository)
    mock_repository.lade.return_value = [{"name": "Moritz", "score": 10, "modus": "classic"}]

    lade_alle(mock_repository)

    assert len(highscores) == 1


