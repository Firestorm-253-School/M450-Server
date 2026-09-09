from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status

from .connection_manager import ConnectionManager
from ..services.game_service import GameService
from ..services.player_service import PlayerService

router = APIRouter()

connection_manager = ConnectionManager()
game_service = GameService(connection_manager)
player_service = PlayerService()


@router.websocket("/ws/game")
async def game_socket(websocket: WebSocket):
    player = await connection_manager.connect(websocket, player_service)

    if player is None:
        await websocket.close(
            code=status.WS_1008_POLICY_VIOLATION
        )
        return
    
    try:
        while True:
            message = await websocket.receive_json()

            response = await game_service.handle_message(
                player=player,
                message=message,
            )
            await websocket.send_json(response)

    except WebSocketDisconnect:
        await connection_manager.disconnect(player.id)

    except Exception:
        await connection_manager.disconnect(player.id)

        await websocket.close(
            code=status.WS_1011_INTERNAL_ERROR
        )
