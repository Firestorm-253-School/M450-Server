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
async def test_player():
    return Player(id="Test Player")

@pytest.fixture
def add_player_to_game(game_service):
    def _add(player: Player, game_id: str) -> Game:
        game = Game(id=game_id)
        game.add_player(player)
        game_service.games[game_id] = game
        game_service.player_games[player.id] = game_id
        return game
    return _add

@pytest.fixture
def game_service_with_games(game_service, add_player_to_game):
    add_player_to_game(Player(id="Test Player"), "123")
    return game_service


@pytest.mark.parametrize("message", [
    {"type": "create_game"}
])
@pytest.mark.anyio
async def test_handle_message_create_game(message, game_service, test_player):
    result = await game_service.handle_message(test_player, message)

    assert result is not None
    assert result["type"] == "game_created"
    assert result["game_id"] is not None
    game = game_service.games[result["game_id"]]
    assert test_player.id in game.players
    assert game.started is False
    assert game.tick == 0


@pytest.mark.parametrize("message, expected", [
    ({"type": "join_game", "game_id": "123"}, True),
    ({"type": "join_game", "game_id": "456"}, False)
])
@pytest.mark.anyio
async def test_handle_message_join_game(message, expected, game_service_with_games, test_player):
    result = await game_service_with_games.handle_message(test_player, message)
    assert result is not None
    
    assert (result["game_id"] is not None) == expected

    if result["game_id"] is not None:
        assert result["type"] == "game_joined"
        game = game_service_with_games.games[result["game_id"]]
        assert test_player.id in game.players
        assert game.started is False
        assert game.tick == 0
    else:
        assert result["type"] == "game_join_failed"
        


@pytest.mark.parametrize("has_current_game", [False, True])
@pytest.mark.anyio
async def test_handle_message_leave_game(has_current_game, game_service, add_player_to_game, test_player):
    game_id = "123" if has_current_game else None
    if has_current_game:
        add_player_to_game(test_player, game_id)

    result = await game_service.handle_message(test_player, {"type": "leave_game"})

    assert result == {"type": "game_left", "game_id": game_id}
    assert game_service.player_games.get(test_player.id) is None
    if has_current_game:
        assert game_id not in game_service.games


@pytest.mark.anyio
async def test_handle_message_unknown_type_returns_none(game_service, test_player):
    result = await game_service.handle_message(test_player, {"type": "not_a_real_type"})

    assert result is None


@pytest.mark.anyio
async def test_handle_message_join_game_without_game_id_raises(game_service, test_player):
    with pytest.raises(ValueError):
        await game_service.handle_message(test_player, {"type": "join_game"})
