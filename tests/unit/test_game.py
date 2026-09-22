from snake_game_server.models.game import Game


def test_move_advances_head_in_current_direction():
    game = Game(id="g1", snake_body=[(5, 5), (4, 5)], direction=(1, 0))
    game.move()
    assert game.snake_body[0] == (6, 5)


def test_move_keeps_body_length_constant():
    game = Game(id="g1", snake_body=[(5, 5), (4, 5), (3, 5)], direction=(1, 0))
    game.move()
    assert len(game.snake_body) == 3


def test_set_direction_ignores_reversal():
    game = Game(id="g1", snake_body=[(5, 5), (4, 5)], direction=(1, 0))
    game.set_direction((-1, 0))
    assert game.direction == (1, 0)


def test_set_direction_allows_turn():
    game = Game(id="g1", snake_body=[(5, 5), (4, 5)], direction=(1, 0))
    game.set_direction((0, 1))
    assert game.direction == (0, 1)


def test_head_hits_wall_at_left_border():
    game = Game(id="g1", snake_body=[(0, 5), (1, 5)])
    assert game.head_hits_wall()


def test_head_hits_wall_at_right_border():
    game = Game(id="g1", snake_body=[(23, 5), (22, 5)])
    assert game.head_hits_wall()


def test_head_hits_wall_false_when_inside():
    game = Game(id="g1", snake_body=[(12, 9), (11, 9)])
    assert not game.head_hits_wall()


def test_head_hits_wall_detects_inner_obstacle():
    game = Game(id="g1", snake_body=[(10, 10), (9, 10)], walls=frozenset({(10, 10)}))
    assert game.head_hits_wall()


def test_spawn_apple_adds_apple_on_free_position():
    game = Game(id="g1")

    game.spawn_apple()

    assert len(game.apples) == 1
    assert game.apples[0] not in game.snake_body
    assert game.apples[0] not in game.walls


def test_head_is_on_apple_returns_true_when_head_on_apple():
    game = Game(id="g1", snake_body=[(5, 5), (4, 5)], apples=[(5, 5)])

    assert game.head_is_on_apple()
