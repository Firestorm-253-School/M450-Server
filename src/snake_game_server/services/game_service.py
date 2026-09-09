from uuid import uuid4

from snake_game_server.models.game import Game
from snake_game_server.models.player import Player


class GameService:
    def __init__(self, connection_manager):
        self.connection_manager = connection_manager
        self.games: dict[str, Game] = {}
        self.player_games: dict[str, str] = {}

    async def create_game(self, player: Player) -> Game:
        self._leave_current_game(player)

        game = Game(id=str(uuid4()))
        game.add_player(player)
        self.games[game.id] = game
        self.player_games[player.id] = game.id
        return game

    async def join_game(self, game_id: str, player: Player) -> Game:
        game = self.games.get(game_id)
        if game is None:
            raise ValueError(f"Game {game_id!r} does not exist")

        self._leave_current_game(player)
        game.add_player(player)
        self.player_games[player.id] = game.id
        return game

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

        if self.player_games.get(player.id) == game_id:
            self.player_games.pop(player.id, None)

    async def handle_message(
        self,
        player: Player,
        message: dict,
    ) -> dict:
        message_type = message.get("type")

        match message_type:
            case "create_game":
                game = await self.create_game(player)
                return {"type": "game_created", "game_id": game.id}

        match message_type:
            case "join_game":
                game_id = message.get("game_id")
                if not isinstance(game_id, str):
                    raise ValueError("join_game requires a game_id")

                game = await self.join_game(game_id, player)
                return {
                    "type": "game_joined",
                    "game_id": game.id,
                    "player_count": len(game.players),
            }

        match message_type:
            case "leave_game":
                game_id = self.player_games.get(player.id)
                if game_id is not None:
                    await self.remove_player_from_game(game_id, player)
                return {"type": "game_left", "game_id": game_id}

        raise ValueError(f"Unknown message type: {message_type!r}")

    def _leave_current_game(self, player: Player) -> None:
        game_id = self.player_games.pop(player.id, None)
        if game_id is None:
            return

        game = self.games.get(game_id)
        if game is not None:
            game.remove_player(player)
            if not game.players:
                self.games.pop(game_id)
