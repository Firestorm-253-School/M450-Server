from fastapi import WebSocket

from snake_game_server.services.player_service import PlayerService


class ConnectionManager:
    def __init__(self):
        self.connections: dict[str, WebSocket] = {}


    async def connect(
        self,
        websocket: WebSocket,
        player_service: PlayerService,
    ):
        player_id = websocket.query_params.get("player_id")
        if player_id is None:
            return None

        player = await player_service.get_or_create(player_id)

        await websocket.accept()
        self.connections[player.id] = websocket

        return player


    async def disconnect(self, player_id: str):
        self.connections.pop(player_id, None)


    async def send_to_player(
        self,
        player_id: str,
        message: dict,
    ):
        websocket = self.connections.get(player_id)

        if websocket is not None:
            await websocket.send_json(message)


    async def broadcast(self, message: dict):
        for websocket in self.connections.values():
            await websocket.send_json(message)
