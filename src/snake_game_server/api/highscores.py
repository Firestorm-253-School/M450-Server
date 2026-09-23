from fastapi import APIRouter, HTTPException

from ..services import highscore_service as service
from snake_game_server.pruefung3.highscore_repository import HighscoreRepository

router = APIRouter()


@router.get("/api/highscores")
def get_highscores(modus: str | None = None) -> dict:
    try:
        return service.uebersicht(modus)
    except ValueError as fehler:
        raise HTTPException(422, str(fehler)) from fehler


@router.post("/api/highscores", status_code=201)
def add_highscore(eintrag: dict) -> dict:
    try:
        return service.speichere_dauerhaft(eintrag.get("name"), eintrag.get("score"), eintrag.get("modus"), service.highscore_repository)
    except (ValueError, TypeError) as fehler:
        raise HTTPException(422, str(fehler)) from fehler