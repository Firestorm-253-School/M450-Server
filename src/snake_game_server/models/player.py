from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from snake_game_server.models.game import Game


@dataclass(frozen=False, slots=True)
class Player:
    id: str

    current_game: Game = field(default=None)
    snake_body: list[tuple[int, int]] = field(
        default_factory=lambda: [(2, 2), (1, 2)]
    )
    direction: tuple[int, int] = (1, 0)
    alive: bool = True

    direction_to_set: list[tuple[int, int]] = field(default=direction)
