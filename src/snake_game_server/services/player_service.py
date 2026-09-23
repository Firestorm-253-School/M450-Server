from snake_game_server.models.player import Player
from snake_game_server.models.game import Game


class PlayerService:
    def __init__(self):
        self.players: dict[str, Player] = {}

    def set_direction(self, player_id: str, direction: tuple[int, int]) -> None:
        player = self.players.get(player_id)
        if not player or not player.alive:
            return

        opposite = (-player.direction[0], -player.direction[1])
        if direction != opposite:
            player.direction = direction

    def move(self, player_id: str) -> None:
        player = self.players.get(player_id)
        if not player or not player.alive:
            return

        head_x, head_y = player.snake_body[0]
        dx, dy = player.direction
        new_head = (head_x + dx, head_y + dy)
        player.snake_body = [new_head] + player.snake_body[:-1]
        
    def get_or_create(self, player_id: str) -> Player:
        player = self.players.get(player_id)

        if player is None:
            player = Player(id=player_id)
            self.players[player_id] = player

        return player

    def join_game(self, player_id: str, game: Game) -> None:
        player = self.get_or_create(player_id)

        if game is None:
            return
        
        player.current_game = game

    def step(self, player: Player) -> bool:
        if player.current_game is None or not player.alive:
            return False
        
        self.set_direction(player.id, player.direction_to_set)

        old_tail = player.snake_body[-1]
        self.move(player.id)

        if self.head_hits_wall(player.id):
            player.alive = False
            return True
        
        if self.head_hits_snake(player.id):
            player.alive = False
            return True

        if self.head_is_on_apple(player):
            player.current_game.apples.remove(player.snake_body[0])
            player.snake_body.append(old_tail)

        return False


    def head_hits_wall(self, player_id: str) -> bool:
        player = self.players.get(player_id)
        if not player:
            return False
        return player.snake_body[0] in player.current_game.game_map.walls

    def head_hits_snake(self, player_id: str) -> bool:
        player = self.players.get(player_id)
        if not player:
            return False
        
        return player.snake_body[0] in [
            body_part
            for any_player in player.current_game.players.values()
            for body_part in (any_player.snake_body if any_player.id == player.id else any_player.snake_body[1:])
        ]
    
    def head_is_on_apple(self, player: Player) -> bool:
        return player.snake_body[0] in player.current_game.apples
