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
