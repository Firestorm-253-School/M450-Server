from snake_game_server.models.game import Game
from snake_game_server.models.player import Player


def test_spawn_apple_adds_apple_on_free_position():
    player = Player(id="p1")
    game = Game(id="g1")
    game.add_player(player)

    game.spawn_apple()

    assert len(game.apples) == 1
    assert game.apples[0] not in player.snake_body
    assert game.apples[0] not in game.game_map.walls
