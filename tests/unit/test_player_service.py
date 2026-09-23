import pytest

from snake_game_server.services.player_service import PlayerService

@pytest.fixture
def player_service():
    return PlayerService()

def test_get_or_create_create_new_player(player_service):
    player = player_service.get_or_create("Test Player")

    assert player.id == "Test Player"
    assert "Test Player" in player_service.players

def test_get_or_create_returns_same_player(player_service):
    first = player_service.get_or_create("Test Player")
    second= player_service.get_or_create("Test Player")

    assert first is second
    assert len(player_service.players) == 1