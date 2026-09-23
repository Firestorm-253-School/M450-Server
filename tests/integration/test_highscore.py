#from fastapi.testclient import TestClient
#
#from snake_game_server.app import app
#from snake_game_server.api import highscores as highscores_api
#
#client = TestClient(app)
#
#def setup_function():
#    highscores_api.highscores.clear()
#
#def test_post_highscore():
#    response = client.post(
#        "/api/highscores",
#        json={"name": "Anna", "score": 120},
#    )
#
#    assert response.status_code == 201
#    assert response.json()["name"] == "Anna"
#    assert response.json()["score"] == 120
#
#def test_get_highscore():
#    client.post("/api/highscores", json={"name": "Anna", "score": 120})
#    client.post("/api/highscores", json={"name": "Max", "score": 80})
#    client.post("/api/highscores", json={"name": "Ben", "score": 50})
#    
#    response = client.get("/api/highscores")
#    print(response)
#    assert response.status_code == 200
#    data = response.json()
#    assert len(data) == 3
#    assert data[0]["name"] == "Anna"
#    assert data[0]["score"] == 120
#    assert data[1]["name"] == "Max"
#    assert data[2]["name"] == "Ben"
#