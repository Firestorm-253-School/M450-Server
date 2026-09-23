import asyncio
import pytest

from snake_game_server.services.game_service import GameService
from snake_game_server.services.player_service import PlayerService
from snake_game_server.sockets.connection_manager import ConnectionManager
from snake_game_server.models.player import Player
from snake_game_server.models.game import Game
from snake_game_server.models.maps import PRO


class FakeConnectionManager:
    def __init__(self):
        self.sent: list[tuple[str, dict]] = []

    async def send_to_player(self, player_id: str, message: dict) -> None:
        self.sent.append((player_id, message))

@pytest.fixture
def fakeGame_service():
    return GameService(connection_manager=FakeConnectionManager())

@pytest.fixture
def player_service():
    return PlayerService()

@pytest.fixture
async def game_service():
    connection_manager = ConnectionManager()
    return GameService(connection_manager)

@pytest.fixture
def test_player(player_service):
    return player_service.get_or_create("Test Player")

@pytest.fixture
def add_player_to_game(game_service, player_service):
    def _add(player: Player, game_id: str) -> Game:
        player_service.players[player.id] = player
        game = Game(id=game_id)
        game.add_player(player)
        game_service.games[game_id] = game
        game_service.player_games[player.id] = game_id
        return game
    return _add

@pytest.fixture
def game_service_with_games(game_service, add_player_to_game):
    add_player_to_game(Player(id="Player 2"), "123")
    return game_service


@pytest.mark.anyio
async def test_set_direction_does_not_move_immediately(game_service_with_games, player_service):    
    game = list(game_service_with_games.games.values())[0]
    player = list(game.players.values())[0]

    response = await game_service_with_games.handle_message(
        player=player,
        message={"type": "set_direction", "direction": "up"},
        player_service=player_service
    )

    assert response["type"] == "game_state"
    assert response["snake"][0] == [2, 2]


@pytest.mark.anyio
async def test_set_direction_starts_a_tick_loop_that_moves_the_snake(game_service, player_service, test_player):
    await game_service.handle_message(
        player=test_player,
        message={"type": "create_game"},
        player_service=player_service,
    )
    game = game_service._require_current_game(test_player)
    start_head = test_player.snake_body[0]

    await game_service.handle_message(
        player=test_player,
        message={"type": "set_direction", "direction": "down"},
        player_service=player_service
    )

    await asyncio.sleep(0.35)

    assert test_player.snake_body[0] != start_head
    game_service._stop_tick_loop(game.id)


@pytest.mark.anyio
async def test_tick_loop_ends_game_when_head_touches_border(fakeGame_service, player_service, test_player):
    await fakeGame_service.handle_message(
        player=test_player,
        message={"type": "create_game"},
        player_service=player_service,
    )
    game = fakeGame_service._require_current_game(test_player)
    test_player.snake_body = [(1, 9), (2, 9)]
    test_player.direction = (-1, 0)

    await fakeGame_service.handle_message(
        player=test_player,
        message={"type": "set_direction", "direction": "left"},
        player_service=player_service
    )

    await asyncio.sleep(0.25)

    assert test_player.alive is False
    assert game.id not in fakeGame_service.tick_tasks
    assert ("Test Player", {"type": "game_over", "game_id": game.id}) in fakeGame_service.connection_manager.sent


@pytest.mark.anyio
async def test_create_game_uses_requested_map(game_service, player_service, test_player):
    await game_service.handle_message(
        player=test_player,
        message={"type": "create_game", "map": "pro"},
        player_service=player_service
    )
    game = test_player.current_game

    assert game.game_map.walls == PRO.walls
    assert test_player.snake_body[0] == PRO.start_positions[0]


@pytest.mark.anyio
async def test_tick_loop_ends_game_when_head_hits_inner_wall(fakeGame_service, player_service, test_player):
    await fakeGame_service.handle_message(
        player=test_player,
        message={"type": "create_game", "map": "medium"},
        player_service=player_service
    )
    game = test_player.current_game
    # Medium hat ein Hindernis bei x=5-8, y=3; Kopf direkt davor platzieren.
    test_player.snake_body = [(4, 3), (3, 3)]
    test_player.direction = (1, 0)

    await fakeGame_service.handle_message(
        player=test_player,
        message={"type": "set_direction", "direction": "right"},
        player_service=player_service
    )

    await asyncio.sleep(0.25)

    assert test_player.alive is False
    assert ("Test Player", {"type": "game_over", "game_id": game.id}) in fakeGame_service.connection_manager.sent


@pytest.mark.anyio
async def test_set_direction_rejects_unknown_direction(game_service_with_games, player_service):
    game = list(game_service_with_games.games.values())[0]
    player = list(game.players.values())[0]

    with pytest.raises(ValueError):
        await game_service_with_games.handle_message(
            player=player,
            message={"type": "set_direction", "direction": "sideways"},
            player_service=player_service,
        )



@pytest.mark.anyio
async def test_handle_message_create_game(game_service, player_service, test_player):
    message = {"type": "create_game"}
    
    result = await game_service.handle_message(
        player=test_player,
        message=message,
        player_service=player_service
    )

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
async def test_handle_message_join_game(message, expected, game_service_with_games, player_service, test_player):
    result = await game_service_with_games.handle_message(
        player=test_player,
        message=message,
        player_service=player_service
    )
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
async def test_handle_message_leave_game(has_current_game, game_service, player_service, add_player_to_game, test_player):
    game_id = "123" if has_current_game else None
    if has_current_game:
        add_player_to_game(test_player, game_id)

    result = await game_service.handle_message(
        player=test_player,
        message={"type": "leave_game"},
        player_service=player_service
    )

    assert result == {"type": "game_left", "game_id": game_id}
    assert game_service.player_games.get(test_player.id) is None
    if has_current_game:
        assert game_id not in game_service.games


@pytest.mark.anyio
async def test_handle_message_unknown_type_returns_none(game_service, player_service, test_player):
    result = await game_service.handle_message(
        player=test_player,
        message={"type": "not_a_real_type"},
        player_service=player_service
    )

    assert result is None


@pytest.mark.anyio
async def test_handle_message_join_game_without_game_id_raises(game_service, player_service, test_player):
    with pytest.raises(ValueError):
        await game_service.handle_message(
            player=test_player,
            message={"type": "join_game"},
            player_service=player_service
        )


@pytest.mark.anyio
async def test_game_state_contains_apples():
    service = GameService(connection_manager=FakeConnectionManager())
    player_service = PlayerService()
    player = player_service.get_or_create("p1")

    await service.handle_message(
        player=player,
        message={"type": "create_game"},
        player_service=player_service,
    )
    game = service._require_current_game(player)

    response = service._game_state_message(game, player)

    assert "apples" in response
    assert len(response["apples"]) == 1


@pytest.mark.anyio
async def test_snake_eats_apple_removes_apple_and_grows():
    service = GameService(connection_manager=FakeConnectionManager())
    player_service = PlayerService()
    player = player_service.get_or_create("p1")

    await service.handle_message(
        player=player,
        message={"type": "create_game"},
        player_service=player_service,
    )
    game = service._require_current_game(player)

    player.snake_body = [(5, 5), (4, 5)]
    player.direction = (1, 0)
    game.apples = [(6, 5)]

    await service.handle_message(
        player=player,
        message={"type": "set_direction", "direction": "right"},
        player_service=player_service,
    )

    await asyncio.sleep(0.2)

    service._stop_tick_loop(game.id)

    assert player.snake_body[0] == (6, 5)
    assert len(player.snake_body) == 3
    assert game.apples == []


@pytest.mark.anyio
async def test_apple_spawns_after_spawn_interval():
    service = GameService(connection_manager=FakeConnectionManager())
    player_service = PlayerService()
    player = player_service.get_or_create("p1")

    await service.handle_message(
        player=player,
        message={"type": "create_game"},
        player_service=player_service,
    )
    game = service._require_current_game(player)

    game.apples = []
    game.apple_spawn_interval_ticks = 1

    await service.handle_message(
        player=player,
        message={"type": "set_direction", "direction": "down"},
        player_service=player_service,
    )

    await asyncio.sleep(0.2)

    service._stop_tick_loop(game.id)

    assert len(game.apples) == 1
