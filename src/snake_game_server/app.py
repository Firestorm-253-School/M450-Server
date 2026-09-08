from fastapi import FastAPI

from .api.auth import router as auth_router
from .api.players import router as players_router
from .sockets.game_socket import router as socket_router


app = FastAPI()

app.include_router(auth_router)
app.include_router(players_router)
app.include_router(socket_router)