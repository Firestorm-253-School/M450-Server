from fastapi import APIRouter, HTTPException

from ..services import highscore_service as service
from ..services.highscore_service import ORDNER
from ..services.highscore_repository import HighscoreRepository

router = APIRouter()


highscore_repository = HighscoreRepository(ORDNER)


@router.get("/api/highscores")
def get_highscores(modus: str | None = None) -> dict:
    try:
        return service.uebersicht(modus)
    except ValueError as fehler:
        raise HTTPException(422, str(fehler)) from fehler


@router.post("/api/highscores", status_code=201)
def add_highscore(eintrag: dict) -> dict:
    try:
        return service.speichere_dauerhaft(highscore_repository, eintrag.get("name"), eintrag.get("score"), eintrag.get("modus"))
    except (ValueError, TypeError) as fehler:
        raise HTTPException(422, str(fehler)) from fehler