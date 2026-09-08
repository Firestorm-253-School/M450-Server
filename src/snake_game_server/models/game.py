from dataclasses import dataclass, field

from .player import Player


@dataclass
class Game:
    id: str
    players: dict[str, Player] = field(default_factory=dict)
    started: bool = False
    tick: int = 0

    def add_player(self, player: Player) -> None:
        self.players[player.id] = player

    def remove_player(self, player: Player) -> None:
        self.players.pop(player.id, None)

    def has_player(self, player_id: str) -> bool:
        return player_id in self.players
