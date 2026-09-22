import pytest
from fastapi.testclient import TestClient
from snake_game_server.app import app

# -------- T4 --------

@pytest.fixture()
def client():
    return TestClient(app)


@pytest.mark.integration
def test_api_get_highscores(client: TestClient):
    response = client.get(
        "/api/highscores"
    )

    assert response.status_code == 200
    
    body = response.json()
    
    assert "highscore" in body
    assert "hinweis" in body

