import pytest
from fastapi.testclient import TestClient

from snake_game_server.app import app
from snake_game_server.services import highscore_service as service


@pytest.fixture(autouse=True)
def clear_highscores():
    service.highscores.clear()


@pytest.fixture
def client():
    return TestClient(app)


# T4a: POST mit gültigem Eintrag = 201, erscheint danach im passenden Modus
def test_post_gueltigen_eintrag_erstellt_und_erscheint_im_passenden_modus(client):
    response = client.post(
        "/api/highscores",
        json={"name": "Anna", "score": 120, "modus": "classic"},
    )

    assert response.status_code == 201
    assert response.json() == {"name": "Anna", "score": 120, "modus": "classic"}

    result = client.get("/api/highscores", params={"modus": "classic"})

    assert result.status_code == 200
    assert result.json()["highscore"] == [{"name": "Anna", "score": 120, "modus": "classic"}]


# T4b: POST mit ungültigem Eintrag = 422, nichts wurde gespeichert (mit GET geprüft)
def test_post_ungueltigen_eintrag_lehnt_ab_und_speichert_nichts(client):
    response = client.post(
        "/api/highscores",
        json={"name": "", "score": 120, "modus": "classic"},
    )

    assert response.status_code == 422

    result = client.get("/api/highscores")

    assert result.json()["highscore"] == []


# T4c: GET mit ?modus= filtert korrekt
def test_get_mit_modus_filtert_korrekt(client):
    client.post("/api/highscores", json={"name": "Anna", "score": 50, "modus": "classic"})
    client.post("/api/highscores", json={"name": "Ben", "score": 100, "modus": "pro"})

    response = client.get("/api/highscores", params={"modus": "pro"})

    assert response.status_code == 200
    assert response.json()["highscore"] == [{"name": "Ben", "score": 100, "modus": "pro"}]


# T4c: GET mit unbekanntem Modus = 422
def test_get_mit_unbekanntem_modus_gibt_422(client):
    response = client.get("/api/highscores", params={"modus": "extreme"})

    assert response.status_code == 422
