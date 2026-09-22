import asyncio
from uuid import uuid4
from typing import Union

from snake_game_server.models.game import Game
from snake_game_server.models.maps import DEFAULT_MAP_NAME, MAPS_BY_NAME
from snake_game_server.models.player import Player

DIRECTION_VECTORS = {
    "up": (0, -1),
    "down": (0, 1),
    "left": (-1, 0),
    "right": (1, 0),
}

TICK_INTERVAL_SECONDS = 0.15


class GameService:
    def __init__(self, connection_manager):
        self.connection_manager = connection_manager
        self.games: dict[str, Game] = {}
        self.player_games: dict[str, str] = {}
        self.tick_tasks: dict[str, asyncio.Task] = {}

    async def create_game(self, player: Player, map_name: str = DEFAULT_MAP_NAME) -> Game:
        self._leave_current_game(player)

        game_map = MAPS_BY_NAME.get(map_name, MAPS_BY_NAME[DEFAULT_MAP_NAME])
        start_x, start_y = game_map.start_positions[0]

        game = Game(
            id=str(uuid4()),
            walls=game_map.walls,
            snake_body=[(start_x, start_y), (start_x - 1, start_y)],
        )
        game.add_player(player)
        self.games[game.id] = game
        self.player_games[player.id] = game.id
        return game

    async def join_game(self, game_id: str, player: Player) -> Game:
        game = self.games.get(game_id)
        if game is None:
            return None

        if self.player_games.get(player.id) != game_id:
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
            self._stop_tick_loop(game_id)
            self.games.pop(game_id)

        if self.player_games.get(player.id) == game_id:
            self.player_games.pop(player.id, None)

    async def handle_message(
        self,
        player: Player,
        message: dict,
    ) -> Union[dict, None]:
        message_type = message.get("type")

        match message_type:
            case "create_game":
                map_name = message.get("map", DEFAULT_MAP_NAME)
                game = await self.create_game(player, map_name)
                return {"type": "game_created", "game_id": game.id}

            case "join_game":
                game_id = message.get("game_id")
                if not isinstance(game_id, str):
                    raise ValueError("join_game requires a game_id")

                game = await self.join_game(game_id, player)
                
                if game is None:
                    return {
                        "type": "game_join_failed",
                        "game_id": None,
                        "player_count": None,
                    }
                
                return {
                    "type": "game_joined",
                    "game_id": game.id,
                    "player_count": len(game.players),
                }

            case "leave_game":
                game_id = self.player_games.get(player.id)
                if game_id is not None:
                    await self.remove_player_from_game(game_id, player)
                return {"type": "game_left", "game_id": game_id}
            
            case "set_direction":
                game = self._require_current_game(player)

                direction_name = message.get("direction")
                direction = DIRECTION_VECTORS.get(direction_name)
                if direction is None:
                    raise ValueError(f"Unknown direction: {direction_name!r}")

                game.set_direction(direction)

                if not game.started:
                    game.started = True
                    self._start_tick_loop(game)

                return self._game_state_message(game)
            
            case _:
                return None
       
        

    def _game_state_message(self, game: Game) -> dict:
        return {
            "type": "game_state",
            "game_id": game.id,
            "snake": [list(position) for position in game.snake_body],
        }

    def _start_tick_loop(self, game: Game) -> None:
        if game.id in self.tick_tasks:
            return
        self.tick_tasks[game.id] = asyncio.create_task(self._tick_loop(game))

    def _stop_tick_loop(self, game_id: str) -> None:
        task = self.tick_tasks.pop(game_id, None)
        if task is not None:
            task.cancel()

    async def _tick_loop(self, game: Game) -> None:
        try:
            while game.id in self.games:
                await asyncio.sleep(TICK_INTERVAL_SECONDS)
                game.move()

                if game.head_hits_wall():
                    game.alive = False
                    await self._broadcast(game, {"type": "game_over", "game_id": game.id})
                    return

                await self._broadcast(game, self._game_state_message(game))
        except asyncio.CancelledError:
            pass
        finally:
            self.tick_tasks.pop(game.id, None)

    async def _broadcast(self, game: Game, message: dict) -> None:
        for player_id in list(game.players):
            await self.connection_manager.send_to_player(player_id, message)

    def _require_current_game(self, player: Player) -> Game:
        game_id = self.player_games.get(player.id)
        game = self.games.get(game_id) if game_id is not None else None
        if game is None:
            raise ValueError("Player is not currently in a game")
        return game

    def _leave_current_game(self, player: Player) -> None:
        game_id = self.player_games.pop(player.id, None)
        if game_id is None:
            return

        game = self.games.get(game_id)
        if game is not None:
            game.remove_player(player)
            if not game.players:
                self._stop_tick_loop(game_id)
                self.games.pop(game_id)
