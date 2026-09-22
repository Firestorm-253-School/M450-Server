from fastapi.testclient import TestClient

from snake_game_server.app import app
from snake_game_server.api import highscores as highscores_api
from snake_game_server.services import highscore_service

client = TestClient(app)

#def setup_function():
#    highscore_service.highscores.clear()

def test_post_highscore():
    response = client.post(
        "/api/highscores",
        json={"name": "Anna", "score": 120, "modus": "pro"},
    )
    assert response.status_code == 201

def test_get_highscore():
    response = client.get(
        "/api/highscores",
    )
    data = response.json()
    assert data == {'highscore': [{'name': 'Anna', 'score': 120, 'modus': 'pro'}], 'hinweis': ''}

def test_post_highscore_ungültig():
    response = client.post(
        "/api/highscores",
        json={"name": "Anna", "modus": "pro"},
    )
    assert response.status_code == 422