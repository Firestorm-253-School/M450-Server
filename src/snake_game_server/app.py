from fastapi import FastAPI

from .api.players import router as players_router
from .sockets.game_socket import router as socket_router
from .api.highscores import router as highscores_router


app = FastAPI()

app.include_router(players_router)
app.include_router(socket_router)

app.include_router(highscores_router)