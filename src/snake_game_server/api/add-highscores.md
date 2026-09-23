curl -X POST http://127.0.0.1:8000/api/highscores \
  -H "Content-Type: application/json" \
  -d '{ "name": "Moritz", "score": 10, "modus": "classic" }'


curl -X POST http://127.0.0.1:8000/api/highscores \
  -H "Content-Type: application/json" \
  -d '{ "name": "Mia", "score": 120, "modus": "pro" }'


curl -X POST http://127.0.0.1:8000/api/highscores \
  -H "Content-Type: application/json" \
  -d '{ "name": "Max", "score": 130, "modus": "medium" }'