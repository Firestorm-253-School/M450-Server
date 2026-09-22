import asyncio

import pytest

from snake_game_server.models.player import Player
from snake_game_server.services.game_service import GameService


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
