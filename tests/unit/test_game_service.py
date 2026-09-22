import asyncio
import pytest

from snake_game_server.services.game_service import GameService
from snake_game_server.sockets.connection_manager import ConnectionManager
from snake_game_server.models.player import Player
from snake_game_server.models.game import Game


class FakeConnectionManager:
    def __init__(self):
        self.sent: list[tuple[str, dict]] = []

    async def send_to_player(self, player_id: str, message: dict) -> None:
        self.sent.append((player_id, message))


@pytest.mark.anyio
async def test_set_direction_does_not_move_immediately():
    service = GameService(connection_manager=FakeConnectionManager())
    player = Player(id="p1")

    await service.handle_message(player=player, message={"type": "create_game"})
    response = await service.handle_message(
        player=player,
        message={"type": "set_direction", "direction": "up"},
    )

    assert response["type"] == "game_state"
    assert response["snake"][0] == [2, 2]


@pytest.mark.anyio
async def test_set_direction_starts_a_tick_loop_that_moves_the_snake():
    service = GameService(connection_manager=FakeConnectionManager())
    player = Player(id="p1")

    await service.handle_message(player=player, message={"type": "create_game"})
    game = service._require_current_game(player)
    start_head = game.snake_body[0]

    await service.handle_message(
        player=player,
        message={"type": "set_direction", "direction": "down"},
    )

    await asyncio.sleep(0.35)

    assert game.snake_body[0] != start_head
    service._stop_tick_loop(game.id)


@pytest.mark.anyio
async def test_tick_loop_ends_game_when_head_touches_border():
    connection_manager = FakeConnectionManager()
    service = GameService(connection_manager=connection_manager)
    player = Player(id="p1")

    await service.handle_message(player=player, message={"type": "create_game"})
    game = service._require_current_game(player)
    game.snake_body = [(1, 9), (2, 9)]
    game.direction = (-1, 0)

    await service.handle_message(
        player=player,
        message={"type": "set_direction", "direction": "left"},
    )

    await asyncio.sleep(0.25)

    assert game.alive is False
    assert game.id not in service.tick_tasks
    assert ("p1", {"type": "game_over", "game_id": game.id}) in connection_manager.sent


@pytest.mark.anyio
async def test_create_game_uses_requested_map():
    from snake_game_server.models.maps import PRO

    service = GameService(connection_manager=FakeConnectionManager())
    player = Player(id="p1")

    await service.handle_message(
        player=player,
        message={"type": "create_game", "map": "pro"},
    )
    game = service._require_current_game(player)

    assert game.walls == PRO.walls
    assert game.snake_body[0] == PRO.start_positions[0]


@pytest.mark.anyio
async def test_tick_loop_ends_game_when_head_hits_inner_wall():
    connection_manager = FakeConnectionManager()
    service = GameService(connection_manager=connection_manager)
    player = Player(id="p1")

    await service.handle_message(
        player=player,
        message={"type": "create_game", "map": "medium"},
    )
    game = service._require_current_game(player)
    # Medium hat ein Hindernis bei x=5-8, y=3; Kopf direkt davor platzieren.
    game.snake_body = [(4, 3), (3, 3)]
    game.direction = (1, 0)

    await service.handle_message(
        player=player,
        message={"type": "set_direction", "direction": "right"},
    )

    await asyncio.sleep(0.25)

    assert game.alive is False
    assert ("p1", {"type": "game_over", "game_id": game.id}) in connection_manager.sent


@pytest.mark.anyio
async def test_set_direction_rejects_unknown_direction():
    service = GameService(connection_manager=FakeConnectionManager())
    player = Player(id="p1")

    await service.handle_message(player=player, message={"type": "create_game"})

    with pytest.raises(ValueError):
        await service.handle_message(
            player=player,
            message={"type": "set_direction", "direction": "sideways"},
        )


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
