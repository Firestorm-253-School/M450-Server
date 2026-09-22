from dataclasses import dataclass, field

from .maps import CLASSIC
from .player import Player


@dataclass
class Game:
    id: str
    players: dict[str, Player] = field(default_factory=dict)
    started: bool = False
    tick: int = 0
    snake_body: list[tuple[int, int]] = field(
        default_factory=lambda: [(2, 2), (1, 2)]
    )
    direction: tuple[int, int] = (1, 0)
    walls: frozenset[tuple[int, int]] = field(default_factory=lambda: CLASSIC.walls)
    alive: bool = True

    def add_player(self, player: Player) -> None:
        self.players[player.id] = player

    def remove_player(self, player: Player) -> None:
        self.players.pop(player.id, None)

    def has_player(self, player_id: str) -> bool:
        return player_id in self.players

    def set_direction(self, direction: tuple[int, int]) -> None:
        opposite = (-self.direction[0], -self.direction[1])
        if direction != opposite:
            self.direction = direction

    def move(self) -> None:
        head_x, head_y = self.snake_body[0]
        dx, dy = self.direction
        new_head = (head_x + dx, head_y + dy)
        self.snake_body = [new_head] + self.snake_body[:-1]

    def head_hits_wall(self) -> bool:
        return self.snake_body[0] in self.walls
