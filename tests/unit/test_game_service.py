import pytest
from snake_game_server.services.game_service import GameService
from snake_game_server.sockets.connection_manager import ConnectionManager
from snake_game_server.models.player import Player
from snake_game_server.models.game import Game

@pytest.fixture
async def game_service():
    connection_manager = ConnectionManager()
    return GameService(connection_manager)

@pytest.fixture
async def player():
    return Player(id="Test Player")

@pytest.mark.parametrize("message", [
    {"type": "create_game"}
])
@pytest.mark.anyio
async def test_handle_message_create_game(message, game_service, player):
    result = await game_service.handle_message(player, message)

    assert result is not None
    assert result["type"] == "game_created"
    assert result["game_id"] is not None
    game = game_service.games[result["game_id"]]
    assert player.id in game.players
    assert game.started is False
    assert game.tick == 0


@pytest.fixture
async def game_service_with_games():
    connection_manager = ConnectionManager()
    game_service = GameService(connection_manager)

    player = Player(id=555)
    game = await game_service.create_game(player)
    game.id = "123"
    game_service.games = { game.id: game }
    return game_service

@pytest.mark.parametrize("message, expected", [
    ({"type": "join_game", "game_id": "123"}, True),
    ({"type": "join_game", "game_id": "456"}, False)
])
@pytest.mark.anyio
async def test_handle_message_join_game(message, expected, game_service_with_games, player):
    result = await game_service_with_games.handle_message(player, message)
    assert result is not None
    
    assert (result["game_id"] is not None) == expected

    if result["game_id"] is not None:
        assert result["type"] == "game_joined"
        game = game_service_with_games.games[result["game_id"]]
        assert player.id in game.players
        assert game.started is False
        assert game.tick == 0
    else:
        assert result["type"] == "game_join_failed"
        


@pytest.mark.parametrize("message", [
    {"type": "leave_game", "game_id": "123"},
    {"type": "leave_game", "game_id": "456"}
])
@pytest.mark.anyio
async def test_handle_message_leave_game(message, game_service, player):
    result = await game_service.handle_message(player, message)

    assert result is not None
    assert result["type"] == "game_left"

    if result["game_id"] is not None:
        game = game_service.games[result["game_id"]]
        assert player.id not in game.players
        assert game.started is False
        assert game.tick == 0
    else:
        assert game_service.player_games.get(player.id) is None
