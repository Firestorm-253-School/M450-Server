import random
from dataclasses import dataclass, field

from .maps import CLASSIC, GameMap
from .player import Player


@dataclass
class Game:
    id: str
    players: dict[str, Player] = field(default_factory=dict)
    started: bool = False
    tick: int = 0
    apples: list[tuple[int, int]] = field(default_factory=list)
    apple_spawn_interval_ticks: int = 20
    max_apples: int = 3
    width: int = 24
    height: int = 18
    game_map: GameMap = field(default_factory=lambda: CLASSIC)

    def add_player(self, player: Player) -> None:
        self.players[player.id] = player
        player.current_game = self

    def remove_player(self, player_id: str) -> None:
        self.players.pop(player_id, None)

    def has_player(self, player_id: str) -> bool:
        return (player_id in self.players)

    def spawn_apple(self) -> None:
        if len(self.apples) >= self.max_apples:
            return

        occupied_positions = set(self.game_map.walls) | set(self.apples)
        for player in self.players.values():
            occupied_positions.update(player.snake_body)

        free_positions = [
            (x, y)
            for x in range(self.width)
            for y in range(self.height)
            if (x, y) not in occupied_positions
        ]

        if free_positions:
            self.apples.append(random.choice(free_positions))
