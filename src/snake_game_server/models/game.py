import random
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
    apples: list[tuple[int, int]] = field(default_factory=list)
    apple_spawn_interval_ticks: int = 20
    max_apples: int = 3
    width: int = 24
    height: int = 18

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

    def head_is_on_apple(self) -> bool:
        return self.snake_body[0] in self.apples

    def spawn_apple(self) -> None:
        if len(self.apples) >= self.max_apples:
            return
        occupied_positions = set(self.snake_body) | set(self.walls) | set(self.apples)

        free_positions = [
            (x, y)
            for x in range(self.width)
            for y in range(self.height)
            if (x, y) not in occupied_positions
        ]

        if free_positions:
            self.apples.append(random.choice(free_positions))
