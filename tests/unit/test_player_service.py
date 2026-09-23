import pytest

from snake_game_server.models.game import Game
from snake_game_server.models.maps import GameMap
from snake_game_server.services.player_service import PlayerService

@pytest.fixture
def player_service():
    return PlayerService()

@pytest.fixture
def player_with_game(player_service):
    player = player_service.get_or_create("p1")
    game = Game(id="g1")
    game.add_player(player)
    return player

def test_get_or_create_create_new_player(player_service):
    player = player_service.get_or_create("Test Player")

    assert player.id == "Test Player"
    assert "Test Player" in player_service.players

def test_get_or_create_returns_same_player(player_service):
    first = player_service.get_or_create("Test Player")
    second= player_service.get_or_create("Test Player")

    assert first is second
    assert len(player_service.players) == 1


def test_move_advances_head_in_current_direction(player_service, player_with_game):
    player = player_with_game
    player.snake_body = [(5, 5), (4, 5)]
    player.direction = (1, 0)

    player_service.move(player.id)

    assert player.snake_body[0] == (6, 5)


def test_move_keeps_body_length_constant(player_service, player_with_game):
    player = player_with_game
    player.snake_body = [(5, 5), (4, 5), (3, 5)]
    player.direction = (1, 0)

    player_service.move(player.id)

    assert len(player.snake_body) == 3


def test_set_direction_ignores_reversal(player_service, player_with_game):
    player = player_with_game
    player.direction = (1, 0)

    player_service.set_direction(player.id, (-1, 0))

    assert player.direction == (1, 0)


def test_set_direction_allows_turn(player_service, player_with_game):
    player = player_with_game
    player.direction = (1, 0)

    player_service.set_direction(player.id, (0, 1))

    assert player.direction == (0, 1)


def test_head_hits_wall_at_left_border(player_service, player_with_game):
    player = player_with_game
    player.snake_body = [(0, 5), (1, 5)]

    assert player_service.head_hits_wall(player.id)


def test_head_hits_wall_at_right_border(player_service, player_with_game):
    player = player_with_game
    player.snake_body = [(23, 5), (22, 5)]

    assert player_service.head_hits_wall(player.id)


def test_head_hits_wall_false_when_inside(player_service, player_with_game):
    player = player_with_game
    player.snake_body = [(12, 9), (11, 9)]

    assert not player_service.head_hits_wall(player.id)


def test_head_hits_wall_detects_inner_obstacle(player_service, player_with_game):
    player = player_with_game
    player.current_game.game_map = GameMap(
        width=24,
        height=18,
        walls=frozenset({(10, 10)}),
        start_positions=((0, 0),),
    )
    player.snake_body = [(10, 10), (9, 10)]

    assert player_service.head_hits_wall(player.id)


def test_head_is_on_apple_returns_true_when_head_on_apple(player_service, player_with_game):
    player = player_with_game
    player.snake_body = [(5, 5), (4, 5)]
    player.current_game.apples = [(5, 5)]

    assert player_service.head_is_on_apple(player)