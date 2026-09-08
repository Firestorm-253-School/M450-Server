from snake_game_server.models.game import Game
from snake_game_server.models.player import Player


class GameService:
    def __init__(self, connection_manager):
        self.connection_manager = connection_manager
        self.games: dict[str, Game] = {}

    async def add_player_to_game(
        self,
        game_id: str,
        player: Player,
    ) -> Game:
        game = self.games.setdefault(
            game_id,
            Game(id=game_id),
        )
        game.add_player(player)
        return game

    async def remove_player_from_game(
        self,
        game_id: str,
        player: Player,
    ) -> None:
        game = self.games.get(game_id)
        if game is None:
            return

        game.remove_player(player)

        if not game.players:
            self.games.pop(game_id)
