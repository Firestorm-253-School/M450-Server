from fastapi import APIRouter

router = APIRouter()

highscores: list[dict] = []


@router.get("/api/highscores")
def get_highscores() -> list[dict]:
    return sorted(highscores, key=lambda entry: entry["score"], reverse=True)[:10]


@router.post("/api/highscores", status_code=201)
def add_highscore(entry: dict) -> dict:
    highscores.append(entry)
    return entry