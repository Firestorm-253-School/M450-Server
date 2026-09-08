from snake_game_server.models.player import Player


class PlayerService:
    def __init__(self):
        self.players: dict[str, Player] = {}

    async def get_or_create(self, player_id: str) -> Player:
        player = self.players.get(player_id)

        if player is None:
            player = Player(id=player_id)
            self.players[player_id] = player

        return player
